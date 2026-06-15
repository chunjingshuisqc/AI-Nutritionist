# AI 智能营养师系统

基于 FastAPI、Vue 3、MySQL、ChromaDB 和大模型接口实现的智能营养管理系统。系统能够结合用户基本信息、体检报告和饮食偏好，完成健康分析、营养问答与个性化周食谱生成。

## 项目简介

本项目采用前后端分离架构，后端使用 FastAPI 提供 RESTful API，前端使用 Vue 3 和 Element Plus 构建交互页面。

系统通过 MySQL 存储用户、体检报告、饮食偏好和食谱等结构化数据，通过 ChromaDB 存储营养知识向量，并自主实现 RAG 检索增强生成流程。

用户提出问题或生成食谱时，系统会先检索相关营养知识，再结合用户健康数据与饮食偏好调用大模型生成结果。

## 主要功能

* 用户基本信息管理
* 体检报告录入与查询
* 口味偏好和饮食禁忌管理
* BMI 自动计算
* 营养知识向量化存储
* 基于 ChromaDB 的语义检索
* AI 营养健康咨询
* 用户健康指标分析
* 个性化七天食谱生成
* 食谱和购物清单保存
* 模拟模式下的本地功能联调

## 技术栈

### 后端

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* PyMySQL
* Pydantic
* pydantic-settings
* ChromaDB
* httpx
* uv

### 前端

* Vue 3
* TypeScript
* Vite
* Vue Router
* Pinia
* Axios
* Element Plus
* ECharts
* marked
* DOMPurify

### 数据存储

* MySQL：存储用户、体检报告、口味偏好和食谱
* ChromaDB：存储营养知识文本及其向量

## 项目结构

```text
AI_Nutrition/
├── backend/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── llm_client.py
│   │   ├── vector_store.py
│   │   └── rag_engine.py
│   ├── routers/
│   │   ├── users.py
│   │   ├── health.py
│   │   ├── preferences.py
│   │   ├── meal_plan.py
│   │   └── agent.py
│   ├── knowledge_base/
│   │   └── init_data.py
│   ├── scripts/
│   │   └── seed_data.py
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## 系统流程

```text
用户请求
   ↓
FastAPI 接收请求
   ↓
读取 MySQL 中的用户与健康数据
   ↓
将用户问题转换为向量
   ↓
从 ChromaDB 检索相关营养知识
   ↓
构建包含用户信息和检索结果的提示词
   ↓
调用大模型生成健康建议或食谱
   ↓
保存结果并返回前端
```

## 环境要求

建议使用：

```text
Python 3.11 或 3.12
Node.js 20+
MySQL 8.0+
```

## 环境变量配置

复制环境变量模板：

Windows CMD：

```bash
copy .env.example .env
```

PowerShell：

```powershell
Copy-Item .env.example .env
```

Linux 或 macOS：

```bash
cp .env.example .env
```

修改 `.env`：

```env
APP_NAME=AI营养师Agent
APP_VERSION=1.0.0
DEBUG=true

# true 表示使用模拟大模型和模拟向量
MOCK_MODE=true

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ai_nutritionist?charset=utf8mb4

LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=your-model-name

EMBEDDING_API_KEY=your-api-key
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=your-embedding-model-name

CHROMA_PERSIST_DIR=./data/chroma
CHROMA_COLLECTION_NAME=nutrition_knowledge
```

请勿将真实 `.env`、API Key 或数据库密码提交到 GitHub。

## 数据库初始化

先在 MySQL 中创建数据库：

```sql
CREATE DATABASE IF NOT EXISTS ai_nutritionist
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;
```

项目启动时会根据 SQLAlchemy 模型自动检查并创建数据表。

也可以执行模拟数据脚本：

```bash
uv run python -m backend.scripts.seed_data
```

模拟数据包括：

* 示例用户
* 示例体检报告
* 示例口味偏好

## 启动后端

```bash
uv run uvicorn backend.main:app --reload
```

后端地址：

```text
http://127.0.0.1:8000
```

Swagger 接口文档：

```text
http://127.0.0.1:8000/docs
```

ReDoc 文档：

```text
http://127.0.0.1:8000/redoc
```

## 前端安装

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

启动开发服务器：

```bash
npm run dev
```

前端地址：

```text
http://localhost:5173
```


## 主要接口

### 用户管理

```text
POST /api/users/
GET  /api/users/{user_id}
```

### 体检报告

```text
POST /api/health/{user_id}
GET  /api/health/{user_id}/reports
```

### 口味偏好

```text
POST /api/preferences/{user_id}
GET  /api/preferences/{user_id}
```

### 智能食谱

```text
POST /api/meal-plans/generate/{user_id}
GET  /api/meal-plans/{user_id}
GET  /api/meal-plans/detail/{plan_id}
```

### AI 营养咨询

```text
POST /api/agent/chat/{user_id}
POST /api/agent/analyze/{user_id}
```

## RAG 实现说明

主要模块包括：

```text
llm_client.py
负责调用大模型和 Embedding 接口

vector_store.py
负责 ChromaDB 向量存储和语义检索

rag_engine.py
负责健康指标分析、知识检索、上下文构建和模型调用
```

完整流程：

```text
用户问题
→ Embedding 向量化
→ ChromaDB 语义检索
→ 拼接营养知识和用户数据
→ 调用大模型
→ 返回回答
```

## 安全说明

项目通过 `.env` 管理以下敏感配置：

* MySQL 用户名和密码
* 大模型 API Key
* Embedding API Key
* 模型接口地址

`.gitignore` 中应包含：

```gitignore
.env
.venv/
frontend/node_modules/
frontend/dist/
data/
*.sqlite3
__pycache__/
```


## 项目说明

本项目主要用于学习和展示 FastAPI、Vue 3、MySQL、ChromaDB 和 RAG 应用开发流程。

系统提供的健康分析与饮食建议仅用于技术演示和饮食辅助参考，不能替代医生诊断或专业医疗意见。

## License

本项目仅供学习与交流使用。

<img width="1840" height="795" alt="315e2c74ad1d9d97b155a2baf1cd4bcf" src="https://github.com/user-attachments/assets/94e0d543-ba26-41c5-9efc-235eb8d8a778" />
<img width="1813" height="853" alt="0ba5d1f147caecf2c14dc44a4329b79f" src="https://github.com/user-attachments/assets/59f694ad-3fce-48d5-8cae-cd6a7776b5d1" />

