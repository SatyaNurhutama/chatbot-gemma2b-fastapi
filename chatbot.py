import uuid
from fastapi import FastAPI, Request
from chat_manager import ChatSession
from token_utils import count_tokens
from chat_db import init_db, save_session, load_session

import ollama

app = FastAPI()
session = ChatSession(max_messages=10)
MAX_TOKENS = 2048
RESERVED_FOR_REPLY = 256 

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    template = body.get("template", "default")
    session_id = body.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())  # generate anonymous session_id

    # Load from DB
    session = ChatSession(max_messages=10, template=template)
    stored_history = await load_session(session_id)
    if stored_history:
        session.load_history(stored_history)
    
    session.add_user_message(user_input)

    # Validate token
    token_count = count_tokens(session.get_history())
    if token_count > (MAX_TOKENS - RESERVED_FOR_REPLY):
        return {"error": "Token limit exceeded"}
    
    response = ollama.chat(
        model="gemma:2b", 
        messages=session.get_history(),
    )

    reply = response['message']['content']
    session.add_assistant_message(reply)

    await save_session(session_id, session.export_history())
    
    return {
        "reply": reply,
        "session_id": session_id
    }
