FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry install

COPY . /app

# application port
EXPOSE 8000
# debug port
EXPOSE 5678

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
