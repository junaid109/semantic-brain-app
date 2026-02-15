from api.ingestion import ingest_document
from loguru import logger
import time

def seeding_demo_data():
    logger.info("Seeding 'Semantic Brain' with Enterprise Sample Data...")
    
    # Sample 1: Project Apollo
    ingest_document(
        doc_id="DOC-001",
        title="Project Apollo Phase 1 Strategy",
        content="Apollo is our next-gen AI cloud initiative. Led by Sarah Chen from Engineering.",
        entities=[
            {"name": "Project Apollo", "type": "Project", "relation": "DESCRIBES"},
            {"name": "Sarah Chen", "type": "Person", "relation": "MENTIONS", "relates_to": "Engineering", "target_type": "Department"},
            {"name": "Engineering", "type": "Department", "relation": "OWNER_OF"}
        ]
    )

    # Sample 2: Budget Allocation
    ingest_document(
        doc_id="DOC-002",
        title="Q1 Fiscal Budget",
        content="The budget for Project Apollo is $2M. Approved by CFO Marcus.",
        entities=[
            {"name": "Project Apollo", "type": "Project", "relation": "HAS_BUDGET"},
            {"name": "Marcus", "type": "Person", "relation": "APPROVED_BY", "relates_to": "Finance", "target_type": "Department"},
            {"name": "Finance", "type": "Department", "relation": "MANAGES"}
        ]
    )

    # Sample 3: Infrastructure
    ingest_document(
        doc_id="DOC-003",
        title="Azure Migration Plan",
        content="Project Apollo will run on Azure Cosmos DB for the graph data.",
        entities=[
            {"name": "Project Apollo", "type": "Project", "relation": "REQUIRES"},
            {"name": "Azure Cosmos DB", "type": "Technology", "relation": "USED_BY"},
            {"name": "Microsoft", "type": "Company", "relation": "PROVIDER_OF", "relates_to": "Azure Cosmos DB", "target_type": "Technology"}
        ]
    )

    logger.success("Demo data seeded! You can now ask: 'Who is leading Project Apollo and what is the budget?'")

if __name__ == "__main__":
    seeding_demo_data()
