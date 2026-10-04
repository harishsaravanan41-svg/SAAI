from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import User
from backend.auth.dependencies import get_current_user
from backend.schemas.chat import ChatRequest, ChatResponse
from ai_model.qwen_client import qwen_orchestrator
import json

router = APIRouter(prefix="/api", tags=["Chat & AI Assistant"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Standard Batch Assistant Endpoint
    """
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]

    result = await qwen_orchestrator.chat(
        user_message=request.message,
        chat_history=history_dicts,
        db=db,
        current_user=current_user
    )

    return ChatResponse(
        response=result["response"],
        tool_executed=None,
        tool_arguments=None,
        tool_status=None,
        provider=result["provider"]
    )


@router.post("/chat/stream")
async def chat_stream_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    High-Performance Real-Time Streaming Endpoint (SSE):
    Streams generated tokens directly as they arrive from Qwen 2.5 1.5B.
    """
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history]

    async def event_generator():
        async for token in qwen_orchestrator.chat_stream(
            user_message=request.message,
            chat_history=history_dicts,
            db=db,
            current_user=current_user
        ):
            # Send Server-Sent Event chunk
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
