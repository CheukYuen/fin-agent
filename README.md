# AI Agent FastAPI Template

> **学习后端 & Cursor AI Code 专用 README**

---

## 一、项目目标

* **快速上手**：提供一个最小可行（MVP）的 AI Agent 示例，核心栈包括 **FastAPI + OpenAI SDK + Redis**。
* **会话管理**：使用 Redis 持久化对话上下文，支持多会话并发。
* **模型无关**：默认集成 GPT‑3.5‑Turbo，可轻松切换至 GPT‑4o、Anthropic Claude 等未来模型。
* **易于扩展**：代码结构清晰，预留 Tool 调用、SSE 流式响应、监控与日志等模块。
* **容器化友好**：自带 Dockerfile 与 docker‑compose，一键部署本地或私有云 / K8s。

---

## 二、项目结构（开发 → 容器化友好）

```text
ai_agent_fastapi/
├── app/
│   ├── main.py                # FastAPI 入口
│   ├── api_router.py          # 路由封装
│   ├── services/
│   │   ├── llm_service.py     # OpenAI 调用逻辑
│   │   └── redis_service.py   # Redis 封装
│   ├── models/
│   │   └── schema.py          # Pydantic 请求 / 响应模型
│   └── config.py              # 环境变量与设置
├── tests/                     # pytest 用例（可选）
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量模板
├── Dockerfile                 # 应用镜像
├── docker-compose.yml         # 一键启动 App + Redis
└── README.md                  # 当前文档
```

> **Tips**
>
> * `tests/` 中示例用 pytest + httpx 覆盖核心业务逻辑。
> * 生产环境可接入 Prometheus & Grafana 做监控、Sentry 做异常跟踪。

---

## 三、开发阶段（本地直接运行）

1. **安装依赖**

   ```bash
   python -m venv venv && source venv/bin/activate  # 可选
   pip install --upgrade pip -r requirements.txt
   ```

2. **配置环境** （复制模板并填写 Key）

   ```bash
   cp .env.example .env
   # 填写 OPENAI_API_KEY=sk-*** 及 REDIS_URL=redis://localhost:6379/0
   ```

3. **启动 Redis**

   ```bash
   # macOS (brew) 示例
   brew services start redis
   # 或使用 docker
   docker run -p 6379:6379 -d redis:6
   ```

4. **启动 API Server**

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **测试接口**

   * 浏览器打开 `http://localhost:8000/docs` （自动生成的 Swagger UI）。
   * 通过 `POST /chat` 发送 JSON：

     ```json
     {
       "session_id": "demo",
       "message": "Hello, AI!"
     }
     ```

---

## 四、学习路径建议

| 阶段    | 关键目标                           | 建议实践                                             |
| ----- | ------------------------------ | ------------------------------------------------ |
| 📍 入门 | 跑通本地 FastAPI + Redis + OpenAI  | 完成一次对话请求 & 回答                                    |
| 🧠 状态 | 深入理解 Redis 数据结构、TTL 策略         | 用 `lrange` 查看历史，实验过期策略                           |
| 🐳 容器 | 理解 Dockerfile、Compose 原理       | 构建镜像 → `docker-compose up` 一键启动                  |
| 🚀 流式 | 加入 SSE（Server‑Sent Events）流式返回 | 将 `uvicorn` + `StreamingResponse` 接入前端           |
| 🔍 监控 | 接入日志（loguru）、Prometheus 指标     | 监控 QPS、响应时间、错误率                                  |
| 🧪 测试 | 编写 pytest + GitHub Actions CI  | 确保核心接口自动化回归                                      |
| 📈 扩展 | 多模型路由、工具插件化                    | 研究 OpenAI function calling / Anthropic tool\_use |

> **持续迭代**：每完成一阶段，回顾代码质量、性能瓶颈，再进入下一阶段。

---

### 参考

* [FastAPI 官方文档](https://fastapi.tiangolo.com/)
* [OpenAI Python SDK](https://github.com/openai/openai-python)
* [Redis 官方命令](https://redis.io/commands/)
* [Docker & Compose](https://docs.docker.com/)
* [Loguru](https://github.com/Delgan/loguru) – 简单优雅的日志框架

> **Happy Coding!**
