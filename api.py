import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi import Request
from rate_limit import enforce_rate_limit
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Local AI Agent API",
    description="An API for a tool-calling AI agent with RAG.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://project-06-ai-agent-web-app-murex.vercel.app",
    "https://project-06-ai-agent-web-o19vfvw37-deraras-projects.vercel.app", os.getenv("FRONTEND_URL", "http://localhost:5173"),],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class AgentRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="The question or task for the AI agent",
    )

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be blank.")

        return value

class AgentResponse(BaseModel):
    answer: str
    trace: list[dict]

@app.get("/health")
def health_check():
    """Check whether the API process is responding."""
    return {"status": "ok"}

@app.post("/chat", response_model=AgentResponse)
def chat_with_agent(
    payload: AgentRequest,
    request: Request,
) -> AgentResponse:
    enforce_rate_limit(request)
    """Send a question to the agent and return its answer and trace."""

    try:
        provider = os.getenv("AI_PROVIDER", "ollama").lower()

        if provider == "groq":
            from groq_agent import run_groq_agent
            answer, trace = run_groq_agent(request.message)

        elif provider == "ollama":
            from main import run_agent
            answer, trace = run_agent(request.message)

        else: 
            raise ValueError(
                f"Unsupported AI provider: {provider}"
            )

        return AgentResponse(answer=answer, trace=trace)

    except Exception as exc:
        # Avoid exposing internal exception details to API clients.
        raise HTTPException(
            status_code=500,
            detail="The agent encountered an unexpected error.",
        ) from exc