from typing import AsyncGenerator
import openai
from openai import AsyncOpenAI
from app.config import settings
from fastapi import HTTPException

# 初始化 OpenAI 客户端（连接阿里云百炼）
client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

async def stream_response(
    prompt: str, 
    model: str = settings.DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> AsyncGenerator[str, None]:
    """
    流式调用Qwen模型生成回复
    
    Args:
        prompt: 用户输入的提示词
        model: 模型名称，默认使用qwen-plus
        temperature: 生成温度，控制回复的随机性
        max_tokens: 最大生成token数
        
    Yields:
        str: 流式生成的文本片段
        
    Raises:
        HTTPException: 当API调用失败时抛出异常
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except openai.APIError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI服务调用失败: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"未知错误: {str(e)}"
        )

async def get_completion(
    prompt: str,
    model: str = settings.DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    非流式调用Qwen模型获取完整回复
    
    Args:
        prompt: 用户输入的提示词
        model: 模型名称，默认使用qwen-plus
        temperature: 生成温度
        max_tokens: 最大生成token数
        
    Returns:
        str: 完整的AI回复
        
    Raises:
        HTTPException: 当API调用失败时抛出异常
    """
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content or ""
        
    except openai.APIError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI服务调用失败: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"未知错误: {str(e)}"
        )
