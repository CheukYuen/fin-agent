import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    # 阿里云百炼平台配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # 这里是阿里云的API Key
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    # Qwen 模型配置
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-plus")
    
    # Redis 配置
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # 应用配置
    APP_NAME = os.getenv("APP_NAME", "金融AI助手")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
