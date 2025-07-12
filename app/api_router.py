from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.llm_service import stream_response
from app.services.redis_service import save_message, load_history
from app.models.schema import ChatRequest, ChatResponse
import asyncio

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    history = load_history(req.session_id)
    prompt = "\n".join(history + [req.message])
    gen = stream_response(prompt, model=req.model or "gpt-3.5-turbo")
    reply = ""
    async for chunk in gen:
        reply += chunk
    save_message(req.session_id, req.message, reply)
    return ChatResponse(reply=reply)

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    history = load_history(req.session_id)
    prompt = "\n".join(history + [req.message])
    async def event_gen():
        async for chunk in stream_response(prompt, model=req.model or "gpt-3.5-turbo"):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.05)
    return StreamingResponse(event_gen(), media_type="text/event-stream")
