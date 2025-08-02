<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">MiniRAG</h1>
<p align="center">
	<a href=""><img src="https://img.shields.io/badge/MiniRAG-brightgreen.svg"></a>
    <img src="https://img.shields.io/badge/LangChain-blue">
    <img src="https://img.shields.io/badge/LangGraph-blue">
    <img src="https://img.shields.io/badge/PGVector-blue">
</p>
一个基于知识库问答的最迷你RAG系统，使用 PGVector 向量存储和检索文档，结合 SiliconFlow API 进行嵌入和重排序。

## 功能
麻雀虽小，五脏俱全。
- 文档读取与分块
- 文档嵌入与向量存储
- 向量检索与重排
- 检索优化
- 工作流编排

## 依赖项

- Python 3.11+
- 主要库：
  - `langchain`
  - `langgraph`

## 配置

1. 复制 `.env.example` 为 `.env` 并填写以下内容：
   ```
   SILICONFLOW_API_KEY=your_api_key
   PG_USER=your_db_user
   PG_PASSWORD=your_db_password
   PG_HOST=your_db_host
   PG_PORT=your_db_port
   ```
2. 确保 PostgreSQL 数据库已启动并配置正确。

## 使用方法

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行示例脚本：
   ```bash
   python demo_embedding.py  # 文档嵌入示例
   python demo_minirag.py    # 问答系统示例
   ```

## 项目结构

```
├── .env                    # 环境变量配置
├── README.md               # 项目说明
├── demo_embedding.py       # 文档嵌入示例
├── demo_minirag.py         # 问答系统示例
├── src/
│   ├── config.py           # 配置加载
│   ├── embedding.py        # 嵌入逻辑
│   ├── prompts.py          # 提示词模板
│   ├── reranker.py         # 重排序逻辑
│   └── workflow.py         # 工作流定义
```

## PGVector 部署
- 推荐使用docker部署
```
docker volume create pgvector
docker run -d \
  --name pgvector \
  -e POSTGRES_USER=username \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=database \
  -p 5432:5432 \
  -v pgvector:/var/lib/postgresql/data \
  ankane/pgvector
```