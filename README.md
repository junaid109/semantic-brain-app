# Semantic Brain: Enterprise Search

A RAG (Retrieval-Augmented Generation) system utilizing a Semantic Graph for advanced relationship understanding.

## Tech Stack
- **Python**: Orchestration & API.
- **Microsoft Agent Framework**: Multi-agent Researcher/Verifier workflows.
- **Rust**: High-performance graph traversal (PyO3).
- **Neo4j**: Semantic Graph storage.
- **FastAPI**: Streaming API endpoint.

## Project Structure
- `api/`: FastAPI server and database logic.
- `agents/`: AgentChat (Magentic-One) orchestration.
- `core/`: Rust performance bridge.
- `config/`: Application settings.

## Setup
1. Clone the repository.
2. Setup a Python virtual environment.
3. Install dependencies: `pip install -e .`
4. Configure `.env` based on `.env.example`.
5. (Optional) Compile Rust core: `cd core && maturin develop`.
