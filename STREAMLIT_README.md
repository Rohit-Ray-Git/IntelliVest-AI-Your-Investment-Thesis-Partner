# 🚀 IntelliVest AI - Streamlit UI

## 📋 Overview

This directory contains the professional Streamlit user interface for IntelliVest AI, providing a modern, interactive web interface for investment thesis generation and analysis.

## 🎯 Features

### **Professional UI Design**
- 🎨 Modern, responsive design with gradient backgrounds
- 📱 Mobile-friendly interface
- 🎯 Professional color scheme and typography
- 📊 Interactive visualizations and charts

### **Real-time Progress Tracking**
- 🔄 Live progress indicators
- 🤖 Agent status monitoring
- ⏱️ Real-time execution time tracking
- 📋 Detailed progress logs

### **Comprehensive Analysis Display**
- 📈 Investment thesis reports
- 🔍 Research analysis results
- 😊 Sentiment analysis with visualizations
- 💰 Valuation analysis
- 🔍 Critique and validation
- ✏️ Final revised thesis

### **Interactive Features**
- ⚙️ Configurable analysis options
- 📊 System status monitoring
- 📥 Report download capabilities
- 🔄 Analysis history tracking

## 📁 Files

### **Core Application Files**
- `streamlit_app.py` - Basic Streamlit interface
- `streamlit_app_enhanced.py` - Enhanced interface with real-time tracking
- `launch_streamlit.py` - Simple launcher script

### **Launcher Scripts**
- `run_streamlit.py` - Comprehensive launcher with dependency checking
- `launch_streamlit.py` - Simple launcher with interface selection

## 🚀 Quick Start

### **Option 1: Simple Launch**
```bash
python launch_streamlit.py
```

### **Option 2: Comprehensive Launch**
```bash
python run_streamlit.py
```

### **Option 3: Direct Streamlit**
```bash
streamlit run streamlit_app.py
# or
streamlit run streamlit_app_enhanced.py
```

## 🎨 Interface Comparison

### **Basic Interface (`streamlit_app.py`)**
- ✅ Clean, simple design
- ✅ Core functionality
- ✅ Easy to understand
- ✅ Lightweight

### **Enhanced Interface (`streamlit_app_enhanced.py`)**
- ✅ Advanced styling and animations
- ✅ Real-time agent status tracking
- ✅ Enhanced progress visualization
- ✅ Professional report formatting
- ✅ Interactive charts and gauges

## 📊 UI Components

### **Header Section**
- Professional gradient header
- Application branding
- Status indicators

### **Sidebar Configuration**
- Analysis type selection
- Advanced options
- System status monitoring
- Recent analysis history

### **Main Interface**
- Company input field
- Analysis progress tracking
- Results display tabs
- Download options

### **Progress Tracking**
- Real-time progress bar
- Agent status grid
- Live progress log
- Execution time tracking

### **Results Display**
- Executive summary
- Research analysis
- Sentiment analysis with gauges
- Valuation analysis
- Critique and validation
- Final revised thesis

## 🎯 Usage Guide

### **1. Starting an Analysis**
1. Enter company name or stock symbol
2. Select analysis type (optional)
3. Configure advanced options (optional)
4. Click "🚀 Start Analysis"

### **2. Monitoring Progress**
- Watch real-time progress bar
- Monitor agent status indicators
- View detailed progress log
- Track execution time

### **3. Reviewing Results**
- Read executive summary
- Explore detailed analysis tabs
- View interactive visualizations
- Download reports

### **4. Configuration Options**
- **Analysis Type**: Full, Research, Sentiment, Valuation, or Thesis only
- **Advanced Fallback**: Enable multi-LLM fallback system
- **Max Fallbacks**: Set maximum number of AI model fallbacks
- **Custom Tools**: Enable specialized investment tools
- **Analysis Depth**: Basic, Standard, Comprehensive, or Expert

## 🛠️ Technical Details

### **Dependencies**
```python
streamlit>=1.47.1
plotly>=5.5.0
pandas>=2.3.1
asyncio
threading
json
time
datetime
```

### **Session State Management**
- Analysis running status
- Progress tracking
- Results storage
- Agent status tracking
- Step progress indicators

### **Real-time Updates**
- Threading for background analysis
- Session state updates
- Progress log management
- Agent status synchronization

### **Error Handling**
- Graceful error display
- Fallback mechanisms
- User-friendly error messages
- System status monitoring

## 🎨 Customization

### **Styling**
The interface uses custom CSS for professional styling:
- Gradient backgrounds
- Card-based layouts
- Status indicators
- Hover effects
- Responsive design

### **Themes**
- Light theme (default)
- Professional color scheme
- Consistent branding
- Accessibility considerations

### **Charts and Visualizations**
- Plotly gauge charts for sentiment
- Progress bars for tracking
- Status cards for agents
- Interactive data tables

## 📱 Browser Compatibility

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🔧 Troubleshooting

### **Common Issues**

1. **Streamlit not starting**
   ```bash
   pip install streamlit
   streamlit --version
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **API key issues**
   - Check `.env` file configuration
   - Verify API key validity
   - Ensure proper environment setup

4. **Analysis not running**
   - Check system status in sidebar
   - Verify agent availability
   - Review error logs

### **Performance Optimization**
- Use enhanced interface for better tracking
- Monitor system resources
- Close unnecessary browser tabs
- Check network connectivity

## 📈 Future Enhancements

### **Planned Features**
- 📄 PDF report generation
- 📊 CSV data export
- 🔄 Analysis comparison
- 📈 Historical analysis tracking
- 🎯 Custom analysis templates
- 📱 Mobile app version

### **UI Improvements**
- 🎨 Dark theme option
- 📊 More interactive charts
- 🔄 Real-time data feeds
- 📱 Progressive Web App (PWA)
- 🎯 Customizable dashboards

## 🤝 Contributing

To contribute to the Streamlit UI:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### **Development Guidelines**
- Follow Streamlit best practices
- Maintain responsive design
- Add proper error handling
- Include documentation
- Test on multiple browsers

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main project README
3. Check system status in the UI
4. Review error logs and progress

---

**🚀 Ready to analyze investments with professional-grade AI!** 