import os
from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from loguru import logger

class GraphDB:
    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = user or os.getenv("NEO4J_USER", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD", "password")
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None):
        if not self.driver:
            logger.warning("Graph database driver not initialized.")
            return []
        
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def create_entity(self, name: str, node_type: str, properties: Dict[str, Any] = None):
        """Creates a node in the graph."""
        query = (
            f"MERGE (n:{node_type} {{name: $name}}) "
            f"SET n += $props "
            f"RETURN n"
        )
        return self.execute_query(query, {"name": name, "props": properties or {}})

    def create_relationship(self, from_node: str, to_node: str, rel_type: str, properties: Dict[str, Any] = None):
        """Creates a relationship between two nodes."""
        query = (
            "MATCH (a {name: $from_name}), (b {name: $to_name}) "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            "SET r += $props "
            "RETURN r"
        )
        return self.execute_query(query, {
            "from_name": from_node,
            "to_name": to_node,
            "props": properties or {}
        })

# Initialize a global instance or handle via FastAPI dependency injection
db = GraphDB()
