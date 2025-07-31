# 🚀 **IntelliVest AI - Your Investment Thesis Partner**

> **Production-Ready Agentic AI System for Investment Analysis**

## 📋 **Overview**

IntelliVest AI is a sophisticated, production-ready agentic AI system that provides comprehensive investment analysis using advanced AI models and real-time data. The system combines CrewAI orchestration, advanced fallback systems, and custom tools to deliver professional-grade investment insights.

## 🎯 **Key Features**

- **🤖 Agentic AI Framework**: CrewAI with 5 specialized agents
- **🧠 Advanced Fallback System**: Multi-LLM orchestration with intelligent routing
- **🎯 Primary Model**: Gemini 2.5 Flash with robust fallbacks
- **🛠️ Custom Tools**: 6 investment tools with real data access
- **📊 Real-time Monitoring**: Comprehensive metrics and analytics
- **🚀 Production Ready**: Enterprise-grade reliability and performance

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
git clone <repository-url>
cd IntelliVest-AI

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

## 🛠️ **Custom Tools**

The system includes 6 specialized tools:

1. **🕷️ Web Crawler**: Real-time web data extraction
2. **📊 Financial Data**: Market data and financial metrics
3. **🧠 Sentiment Analysis**: Market sentiment quantification
4. **💰 Valuation Tools**: Financial modeling and analysis
5. **📝 Thesis Generation**: Professional investment thesis creation
6. **🔍 Critique Tools**: Quality assurance and improvement

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

## 📁 **Project Structure**

```
IntelliVest-AI/
├── 🚀 production_integration.py      # Main production interface
├── 🧪 test_production_integration.py # Comprehensive test suite
├── 📋 requirements.txt               # Dependencies
├── 📖 README.md                      # This file
├── 🔧 .env                           # API configuration
├── 🤖 agents/                        # CrewAI agents
│   └── crew_agents_with_tools.py     # Main agent definitions
├── 🧠 llm/                          # LLM management
│   └── advanced_fallback_system.py   # Multi-LLM orchestration
├── 🛠️ tools/                        # Custom tools
│   └── investment_tools.py           # Investment analysis tools
├── 🔄 workflows/                     # LangGraph workflows
│   └── investment_workflow.py        # Advanced workflows
├── 🌐 frontend/                      # Streamlit web interface
├── 🔌 api/                          # FastAPI backend
├── 🛠️ utils/                        # Utility functions
├── 📊 output/                       # Analysis outputs
└── 🚀 app/                          # Legacy app files
```

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

### **Production Deployment**
```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY=your_key
export OPENAI_API_KEY=your_groq_key

# Run production system
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

