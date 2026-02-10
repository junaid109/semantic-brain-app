from typing import List, Dict, Any
from .graph_db import db
from loguru import logger

def ingest_document(doc_id: str, title: str, content: str, entities: List[Dict[str, Any]]):
    """
    Ingests a document and its extracted entities into the Semantic Graph.
    
    entities: List of dicts like {"name": "Project X", "type": "Project", "relation": "MENTIONS"}
    """
    logger.info(f"Ingesting document: {title} ({doc_id})")
    
    # Create Document node
    db.create_entity(title, "Document", {"doc_id": doc_id, "content": content})
    
    for entity in entities:
        name = entity.get("name")
        label = entity.get("type", "Entity")
        rel = entity.get("relation", "MENTIONS")
        
        # Create Entity node
        db.create_entity(name, label)
        
        # Create relationship from Document to Entity
        db.create_relationship(title, name, rel)
        
        # If there are relationships between entities, they should be handled here
        # Example: "Project X" belongs to "Department Y"
        if "relates_to" in entity:
            target = entity["relates_to"]
            target_type = entity.get("target_type", "Entity")
            db.create_entity(target, target_type)
            db.create_relationship(name, target, "RELATES_TO")

def get_related_context(entity_name: str, depth: int = 1) -> List[Dict[str, Any]]:
    """
    Traverses the graph to find related context for a given entity.
    """
    query = (
        "MATCH (e {name: $name})-[r*1..$depth]-(related) "
        "RETURN e.name as start, type(r[-1]) as relation, related.name as end, labels(related) as labels"
    )
    return db.execute_query(query, {"name": entity_name, "depth": depth})
