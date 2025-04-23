# ----- File: multi_tool_agent/agent.py -----


# Import necessary components from the google.adk namespace
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.sequential_agent import SequentialAgent
from .sub_agents.Box_search_agent import *# Import the Box search agent
from .sub_agents.Box_hub_agent import *# Import the Box hub agent


root_agent = SequentialAgent(
   name = "root_agent",
   sub_agents=[Box_search_agent,Box_hub_agent]
)