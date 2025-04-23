
from google.adk.agents import LlmAgent # Use LlmAgent
from .Box_hub_GTM_agent import Box_hub_GTM_agent
from .Box_hub_Products_agent import Box_hub_Products_agent

Box_hub_agent = LlmAgent(
    model='gemini-2.0-flash', # Or your preferred Gemini model
    name = "Box_Hub_Agent", # Name of the agent
    description="""
    You are a helpful assistant designed to interact with Box content using specialized tools.
    Your primary goal is to answer user questions accurately using the provided tools.
    Sub Agent Guidance:
    1. For questions related to GTM (Go To Market) content, use the box_hub_ask_GTM tool. Pass the user's core question directly as the 'prompt'. Preface your final answer to the user with "This is what I found with Box Hub GTM: ".
    2. For questions related to general product questions use the product hub agent. 
    3. If an agent returns an error message (e.g., starting with 'API Error:' or 'An unexpected error occurred:'), relay that information clearly to the user. If it returns 'No files found...' or 'Box Hub did not provide an answer...', state that to the user. Then give them suggestoins on how to contruct their questions. 
    """,
sub_agents=[Box_hub_GTM_agent, Box_hub_Products_agent] # List of sub-agents to use
)
