FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent/ ./agent/
COPY tests/ ./tests/
COPY data/ ./data/
COPY main.py .
COPY pyproject.toml .

RUN pip install -e .

RUN useradd --create-home --shell /bin/bash agent && \
    chown -R agent:agent /app
USER agent

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import sys; from agent.agent import Agent; sys.exit(0 if Agent().answer('test') else 1)"

CMD ["python", "main.py", "What is 2 + 2?"]
