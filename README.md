# AI Agent API — FastAPI, Groq, Tools & RAG

A deployed Python AI-agent backend that combines LLM reasoning, structured tool execution, knowledge-base retrieval, and API rate limiting. Built with FastAPI and designed to support both local development and a lightweight serverless cloud deployment.

**Live API:** https://project-05-ai-agent-api.vercel.app  
**Interactive API documentation:** https://project-05-ai-agent-api.vercel.app/docs  
**Live frontend:** https://project-06-ai-agent-web-app-murex.vercel.app

## Features

- **Agentic tool calling:** The model can select and execute Python functions and return a step-by-step execution trace.
- **Seven tools:** `calculate_percentage`, `add_numbers`, `multiply_numbers`, `subtract_numbers`, `calculate_remaining_after_reduction`, `get_current_datetime`, and `search_knowledge_base`.
- **Retrieval-augmented generation (RAG):** Retrieves relevant text from a small curated knowledge base to support answers.
- **Two execution modes:** Groq-hosted inference for the deployed API, and an Ollama-based local workflow.
- **Request validation:** FastAPI and Pydantic validate incoming requests and outgoing responses.
- **Rate limiting:** Upstash Redis-backed request counters help protect the hosted model quota. The current configuration allows 10 requests per IP per hourly window.
- **CORS:** Allows the configured frontend to communicate with the API.

## Architecture

```text
React + TypeScript frontend (Vercel)
             |
             | POST /chat
             v
      FastAPI backend (Vercel)
             |
       Upstash Redis
       rate-limit check
             |
             v
        AI provider
        /         \
  Groq (cloud)  Ollama (local)
        |             |
        +------ Tool calling ------+
                     |
             Python utility tools
                     |
            Knowledge-base search
                     |
        Answer + tool execution trace
                     |
                     v
               React frontend
```

### Cloud versus local RAG

| Mode | Inference | Retrieval |
| --- | --- | --- |
| Cloud / Vercel | Groq (`openai/gpt-oss-20b`, subject to provider availability) | Lightweight TF-IDF search over `cloud_rag_index.json` |
| Local development | Ollama | Sentence Transformers embeddings and semantic retrieval |

The cloud index stores document text chunks without the unused embedding arrays. This avoids deploying the heavy local embedding stack to the serverless environment. The cloud retrieval path is **TF-IDF**, not vector similarity search.

## API

### `GET /health`

Health-check endpoint.

Example response:

```json
{"status": "ok"}
```

### `POST /chat`

Request:

```json
{"message": "Calculate 15% of 240"}
```

Example response (trace shape illustrated):

```json
{
  "answer": "15% of 240 is 36.",
  "trace": [
    {
      "step": 1,
      "tool": "calculate_percentage",
      "arguments": {"percentage": 15, "value": 240},
      "result": 36
    }
  ]
}
```

Try the endpoint interactively at [Swagger UI](https://project-05-ai-agent-api.vercel.app/docs). Actual wording and trace details may vary by request.

## Local setup

Prerequisites: Python 3.12+ and an available AI provider. For the local Ollama workflow, install and run Ollama with the model configured in the project.

1. Clone this repository and open the backend directory.
2. Create and activate a Python virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies required for the mode you intend to run. For the lightweight cloud-compatible mode, install the packages declared in `pyproject.toml`:

   ```powershell
   pip install .
   ```

4. Configure environment variables (see below).
5. Start the API:

   ```powershell
   uvicorn api:app --reload
   ```

6. Visit `http://127.0.0.1:8000/docs`.

**Note:** The local Ollama/semantic-RAG workflow also needs its original local model and embedding dependencies; the minimal cloud dependency set does not install those heavy packages.

## Environment variables

| Variable | Required for | Description |
| --- | --- | --- |
| `AI_PROVIDER` | Both | `groq` for cloud or `ollama` for local mode |
| `GROQ_API_KEY` | Groq mode | Secret API key for hosted inference |
| `UPSTASH_REDIS_REST_URL` | Deployed rate-limited API | Upstash Redis REST endpoint |
| `UPSTASH_REDIS_REST_TOKEN` | Deployed rate-limited API | Secret Upstash REST token |
| `FRONTEND_URL` | CORS configuration, where used | Allowed frontend origin |

Store secrets in Vercel Environment Variables for production. Never commit `.env` files, tokens, or API keys. If the rate limiter is enabled but its Upstash credentials are absent or unusable, `/chat` may return HTTP 503.

## Deployment

The backend is deployed independently to Vercel using `api:app` as the FastAPI entry point. The cloud dependency list is defined in `pyproject.toml` and includes FastAPI, Pydantic, Groq, and HTTPX.

Deployment checklist:

1. Deploy the backend repository to Vercel.
2. Set `AI_PROVIDER=groq`, `GROQ_API_KEY`, and both Upstash REST environment variables.
3. Configure the frontend origin for CORS.
4. Verify `/health`, `/docs`, a calculation tool call, and a knowledge-base retrieval request.
5. Verify the rate limiter returns HTTP 429 after the configured request threshold.

## Security and limitations

- The IP-based limiter is a basic quota safeguard, not complete protection against automated abuse.
- Public requests are subject to Groq and Upstash service limits.
- The bundled cloud RAG index contains document text. Review it before committing it to a public repository.
- Generated answers may be imperfect; tool traces make supported calculations and retrieval steps easier to inspect.

## Related project

**AI Agent Web App:** https://project-06-ai-agent-web-app-murex.vercel.app
