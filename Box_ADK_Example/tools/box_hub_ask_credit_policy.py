import os
import logging 
import requests
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables for Credit Policy Hub
BOX_HUB_TOKEN = os.getenv("BOX_HUB_TOKEN", "YOUR_HUB_TOKEN_HERE")
BOX_HUB_CREDIT_POLICY_ID = os.getenv("BOX_HUB_CREDIT_POLICY_ID", "YOUR_CREDIT_POLICY_HUB_ID_HERE")

def box_hub_ask_credit_policy(prompt: str) -> str:
    """
    Sends a prompt to the Credit Policy Box AI Hub for compliance analysis.
    
    Args:
        prompt: The credit policy question or loan scenario to analyze.
        
    Returns:
        Credit policy analysis response or error message.
    """
    logger.info(f"Asking Credit Policy Hub (ID: {BOX_HUB_CREDIT_POLICY_ID}): '{prompt}'")
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
                "id": BOX_HUB_CREDIT_POLICY_ID
            }
        ],
        "prompt": prompt,
        "includes_citations": True  # Enable citations for policy references
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f"Credit Policy Hub API response status: {response.status_code}")
        response.raise_for_status()

        response_data = response.json()
        answer = response_data.get("answer")
        if answer:
            return answer
        else:
            completion_reason = response_data.get("completion_reason", "No reason provided.")
            logger.warning(f"Credit Policy Hub did not provide an answer. Reason: {completion_reason}")
            return f"Credit Policy Hub did not provide an answer. Reason: {completion_reason}"

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Credit Policy Hub API call: {e}")
        error_details = f"Status: {e.response.status_code}. Details: {e.response.text}" if hasattr(e, 'response') and e.response else "No response details."
        return f"API Error: Failed to ask Credit Policy Hub. {error_details}"
    except Exception as e:
        logger.error(f"An unexpected error occurred in box_hub_ask_credit_policy: {e}", exc_info=True)
        return f"An unexpected error occurred: {e}"