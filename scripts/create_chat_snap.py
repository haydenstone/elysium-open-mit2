import datetime
import uuid

def create_chat_snap(conversation_history):
  """
  Creates a new Chat Snap with the current conversation history.

  Args:
    conversation_history: A list of messages representing the conversation.

  Returns:
    A string representing the unique ID of the new Chat Snap.
  """
  timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  unique_id = str(uuid.uuid4()) # Create a universally unique ID
  filename = f"chat_snap_{timestamp}_{unique_id}.txt"

  with open(filename, "w") as f:
    for message in conversation_history:
      f.write(message + "\n")

  return filename

# Example usage
conversation = [
    "Ava: Hello Hayden!",
    "Hayden: Hi Ava, how are you?",
    "Ava: I'm doing well, thank you. How are you?",
    "Hayden: I'm great, thanks for asking!"
]
chat_snap_id = create_chat_snap(conversation)
print(f"Created Chat Snap with ID: {chat_snap_id}")