# 🚀 IntelliVest AI - Your Investment Thesis Partner

> **AI-Powered Investment Research & Thesis Builder** - A multi-agent system that analyzes financial news, performs sentiment analysis, and generates professional investment thesis with critique and revision capabilities.

## 📊 Project Overview

IntelliVest AI is an intelligent investment research platform that leverages multiple AI agents to gather, analyze, and synthesize financial information into comprehensive investment theses. The system uses advanced web crawling, sentiment analysis, valuation assessment, and AI-powered critique to deliver professional-grade investment insights.

## ✨ Key Features

### 🤖 Multi-Agent Pipeline
- **🔍 News Search Agent**: Uses Tavily API to find recent financial news articles
- **🕷️ Crawler Agent**: Extracts content from financial websites using Crawl4AI
- **🧠 Sentiment Agent**: Analyzes market sentiment using Google Gemini AI
- **💰 Valuation Agent**: Assesses company valuation and financial metrics
- **📄 Thesis Writer Agent**: Generates comprehensive investment theses
- **🧐 Critic Agent**: Reviews and critiques theses for biases and gaps
- **🛠️ Thesis Rewrite Agent**: Revises theses based on critique feedback

### 🔍 Data Sources & Analysis
- **Real-time News**: Financial news from CNBC, Reuters, Bloomberg, and company investor sites
- **Content Extraction**: Advanced web crawling with markdown conversion
- **Sentiment Analysis**: AI-powered sentiment classification (Positive/Negative/Neutral)
- **Valuation Insights**: P/E ratios, PEG ratios, DCF analysis, and market positioning
- **Risk Assessment**: Comprehensive bias detection and risk factor identification

### 📈 Output Capabilities
- **Investment Thesis**: Professional-grade investment recommendations
- **Sentiment Analysis**: Market mood and sentiment justification
- **Valuation Assessment**: Financial metrics and valuation status
- **Critique Report**: Bias detection and improvement suggestions
- **Revised Thesis**: Enhanced thesis incorporating feedback

## 🛠️ Technology Stack

### Core AI & LLM
- **Primary LLM**: Google Gemini 2.5 Flash (via `google-generativeai`)
- **Fallback LLM**: Groq DeepSeek (via OpenAI-compatible API)
- **Agent Framework**: Custom async agent architecture

### Web Crawling & Data
- **Web Crawler**: Crawl4AI with Playwright backend
- **News Search**: Tavily API for financial news discovery
- **Content Processing**: Markdown extraction and formatting

### Development & Deployment
- **Language**: Python 3.10+
- **Async Framework**: asyncio for concurrent processing
- **Environment Management**: python-dotenv
- **Package Management**: pip with comprehensive requirements.txt

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- API keys for:
  - Google AI (Gemini) - Primary LLM
  - Groq API - Fallback LLM
  - Tavily API - News search

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohit-Ray-Git/IntelliVest-AI-Your-Investment-Thesis-Partner.git
   cd IntelliVest-AI-Your-Investment-Thesis-Partner
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers (for web crawling)**
   ```bash
   playwright install
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file with your API keys
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
   echo "TAVILY_API_KEY=your_tavily_api_key_here" >> .env
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Usage

### Command Line Interface
```bash
python main.py
```

The application will prompt you to enter a company or stock name, then automatically:

1. **Search** for recent financial news about the company
2. **Crawl** and extract content from relevant articles
3. **Analyze** sentiment and market mood
4. **Assess** valuation and financial metrics
5. **Generate** a comprehensive investment thesis
6. **Critique** the thesis for biases and improvements
7. **Revise** the thesis based on feedback

### Example Output
```
🚀 IntelliVest AI — Investment Thesis Generator

📌 Enter company or stock name to research: NVIDIA

🔍 Searching news for: NVIDIA
🌐 Crawling and extracting articles...
🧠 Running Sentiment Analysis...
💸 Running Valuation...
📄 Generating Investment Thesis...
🧐 Running Thesis Critique...
🛠 Rewriting Thesis Based on Critique...

✅ Pipeline Complete.

--- Investment Thesis ---
[Professional investment thesis with buy/hold/sell recommendation]

--- Critique ---
[Detailed critique highlighting biases and improvements]

--- Revised Thesis ---
[Enhanced thesis incorporating feedback]
```

## 🏗️ Project Structure

```
IntelliVest-AI/
├── agents/                     # AI Agent Modules
│   ├── crawler_agent.py       # Web crawling and content extraction
│   ├── sentiment_agent.py     # Sentiment analysis
│   ├── valuation_agent.py     # Financial valuation assessment
│   ├── thesis_writer_agent.py # Investment thesis generation
│   ├── critic_agent.py        # Thesis critique and review
│   └── thesis_rewrite_agent.py # Thesis revision based on feedback
├── utils/                      # Utility Functions
│   ├── search.py              # Tavily API integration
│   ├── llm.py                 # LLM calling utilities
│   └── formatting.py          # Output formatting helpers
├── app/                        # Web Application (Future)
│   └── streamlit_ui.py        # Streamlit interface
├── output/                     # Generated Reports
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### Required API Keys
Create a `.env` file in the project root with:

```env
# Primary LLM (Required)
GOOGLE_API_KEY=your_gemini_api_key_here

# Fallback LLM (Recommended)
GROQ_API_KEY=your_groq_api_key_here

# News Search (Required)
TAVILY_API_KEY=your_tavily_api_key_here
```

### API Key Setup
1. **Google AI (Gemini)**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Groq**: Get API key from [Groq Console](https://console.groq.com/)
3. **Tavily**: Get API key from [Tavily AI](https://tavily.com/)

## 🧪 Testing Individual Agents

Each agent can be tested independently:

```bash
# Test sentiment analysis
python agents/sentiment_agent.py

# Test valuation assessment
python agents/valuation_agent.py

# Test thesis generation
python agents/thesis_writer_agent.py

# Test web crawling
python agents/crawler_agent.py
```

## 🔄 Pipeline Flow

1. **Input**: Company/stock name from user
2. **News Search**: Tavily API finds recent financial articles
3. **Content Extraction**: Crawl4AI extracts markdown content
4. **Sentiment Analysis**: Gemini AI analyzes market sentiment
5. **Valuation Assessment**: Financial metrics and valuation analysis
6. **Thesis Generation**: Comprehensive investment thesis creation
7. **Critique**: Bias detection and improvement suggestions
8. **Revision**: Enhanced thesis incorporating feedback
9. **Output**: Final investment recommendation with supporting analysis

## 🚧 Future Enhancements

- **Web Interface**: Streamlit-based UI for easier interaction
- **Financial Data Integration**: Real-time stock data and financial ratios
- **Report Export**: PDF and markdown export capabilities
- **Historical Analysis**: Track thesis performance over time
- **Multi-Company Comparison**: Side-by-side analysis of competitors
- **Risk Scoring**: Quantitative risk assessment metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Investment decisions should be based on comprehensive research and consultation with financial advisors. The authors are not responsible for any financial losses resulting from the use of this tool.

## 🆘 Support

If you encounter any issues:

1. Check that all API keys are properly configured
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify Playwright browsers are installed: `playwright install`
4. Check the console output for specific error messages

For bugs or feature requests, please open an issue on GitHub.
