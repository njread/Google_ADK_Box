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
SALESFORCE_SEARCH_TOKEN = os.getenv("SALESFORCE_SEARCH_TOKEN", "YOUR_METADATA_TOKEN_HERE")

def Salesforce_generic_search(prompt: str) -> str:
    """
    Sends a prompt to a specific Salesforce Search to get answers based on its associated content.

    Args:
      prompt: The question or prompt to ask the Salesforce search.

    Returns:
      The answer provided by the Salesforce Hub, or an error message.
    """
    logger.info(f"Finding Salesforce content from: '{prompt}'")
    url = f"https://MyDomainName.my.salesforce.com/services/data/v63.0/parameterizedSearch/?q={prompt}"
    headers = {
        "Authorization": f"Bearer {SALESFORCE_SEARCH_TOKEN}"
    }
   
    try:
        # Change this line from POST to GET
        response = requests.get(url, headers=headers)  # Change from POST to GET
        logger.info(f"Salesforce Search API response status: {response.status_code}")
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
            return f"No Salesforce content found matching '{prompt}'."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Salesforce Search call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') and e.response else "No response details."
        return f"API Error: Failed to ask Salesforce Search. {error_details}"
    except Exception as e:
        logger.error(f"An unexpected error occurred in Salesforce_generic_search: {e}", exc_info=True)
        return f"An unexpected error occurred: {e}"