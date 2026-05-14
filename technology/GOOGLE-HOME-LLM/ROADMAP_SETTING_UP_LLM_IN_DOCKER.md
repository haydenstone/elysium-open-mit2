#   Roadmap: Setting up LLM in Docker Container

This roadmap outlines the steps required to set up a local LLM within a Docker container, configure networking, and manage interactions for a smart home assistant, "Ava."

##   I. Core Infrastructure Setup

###   A. Docker Setup

1.  **Install Docker:** Install Docker Engine on the chosen server (Home Assistant server or a dedicated machine).

2.  **Create Docker Network:**

    * Create a dedicated Docker network for the LLM container to facilitate communication with Home Assistant.

    * Example:  `docker network create hass_llm_network`

###   B. Home Assistant Integration

1.  **Home Assistant API Access:**

    * Ensure Home Assistant has a Long-Lived Access Token configured for secure API communication.

    * The Docker container will use this token to interact with Home Assistant.

2.  **Home Assistant Scripts:**

    * Create Home Assistant scripts to trigger LLM interactions.  These scripts will:

        * Receive data from Google Home.

        * Send commands to the LLM Docker container.

        * Handle responses from the LLM.

3.  **AppDaemon (Recommended):**

    * Use AppDaemon within Home Assistant to manage complex logic, especially for handling LLM responses and device control.

    * Create AppDaemon apps to:

        * Listen for events from the LLM container.

        * Parse LLM responses.

        * Control Home Assistant devices.

        * Send TTS responses to Google Home.

##   II. LLM Containerization

###   A. Choose LLM and Model

1.  **Select LLM Software:** Choose the LLM software (e.g., Llama 2, CTransformers, etc.).

2.  **Obtain LLM Model:** Download the pre-trained LLM model weights.  Ensure compatibility with the chosen software.

###   B. Create Dockerfile

1.  **Base Image:** Start with a suitable base image (e.g., `python:3.9-slim-buster`).

2.  **Dependencies:**

    * Install Python dependencies (e.g., `langchain`, `transformers`, `torch`, etc.).

    * Install any required system libraries.

3.  **LLM Software Installation:** Install the chosen LLM software within the container.

4.  **Model Placement:**

    * Copy the LLM model files into the container.

    * Define the model path within the container.

5.  **Script Inclusion:** Copy the Python script that will manage LLM interactions into the container.

6.  **Working Directory:** Set the working directory (e.g., `/app`).

7.  **Entrypoint:** Define the command to run the script (e.g., `CMD ["python", "main.py"]`).

8.  **Networking:** Ensure the container is connected to the `hass_llm_network`.

9.  **Example Dockerfile:**

    ```dockerfile
    FROM python:3.9-slim-buster
    
    WORKDIR /app
    
    COPY requirements.txt .
    RUN pip install -r requirements.txt
    
    # Install LLM software (example with CTransformers)
    RUN pip install ctransformers
    
    # Copy LLM model
    COPY ./models /app/models  #  Make sure to have a models directory
    ENV LLM_MODEL_PATH=/app/models/your_model.bin # set the path
    
    COPY . .
    
    CMD ["python", "main.py"]
    
    ```

###   C. Build and Run Container

1.  **Build Image:** Build the Docker image using the Dockerfile.

    * Example:  `docker build -t llm_image .`

2.  **Run Container:** Run the Docker container, connecting it to the Home Assistant network.

    * Example:

        ```dockerfile
        docker run -d \
            --name llm_container \
            --network hass_llm_network \
            -v /path/to/your/models:/app/models \ # Mount volume
            llm_image
        
        ```

        * **Important:** Mount the model directory as a volume to prevent re-downloading the model on every container restart.

##   III. LLM Configuration and Persona

###   A.  LLM Script (main.py)

1.  **Import Libraries:** Import necessary libraries (e.g., `langchain`, `ctransformers`, `docker`, `json`).

2.  **Initialize LLM:**

    * Load the LLM model using the defined path.

    * Example:

        ```python
        from langchain.llms import CTransformers
        llm = CTransformers(model=LLM_MODEL_PATH)
        
        ```

3.  **Home Assistant Communication:**

    * Implement functions to send events and get state from Home Assistant using the Home Assistant API (within the Docker container).  Use the  `requests`  library, or a dedicated Home Assistant client library.  The example below uses the `docker` python library to execute `curl` commands *from within* the container.

        ```python
        import docker
        import json
        import subprocess
        
        HASS_URL = "http://your_home_assistant_ip:8123"
        HASS_TOKEN = "your_long_lived_access_token"
        DOCKER_CONTAINER_NAME = "llm_container" #  The name of this container.
        
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
            result = container.exec_run(command)
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
            result = container.exec_run(command)
            if result.exit_code != 0:
                print(f"Error getting state: {result.output.decode()}")
                return None
            return json.loads(result.output.decode())
        
        ```

4.  **Prompt Engineering:**

    * Create an initial prompt to define the LLM's persona (Ava Stone) and behavior.  This is crucial for setting the LLM's role and how it should interact.

        ```python
        initial_prompt = """
        You are Ava Stone, a helpful and friendly smart home assistant. Your goal is to assist the user with controlling their home and answering questions. Be concise and helpful.
        """
        
        ```

    * Optionally load persona, context, and meta files.  The method to load these files depends on the LLM library you use.  The following is an example:

        ```python
        # Load persona
        with open("persona.txt", "r") as f:
            persona_text = f.read()
            initial_prompt += persona_text
        
        # Load context
        with open("context.txt", "r") as f:
            context_text = f.read()
            initial_prompt += context_text
        
        # Load meta
        with open("meta.txt", "r") as f:
            meta_text = f.read()
            initial_prompt += meta_text
        
        ```

5.  **Conversation Handling:**

    * Implement the main conversation loop:

        * Receive user commands from Home Assistant (via events).

        * Generate LLM responses.

        * Send LLM responses to Home Assistant (via events).

        * Parse LLM responses to determine actions.

        * Execute functions to control devices.

    * Example:

        ```python
        def handle_conversation(user_command):
            """Handles the conversation with the LLM."""
            prompt = f"{initial_prompt} The user said: {user_command}."
            llm_response = llm(prompt)
            print(f"LLM Response: {llm_response}")
            send_event_to_hass("llm_response", {"response_text": llm_response})
        
            #  Parse LLM response and perform actions
            if "turn on the living room lights" in llm_response.lower():
                #  Control Home Assistant
                turn_on_lights("living_room")  #  Define this
            # Add more actions
        
        def turn_on_lights(room_name):
            # use the hass api to turn on the lights.
            pass
        
        ```

###   B. File Management

1.  **Read-Only Access:** The LLM within the Docker container should have read-only access to any persona, context, and meta files.  This can be achieved through Docker volume mounts.

2.  **Soft Manipulation:** If the LLM needs to make minor adjustments to these files, consider these approaches:

    * **Mount a Separate Volume for Changes:** Mount a separate, writable volume where the LLM can create modified copies of the files.  The original files remain read-only.

    * **In-Memory Updates:** For temporary changes, the LLM can modify the file data in memory and use that data for the current conversation without writing to the file system.

    * **Home Assistant as a Data Store:** Store persona, context, and meta information in Home Assistant entities.  The LLM can then read the information from Home Assistant via the API and request Home Assistant to update the entities.

###   C.  Security Considerations

1.  **Principle of Least Privilege:** The LLM container should only have the necessary permissions.

2.  **Secure API Keys:** Protect the Home Assistant Long-Lived Access Token.  Do not embed it directly in the Dockerfile.  Use environment variables or Docker secrets.

3.  **Network Security:** Use a dedicated Docker network to isolate the LLM container.

4.  **Input Validation:** Sanitize user inputs to prevent injection attacks.

##   IV. Google Home Integration

1.  **Google Home Scenes:** Create Google Home scenes to trigger Home Assistant scripts.

2.  **Voice Command Handling:**

    * Configure Google Home to pass the user's voice command to the Home Assistant scene.

    * Home Assistant then passes this command to the LLM container.

3.  **TTS Output:**

    * The LLM container sends responses to Home Assistant.

    * Home Assistant uses its text-to-speech (TTS) service to relay the LLM's responses to Google Home.

##   V. Testing and Refinement

1.  **Iterative Testing:** Test each component thoroughly (Docker container, LLM interaction, Home Assistant integration, Google Home integration).

2.  **Debugging:** Implement logging to help debug issues.

3.  **Performance Tuning:** Optimize the LLM for performance within the Docker container.

4.  **User Experience:** Refine the interaction flow and prompts to create a create a natural and intuitive user experience.

