# Plan-and-Execute Agent

[English](README.md) | 中文

一个基于 LangGraph 构建的智能 Plan-and-Execute Agent，能够自动制定计划、执行任务并迭代优化，特别擅长处理复杂的研究和报告生成任务。

<div align="center">
  <img src="./static/studio_ui.png" alt="Plan-and-Execute Agent in LangGraph Studio" width="75%" />
</div>

## 🚀 特性

### 🧠 智能规划
- **时间感知规划**：自动获取当前时间信息，确保规划的时效性
- **工具感知**：了解可用工具（如 TavilySearchResults），制定合理的执行计划
- **复杂度适配**：根据任务复杂度自动调整计划的详细程度

### 🔧 强化执行
- **文档状态管理**：智能跟踪和管理正在创建的文档内容
- **上下文感知**：执行器能够理解当前文档状态，进行精确的修改和优化
- **工具集成**：无缝集成搜索工具，获取最新信息

### 🔄 智能重规划
- **循环检测**：自动识别并打破执行循环
- **失败分析**：分析执行失败原因，调整策略避免重复错误
- **完成判断**：智能判断任务完成时机，提供最终结果

### ⏰ 时间上下文
- 所有组件都具备时间感知能力
- 搜索和研究任务考虑信息的时效性
- 时间敏感任务的特殊处理

## 🏗️ 架构

```
Plan-and-Execute Agent
├── Planner: 制定执行计划
├── Executor: 执行具体任务
├── Replanner: 分析结果并重新规划
└── State: 统一状态管理（包括文档跟踪）
```

核心组件：
- **State Management** (`state.py`): 统一状态管理，包括时间信息和文档草稿
- **Planner** (`planner.py`): 智能规划器，理解工具能力和文档工作流
- **Executor** (`executor.py`): 强化执行器，支持文档创建和修改
- **Replanner** (`replanner.py`): 智能重规划器，避免循环并优化执行路径

## 🛠️ 开发环境设置

### 前置要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) 包管理器
- [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)

### 快速开始

1. **克隆项目**
```bash
git clone <repository-url>
cd plan-and-execute
```

2. **安装 uv 包管理器**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. **安装依赖**
```bash
# 创建虚拟环境并安装依赖
uv sync

# 或者安装到现有环境
uv pip install -e .
```

4. **配置环境变量**
```bash
cp .env.example .env
```

编辑 `.env` 文件，添加必要的 API 密钥：
```env
# OpenAI API Key (必需)
OPENAI_API_KEY=sk-...

# Tavily API Key (用于搜索功能)
TAVILY_API_KEY=tvly-...

# LangSmith API Key (可选，用于追踪)
LANGSMITH_API_KEY=lsv2...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=plan-and-execute
```

5. **启动 LangGraph Studio**
```bash
# 确保在项目根目录
langgraph dev
```

或者如果你全局安装了 LangGraph CLI：
```bash
langgraph dev --port 8123
```

6. **打开 LangGraph Studio**
访问 http://localhost:8123 打开 LangGraph Studio 界面

## 📖 使用指南

### 基本使用

在 LangGraph Studio 中，你可以通过以下方式与 Agent 交互：

1. **简单问答**
```
输入："什么是人工智能？"
```

2. **信息搜索**
```
输入："搜索2024年最新的AI发展趋势"
```

3. **报告生成**
```
输入："生成一份关于全球智慧城市发展趋势的详细报告"
```

### 高级功能

**文档创建和迭代优化**：
- Agent 会自动创建文档草稿
- 基于搜索结果持续改进内容
- 智能判断何时完成

**时间感知搜索**：
- 自动使用当前时间评估信息相关性
- 时间敏感任务的特殊处理

## 🔧 自定义配置

### 修改模型
在相应的组件文件中修改模型配置：
```python
# planner.py, replanner.py
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# executor.py  
llm = ChatOpenAI(model="gpt-4-turbo-preview")
```

### 添加新工具
在 `tools.py` 中添加新的工具：
```python
from your_tool import YourTool

tools = [tavily_tool, YourTool()]
```

### 自定义提示词
各组件的提示词可以在对应文件中修改：
- **Planner**: `planner.py` 中的 `planner_prompt_template_text`
- **Executor**: `executor.py` 中的 `executor_system_prompt`
- **Replanner**: `replanner.py` 中的 `replanner_prompt_template_text`

## 🚀 部署

### LangGraph Cloud 部署
```bash
# 构建并部署到 LangGraph Cloud
langgraph build
langgraph deploy
```

### Docker 部署
```bash
# 构建 Docker 镜像
docker build -t plan-and-execute-agent .

# 运行容器
docker run -p 8000:8000 --env-file .env plan-and-execute-agent
```

## 🧪 测试

```bash
# 运行测试
uv run pytest tests/

# 运行集成测试
uv run pytest tests/integration/
```

## 📝 开发说明

### 开发流程
1. 在 LangGraph Studio 中测试和调试
2. 利用热重载功能实时查看代码更改
3. 使用状态编辑功能调试特定节点
4. 利用 LangSmith 集成进行深度追踪

### 关键改进点
- **状态管理**：通过 `current_draft_report` 字段实现文档持续跟踪
- **循环检测**：Replanner 能识别和打破执行循环
- **时间感知**：所有组件都具备时间上下文意识
- **工具感知**：规划器理解可用工具的能力和限制

## 🤝 贡献

欢迎贡献代码！请确保：
1. 代码符合项目风格
2. 添加适当的测试
3. 更新相关文档

## 📄 许可证

[MIT License](LICENSE)

## 🔗 相关资源

- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)
- [LangSmith](https://smith.langchain.com/)
- [uv 包管理器](https://docs.astral.sh/uv/) 