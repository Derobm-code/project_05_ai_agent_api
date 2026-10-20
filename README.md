# Project 04 — AI Agent API with FastAPI and Docker

## About This Project

This is my fourth AI engineering project.

In my previous projects, I learned how to build a RAG system and an AI agent that can use tools. In this project, I wanted to take things further by turning my AI agent into an API that can run inside Docker.

The goal was to learn how to make an AI application accessible through HTTP requests instead of running everything directly from the terminal.

## What I Built

I built an AI agent API using Python, FastAPI, Ollama, and Docker.

The application can:

- Receive requests through a REST API.
- Use an AI agent to process questions.
- Call Python tools to perform calculations.
- Search a local knowledge base using RAG.
- Return answers through API responses.
- Run inside a Docker container.

I also added automated tests to check that different parts of the application work correctly.

## Technologies Used

- **Python** — Main programming language
- **FastAPI** — Building the API
- **Ollama** — Running local language models
- **Sentence Transformers** — Creating text embeddings
- **Docker** — Containerizing the application
- **Docker Compose** — Running the application container
- **Pytest** — Testing the code
- **Git and GitHub** — Version control

## Project Structure

```text
project-04-ai-agent-api/
├── api.py
├── main.py
├── tools.py
├── tool_models.py
├── tool_config.py
├── rag_tool.py
├── embeddings.py
├── chunking.py
├── similarity.py
├── documents/
├── static/
├── tests/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .dockerignore
└── README.md
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Derobm-code/project_04_ai_agent_api.git
cd project_04_ai_agent_api
```

### 2. Make sure Docker and Ollama are installed

This project uses Ollama to run the AI model locally.

Ollama needs to be running, and the model used by the agent needs to be available.

The Docker configuration also needs to allow the container to connect to Ollama on the host computer.

### 3. Build the Docker image

```bash
docker compose build
```

The first build might take some time because Python and the AI libraries need to be installed.

### 4. Start the application

```bash
docker compose up -d
```

### 5. Open the API documentation

Visit:

http://127.0.0.1:8000/docs

FastAPI provides an interactive page where the API endpoints can be tested.

### 6. Test the health endpoint

Open:

http://127.0.0.1:8000/health

Expected response:

```json
{
  "status": "ok"
}
```

You can also test the agent endpoint through the API documentation.

### 7. Stop the application

```bash
docker compose down
```

## Testing

I wrote tests for different parts of the application, including the API, agent logic, tools, and RAG functionality.

To run the tests in a Python environment with the required dependencies installed:

```bash
python -m pytest tests/
```

## What I Learned

This project helped me understand:

- How to build API endpoints with FastAPI.
- How to connect an AI agent to an API.
- How to send requests and receive responses.
- How Docker images and containers work.
- How to write a Dockerfile and Docker Compose configuration.
- How to test an API.
- How to debug build errors and container issues.
- How to push a complete project to GitHub.

One challenge I faced was building the Docker image because some AI libraries were large and took time to install. I also had to fix a few errors in the Dockerfile.

After fixing those issues, I managed to build the image, start the container, and test the API successfully.

## Future Improvements

Some things I would like to improve later:

- Build a better user interface.
- Add more tools to the agent.
- Improve error handling and logging.
- Add more API tests.
- Make the Docker image smaller.
- Explore deployment options.

## Final Thoughts

This project helped me move from building AI scripts to building an AI application that can be accessed through an API and run in a container.

I am learning AI engineering by building projects step by step, understanding the errors, and improving my code as I go.

This is part of my journey to becoming a better Python and AI engineer.