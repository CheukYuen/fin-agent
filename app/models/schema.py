from pydantic import BaseModel, Field
from typing import Optional
from app.config import settings

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="会话ID，用于保持对话上下文")
    message: str = Field(..., description="用户消息内容", min_length=1)
    model: Optional[str] = Field(
        default=settings.DEFAULT_MODEL, 
        description="AI模型名称，默认使用qwen-plus"
    )
    temperature: Optional[float] = Field(
        default=0.7, 
        description="生成温度，控制回复的随机性",
        ge=0.0,
        le=2.0
    )
    max_tokens: Optional[int] = Field(
        default=2000,
        description="最大生成token数量",
        gt=0,
        le=4000
    )

class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI回复内容")
    session_id: str = Field(..., description="会话ID")
    model: str = Field(..., description="使用的AI模型名称")

class HealthResponse(BaseModel):
    status: str = Field(..., description="服务状态")
    message: str = Field(..., description="状态消息")
