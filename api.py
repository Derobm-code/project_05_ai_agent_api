from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from main import run_agent

app = FastAPI(
    title="Local AI Agent API",
    description="An API for a tool-calling AI agent with RAG.",
    version="0.1.0",
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
def chat_with_agent(request: AgentRequest) -> AgentResponse:
    """Send a question to the agent and return its answer and trace."""

    try:
        answer, trace = run_agent(request.message)

        return AgentResponse(
            answer=answer,
            trace=trace,
        )

    except Exception as exc:
        # Avoid exposing internal exception details to API clients.
        raise HTTPException(
            status_code=500,
            detail="The agent encountered an unexpected error.",
        ) from exc