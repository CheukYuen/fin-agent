import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_root_endpoint():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert settings.APP_NAME in data["message"]

def test_health_check():
    """测试健康检查"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_chat_endpoint_structure():
    """测试聊天接口结构（不实际调用AI）"""
    # 测试缺少必填字段
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422  # 验证错误
    
    # 测试字段验证
    response = client.post("/api/v1/chat", json={
        "session_id": "",  # 空字符串应该有效
        "message": ""      # 空消息应该被拒绝
    })
    assert response.status_code == 422

def test_config_values():
    """测试配置值"""
    assert settings.DEFAULT_MODEL == "qwen-plus"
    assert settings.OPENAI_BASE_URL == "https://dashscope.aliyuncs.com/compatible-mode/v1"
    assert settings.APP_NAME == "金融AI助手"

# 如果你想测试实际的AI调用（需要有效的API密钥）
@pytest.mark.skip(reason="需要有效的阿里云API密钥")
def test_actual_chat():
    """测试实际聊天功能（需要有效API密钥）"""
    response = client.post("/api/v1/chat", json={
        "session_id": "test_session",
        "message": "你好，请简单介绍一下你自己。"
    })
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "session_id" in data
    assert data["model"] == settings.DEFAULT_MODEL
