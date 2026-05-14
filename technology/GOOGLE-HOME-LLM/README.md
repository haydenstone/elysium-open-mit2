#   GOOGLE_HOME_LLM_README.md

##   Google Home LLM Integration for Advanced Smart Home Control

This document outlines a proof-of-concept for integrating a Local Large Language Model (LLM) with Google Home and Home Assistant to create a more intuitive and powerful smart home control system.  The primary goal is to enable natural language interaction with your smart home, using an LLM persona (in this case, "Ava") to understand and respond to voice commands, control devices, and provide information.

##   Concept

The core idea is to use Google Home to trigger a Home Assistant scene, which in turn activates a script running in a Docker container. This script will:

1.  **Receive Arguments:** Accept arguments passed from the Google Home scene trigger.
2.  **Process Arguments:** Parse the arguments to determine the desired actions.
3.  **LLM Integration:** Integrate a local LLM, such as a model from Hugging Face Transformers or via LangChain, with the script. The LLM can be used to:

    * Understand complex and nuanced voice commands (e.g., 'Dim the lights in the living room a bit').
    * Generate dynamic responses and feedback (e.g., 'Okay, dimming the living room lights to 60%.').
    * Perform context-aware actions (e.g., 'Turn on the lights' could turn on different lights depending on the time of day).
4.  **Execute Functions:** Control smart home devices and perform other actions based on the processed arguments and LLM output.

##   Implementation

###   1. Home Assistant Script

* Create a Home Assistant script that triggers an event or sends a message with the arguments.
* Use Home Assistant's event bus or MQTT to communicate with the Docker container.

###   2. Docker Container Setup

* Create a Dockerfile for the script, including any necessary dependencies.
* Build the Docker image and run the container on the Home Assistant server or another machine on your network.
* Example Dockerfile:

    ```dockerfile
    FROM python:3.9-slim-buster

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install -r requirements.txt

    COPY . .

    CMD ["python", "main.py"] #Or your script name
    ```

###   3. Argument Parsing

* In your script (e.g., `main.py`), use a library or function to parse the arguments passed from Home Assistant.
* Example (Python):

    ```python
    import sys

    arguments = sys.argv[1:] # Arguments after the script name

    # Process arguments
    if "lights on" in " ".join(arguments):
        # Control lights
        print("Lights on command received")

    if "brightness 50%" in " ".join(arguments):
        # set brightness
        print("brightness 50% command received")
    ```

###   4. LLM Integration

* Integrate a local LLM with the script using an API or library (e.g., LangChain, Transformers).
* Use the LLM to process natural language arguments, maintain conversation context, and generate dynamic responses.
* Example (Python):

    ```python
    from langchain.llms import CTransformers

    llm = CTransformers(model="path/to/your/model")

    def get_llm_response(prompt):
        llm_response = llm(prompt)
        return llm_response

    # Example usage in argument processing:
    if arguments:
        prompt = f"The user said: {' '.join(arguments)}.  Respond as Ava Stone."
        response = get_llm_response(prompt)
        print(f"LLM Response: {response}")
    ```

###   5. Function Execution

* Based on the parsed arguments or LLM output, execute the appropriate functions.
* This can involve controlling devices via Home Assistant's API or other methods.  The LLM can determine which functions to call based on the user's request.

###   6. Google Home Scene

* Create a Google Home scene that triggers the Home Assistant script.
* Test the scene with different arguments to ensure the script functions correctly.

##   Example Scenario: Conversing with Ava

This scenario demonstrates a more extended conversation with the LLM persona, Ava Stone, and how she can control home automation and provide helpful information.

**1. Initializing the Conversation:**

* **Voice Command:** "Hey Google, start Ava Stone conversation"
* **Home Assistant Routine:** Activates the `llm_conversation_start` script.
* **LLM Prompt:** The script sends an initial prompt to the LLM, setting the context:  "You are Ava Stone, a helpful and friendly smart home assistant.  Your goal is to assist the user with controlling their home and answering questions.  Be concise and helpful.  The first message from the user is: 'Hello'."
* **LLM Response:** "Hello! I'm Ava Stone. How can I assist you today?"
* **Google Home:** Speaks the LLM response using TTS.

**2. Controlling Home Automation:**

* **Voice Command:** "Hey Google, tell Ava to turn on the living room lights."
* **Home Assistant Routine:** The phrase  "tell Ava to" is key.  For example, the routine could send the phrase after "tell Ava to" to the LLM.
* **LLM Prompt:** "The user said: 'turn on the living room lights'.  You should turn on the living room lights, and tell the user that you did it."
* **LLM Response:** "Okay, I've turned on the living room lights for you."
    * The python script would then use the Home Assistant API to turn on the lights.
* **Google Home:** "Okay, I've turned on the living room lights for you."

**3. Asking for Information:**

* **Voice Command:** "Hey Google, ask Ava what the temperature is inside."
* **Home Assistant Routine:** The phrase "ask Ava" is key.
* **LLM Prompt:** "The user said: 'what is the temperature inside?'.  You should check the temperature and tell the user."
* **LLM Response:** "The temperature inside is currently 72 degrees Fahrenheit."
    * The python script would then use the Home Assistant API to get the temperature.
* **Google Home:** "The temperature inside is currently 72 degrees Fahrenheit."

**4. Chain of commands**

* **Voice Command:** "Hey Google, tell Ava to turn off the lights and then play some music"
* **Home Assistant Routine**:  The phrase "tell Ava" is key.
* **LLM Prompt**: "The user said "turn off the lights and then play some music".  You should turn off the lights, and then play some music.  Tell the user you are doing so."
* **LLM Response**: "Ok, I'm turning off the lights and playing some music"
    * The python script would then use the Home Assistant API to turn off the lights, and then play music.
* **Google Home**: "Ok, I'm turning off the lights and playing some music"

**5. Ava Providing Examples of What She Can Do:**

* **Voice Command:** "Hey Google, ask Ava what she can do."
* **LLM Prompt:** "The user asked what you can do. Provide a few examples of your capabilities."
* **LLM Response:** "I can control lights, adjust the thermostat, play music, answer questions about your home, and much more. For example, you can say, 'Turn on the kitchen lights' or 'What's the temperature outside?'"
* **Google Home:** "I can control lights, adjust the thermostat, play music, answer questions about your home, and much more. For example, you can say, 'Turn on the kitchen lights' or 'What's the temperature outside?'"

**6. Ending the Conversation:**

* **Voice Command:** "Hey Google, tell Ava to stop."
* **LLM Prompt:** "The user said 'stop'. End the conversation."
* **LLM Response:** "Okay, I'm ending the conversation now. Goodbye!"
* **Google Home:** "Okay, I'm ending the conversation now. Goodbye!"
* **Home Assistant:** Sets the  `conversation_active`  input boolean to  `false`.

##   Benefits

* **Natural Language Control:** Users can interact with their smart home using intuitive, conversational language.
* **Contextual Awareness:** The LLM can maintain context throughout the conversation, allowing for more natural and follow-up requests.
* **Dynamic Responses:** The LLM generates dynamic and informative responses, providing a more engaging user experience.
* **Extensibility:** The system can be extended to support new devices, services, and conversation flows.

##   Important Considerations

* **LLM Selection and Configuration:** Choosing the right LLM and configuring it with the appropriate persona (Ava Stone) is crucial for achieving the desired behavior.
* **Prompt Engineering:** Crafting effective prompts for the LLM is essential for guiding its responses and actions.
* **Home Assistant Integration:** Robust integration with Home Assistant is required to control devices and access data.
* **Latency:** Consider the processing time of the LLM and network latency to ensure a smooth and responsive user experience.
* **Error Handling:** Implement error handling for all components, including LLM failures, API errors, and network issues.
* **Security:** Secure your Home Assistant API and Docker container to protect your smart home system.
