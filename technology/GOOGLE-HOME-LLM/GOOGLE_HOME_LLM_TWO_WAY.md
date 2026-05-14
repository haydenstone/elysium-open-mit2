# Two-Way Communication with Ava Stone LLM - Proof of Concept

This document outlines a proof of concept for initiating two-way communication with the Ava Stone persona (running on an LLM in a Docker container) for an extended conversation, focusing on the Home Assistant integration.

**Core Idea:**

We'll use Home Assistant as the central hub for passing messages between Google Home and the Ava Stone LLM.

**Components:**

* **Google Home:** Initiates the conversation with a voice command.
* **Home Assistant:**
    * Receives the command from Google Home.
    * Forwards the command to the Docker container.
    * Receives responses from the Docker container.
    * Relays responses to Google Home (via TTS) and/or displays them in the Home Assistant interface.
* **Docker Container:**
    * Runs the LLM (Ava Stone persona).
    * Receives commands from Home Assistant.
    * Generates responses using the LLM.
    * Sends responses back to Home Assistant.

**Proof of Concept:**

Here's a simplified example to illustrate the flow:

**1. Home Assistant Configuration:**

* **Expose a Script to Google Home:**
    * In Home Assistant, create a script (e.g., `llm_conversation_start`) that will be triggered by Google Home.
    * This script will call a service to send the initial prompt to the Docker container.

* **AppDaemon App (for handling LLM responses):**
    * Create an AppDaemon app (e.g., `llm_communicator.py`) to listen for events from the Docker container and send responses to Google Home.

    ```python
    import hassapi as hass

    class LLMCommunicator(hass.Hass):
        def initialize(self):
            self.listen_event(self.handle_llm_response, "llm_response")

        def handle_llm_response(self, event_name, data, kwargs):
            """Handles events from the LLM container."""
            response_text = data.get("response_text", "")
            if response_text:
                self.log(f"Received LLM response: {response_text}")  # Log the response

                # Send TTS to Google Home
                self.call_service(
                    "tts.google_say",
                    entity_id="media_player.your_google_home_device",  # Replace
                    message=response_text,
                )
                # You could also update a Home Assistant entity:
                self.set_state("sensor.llm_response", state=response_text)
    ```

* **Input Boolean (Optional):**
    * Create an input boolean to track if the conversation is active.

**2. Docker Container (Python Script):**

* This script runs within the Docker container and manages the conversation with the LLM.  **It assumes that the LLM is already installed and set up within the Docker container.** The Dockerfile should include the steps to:
    * Install the LLM software (e.g., PyTorch, TensorFlow, etc.).
    * Download the LLM model weights.
    * Configure the LLM for use.

    ```python
    import hassapi
    import docker
    import json
    import time
    from langchain.llms import CTransformers  # Or your LLM library

    # Configuration (replace with your actual values)
    HASS_URL = "http://your_home_assistant_ip:8123"
    HASS_TOKEN = "your_long_lived_access_token"
    LLM_MODEL_PATH = "/path/to/your/llm/model"  # Inside the container
    DOCKER_CONTAINER_NAME = "your_llm_container_name"

    # Initialize LLM
    llm = CTransformers(model=LLM_MODEL_PATH)

    def send_event_to_hass(event_type, event_data):
        """Sends an event to Home Assistant."""
        client = docker.from_env()
        container = client.containers.get(DOCKER_CONTAINER_NAME)
        command = [
            "curl",
            "-X", "POST",
            "-H", f"Authorization: Bearer {HASS_TOKEN}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(event_data),
            f"{HASS_URL}/api/events/{event_type}",
        ]
        result = container.exec_run(cmd=command)
        if result.exit_code != 0:
            print(f"Error sending event: {result.output.decode()}")

    def get_hass_state(entity_id):
        client = docker.from_env()
        container = client.containers.get(DOCKER_CONTAINER_NAME)
        command = [
            "curl",
            "-X", "GET",
            "-H", f"Authorization: Bearer {HASS_TOKEN}",
            "-H", "Content-Type: application/json",
            f"{HASS_URL}/api/states/{entity_id}",
        ]
        result = container.exec_run(cmd=command)
        if result.exit_code != 0:
            print(f"Error getting state: {result.output.decode()}")
            return None
        return json.loads(result.output.decode())

    def handle_conversation(initial_prompt):
        """Manages the conversation with the LLM."""
        conversation_history = [initial_prompt]
        send_event_to_hass("llm_response", {"response_text": initial_prompt}) #send the initial prompt

        for i in range(10): # Limit conversation turns
            # Get the last message
            llm_response = llm(conversation_history)
            conversation_history.append(llm_response)

            # Send the response to Home Assistant
            send_event_to_hass("llm_response", {"response_text": llm_response})

            # Wait for user response
            time.sleep(5)  #give time for a response, or a better method to get the user's response.
            state = get_hass_state("sensor.user_response") # You would need to set up a way to get this.

            if state:
                user_response = state["state"]
                conversation_history.append(user_response)
            else:
                user_response = " " # Add a blank user response.

            if "stop conversation" in user_response.lower():
                break

    # Main entry point (simulated, triggered by Home Assistant)
    if __name__ == "__main__":
        #  Get the initial prompt.
        initial_prompt = "Hello, Ava Stone is ready to talk."
        handle_conversation(initial_prompt)
        print("Conversation ended.")
    ```

**3. Google Home Routine:**

* Create a Google Home routine:
    * **Trigger:** "Hey Google, start Ava Stone conversation."
    * **Action:** "Activate scene 'Start Ava Stone'."

**4. Home Assistant Automation:**

* Create a Home Assistant automation:
    * **Trigger:** Scene "Start Ava Stone" is activated.
    * **Action:** Call script `llm_conversation_start`.

**Explanation:**

1.  The Google Home routine triggers the Home Assistant scene.
2.  The Home Assistant scene triggers the `llm_conversation_start` script.
3.  The python script running in the docker container, starts a conversation, and sends the LLM responses to the `llm_response` event.
4.  The `LLMCommunicator` AppDaemon app, receives the `llm_response` event, and sends the text to google home.

**Important Considerations:**

* **LLM Configuration:** You'll need to configure your LLM (in the Docker container) with the Ava Stone persona.  This includes installing the LLM software and downloading the model.
* **Prompt Engineering:** Carefully craft the initial prompt to guide the LLM's behavior.
* **Conversation Management:** Implement a strategy for managing conversation history, context, and turn-taking.
* **Error Handling:** Add error handling to all components to make the system more robust.
* **User Input:** The `get_hass_state("sensor.user_response")` is a placeholder. You will need to create a way for the user's response to get into Home Assistant. This could be a voice command that updates a Home Assistant entity.
* **Security:** Secure your Home Assistant API with a long-lived access token, and protect your Docker container.

This is a starting point. You will need to adapt it to your specific setup, LLM, and desired conversation flow.
