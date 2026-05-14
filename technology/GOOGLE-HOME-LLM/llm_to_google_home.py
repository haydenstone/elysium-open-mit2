# This file is a Home Assistant AppDaemon app. AppDaemon is a separate application that runs alongside Home Assistant and allows you to write more complex automation using Python.
# You'll need to have AppDaemon installed and configured in your Home Assistant setup.
# The file should be placed in the apps directory within your AppDaemon configuration. The default location is /config/apps, but it might be different depending on your setup.

import hassapi  # Library to interact with Home Assistant

class LLMCommunicator(hassapi.Hass):
  def initialize(self):
    self.listen_event(self.handle_llm_response, "llm_response")

  def handle_llm_response(self, event_name, data, kwargs):
    """Handles events from the LLM container."""
    response_text = data.get("response_text")
    if response_text:
      self.call_service(
        "tts.google_say",  # Or another TTS service
        entity_id="media_player.my_google_home",  # Replace with your device
        message=response_text,
      )