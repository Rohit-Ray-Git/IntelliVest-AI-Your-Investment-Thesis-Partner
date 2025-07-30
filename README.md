# 🚀 IntelliVest AI - Your Investment Thesis Partner

> **AI-Powered Investment Research & Thesis Builder** - A multi-agent tool that gathers real-time financial data, performs analysis, and generates professional investment theses.

## 📊 Project Overview

IntelliVest AI is a comprehensive investment research platform that combines web crawling, financial data analysis, and AI-powered insights to generate professional investment theses. The system uses multiple specialized agents to gather, analyze, and synthesize information from various sources.

## ✨ Features

### 🤖 Multi-Agent Architecture
- **🕷️ Crawler Agent**: Crawls financial websites, news, and blogs
- **📊 Data Agent**: Fetches live financial ratios and stock data
- **💬 Sentiment Agent**: Analyzes news sentiment and market mood
- **💰 Valuation Agent**: Computes financial metrics and comparisons
- **🧾 Thesis Builder Agent**: Generates comprehensive investment theses
- **🧐 Critic Agent**: Reviews bias and highlights risks

### 🔍 Data Sources
- **Real-time Financial Data**: yfinance, Alpha Vantage, FMP API
- **News & Articles**: Web crawling with Crawl4AI
- **Market Sentiment**: NLP analysis of financial news
- **Peer Comparisons**: Industry benchmarking

### 📈 Analysis Capabilities
- **SWOT Analysis**: Strengths, Weaknesses, Opportunities, Threats
- **Financial Metrics**: P/E, PEG, YoY growth, market cap analysis
- **Risk Assessment**: Comprehensive risk factor identification
- **Valuation Models**: Multiple valuation approaches
- **Industry Comparison**: Peer and sector analysis

### 🎨 User Interface
- **Streamlit Web App**: Modern, interactive interface
- **Real-time Updates**: Live data and analysis
- **Export Options**: PDF reports and data exports
- **Report History**: Save and revisit past analyses

## 🛠️ Technology Stack

### Core Frameworks
- **Agent Framework**: CrewAI, LangChain, LangGraph
- **LLM Integration**: OpenAI GPT, Google Gemini, LiteLLM
- **Web Crawling**: Crawl4AI, Playwright, BeautifulSoup
- **Financial Data**: yfinance, pandas, numpy

### UI & Deployment
- **Web Interface**: Streamlit
- **Data Visualization**: Altair, Plotly
- **Report Generation**: PDFKit, Markdown
- **Vector Database**: FAISS, ChromaDB

### Development Tools
- **Language**: Python 3.10+
- **Package Management**: pip, requirements.txt
- **Version Control**: Git
- **Environment**: Virtual environments

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- API keys for LLM services (OpenAI, Google AI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohit-Ray-Git/IntelliVest-AI-Your-Investment-Thesis-Partner.git
   cd IntelliVest-AI-Your-Investment-Thesis-Partner
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

5. **Configure environment variables**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env
   # Add your API keys to .env
   ```

6. **Run the application**
   ```bash
   streamlit run app/streamlit_ui.py
   ```

## 📁 Project Structure

```
ai-investment-agent/
├── agents/                 # Multi-agent system
│   ├── crawler_agent.py    # Web crawling agent
│   ├── data_agent.py       # Financial data agent
│   ├── sentiment_agent.py  # Sentiment analysis agent
│   ├── valuation_agent.py  # Valuation analysis agent
│   ├── thesis_writer_agent.py  # Thesis generation agent
│   └── critic_agent.py     # Review and critique agent
├── utils/                  # Utility functions
│   ├── crawl4ai_helper.py  # Crawl4AI integration
│   ├── finance_api.py      # Financial data APIs
│   └── formatting.py       # Data formatting utilities
├── app/                    # Web application
│   └── streamlit_ui.py     # Streamlit interface
├── output/                 # Generated reports
│   └── reports/            # PDF and data exports
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FMP_API_KEY=your_fmp_api_key

# Configuration
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini
CRAWL_MAX_PAGES=10
ENABLE_PDF_EXPORT=true
```

## 📖 Usage

### Basic Usage
1. **Start the application**: `streamlit run app/streamlit_ui.py`
2. **Enter company name or ticker**: e.g., "AAPL" or "Apple Inc."
3. **Configure analysis parameters**: Time period, metrics, etc.
4. **Generate report**: Click "Generate Investment Thesis"
5. **Review results**: Analyze the comprehensive report
6. **Export**: Download PDF or data files

### Advanced Features
- **Custom Analysis**: Modify agent prompts and parameters
- **Batch Processing**: Analyze multiple companies
- **Historical Comparison**: Compare current vs. historical data
- **Risk Assessment**: Detailed risk factor analysis

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .
isort .

# Lint code
flake8
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Crawl4AI**: For web crawling capabilities
- **CrewAI**: For multi-agent orchestration
- **yfinance**: For financial data access
- **Streamlit**: For the web interface
- **OpenAI & Google**: For LLM capabilities

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Rohit-Ray-Git/IntelliVest-AI-Your-Investment-Thesis-Partner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Rohit-Ray-Git/IntelliVest-AI-Your-Investment-Thesis-Partner/discussions)
- **Email**: [Your Email]

## 🔮 Roadmap

- [ ] **Real-time Alerts**: Market movement notifications
- [ ] **Portfolio Integration**: Connect to brokerage accounts
- [ ] **Advanced ML Models**: Custom prediction models
- [ ] **Mobile App**: React Native mobile application
- [ ] **API Service**: RESTful API for third-party integration
- [ ] **Backtesting**: Historical strategy testing
- [ ] **Social Features**: Share and discuss theses

---

**Disclaimer**: This tool is for educational and research purposes only. Investment decisions should be based on comprehensive analysis and professional advice. Past performance does not guarantee future results.
