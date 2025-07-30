# 🚀 IntelliVest AI - Your Investment Thesis Partner

> **AI-Powered Investment Research & Thesis Builder** - A comprehensive multi-agent system with web UI that analyzes financial news, performs sentiment analysis, and generates professional investment thesis with real-time progress tracking.

## 📊 Project Overview

IntelliVest AI is an intelligent investment research platform that leverages multiple AI agents to gather, analyze, and synthesize financial information into comprehensive investment theses. The system features a modern web interface, advanced web crawling with crawl4ai, multi-provider AI integration, and real-time progress tracking.

## ✨ Key Features

### 🌐 Modern Web Interface
- **Beautiful UI**: Modern, responsive web interface built with HTML, JavaScript, and Tailwind CSS
- **Real-time Progress**: Live progress tracking during analysis with detailed logs
- **Scraped URLs Display**: Shows all successfully crawled websites with clickable links
- **Professional Results**: Formatted investment thesis, critique, and revised analysis
- **Error Handling**: Graceful error recovery with helpful messages

### 🤖 Multi-Agent Pipeline
- **🔍 News Search Agent**: Uses Tavily API to find recent financial news articles
- **🕷️ Crawler Agent**: Extracts content from financial websites using crawl4ai and aiohttp
- **🧠 Sentiment Agent**: Analyzes market sentiment using multiple AI providers
- **💰 Valuation Agent**: Assesses company valuation and financial metrics
- **📄 Thesis Writer Agent**: Generates comprehensive investment theses
- **🧐 Critic Agent**: Reviews and critiques theses for biases and gaps
- **🛠️ Thesis Rewrite Agent**: Revises theses based on critique feedback

### 🔍 Data Sources & Analysis
- **Real-time News**: Financial news from MarketBeat, CNN, company blogs, and investor sites
- **Content Extraction**: Advanced web crawling with markdown conversion using crawl4ai
- **Sentiment Analysis**: AI-powered sentiment classification with multiple fallback providers
- **Valuation Insights**: P/E ratios, PEG ratios, DCF analysis, and market positioning
- **Risk Assessment**: Comprehensive bias detection and risk factor identification

### 📈 Output Capabilities
- **Investment Thesis**: Professional-grade investment recommendations
- **Sentiment Analysis**: Market mood and sentiment justification
- **Valuation Assessment**: Financial metrics and valuation status
- **Critique Report**: Bias detection and improvement suggestions
- **Revised Thesis**: Enhanced thesis incorporating feedback
- **Scraped URLs**: Complete list of analyzed websites with status

## 🛠️ Technology Stack

### Frontend & UI
- **Web Interface**: HTML5, JavaScript, Tailwind CSS
- **Progress Tracking**: Real-time progress bars and status updates
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Professional design with animations and icons

### Backend & API
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **CORS Support**: Cross-origin resource sharing for frontend-backend communication
- **Async Processing**: Non-blocking I/O operations throughout

### Core AI & LLM
- **Primary LLM**: Google Gemini models (2.5-flash, 1.5-flash, 1.5-pro, 2.0-flash-exp)
- **Fallback LLM**: Groq models (deepseek-r1-distill-llama-70b, llama3.1-70b, llama3.1-8b, gemma2-9b, mixtral-8x7b)
- **AI Client**: RobustAIClient with automatic fallback and retry logic
- **Agent Framework**: Custom async agent architecture

### Web Crawling & Data
- **Web Crawler**: crawl4ai with aiohttp backend (no Playwright dependency)
- **News Search**: Tavily API for financial news discovery
- **Content Processing**: Markdown extraction and formatting
- **Error Handling**: Graceful handling of failed URLs and encoding issues

### Development & Deployment
- **Language**: Python 3.10+
- **Async Framework**: asyncio for concurrent processing
- **Environment Management**: python-dotenv
- **Package Management**: pip with comprehensive requirements.txt
- **Virtual Environment**: Isolated Python environment

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Modern web browser
- API keys for enhanced features (optional - works with fallbacks)

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

4. **Configure environment variables (optional)**
   ```bash
   # Create .env file with your API keys for enhanced AI features
   echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
   echo "TAVILY_API_KEY=your_tavily_api_key_here" >> .env
   ```

5. **Run the application**
   ```bash
   python run_app.py
   ```

### Alternative Launch Methods

**Windows Batch File:**
```bash
start_intellivest.bat
```

**PowerShell Script:**
```powershell
.\start_intellivest.ps1
```

## 📋 Usage

### Web Interface
1. **Launch Application**: Run `python run_app.py`
2. **Open Browser**: Application automatically opens in your default browser
3. **Enter Company**: Type a company name (e.g., "Google", "Apple", "Tesla")
4. **Watch Progress**: Real-time progress tracking shows each step
5. **View Results**: Professional investment thesis with analysis

### Command Line Interface
```bash
python main.py
```

### API Endpoints
- **Health Check**: `GET /health`
- **Generate Thesis**: `POST /generate-thesis`
- **API Documentation**: `http://127.0.0.1:8001/docs`

## 🏗️ Project Structure

```
IntelliVest-AI/
├── agents/                     # AI Agent Modules
│   ├── crawler_agent.py       # Web crawling with crawl4ai
│   ├── sentiment_agent.py     # Sentiment analysis
│   ├── valuation_agent.py     # Financial valuation assessment
│   ├── thesis_writer_agent.py # Investment thesis generation
│   ├── critic_agent.py        # Thesis critique and review
│   └── thesis_rewrite_agent.py # Thesis revision based on feedback
├── api/                        # FastAPI Backend
│   └── main.py                # API endpoints and server
├── frontend/                   # Web Interface
│   └── index.html             # Modern web UI
├── utils/                      # Utility Functions
│   ├── search.py              # Tavily API integration
│   ├── ai_client.py           # Robust AI client with fallbacks
│   └── formatting.py          # Output formatting helpers
├── main.py                     # Command line entry point
├── run_app.py                  # Complete application launcher
├── start_intellivest.bat      # Windows launcher
├── start_intellivest.ps1      # PowerShell launcher
├── get_api_keys.py            # API key setup guide
├── test_models.py             # Model configuration tester
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Configuration

### Required API Keys
Create a `.env` file in the project root with:

```env
# Enhanced AI Features (Optional - works with fallbacks)
GOOGLE_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# News Search (Required)
TAVILY_API_KEY=your_tavily_api_key_here
```

### API Key Setup
1. **Google AI (Gemini)**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Groq**: Get API key from [Groq Console](https://console.groq.com/keys)
3. **Tavily**: Get API key from [Tavily AI](https://tavily.com/)

### Setup Helper
```bash
python get_api_keys.py  # Opens setup guides and creates .env template
```

## 🤖 AI Models & Providers

### Google Gemini Models
- `gemini/gemini-1.5-flash` - Fast and efficient
- `gemini/gemini-1.5-pro` - More capable model
- `gemini/gemini-2.0-flash-exp` - Latest experimental model

### Groq Models
- `groq/llama3.1-70b-8192` - Large, powerful model
- `groq/llama3.1-8b-8192` - Smaller, faster model
- `groq/gemma2-9b-it` - Google's Gemma model
- `groq/mixtral-8x7b-32768` - Mixture of experts model

### Fallback System
- **Automatic Fallback**: If one model fails, automatically tries the next
- **Rate Limit Handling**: Switches providers when rate limits are hit
- **Comprehensive Fallbacks**: Professional responses even without API keys
- **Error Recovery**: Graceful degradation when all APIs fail

## 🧪 Testing & Development

### Test AI Models
```bash
python test_models.py  # Verify model configuration
```

### Test Individual Components
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

### API Testing
```bash
# Start backend only
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001

# Test API endpoints
curl http://127.0.0.1:8001/health
```

## 🔄 Pipeline Flow

1. **Input**: Company/stock name from web interface or command line
2. **News Search**: Tavily API finds recent financial articles
3. **Content Extraction**: crawl4ai extracts markdown content from URLs
4. **Progress Tracking**: Real-time updates in web UI
5. **Sentiment Analysis**: Multi-provider AI analyzes market sentiment
6. **Valuation Assessment**: Financial metrics and valuation analysis
7. **Thesis Generation**: Comprehensive investment thesis creation
8. **Critique**: Bias detection and improvement suggestions
9. **Revision**: Enhanced thesis incorporating feedback
10. **Output**: Professional investment recommendation with supporting analysis

## 🎯 Key Features in Detail

### Real-time Progress Tracking
- **Live Progress Bar**: Visual progress indicator
- **Step-by-step Logs**: Detailed status updates
- **URL Status**: Success/failure tracking for each scraped website
- **Error Handling**: Clear error messages and recovery

### Comprehensive Web Scraping
- **Multiple Sources**: Financial news, company blogs, investor relations
- **Content Validation**: Ensures sufficient content is extracted
- **Error Recovery**: Continues processing even if some URLs fail
- **Markdown Conversion**: Clean, readable content extraction

### Professional Analysis
- **Investment Thesis**: Buy/hold/sell recommendations with justification
- **Sentiment Analysis**: Market mood assessment with confidence levels
- **Valuation Metrics**: Financial ratios and growth prospects
- **Risk Assessment**: Comprehensive risk factor identification

## 🚧 Future Enhancements

- **Financial Data Integration**: Real-time stock data and financial ratios
- **Report Export**: PDF and markdown export capabilities
- **Historical Analysis**: Track thesis performance over time
- **Multi-Company Comparison**: Side-by-side analysis of competitors
- **Risk Scoring**: Quantitative risk assessment metrics
- **Portfolio Integration**: Track multiple investments
- **Email Alerts**: Notifications for significant market changes

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

## 🆘 Support & Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   python get_api_keys.py  # Get setup instructions
   python test_models.py   # Verify configuration
   ```

2. **Dependency Issues**
   ```bash
   pip install -r requirements.txt
   ```

3. **Port Conflicts**
   ```bash
   # Kill existing processes
   taskkill /f /im python.exe
   # Restart application
   python run_app.py
   ```

4. **Browser Issues**
   - Application opens automatically in default browser
   - Manual access: `file://path/to/frontend/index.html`
   - Backend API: `http://127.0.0.1:8001`

### Getting Help
- Check console output for specific error messages
- Verify all API keys are properly configured
- Ensure virtual environment is activated
- Test individual components with provided test scripts

For bugs or feature requests, please open an issue on GitHub.

## 🎉 Current Status

✅ **Fully Functional Web Application**
✅ **Real-time Progress Tracking**
✅ **Professional Investment Analysis**
✅ **Multi-provider AI Integration**
✅ **Comprehensive Error Handling**
✅ **Modern, Responsive UI**
✅ **Robust Fallback System**
✅ **Easy Setup and Deployment**

