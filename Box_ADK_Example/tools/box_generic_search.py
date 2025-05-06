# ----- File: multi_tool_agent/agent.py -----

import os
import requests
import logging # Optional: for better logging
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from a .env file if it exists
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# !! SECURITY WARNING !!
# Replace these with a secure method, e.g., environment variables
BOX_METADATA_TOKEN = os.getenv("BOX_METADATA_TOKEN", "YOUR_METADATA_TOKEN_HERE")
BOX_HUB_TOKEN = os.getenv("BOX_HUB_TOKEN", "YOUR_HUB_TOKEN_HERE")
BOX_ENTERPRISE_ID = os.getenv("BOX_ENTERPRISE_ID", "YOUR_BOX_ENTERPRISE_ID_HERE")
BOX_HUB_ID = os.getenv("BOX_HUB_ID", "YOUR_BOX_HUB_ID_HERE") # e.g., "216163155"


def box_generic_search(prompt: str) -> str:
    """
    Sends a prompt to a specific Box Search to get answers based on its associated content.

    Args:
      prompt: The question or prompt to ask the Box search.

    Returns:
      The answer provided by the Box Hub, or an error message.
    """
    logger.info(f"Finding Box content from: '{prompt}'")
    url = f"https://api.box.com/2.0/search?query={prompt}"
    headers = {
        "Authorization": f"Bearer {BOX_HUB_TOKEN}"
    }
   
    try:
        # Change this line from POST to GET
        response = requests.get(url, headers=headers)  # Change from POST to GET
        logger.info(f"Box Search API response status: {response.status_code}")
        response.raise_for_status() # Check for HTTP errors

        response_data = response.json()
        entries = response_data.get("entries")
        if entries:
            # Format the results nicely
            results = []
            for entry in entries:
                name = entry.get("name", "Unnamed item")
                item_type = entry.get("type", "unknown")
                item_id = entry.get("id", "unknown")
                results.append(f"- {name} (Type: {item_type}, ID: {item_id})")
            
            return "Found the following items:\n" + "\n".join(results)
        else:
            # Handle cases where the API succeeds but provides no results
            return f"No Box content found matching '{prompt}'."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Box Search call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') and e.response else "No response details."
        return f"API Error: Failed to ask Box Search. {error_details}"
    except Exception as e:
        logger.error(f"An unexpected error occurred in box_generic_search: {e}", exc_info=True)
        return f"An unexpected error occurred: {e}"