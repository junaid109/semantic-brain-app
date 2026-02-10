from typing import Any
from autogen_agentchat.agents import AssistantAgent
from loguru import logger

class Verifier:
    def __init__(self, model_client: Any):
        self.agent = AssistantAgent(
            name="verifier",
            model_client=model_client,
            description="A specialist in verifying factuality and relevance of retrieved research data.",
            system_message=(
                "You are a Verification Specialist. Your goal is to review the data provided by the Researcher. "
                "Ensure the relationships found are logically consistent and directly answer the user's query. "
                "If the information is incomplete or contradictory, flag it and suggest what's missing."
            )
        )
