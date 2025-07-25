# 💬 Gemma Chat Backend

A lightweight, token-aware chatbot backend powered by [Ollama](https://ollama.com) and the [Gemma 2B](https://huggingface.co/google/gemma-2b) LLM — built with FastAPI, session persistence (SQLite), prompt templating, and clean backend design.

---

## Features

- Local LLM chat using `ollama` and `gemma:2b`
- Persistent chat history using SQLite
- Token budget awareness (respects LLM context limit)
- Prompt templates for custom assistant behavior
- Environment-based configuration (`.env`)
- Auto-cleans expired sessions (configurable)
- Built with FastAPI (async-ready and production-friendly)

---

## Tech Stack
- Python 3.10+
- FastAPI
- aiosqlite
- Ollama (for local LLM serving)
- dotenv
- Deque (in-memory message queue)

---

## Project Structure
```
├── chat_manager.py # Session memory (deque + templates)
├── chat_db.py # SQLite async storage
├── chatbot.py # FastAPI app
├── prompt_templates.py # System prompt configurations
├── token_utils.py # Token counting utility
├── .env # Environment config (DB path, Ollama settings)
```

## Set Up .env
```
DB_PATH=/Users/<your-username>/Documents/labs/my_chatbot.db
HF_TOKEN=
```
HF_TOKEN = get the token [here](https://huggingface.co/settings/tokens)

## Example Request (using curl)
```
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is a Python decorator?",
    "template": "default"
}'

```
