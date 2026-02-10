from typing import List, Any
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from .researcher import Researcher
from .verifier import Verifier
from loguru import logger

class SemanticBrainOrchestrator:
    def __init__(self, model_client: Any):
        self.researcher = Researcher(model_client)
        self.verifier = Verifier(model_client)
        
        # Define the team
        self.team = RoundRobinGroupChat(
            [self.researcher.agent, self.verifier.agent],
            max_turns=6
        )

    async def run_query(self, query: str):
        """
        Runs a query through the Researcher -> Verifier pipeline.
        Yields messages for streaming.
        """
        logger.info(f"Starting multi-agent orchestration for query: {query}")
        
        # Start the conversation
        async for message in self.team.run_stream(task=query):
            # Extract content and metadata for streaming
            if hasattr(message, 'content'):
                yield {
                    "agent": message.source,
                    "content": message.content,
                    "type": "text"
                }
            elif hasattr(message, 'tool_calls'):
                yield {
                    "agent": message.source,
                    "content": f"Calling tools: {[t.name for t in message.tool_calls]}",
                    "type": "tool"
                }

# Usage example (async context):
# orchestrator = SemanticBrainOrchestrator(model_client)
# async for chunk in orchestrator.run_query("Who works on Project Apollo?"):
#     print(chunk)
