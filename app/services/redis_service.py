import redis
from app.config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def load_history(session_id: str) -> list:
    return r.lrange(session_id, 0, -1)

def save_message(session_id: str, user_msg: str, bot_msg: str):
    r.rpush(session_id, f"user: {user_msg}")
    r.rpush(session_id, f"bot: {bot_msg}")
