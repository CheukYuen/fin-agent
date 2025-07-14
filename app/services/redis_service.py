from typing import List, Optional
import redis
from redis.exceptions import RedisError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# 初始化Redis连接
try:
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    # 测试连接
    r.ping()
    logger.info("Redis连接成功")
except RedisError as e:
    logger.error(f"Redis连接失败: {str(e)}")
    r = None

def load_history(session_id: str, max_messages: int = 20) -> List[str]:
    """
    加载会话历史记录
    
    Args:
        session_id: 会话ID
        max_messages: 最大消息数量
        
    Returns:
        List[str]: 历史消息列表
    """
    if not r:
        logger.warning("Redis未连接，返回空历史记录")
        return []
    
    try:
        # 获取最近的消息（限制数量避免过长）
        messages = r.lrange(session_id, -max_messages, -1)
        return messages
    except RedisError as e:
        logger.error(f"加载历史记录失败 session_id={session_id}: {str(e)}")
        return []

def save_message(session_id: str, user_msg: str, bot_msg: str) -> bool:
    """
    保存对话消息
    
    Args:
        session_id: 会话ID
        user_msg: 用户消息
        bot_msg: 机器人回复
        
    Returns:
        bool: 保存是否成功
    """
    if not r:
        logger.warning("Redis未连接，无法保存消息")
        return False
    
    try:
        # 保存用户消息和AI回复
        r.rpush(session_id, f"用户: {user_msg}")
        r.rpush(session_id, f"AI: {bot_msg}")
        
        # 设置过期时间（24小时）
        r.expire(session_id, 86400)
        
        return True
    except RedisError as e:
        logger.error(f"保存消息失败 session_id={session_id}: {str(e)}")
        return False

def clear_history(session_id: str) -> bool:
    """
    清除会话历史
    
    Args:
        session_id: 会话ID
        
    Returns:
        bool: 清除是否成功
    """
    if not r:
        logger.warning("Redis未连接，无法清除历史")
        return False
    
    try:
        r.delete(session_id)
        return True
    except RedisError as e:
        logger.error(f"清除历史失败 session_id={session_id}: {str(e)}")
        return False

def get_session_count() -> int:
    """
    获取当前活跃会话数量
    
    Returns:
        int: 会话数量
    """
    if not r:
        return 0
    
    try:
        # 简单统计，实际生产环境可能需要更复杂的逻辑
        return len(r.keys("*"))
    except RedisError as e:
        logger.error(f"获取会话数量失败: {str(e)}")
        return 0
