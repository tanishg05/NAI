import time
import logging
from typing import Dict, Any
from app.agents.diet_planner_agent import DietPlannerAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.core.groq_client import AgentGenerationError

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        # Register implemented agents
        self.registry = {
            "diet_planner": DietPlannerAgent(),
            "recommendation": RecommendationAgent(),
            # Future agents like "food_vision", "nutrition_analysis", "profile_health", "progress_feedback" will go here
        }

    async def route(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routes a request to the appropriate agent and logs execution details.
        """
        if agent_name not in self.registry:
            raise ValueError(f"Agent '{agent_name}' not found in registry.")

        agent = self.registry[agent_name]
        start_time = time.time()
        
        logger.info(f"Routing request to {agent_name} agent...")
        
        try:
            result = await agent.run(payload)
            latency = time.time() - start_time
            logger.info(f"Agent {agent_name} execution successful. Latency: {latency:.2f}s")
            # In the future, Progress & Feedback agent could consume this log/event stream
            return result
            
        except AgentGenerationError as e:
            latency = time.time() - start_time
            logger.error(f"Agent {agent_name} execution failed after {latency:.2f}s: {e}")
            raise e

orchestrator = Orchestrator()
