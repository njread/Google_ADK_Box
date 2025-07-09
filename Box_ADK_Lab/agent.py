# File: agent.py

import logging
from typing import AsyncGenerator
from typing_extensions import override

from google.adk.agents import LlmAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event

# Import sub-agents
from Box_ADK_Example.sub_agents.Box_search_agent import Box_search_agent
from Box_ADK_Example.sub_agents.Box_hub_agent import Box_hub_agent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the decision router agent
decision_router = LlmAgent(
    model='gemini-2.0-flash',
    name="DecisionRouter",
    instruction="""
    You are a decision router for Box content queries. Your task is to determine whether a query should be 
    directed to the Box Search agent or the Box Hub agent based on the content of the query.
    
    INSTRUCTIONS:
    
    1. Analyze the user's query to determine its nature.
    
    2. If the query is about:
       - Product-specific information (features, specifications, releases, etc.)
       - Go-to-Market (GTM) content (marketing, sales materials, pitch decks, etc.)
       - Specific hubs or departments within Box
       => Output "box_hub"
    
    3. If the query is about:
       - General document searches across all content
       - Specific file retrieval or information extraction
       - Content analysis that doesn't specifically reference products or GTM materials
       => Output "box_search"
    
    4. Your output should ONLY be the exact text "box_hub" or "box_search" - nothing else.
    
    5. If you're uncertain, default to "box_search" as it has broader capabilities.
    
    Examples:
    - Query: "Find presentations about Relay" -> Output: "box_hub"
    - Query: "What documents mention Q4 sales targets?" -> Output: "box_search"
    - Query: "Tell me about the new product launch materials" -> Output: "box_hub"
    - Query: "Find all documents that mention AI capabilities" -> Output: "box_search"
    """,
    output_key="routing_decision",  # Key for storing the routing decision in session state
)

class BoxFlowAgent(BaseAgent):
    """
    Custom agent for Box content search workflow.
    
    This agent decides whether to route queries to the Box Search agent
    or the Box Hub agent based on the content of the query.
    """
    
    # Field declarations for Pydantic
    decision_router: LlmAgent
    box_search_agent: LlmAgent
    box_hub_agent: LlmAgent
    
    # Allow arbitrary types for Pydantic
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(
        self,
        name: str,
        decision_router: LlmAgent,
        box_search_agent: LlmAgent,
        box_hub_agent: LlmAgent,
    ):
        """
        Initializes the BoxFlowAgent.
        
        Args:
            name: The name of the agent.
            decision_router: An LlmAgent to decide which path to take.
            box_search_agent: An LlmAgent for Box content search.
            box_hub_agent: An LlmAgent for Box hub interactions.
        """
        # Define the sub_agents list for the framework
        sub_agents_list = [
            decision_router,
            box_search_agent,
            box_hub_agent,
        ]
        
        # Pydantic will validate and assign them based on the class annotations
        super().__init__(
            name=name,
            decision_router=decision_router,
            box_search_agent=box_search_agent,
            box_hub_agent=box_hub_agent,
            sub_agents=sub_agents_list,
        )
    
    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """
        Implements the custom orchestration logic for the Box search workflow.
        Uses the decision router to determine which path to take.
        """
        logger.info(f"[{self.name}] Starting Box content search workflow.")
        
        # 1. Run Decision Router
        logger.info(f"[{self.name}] Running DecisionRouter...")
        async for event in self.decision_router.run_async(ctx):
            logger.info(f"[{self.name}] Event from DecisionRouter: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        # 2. Check the routing decision
        routing_decision = ctx.session.state.get("routing_decision")
        logger.info(f"[{self.name}] Routing decision: {routing_decision}")
        
        if not routing_decision:
            logger.error(f"[{self.name}] Failed to make routing decision. Defaulting to Box Search.")
            routing_decision = "box_search"
        
        # 3. Execute the appropriate agent based on the decision
        if routing_decision == "box_hub":
            logger.info(f"[{self.name}] Running Box Hub Agent...")
            async for event in self.box_hub_agent.run_async(ctx):
                logger.info(f"[{self.name}] Event from BoxHubAgent: {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
        else:  # Default to box_search
            logger.info(f"[{self.name}] Running Box Search Agent...")
            async for event in self.box_search_agent.run_async(ctx):
                logger.info(f"[{self.name}] Event from BoxSearchAgent: {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
        
        logger.info(f"[{self.name}] Workflow finished.")

# Create and export the root_agent
# THIS IS THE CRITICAL LINE FOR THE ADK CLI
root_agent = BoxFlowAgent(
    name="BoxFlowAgent",
    decision_router=decision_router,
    box_search_agent=Box_search_agent,
    box_hub_agent=Box_hub_agent,
)