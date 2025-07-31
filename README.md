# 🚀 **IntelliVest AI - Your Investment Thesis Partner**

> **Advanced Agentic AI System for Investment Analysis**

## 📋 **Overview**

IntelliVest AI is a sophisticated agentic AI system that provides comprehensive investment analysis using advanced AI models and real-time data. The system combines CrewAI orchestration, advanced fallback systems, and custom tools to deliver professional-grade investment insights.

## 🎯 **Key Features**

- **🤖 Agentic AI Framework**: CrewAI with 5 specialized agents
- **🧠 Advanced Fallback System**: Multi-LLM orchestration with intelligent routing
- **🎯 Primary Model**: Gemini 2.5 Flash with robust fallbacks
- **🛠️ Custom Tools**: 6 investment tools with real data access
- **📊 Real-time Monitoring**: Comprehensive metrics and analytics
- **🔄 LangGraph Workflows**: Advanced workflow orchestration

## 🏗️ **System Architecture**

```
IntelliVest AI
├── 🚀 Production Interface (production_integration.py)
├── 🤖 Agents (agents/)
│   └── crew_agents_with_tools.py
├── 🧠 LLM Management (llm/)
│   └── advanced_fallback_system.py
├── 🛠️ Custom Tools (tools/)
│   └── investment_tools.py
├── 🔄 Workflows (workflows/)
│   └── investment_workflow.py
├── 🌐 Web Interface (frontend/)
├── 🔌 API Backend (api/)
└── 🛠️ Utilities (utils/)
```

## 📁 **Project Structure**

### **Core Files**
```
IntelliVest-AI/
├── 🚀 production_integration.py      # Main system interface
├── 🧪 test_production_integration.py # Comprehensive test suite
├── 📋 requirements.txt               # Python dependencies
├── 📖 README.md                      # This documentation
├── 📁 PROJECT_STRUCTURE.md           # Detailed structure guide
├── 📊 PRODUCTION_INTEGRATION_SUMMARY.md # System summary
├── 🔧 .env                           # API configuration
├── 📄 .gitignore                     # Git ignore rules
├── 📄 LICENSE                        # MIT License
└── 🌐 run_app.py                     # Web application launcher
```

### **Module Organization**
```
├── 🤖 agents/                        # CrewAI agents
│   ├── __init__.py                   # Package initialization
│   └── crew_agents_with_tools.py     # Main agent definitions
├── 🧠 llm/                          # LLM management
│   ├── __init__.py                   # Package initialization
│   └── advanced_fallback_system.py   # Multi-LLM orchestration
├── 🛠️ tools/                        # Custom tools
│   ├── __init__.py                   # Package initialization
│   └── investment_tools.py           # Investment analysis tools
├── 🔄 workflows/                     # LangGraph workflows
│   ├── __init__.py                   # Package initialization
│   └── investment_workflow.py        # Advanced workflows
├── 🌐 frontend/                      # Streamlit web interface
├── 🔌 api/                          # FastAPI backend
├── 🛠️ utils/                        # Utility functions
├── 📊 output/                       # Analysis outputs
└── 🚀 app/                          # Legacy app files
```

## 🔄 **Workflow Architecture**

### **1. Agentic Flow**
```
User Request → Production Interface → Analysis Router → Agent Selection → Tool Execution → Result Synthesis → Response
```

### **2. CrewAI Agent Orchestration**
```
Research Agent → Sentiment Agent → Valuation Agent → Thesis Agent → Critique Agent
```

### **3. Advanced Fallback System**
```
Primary Model (Gemini 2.5 Flash) → Fallback 1 (DeepSeek R1) → Fallback 2 (Llama 3.3-70B) → Additional Models
```

### **4. LangGraph Workflow**
```
State Initialization → Research Node → Sentiment Node → Valuation Node → Decision Router → Thesis Node → Critique Node → Final State
```

## 🤖 **Agentic Flow Details**

### **Agent Types & Responsibilities**

#### **🔍 Research Agent**
- **Purpose**: Comprehensive company research and data gathering
- **Tools**: Web crawler, financial data tools
- **Output**: Business model analysis, market position, competitive landscape

#### **🧠 Sentiment Agent**
- **Purpose**: Market sentiment analysis and emotional intelligence
- **Tools**: Sentiment analysis tool, news crawler
- **Output**: Market mood, investor psychology, sentiment trends

#### **💰 Valuation Agent**
- **Purpose**: Financial valuation and metrics analysis
- **Tools**: Financial data tool, valuation tool
- **Output**: Financial ratios, DCF analysis, peer comparison

#### **📝 Thesis Agent**
- **Purpose**: Investment thesis generation and recommendation
- **Tools**: Thesis generation tool, all previous outputs
- **Output**: Structured investment thesis with buy/hold/sell recommendation

#### **🔍 Critique Agent**
- **Purpose**: Quality assurance and bias detection
- **Tools**: Critique tool, thesis review
- **Output**: Bias analysis, improvement suggestions, quality assessment

### **Agent Communication Flow**
```
Research Agent → [Company Data] → Sentiment Agent → [Market Sentiment] → 
Valuation Agent → [Financial Analysis] → Thesis Agent → [Investment Thesis] → 
Critique Agent → [Quality Review] → Final Output
```

## 🛠️ **Advanced Tools & Libraries**

### **🤖 Agentic Frameworks**

#### **CrewAI (v0.150.0)**
- **Purpose**: Multi-agent orchestration and task management
- **Features**: 
  - Agent role definition and backstory
  - Task delegation and coordination
  - Tool integration and execution
  - Sequential and parallel processing
- **Usage**: Primary agent orchestration framework

#### **LangChain (v0.3.27)**
- **Purpose**: LLM framework and tool integration
- **Features**:
  - BaseTool implementation for custom tools
  - LLM abstraction and provider management
  - Chain and prompt management
  - Memory and context handling
- **Usage**: Tool development and LLM integration

#### **LangGraph (v0.6.1)**
- **Purpose**: Advanced workflow orchestration
- **Features**:
  - StateGraph for complex workflows
  - Conditional routing and decision logic
  - State management with TypedDict
  - Checkpointing and state persistence
- **Usage**: Complex workflow orchestration

### **🧠 LLM Providers & Models**

#### **Google Gemini Models**
- **Primary**: `gemini-2.5-flash` (8,192 tokens, cost-effective)
- **Fallback**: `gemini-2.0-flash` (8,192 tokens, reliable)
- **Features**: High performance, cost optimization, real-time analysis

#### **Groq Models**
- **Primary Fallback**: `groq/deepseek-r1-distill-llama-70b` (8,192 tokens)
- **Secondary Fallback**: `groq/llama-3.3-70b-versatile` (8,192 tokens)
- **Additional**: `groq/llama3.1-70b-8192`, `groq/mixtral-8x7b-32768`
- **Features**: Ultra-fast inference, high reliability, cost-effective

### **🛠️ Custom Tools**

#### **WebCrawlerTool**
- **Library**: `Crawl4AI (v0.7.2)`
- **Purpose**: Real-time web data extraction
- **Features**: Async crawling, markdown conversion, error handling
- **Usage**: Financial news and company data gathering

#### **FinancialDataTool**
- **Library**: `yfinance (v0.2.65)`
- **Purpose**: Market data and financial metrics
- **Features**: Real-time stock data, financial ratios, company information
- **Usage**: Financial analysis and valuation

#### **SentimentAnalysisTool**
- **Library**: `TextBlob`
- **Purpose**: Market sentiment quantification
- **Features**: Polarity scoring, key phrase extraction, sentiment categorization
- **Usage**: Market mood analysis

#### **ValuationTool**
- **Purpose**: Financial valuation analysis
- **Features**: P/E, P/B, P/S ratios, valuation assessment
- **Usage**: Company valuation and financial analysis

#### **ThesisGenerationTool**
- **Purpose**: Investment thesis creation
- **Features**: Structured thesis generation, recommendation framework
- **Usage**: Professional investment recommendations

#### **CritiqueTool**
- **Purpose**: Quality assurance and bias detection
- **Features**: Bias analysis, improvement suggestions, quality assessment
- **Usage**: Thesis review and improvement

### **🌐 Web & API Frameworks**

#### **Streamlit (v1.44.0)**
- **Purpose**: Web interface for user interaction
- **Features**: Real-time updates, interactive components, data visualization
- **Usage**: User-friendly investment analysis interface

#### **FastAPI (v0.115.6)**
- **Purpose**: REST API backend
- **Features**: Auto-generated documentation, async support, type validation
- **Usage**: Programmatic access to analysis capabilities

#### **Uvicorn**
- **Purpose**: ASGI server for FastAPI
- **Features**: High-performance async server, WebSocket support
- **Usage**: API server deployment

### **📊 Data & Analysis Libraries**

#### **yfinance (v0.2.65)**
- **Purpose**: Yahoo Finance data access
- **Features**: Real-time stock data, financial statements, market data
- **Usage**: Financial data retrieval and analysis

#### **Crawl4AI (v0.7.2)**
- **Purpose**: Advanced web crawling
- **Features**: Async crawling, markdown extraction, content processing
- **Usage**: Financial news and company data extraction

#### **Tavily (v0.3.8)**
- **Purpose**: Web search and content discovery
- **Features**: Financial news search, content aggregation
- **Usage**: News and information gathering

### **🔄 Advanced Fallback System**

#### **Multi-LLM Orchestration**
- **7 AI Models**: Intelligent routing based on task type
- **Fallback Chains**: Automatic failover with confidence scoring
- **Performance Monitoring**: Real-time health checks and metrics
- **Cost Optimization**: Intelligent model selection based on cost and performance

#### **Task-Based Routing**
- **Research Tasks**: Gemini 2.5 Flash → DeepSeek R1 → Llama 3.3-70B
- **Sentiment Tasks**: Gemini 2.5 Flash → DeepSeek R1 → Llama 3.3-70B
- **Valuation Tasks**: Gemini 2.5 Flash → DeepSeek R1 → Llama 3.3-70B
- **Thesis Tasks**: Gemini 2.5 Flash → DeepSeek R1 → Llama 3.3-70B
- **Critique Tasks**: Gemini 2.5 Flash → DeepSeek R1 → Llama 3.3-70B

## 🔄 **Framework Integration & Interactions**

### **How CrewAI, LangChain & LangGraph Work Together**

The IntelliVest AI system leverages all three frameworks in a sophisticated integration that maximizes their individual strengths:

#### **Integration Flow:**
```
1. User Request → Production Interface
   ↓
2. CrewAI → Creates 5 agents with LangChain tools
   ↓
3. LangChain → Provides tools and LLM interfaces
   ↓
4. LangGraph → Manages complex workflow state
   ↓
5. Advanced Fallback System → Routes to appropriate LLMs
   ↓
6. Final Result → Structured investment analysis
```

#### **Framework Responsibilities:**

**🚀 CrewAI (v0.150.0) - Agent Orchestration:**
- **Agent Management**: Creates and manages 5 specialized agents (Research, Sentiment, Valuation, Thesis, Critique)
- **Task Coordination**: Ensures proper task sequencing and agent communication
- **Result Aggregation**: Combines outputs from all agents into cohesive analysis
- **Role Definition**: Defines agent backstories, goals, and expertise areas

**🛠️ LangChain (v0.3.27) - Tool & LLM Framework:**
- **Tool Development**: Provides `BaseTool` class for creating custom investment tools
- **LLM Integration**: Unified interface for different AI models (Gemini, Groq)
- **Chain Building**: Connects tools and models together in functional chains
- **Memory Management**: Handles context and conversation memory

**🔄 LangGraph (v0.6.1) - Advanced Workflow Orchestration:**
- **State Management**: Tracks workflow state throughout analysis using `TypedDict`
- **Decision Making**: Routes analysis based on conditions and intermediate results
- **Complex Orchestration**: Handles multi-step, conditional workflows
- **Checkpointing**: Saves and restores workflow state for reliability

#### **Specific Framework Interactions:**

**CrewAI + LangChain Integration:**
```python
# CrewAI agents use LangChain tools and LLMs
research_agent = Agent(
    role="Research Analyst",
    tools=[WebCrawlerTool(), FinancialDataTool()],  # LangChain tools
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")  # LangChain LLM
)
```

**LangChain + LangGraph Integration:**
```python
# LangGraph nodes use LangChain tools
def research_node(state: InvestmentState) -> InvestmentState:
    crawler_tool = WebCrawlerTool()  # LangChain tool
    result = crawler_tool.run(state["company_name"])
    state["research_data"] = result
    return state
```

**All Three Frameworks Together:**
```python
# Production system orchestrates all three frameworks
class ProductionIntelliVestAI:
    def __init__(self):
        # CrewAI for agent orchestration
        self.crew_system = SimpleInvestmentAnalysisCrew()
        
        # LangChain tools for functionality
        self.tools = [WebCrawlerTool(), FinancialDataTool(), ...]
        
        # LangGraph for complex workflows
        self.workflow = create_workflow()
```

#### **Why Use All Three Frameworks?**

**CrewAI**: Perfect for **agent-based analysis** where different experts (agents) need to work together sequentially
**LangChain**: Essential for **tool development** and **LLM integration** across multiple providers
**LangGraph**: Ideal for **complex workflows** with **state management** and **conditional logic**

**Together, they create a powerful, flexible system that can handle complex investment analysis workflows with multiple specialized agents, custom tools, and intelligent routing!**

#### **Framework Usage Patterns:**

**For Simple Analysis:**
- **CrewAI** handles the agent orchestration
- **LangChain** provides tools and LLM interfaces

**For Complex Workflows:**
- **LangGraph** manages state and conditional routing
- **CrewAI** provides agent coordination
- **LangChain** supplies tools and model interfaces

**For Production Deployment:**
- **All three** work together for maximum flexibility and reliability
- **Advanced Fallback System** ensures continuous operation
- **Real-time monitoring** tracks performance across all frameworks

## 🎯 **Model Configuration**

### **Primary Model**
- **🎯 Gemini 2.5 Flash**: High-performance, cost-effective analysis

### **Fallback Chain**
1. **🔄 Primary Fallback**: Groq DeepSeek R1 Distill Llama-70B
2. **🔄 Secondary Fallback**: Groq Llama 3.3-70B Versatile
3. **🔄 Tertiary+**: Additional models for maximum reliability

## 🚀 **Quick Start**

### **1. Environment Setup**
```bash
# Clone the repository
git clone https://github.com/Rohit-Ray-Git/IntelliVest-AI-Your-Investment-Thesis-Partner.git
cd IntelliVest-AI-Your-Investment-Thesis-Partner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. API Configuration**
Create a `.env` file with your API keys:
```env
# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key

# Groq API (for fallbacks)
OPENAI_API_KEY=your_groq_api_key
OPENAI_API_BASE=https://api.groq.com/openai/v1

# Alpha Vantage (financial data)
ALPHAVANTAGE_API_KEY=your_alphavantage_key

# Tavily API (web search)
TAVILY_API_KEY=your_tavily_key
```

### **3. Basic Usage**
```python
from production_integration import ProductionIntelliVestAI, AnalysisRequest

# Initialize the system
intellivest_ai = ProductionIntelliVestAI()

# Create analysis request
request = AnalysisRequest(
    company_name="Apple Inc.",
    analysis_type="research",  # Options: research, sentiment, valuation, thesis, full
    include_tools=True,
    use_advanced_fallback=True
)

# Run analysis
result = await intellivest_ai.analyze_company(request)

# View results
print(f"Status: {result.status}")
print(f"Execution Time: {result.execution_time:.2f}s")
print(f"Confidence Score: {result.confidence_score:.2f}")
print(f"Content: {result.content}")
```

## 📊 **Analysis Types**

### **🔍 Research Analysis**
Comprehensive company research including business model, financial metrics, market position, and risk assessment.

### **🧠 Sentiment Analysis**
Market sentiment analysis covering news sentiment, social media trends, analyst ratings, and investor psychology.

### **💰 Valuation Analysis**
Financial valuation using multiple methodologies: DCF, comparable analysis, and relative valuation.

### **📝 Thesis Generation**
Professional investment thesis with clear recommendations, value drivers, and risk assessment.

### **🎯 Full Analysis**
Complete end-to-end analysis using CrewAI with 5 specialized agents working sequentially.

## 📈 **Monitoring & Analytics**

### **Real-time Metrics**
- Total analyses performed
- Success/failure rates
- Average execution times
- Model usage statistics
- Fallback frequency

### **System Status**
```python
# Get system status
status = intellivest_ai.get_system_status()
print(f"System Status: {status['system_status']}")
print(f"Available Models: {status['metrics']['model_usage']}")
```

### **Analysis History**
```python
# Get recent analysis history
history = intellivest_ai.get_analysis_history(limit=10)
for analysis in history:
    print(f"{analysis['company_name']} - {analysis['analysis_type']} - {analysis['status']}")
```

## 🧪 **Testing**

Run the comprehensive test suite:
```bash
python test_production_integration.py
```

This will test:
- ✅ System initialization
- ✅ All analysis types
- ✅ Advanced fallback system
- ✅ Custom tools integration
- ✅ Real-time monitoring
- ✅ Analysis history

## 🌐 **Web Interface**

Start the web application:
```bash
python run_app.py
```

Access the interface at: `http://localhost:8501`

## 🔌 **API Endpoints**

The system provides REST API endpoints for integration:

- `POST /analyze`: Run investment analysis
- `GET /status`: Get system status
- `GET /history`: Get analysis history
- `GET /metrics`: Get performance metrics

## 🎯 **Performance Metrics**

### **Recent Test Results**
- **✅ All Tests Passed**: 10/10 production tests successful
- **⚡ Execution Time**: 26-44 seconds for comprehensive analyses
- **🎯 Confidence Score**: 0.82 average across all analysis types
- **🔄 Success Rate**: 100% in production tests
- **📊 Model Usage**: Gemini 2.5 Flash working perfectly as primary

## 🚀 **Deployment**

### **Local Development**
```bash
# Run with virtual environment
source venv/bin/activate
python run_app.py
```

### **System Deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY=your_key
export OPENAI_API_KEY=your_groq_key

# Run system
python production_integration.py
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For support and questions:
- Check the documentation
- Review the test files for examples
- Open an issue on GitHub

---

**🎉 IntelliVest AI - Transforming Investment Analysis with Advanced AI**
