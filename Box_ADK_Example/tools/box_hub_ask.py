
import os
import logging 
import requests
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# !! SECURITY WARNING !!
# Replace these with a secure method, e.g., environment variables
BOX_METADATA_TOKEN = os.getenv("BOX_METADATA_TOKEN", "YOUR_METADATA_TOKEN_HERE")
BOX_HUB_TOKEN = os.getenv("BOX_HUB_TOKEN", "YOUR_HUB_TOKEN_HERE")
BOX_ENTERPRISE_ID = os.getenv("BOX_ENTERPRISE_ID", "YOUR_BOX_ENTERPRISE_ID_HERE")
BOX_HUB_ID = os.getenv("BOX_HUB_ID", "YOUR_BOX_HUB_ID_HERE") # e.g., "216163155"


def box_hub_ask(prompt: str) -> str:
  """
  Sends a prompt to a specific Box AI Hub to get answers based on its associated content.

  Args:
    prompt: The question or prompt to ask the Box Hub.

  Returns:
    The answer provided by the Box Hub, or an error message.
  """
  logger.info(f"Asking Box Hub (ID: {BOX_HUB_ID}): '{prompt}'")
  url = "https://api.box.com/2.0/ai/ask"
  headers = {
      "Authorization": f"Bearer {BOX_HUB_TOKEN}",
      "Content-Type": "application/json"
  }
  payload = {
      "mode": "multiple_item_qa",
      "items": [
          {
              "type": "hubs",
              "id": BOX_HUB_ID # Use configured Hub ID
          }
      ],
      "prompt": prompt,
      "llm": { # Specify model if needed - check Box API docs
         # "model": "claude_3_opus" # Example
      },
      "includes_citations": False # Set to True if you want citations
  }

  try:
    response = requests.post(url, headers=headers, json=payload)
    logger.info(f"Box Hub ask API response status: {response.status_code}")
    response.raise_for_status() # Check for HTTP errors

    response_data = response.json()
    answer = response_data.get("answer")
    if answer:
        # Return only the answer text
        return answer
    else:
        # Handle cases where the API succeeds but provides no answer
        completion_reason = response_data.get("completion_reason", "No reason provided.")
        logger.warning(f"Box Hub did not provide an answer. Reason: {completion_reason}")
        return f"Box Hub did not provide an answer. Reason: {completion_reason}"

  except requests.exceptions.RequestException as e:
    logger.error(f"Error during Box Hub API call: {e}")
    error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if e.response else "No response details."
    return f"API Error: Failed to ask Box Hub. {error_details}"
  except Exception as e:
      logger.error(f"An unexpected error occurred in box_hub_ask: {e}", exc_info=True)
      return f"An unexpected error occurred: {e}"
