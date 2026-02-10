from typing import List, Tuple
import math

try:
    # Attempt to import the compiled Rust module
    import semantic_brain_core
except ImportError:
    # Fallback to pure Python implementation if Rust module is not compiled
    import logging
    logging.warning("Rust 'semantic_brain_core' not found. Falling back to pure Python implementation.")
    
    class MockRustModule:
        @staticmethod
        def score_relationship_path(edge_weights: List[f64], decay_factor: f64) -> float:
            total_score = sum(edge_weights)
            hop_count = len(edge_weights)
            return total_score * (decay_factor ** hop_count)

        @staticmethod
        def rank_nodes(nodes: List[Tuple[str, float]], connections: List[int]) -> List[Tuple[str, float]]:
            ranked = []
            for i, (node_id, base_score) in enumerate(nodes):
                conn_count = connections[i] if i < len(connections) else 0
                final_score = base_score * (1.0 + (conn_count * 0.1))
                ranked.append((node_id, final_score))
            
            # Sort by score descending
            ranked.sort(key=lambda x: x[1], reverse=True)
            return ranked

    semantic_brain_core = MockRustModule()

def score_path(edge_weights: List[float], decay_factor: float = 0.8) -> float:
    """Computes relevance score for a path of nodes."""
    return semantic_brain_core.score_relationship_path(edge_weights, decay_factor)

def rank_entities(nodes: List[Tuple[str, float]], connections: List[int]) -> List[Tuple[str, float]]:
    """Ranks entities based on base relevance and connection density."""
    return semantic_brain_core.rank_nodes(nodes, connections)
