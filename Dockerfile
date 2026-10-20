FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/home/app/.cache/huggingface

WORKDIR / app

# Runtime library needed by common numberical/ML packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies separately to improve build caching
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Run the application as a non-root user
RUN useradd --create-home --uid 10001 app

COPY --chown=app:app . .

RUN mkdir -p /home/app/.cache/huggingface \
    && chown -R app:app /home/app

USER app

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]