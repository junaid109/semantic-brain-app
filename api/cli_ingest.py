import argparse
from api.ingestion import ingest_document
from loguru import logger

def main():
    parser = argparse.ArgumentParser(description="Ingest sample document into Semantic Brain")
    parser.add_argument("--id", required=True, help="Document ID")
    parser.add_argument("--title", required=True, help="Document Title")
    parser.add_argument("--content", required=True, help="Document Content")
    
    args = parser.parse_args()
    
    # Sample entities for testing
    sample_entities = [
        {"name": "Project Apollo", "type": "Project", "relation": "MENTIONS"},
        {"name": "Engineering", "type": "Department", "relation": "OWNED_BY", "relates_to": "HQ", "target_type": "Location"}
    ]
    
    try:
        ingest_document(args.id, args.title, args.content, sample_entities)
        logger.success(f"Successfully ingested {args.title}")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")

if __name__ == "__main__":
    main()
