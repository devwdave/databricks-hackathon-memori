# Databricks Memori API

FastAPI backend for the Databricks Memori API.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Set your API keys in `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
MEMORI_API_KEY=your-memori-api-key-here
```

## Run

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs at `/docs`.

## Docker

From the repository root:

```bash
docker compose up --build
```

This starts the backend on port `8000`. To include the placeholder frontend container:

```bash
docker compose --profile frontend up --build
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/chat` | Send a message and receive a reply |

### Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```
