from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api_router import router
from app.config import settings
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="基于Qwen模型的金融AI助手API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """根路径欢迎信息"""
    return {
        "message": f"欢迎使用 {settings.APP_NAME}",
        "version": "1.0.0",
        "model": settings.DEFAULT_MODEL,
        "docs": "/docs"
    }
