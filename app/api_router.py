from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.llm_service import stream_response, get_completion
from app.services.redis_service import save_message, load_history
from app.models.schema import ChatRequest, ChatResponse, HealthResponse
from app.config import settings
import asyncio
import logging

# 设置日志
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        message=f"{settings.APP_NAME} 服务运行正常"
    )

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """
    标准聊天接口 - 返回完整回复
    
    Args:
        req: 聊天请求，包含session_id、message等信息
        
    Returns:
        ChatResponse: AI回复结果
        
    Raises:
        HTTPException: 当处理失败时抛出异常
    """
    try:
        # 加载历史消息
        history = load_history(req.session_id)
        
        # 构建完整对话上下文
        messages = history + [req.message]
        prompt = "\n".join(messages)
        
        # 获取AI回复
        reply = await get_completion(
            prompt=prompt,
            model=req.model or settings.DEFAULT_MODEL,
            temperature=req.temperature or 0.7,
            max_tokens=req.max_tokens or 2000
        )
        
        # 保存对话记录
        save_message(req.session_id, req.message, reply)
        
        return ChatResponse(
            reply=reply,
            session_id=req.session_id,
            model=req.model or settings.DEFAULT_MODEL
        )
        
    except Exception as e:
        logger.error(f"聊天处理失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"聊天服务处理失败: {str(e)}"
        )

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """
    流式聊天接口 - 返回Server-Sent Events流
    
    Args:
        req: 聊天请求
        
    Returns:
        StreamingResponse: SSE流式响应
    """
    try:
        # 加载历史消息
        history = load_history(req.session_id)
        
        # 构建完整对话上下文
        messages = history + [req.message]
        prompt = "\n".join(messages)
        
        async def event_generator():
            """生成SSE事件流"""
            reply_chunks = []
            try:
                async for chunk in stream_response(
                    prompt=prompt,
                    model=req.model or settings.DEFAULT_MODEL,
                    temperature=req.temperature or 0.7,
                    max_tokens=req.max_tokens or 2000
                ):
                    reply_chunks.append(chunk)
                    yield f"data: {chunk}\n\n"
                    await asyncio.sleep(0.02)  # 控制流式输出速度
                
                # 保存完整对话
                full_reply = "".join(reply_chunks)
                save_message(req.session_id, req.message, full_reply)
                
                # 发送结束信号
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                logger.error(f"流式聊天失败: {str(e)}")
                yield f"data: {{\"error\": \"处理失败: {str(e)}\"}}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except Exception as e:
        logger.error(f"流式聊天初始化失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"流式聊天服务初始化失败: {str(e)}"
        )
