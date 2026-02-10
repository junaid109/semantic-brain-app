from typing import List, Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from api.ingestion import get_related_context
from core.bridge import score_path, rank_entities
from loguru import logger

class Researcher:
    def __init__(self, model_client: Any):
        self.agent = AssistantAgent(
            name="researcher",
            model_client=model_client,
            description="A specialist in navigating the Semantic Graph to find relevant documents and relationships.",
            system_message=(
                "You are a Graph Researcher. Your goal is to find relationships between documents and entities. "
                "Use the provided tools to fetch context from the graph and rank findings by relevance. "
                "Focus on multi-hop connections (e.g., Doc A -> Project X -> Dept Y)."
            )
        )

    async def get_graph_context(self, entity_name: str, depth: int = 1) -> str:
        """Tool for the agent to fetch context from the graph."""
        logger.info(f"Researcher fetching context for: {entity_name}")
        results = get_related_context(entity_name, depth)
        
        if not results:
            return f"No relationships found for '{entity_name}' at depth {depth}."
        
        # Format results for the agent
        context = []
        for r in results:
            context.append(f"{r['start']} --[{r['relation']}]--> {r['end']} ({r['labels']})")
        
        return "\n".join(context)

    async def rank_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Tool to rank findings using the Rust-optimized bridge."""
        # Preparation for ranking: convert findings to (id, score) and connection counts
        nodes = [(f["name"], f.get("base_score", 1.0)) for f in findings]
        connections = [f.get("conn_count", 0) for f in findings]
        
        ranked = rank_entities(nodes, connections)
        return [{"name": name, "score": score} for name, score in ranked]
