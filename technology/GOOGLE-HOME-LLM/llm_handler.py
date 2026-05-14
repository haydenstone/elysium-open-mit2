# This file goes inside the Docker container.
# When you create your Docker image, this file (and any other necessary files) will be copied into the container's file system.
# The Dockerfile you create will specify where this file should be placed within the container. In the Dockerfile example I provided earlier, the COPY . . command copies all files from the same directory as the Dockerfile into the /app directory in the container.

import hassapi
import docker
import json

# Example of sending data back to Home Assistant
def send_response_to_ha(response_text):
  client = docker.from_env()
  container = client.containers.get('your_llm_container_name')  # Change this
  hass_url = "http://your_home_assistant_ip:8123"  # Change this
  token = "your_long_lived_access_token"  # Change this
  # Construct the event data.
  event_data = {
    "response_text": response_text
  }
  # Send the event to Home Assistant
  command = [
    "curl",
    "-X", "POST",
    "-H", "Authorization: Bearer {}".format(token),
    "-H", "Content-Type: application/json",
    "-d", json.dumps(event_data),
    "{}/api/events/llm_response".format(hass_url),
  ]
  container.exec_run(cmd=command)