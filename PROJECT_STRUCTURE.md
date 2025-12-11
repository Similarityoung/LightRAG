# LightRAG 项目结构说明

本文档详细说明了 LightRAG 项目的文件和目录结构及其功能。

## 根目录文件

| 文件/目录 | 说明 |
| --- | --- |
| `LightRAG/` | 项目根目录 |
| `README.md` / `README-zh.md` | 项目说明文档（英文/中文），包含介绍、安装和使用指南。 |
| `.env` | **配置文件**。包含 API 密钥、数据库连接信息、模型配置等环境变量。 |
| `env.example` | `.env` 文件的示例模板。 |
| `config.ini.example` | 另一种配置格式的示例文件。 |
| `setup.py` / `pyproject.toml` | **Python 包安装配置**。定义了项目依赖、版本和元数据，用于 `pip install`。 |
| `requirements*.txt` | 依赖列表文件。`requirements-offline.txt` 等用于离线环境安装。 |
| `Dockerfile` / `Dockerfile.lite` | **Docker 构建文件**。用于构建 LightRAG 服务的容器镜像。 |
| `docker-compose.yml` | Docker Compose 编排文件，用于一键启动 LightRAG 服务及其依赖（如 Redis, Neo4j 等）。 |
| `docker-build-push.sh` | 用于构建并推送 Docker 镜像的脚本。 |
| `lightrag.service.example` | Systemd 服务配置示例，用于在 Linux 上作为后台服务运行。 |
| `MANIFEST.in` | 打包清单文件，指定打包时包含的非代码文件。 |
| `LICENSE` | 开源许可证文件。 |
| `SECURITY.md` | 安全策略说明。 |
| `AGENTS.md` | 关于 Agent 及其功能的说明文档。 |

## 核心代码库 (`lightrag/`)

这是 LightRAG 的核心 Python 包，包含了所有的业务逻辑。

| 文件/目录 | 说明 |
| --- | --- |
| `lightrag.py` | **核心入口**。定义了 `LightRAG` 类，整合了向量检索、图检索和 LLM 生成的主逻辑。 |
| `base.py` | **基类定义**。定义了存储（Storage）、管道（Pipeline）等的抽象基类和接口。 |
| `operate.py` | **核心操作逻辑**。包含文档切分（Chunking）、实体提取、关系提取、查询（Query）的具体实现算法。 |
| `prompt.py` | **提示词模板**。存储了用于实体提取、摘要生成、问答等任务的 Prompt 模板。 |
| `utils.py` | 通用工具函数库（如日志、文件处理、哈希计算等）。 |
| `utils_graph.py` | 图处理相关的工具函数。 |
| `constants.py` | 项目使用的常量定义。 |
| `types.py` | 类型定义文件。 |
| `exceptions.py` | 自定义异常类。 |
| `rerank.py` | 重排序（Rerank）逻辑实现，用于优化检索结果。 |
| `namespace.py` | 命名空间管理，用于隔离不同用户或项目的数据。 |
| **`api/`** | **API 服务层**。基于 FastAPI 实现的 HTTP 接口，负责处理 Web 请求并调用核心逻辑。 |
| **`kg/`** | **知识图谱与存储层**。包含各种数据库的适配器实现（如 Neo4j, Milvus, Redis, PostgreSQL 等）。 |
| **`llm/`** | **大模型接口层**。封装了不同 LLM 提供商（OpenAI, Ollama, Azure 等）的调用逻辑。 |
| **`evaluation/`** | **评估模块**。用于评估 RAG 系统的性能和质量。 |
| **`tools/`** | 辅助工具模块。 |

## 前端应用 (`lightrag_webui/`)

这是一个基于 Web 的用户界面，用于可视化操作 LightRAG。

| 文件/目录 | 说明 |
| --- | --- |
| `src/` | 前端源代码（React/Vue 等框架）。 |
| `public/` | 静态资源文件。 |
| `package.json` | 前端项目的依赖和脚本配置。 |
| `vite.config.ts` | Vite 构建工具配置。 |
| `tsconfig.json` | TypeScript 配置文件。 |

## 示例与演示 (`examples/`)

包含各种使用场景的 Python 脚本示例。

| 文件/目录 | 说明 |
| --- | --- |
| `lightrag_openai_demo.py` | 使用 OpenAI 模型的标准演示。 |
| `lightrag_ollama_demo.py` | 使用 Ollama 本地模型的演示。 |
| `insert_custom_kg.py` | 插入自定义知识图谱数据的示例。 |
| `graph_visual_*.py` | 图数据可视化的示例脚本。 |
| `generate_query.py` | 生成查询测试数据的脚本。 |
| `rerank_example.py` | 使用重排序功能的示例。 |

## 部署与运维 (`k8s-deploy/`)

| 文件/目录 | 说明 |
| --- | --- |
| `install_lightrag.sh` | Kubernetes 部署脚本。 |
| `uninstall_lightrag.sh` | Kubernetes 卸载脚本。 |
| `databases/` | 数据库相关的 K8s 配置文件。 |

## 其他目录

| 目录 | 说明 |
| --- | --- |
| `docs/` | 详细的项目文档（算法说明、部署指南等）。 |
| `tests/` | 单元测试和集成测试代码，用于保证代码质量。 |
| `reproduce/` | 复现脚本。通常用于复现论文或基准测试中的结果。 |
| `assets/` | 项目使用的静态资源（图片等）。 |
