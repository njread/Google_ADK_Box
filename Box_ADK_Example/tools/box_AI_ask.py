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


def box_AI_ask(prompt: str, items: str) -> str:
  """
  Sends a prompt to Box AI to get answers based on specified file content.

  Args:
    prompt: The question or prompt to ask the AI.
    items: JSON string of file objects in the format [{"type": "file", "id": "FILE_ID"}]
           Example: '[{"type": "file", "id": "12345"}]'

  Returns:
    The answer provided by the Box AI, or an error message.
  """
  logger.info(f"Asking Box AI (ID: {BOX_HUB_ID}): '{prompt}'")
  url = "https://api.box.com/2.0/ai/ask"
  headers = {
      "Authorization": f"Bearer {BOX_HUB_TOKEN}",
      "Content-Type": "application/json"
  }
  
  # Parse items string into proper JSON
  try:
      # If items is a string representation of a single object, wrap it in array brackets
      if items.strip().startswith('{'):
          items_json = f"[{items}]"
      else:
          items_json = items
      
      # Convert to Python objects to ensure valid JSON
      import json
      items_list = json.loads(items_json)
      
      payload = {
          "mode": "multiple_item_qa",
          "items": items_list,
          "prompt": prompt,
          "includes_citations": True
      }

      response = requests.post(url, headers=headers, json=payload)
      logger.info(f"Box ask API response status: {response.status_code}")
      response.raise_for_status()

      response_data = response.json()
      answer = response_data.get("answer")
      if answer:
          return answer
      else:
          completion_reason = response_data.get("completion_reason", "No reason provided.")
          logger.warning(f"Box Ask did not provide an answer. Reason: {completion_reason}")
          return f"Box Ask did not provide an answer. Reason: {completion_reason}"

  except json.JSONDecodeError as e:
      logger.error(f"Invalid JSON format for items: {e}")
      return f"Error: Invalid JSON format for items parameter. Please provide a properly formatted JSON array of file objects."
  except requests.exceptions.RequestException as e:
      logger.error(f"Error during Box Hub API call: {e}")
      error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') else "No response details."
      return f"API Error: Failed to ask Box Hub. {error_details}"
  except Exception as e:
      logger.error(f"An unexpected error occurred in box_AI_ask: {e}", exc_info=True)
      return f"An unexpected error occurred: {e}"