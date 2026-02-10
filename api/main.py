import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from agents.orchestrator import SemanticBrainOrchestrator
from autogen_ext.models.openai import OpenAIChatCompletionClient
from loguru import logger
import os

app = FastAPI(title="Semantic Brain API")

# Setup Model Client (Mock/Real depending on env)
def get_model_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found. Ensure .env is configured.")
        # Returning a dummy or raising error depending on preference
    return OpenAIChatCompletionClient(model="gpt-4-turbo-preview", api_key=api_key)

orchestrator = SemanticBrainOrchestrator(get_model_client())

@app.get("/")
async def root():
    return {"message": "Welcome to Semantic Brain Enterprise Search API"}

@app.post("/query")
async def query_stream(request: Request):
    """
    Streaming endpoint for complex relational queries.
    """
    data = await request.json()
    user_query = data.get("query")
    
    if not user_query:
        return {"error": "Query is required"}

    async def event_generator():
        try:
            async for chunk in orchestrator.run_query(user_query):
                # Yield as Server-Sent Events (SSE)
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            logger.error(f"Error in query stream: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
