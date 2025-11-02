# AI Insurance Assistant — Copilot Instructions

Purpose: Give coding agents the minimal, actionable knowledge to be productive immediately in this repo.

1. Big picture (what to read first)

- FastAPI backend: `main.py` (app startup & lifespan). Routes are in `app/api/routes.py`.
- AI orchestration: `app/services/ai_service.py` (provider selection: fallback, `ollama`, `azure`).
- Knowledge base: `app/services/vector_service.py` (keyword-based FAQ search using `data/insurance_faq.py`).
- Persistence: `app/services/database_service.py` + `app/models/database.py` (async SQLAlchemy + SQLite).
- Frontend: Modern web UI in `static/` (HTML/CSS/JS with Material Icons, dual themes).

2. Key workflows / commands

- Local dev (quick):
  - create venv, install deps: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  - start server: `python main.py` or `./start.sh` (auto-reloads when DEBUG=True)
  - access UI: `http://localhost:8000/static/index.html`
  - API docs: `http://localhost:8000/docs`
- Docker: `docker-compose up -d` (see `docker-compose.yml` and `Dockerfile`)
- Tests: `pytest -q` (tests live in `tests/`)

3. Provider / integration notes (explicit)

- Default provider is configured in `app/config.py` via `model_provider` (env var: `MODEL_PROVIDER`). Valid values: `fallback`, `ollama`, `azure`.
- Ollama: local endpoint configured in `ollama_base_url` (`http://localhost:11434` by default). Calls to Ollama use a 60s timeout — failures fall back to `fallback` provider. See `_call_ollama` in `ai_service.py`.
- Azure OpenAI: enabled when `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_DEPLOYMENT` are set. Client is created in `ai_service.py` if configured.

4. Project-specific conventions and patterns

- Lightweight RAG: the vector store is keyword-based (no external embedding required) — `vector_store_service.search_similar()` returns FAQ dicts used as sources.
- Fallback-first design: the app always offers a reliable rule-based fallback. Any provider error should log and return fallback content (see error handling in `ai_service.get_response`).
- Async database: uses SQLAlchemy 2.x async engine + `async_sessionmaker`. DB URL is `DATABASE_URL` (default: `sqlite+aiosqlite:///./insurance_assistant.db`).
- Config: `pydantic-settings` (`app/config.py`) — prefer editing `.env` and let `get_settings()` pick values.

5. Useful examples (copyable bits)

- Health check: `GET /api/v1/health` (implemented in `app/api/routes.py`) — used to detect whether Ollama/Azure are available.
- Chat call (curl):
  curl -X POST http://localhost:8000/api/v1/chat -H 'Content-Type: application/json' -d '{"message":"What is life insurance?"}'
- Switch provider locally (temporary): `export MODEL_PROVIDER=ollama` and ensure Ollama is running at `OLLAMA_BASE_URL`.

6. Where to look for implementation details

- Prompt engineering and context building: `app/services/ai_service.py` (`_build_context_prompt`).
- Fallback responses & ranking logic: `app/services/vector_service.py` (keyword similarity) and `_get_fallback_response` in `ai_service.py`.
- DB model & conversation persistence: `app/models/database.py` and `save_conversation`/`get_conversation_history` in `database_service.py`.

7. Common pitfalls observed in runtime

- "Address already in use" — caused by multiple servers. Check port 8000 and kill stale processes with `lsof -i :8000`.
- Ollama timeouts (60s) — the code catches timeouts and falls back. To reproduce provider flow, run Ollama locally and set `MODEL_PROVIDER=ollama`.
- CORS issues — if accessing UI from different origin, ensure CORS is configured in `main.py`.

8. Quick tips for contributors/agents

- Preserve fallback behavior when editing provider calls — don't remove the try/except that falls back to rule-based answers.
- Keep changes small and add a test in `tests/` when you alter public endpoints or DB behavior.
- Prefer editing `.env` for configuration changes rather than hard-coding values.

If anything here is unclear or you want more examples (e.g., editing a route, adding an embedding model, or enabling Azure), tell me which section to expand and I'll iterate.
