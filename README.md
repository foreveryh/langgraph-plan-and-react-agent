# Plan-and-Execute Agent

English | [中文](README_ZH.md)

An intelligent Plan-and-Execute Agent built with LangGraph that can automatically create plans, execute tasks, and iteratively optimize, particularly excelling at complex research and report generation tasks.

<div align="center">
  <img src="./static/studio_ui.png" alt="Plan-and-Execute Agent in LangGraph Studio" width="75%" />
</div>

## 🚀 Features

### 🧠 Intelligent Planning
- **Time-Aware Planning**: Automatically obtains current time information to ensure plan timeliness
- **Tool-Aware**: Understands available tools (like TavilySearchResults) to create reasonable execution plans
- **Complexity Adaptation**: Automatically adjusts plan detail level based on task complexity

### 🔧 Enhanced Execution
- **Document State Management**: Intelligently tracks and manages content being created
- **Context Awareness**: Executor understands current document state for precise modifications and optimization
- **Tool Integration**: Seamlessly integrates search tools to retrieve the latest information

### 🔄 Smart Replanning
- **Loop Detection**: Automatically identifies and breaks execution loops
- **Failure Analysis**: Analyzes execution failures and adjusts strategies to avoid repeated errors
- **Completion Judgment**: Intelligently determines when tasks are complete and provides final results

### ⏰ Time Context
- All components have time awareness capabilities
- Search and research tasks consider information timeliness
- Special handling for time-sensitive tasks

## 🏗️ Architecture

```
Plan-and-Execute Agent
├── Planner: Creates execution plans
├── Executor: Executes specific tasks
├── Replanner: Analyzes results and replans
└── State: Unified state management (including document tracking)
```

Core Components:
- **State Management** (`state.py`): Unified state management including time information and document drafts
- **Planner** (`planner.py`): Smart planner that understands tool capabilities and document workflows
- **Executor** (`executor.py`): Enhanced executor supporting document creation and modification
- **Replanner** (`replanner.py`): Smart replanner that avoids loops and optimizes execution paths

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)

### Quick Start

1. **Clone the Project**
```bash
git clone <repository-url>
cd plan-and-execute
```

2. **Install uv Package Manager**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. **Install Dependencies**
```bash
# Create virtual environment and install dependencies
uv sync

# Or install to existing environment
uv pip install -e .
```

4. **Configure Environment Variables**
```bash
cp .env.example .env
```

Edit the `.env` file and add necessary API keys:
```env
# OpenAI API Key (required)
OPENAI_API_KEY=sk-...

# Tavily API Key (for search functionality)
TAVILY_API_KEY=tvly-...

# LangSmith API Key (optional, for tracing)
LANGSMITH_API_KEY=lsv2...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=plan-and-execute
```

5. **Start LangGraph Studio**
```bash
# Make sure you're in the project root directory
langgraph dev
```

Or if you have LangGraph CLI installed globally:
```bash
langgraph dev --port 8123
```

6. **Open LangGraph Studio**
Visit http://localhost:8123 to open the LangGraph Studio interface

## 📖 Usage Guide

### Basic Usage

In LangGraph Studio, you can interact with the Agent in the following ways:

1. **Simple Q&A**
```
Input: "What is artificial intelligence?"
```

2. **Information Search**
```
Input: "Search for the latest AI development trends in 2024"
```

3. **Report Generation**
```
Input: "Generate a detailed report on global smart city development trends"
```

### Advanced Features

**Document Creation and Iterative Optimization**:
- Agent automatically creates document drafts
- Continuously improves content based on search results
- Intelligently determines when to complete

**Time-Aware Search**:
- Automatically uses current time to evaluate information relevance
- Special handling for time-sensitive tasks

## 🔧 Custom Configuration

### Modify Models
Modify model configurations in the respective component files:
```python
# planner.py, replanner.py
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# executor.py  
llm = ChatOpenAI(model="gpt-4-turbo-preview")
```

### Add New Tools
Add new tools in `tools.py`:
```python
from your_tool import YourTool

tools = [tavily_tool, YourTool()]
```

### Customize Prompts
Component prompts can be modified in their respective files:
- **Planner**: `planner_prompt_template_text` in `planner.py`
- **Executor**: `executor_system_prompt` in `executor.py`
- **Replanner**: `replanner_prompt_template_text` in `replanner.py`

## 🚀 Deployment

### LangGraph Cloud Deployment
```bash
# Build and deploy to LangGraph Cloud
langgraph build
langgraph deploy
```

### Docker Deployment
```bash
# Build Docker image
docker build -t plan-and-execute-agent .

# Run container
docker run -p 8000:8000 --env-file .env plan-and-execute-agent
```

## 🧪 Testing

```bash
# Run tests
uv run pytest tests/

# Run integration tests
uv run pytest tests/integration/
```

## 📝 Development Notes

### Development Workflow
1. Test and debug in LangGraph Studio
2. Use hot reload functionality to see code changes in real-time
3. Use state editing functionality to debug specific nodes
4. Leverage LangSmith integration for deep tracing

### Key Improvements
- **State Management**: Continuous document tracking through `current_draft_report` field
- **Loop Detection**: Replanner can identify and break execution loops
- **Time Awareness**: All components have time context awareness
- **Tool Awareness**: Planner understands available tool capabilities and limitations

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. Code follows project style
2. Add appropriate tests
3. Update relevant documentation

## 📄 License

[MIT License](LICENSE)

## 🔗 Related Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)
- [LangSmith](https://smith.langchain.com/)
- [uv Package Manager](https://docs.astral.sh/uv/)
