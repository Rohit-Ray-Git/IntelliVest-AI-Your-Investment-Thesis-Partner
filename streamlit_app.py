"""
🚀 IntelliVest AI - Streamlit Application
=========================================

Advanced AI-Powered Investment Analysis with Parallel Processing
Features:
- Dynamic market discovery with parallel processing
- Multi-agent investment analysis
- Real-time quote rotation and progress indicators
- Comprehensive analysis history
- Professional investment thesis generation
"""

import subprocess
import sys
import os
from pathlib import Path

def launch_streamlit():
    """Launch the Streamlit app if run directly"""
    print("🚀 Launching IntelliVest AI Streamlit App...")
    print("=" * 50)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    print("🌐 Starting Streamlit server...")
    print("📱 The app will open in your default browser")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Try different ports if 8501 is busy
    ports = [8501, 8502, 8503, 8504, 8505]
    
    for port in ports:
        try:
            print(f"🔄 Trying port {port}...")
            # Launch Streamlit
            subprocess.run([
                sys.executable, "-m", "streamlit", "run",
                str(__file__),
                "--server.port", str(port),
                "--server.address", "localhost",
                "--browser.gatherUsageStats", "false"
            ], check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            if "Port" in str(e) and "is already in use" in str(e):
                print(f"⚠️ Port {port} is busy, trying next port...")
                continue
            else:
                print(f"❌ Error launching Streamlit: {e}")
                return False
        except KeyboardInterrupt:
            print("\n🛑 Streamlit server stopped by user")
            return True
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    print("❌ All ports are busy. Please stop other Streamlit instances and try again.")
    return False

# Check if this file is being run directly (not by Streamlit)
if __name__ == "__main__":
    # Check if we're being run by Streamlit or directly
    if "streamlit" not in sys.modules:
        # Run directly - launch Streamlit
        success = launch_streamlit()
        sys.exit(0 if success else 1)
    else:
        # Being run by Streamlit - continue with the app
        pass

# Streamlit app code starts here
import streamlit as st
import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import our systems
from production_integration import ProductionIntelliVestAI, AnalysisRequest
from financial_facts import get_random_fact

# Configure LiteLLM environment variables before importing production system
from dotenv import load_dotenv
load_dotenv()

# Set up LiteLLM environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# Import our production system
from production_integration import ProductionIntelliVestAI, AnalysisRequest

# Import financial facts
from financial_facts import get_random_fact, get_facts_count

# Page configuration
st.set_page_config(
    page_title="IntelliVest AI - Investment Analysis",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Pitch black theme */
    .main {
        background-color: #000000 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
    }
    
    .block-container {
        background-color: #000000 !important;
    }
    
    .stMarkdown {
        background-color: #000000 !important;
    }
    
    /* Text colors for better contrast on black */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 2px;
        color: #ffffff !important;
    }
    
    .main-header h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #f8f9fa !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
        color: #e9ecef !important;
        max-width: 800px;
        margin: 0 auto;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    /* Make all text white for better visibility on black */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, div, span {
        color: #ffffff !important;
    }
    
    /* Streamlit specific text colors */
    .stMarkdown, .stText, .stMetric {
        color: #ffffff !important;
    }
    
    /* Info boxes with better contrast */
    .stAlert {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        color: #ffffff !important;
    }
    
    /* Cards with better styling for black theme */
    .stock-card, .sector-card {
        background-color: #1a1a1a !important;
        border: 2px solid #333333 !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        text-align: center !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Make tabs wider and better spaced */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        width: 100%;
        justify-content: space-between;
        background-color: #1a1a1a !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        min-width: 0;
        padding: 10px 15px;
        font-size: 14px;
        font-weight: 500;
        color: #ffffff !important;
        background-color: #1a1a1a !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 20px;
        background-color: #000000 !important;
    }
    
    /* Ensure full width layout */
    .main .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
        background-color: #000000 !important;
    }
    
    /* Financial facts styling */
    .financial-fact {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.6;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .financial-fact strong {
        color: #f8f9fa;
        font-weight: 600;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Dataframe styling for black theme */
    .stDataFrame {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: #cccccc !important;
    }
    
    /* Sidebar styling for black theme */
    .css-1d391kg {
        background-color: #1a1a1a !important;
    }
    
    .css-1lcbmhc {
        background-color: #1a1a1a !important;
    }
    
    /* Selectbox and input styling */
    .stSelectbox, .stTextInput, .stTextArea, .stNumberInput {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        color: #ffffff !important;
    }
    
    /* Slider styling */
    .stSlider {
        background-color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

class IntelliVestStreamlitApp:
    """Main Streamlit application class"""
    
    def __init__(self):
        """Initialize the Streamlit app"""
        self.system = None
        self.analysis_history = []
        
        # Initialize session state for market highlights caching
        if 'market_highlights_loaded' not in st.session_state:
            st.session_state.market_highlights_loaded = False
            st.session_state.market_highlights_data = None
            st.session_state.market_highlights_timestamp = None
        
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize the production system"""
        try:
            with st.spinner("🚀 Initializing IntelliVest AI System..."):
                self.system = ProductionIntelliVestAI()
            st.success("✅ System initialized successfully!")
        except Exception as e:
            st.error(f"❌ System initialization failed: {e}")
            st.stop()
    
    def update_metrics_after_analysis(self, result):
        """Update metrics after an analysis is completed"""
        # This method is kept for compatibility but metrics are no longer displayed
        pass
    
    def update_metrics_from_system(self):
        """Update session state metrics from system status"""
        # This method is kept for compatibility but metrics are no longer displayed
        pass
            
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 IntelliVest AI</h1>
            <h3>Your Intelligent Investment Thesis Partner</h3>
            <p>Revolutionize Investment Analysis with AI-Powered Market Intelligence & Lightning-Fast Parallel Processing</p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        st.sidebar.markdown("## ⚙️ Configuration")
            
            # Analysis type selection
        analysis_type = st.sidebar.selectbox(
            "📊 Analysis Type",
            ["full", "research", "sentiment", "valuation", "thesis"],
                help="Choose the type of analysis to perform"
            )
        
        # Parallel processing configuration
        st.sidebar.markdown("### ⚡ Performance Settings")
        max_concurrent = st.sidebar.slider(
            "Parallel Workers",
            min_value=1,
            max_value=20,
            value=10,
            help="Number of concurrent workers for parallel processing"
        )
            
            # Advanced options
        st.sidebar.markdown("### 🔧 Advanced Options")
        include_tools = st.sidebar.checkbox(
            "Include Custom Tools",
                    value=True,
            help="Use custom investment analysis tools"
        )
        
        use_advanced_fallback = st.sidebar.checkbox(
            "Use Advanced Fallback",
            value=True,
            help="Enable multi-LLM fallback system"
        )
        
        max_fallbacks = st.sidebar.slider(
                    "Max Fallbacks",
                    min_value=1,
                    max_value=5,
                    value=3,
            help="Maximum number of fallback models to use"
        )
        
        return {
            "analysis_type": analysis_type,
            "max_concurrent": max_concurrent,
            "include_tools": include_tools,
            "use_advanced_fallback": use_advanced_fallback,
            "max_fallbacks": max_fallbacks
        }
    
    def render_analysis_form(self, config):
        """Render the analysis input form"""
        st.markdown("## 📈 Investment Analysis")
        st.info("💡 **Tip:** Use the market insights above to identify trending stocks for analysis!")
        
        # Company input
        company_name = st.text_input(
            "🏢 Company Name or Symbol",
            placeholder="e.g., Apple Inc., AAPL, Tesla, TSLA, RELIANCE.NS",
            help="Enter the company name or stock symbol to analyze"
        )
        
        # Analysis description
        analysis_description = st.text_area(
            "📝 Analysis Focus (Optional)",
            placeholder="Describe specific aspects you want to focus on (e.g., financial health, growth prospects, risks)",
            help="Optional description to guide the analysis"
        )
        
        # Budget limit (optional)
        budget_limit = st.number_input(
            "💰 Budget Limit (Optional)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.1,
            help="Maximum cost for the analysis in USD"
        )
        
        # Run analysis button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            run_analysis = st.button(
                "🚀 Run Analysis",
                type="primary",
                use_container_width=True
            )
        
        return {
            "company_name": company_name,
            "analysis_description": analysis_description,
            "budget_limit": budget_limit,
            "run_analysis": run_analysis
        }
    
    async def run_analysis_with_progress(self, company_name: str, config: Dict, form_data: Dict, progress_bar, status_text):
        """Run analysis with engaging financial facts and background rotation"""
        try:
            # Create the analysis request object
            request = AnalysisRequest(
                company_name=company_name,
                analysis_type=config["analysis_type"],
                include_tools=config["include_tools"],
                use_advanced_fallback=config["use_advanced_fallback"],
                max_fallbacks=config["max_fallbacks"],
                budget_limit=form_data["budget_limit"]
            )

            # Show the first financial fact
            initial_fact = get_random_fact()
            status_text.markdown(f"""
            <div class="financial-fact">
                <strong>💡 Investment Wisdom:</strong><br>
                {initial_fact}
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(10)
            await asyncio.sleep(0.5)

            # Start the analysis in background
            analysis_task = asyncio.create_task(self.system.analyze_company(request))

            # Rotate quotes independently while analysis is running
            async def rotate_quotes_while_loading():
                fact_count = 0
                while not analysis_task.done():
                    new_fact = get_random_fact()
                    status_text.markdown(f"""
                    <div class="financial-fact">
                        <strong>💡 Investment Wisdom:</strong><br>
                        {new_fact}
                    </div>
                    """, unsafe_allow_html=True)

                    # Progress bar simulated step
                    progress = min(10 + fact_count * 3, 90)
                    progress_bar.progress(progress)

                    fact_count += 1
                    await asyncio.sleep(3)  # Wait exactly 3 seconds before next fact

            # Start rotating quotes in parallel
            quote_task = asyncio.create_task(rotate_quotes_while_loading())

            # Wait for analysis to finish
            result = await analysis_task

            # Ensure rotation stops
            quote_task.cancel()

            # Final quote and progress
            final_fact = get_random_fact()
            status_text.markdown(f"""
            <div class="financial-fact">
                <strong>🎉 Analysis Complete!</strong><br>
                Your comprehensive report is ready below.<br><br>
                <strong>💡 Final Wisdom:</strong><br>
                {final_fact}
            </div>
            """, unsafe_allow_html=True)
            progress_bar.progress(100)
            await asyncio.sleep(0.5)

            return result

        except Exception as e:
            raise e
    
    def render_analysis_results(self, result):
        """Render analysis results"""
        if not result:
            return
        
        st.markdown("## 📊 Analysis Results")
        
        # Status and metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_color = "🟢" if result.status == "success" else "🔴"
            st.metric("Status", f"{status_color} {result.status.title()}")
        
        with col2:
            st.metric("Execution Time", f"{result.execution_time:.2f}s")
        
        with col3:
            st.metric("Confidence Score", f"{result.confidence_score:.2f}")
        
        # Analysis content - only show if successful
        if result.status == "success" and result.content:
            self.render_analysis_content(result.content)
        elif result.status == "error":
            st.info("Analysis completed with errors. Please check the error message above.")
    
    def render_analysis_content(self, content):
        """Render the analysis content"""
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Summary", "📊 Details", "🎯 Insights", "📈 Metrics"])
        
        with tab1:
            self.render_summary_tab(content)
            
        with tab2:
            self.render_details_tab(content)
            
        with tab3:
            self.render_insights_tab(content)
            
        with tab4:
            self.render_metrics_tab(content)
    
    def render_summary_tab(self, content):
        """Render summary tab"""
        st.markdown("### 📋 Analysis Summary")
        
        if isinstance(content, dict):
            # Display key information
            if "company_name" in content:
                st.info(f"**Company Analyzed:** {content['company_name']}")
            
            if "analysis_type" in content:
                st.info(f"**Analysis Type:** {content['analysis_type'].title()}")
            
            # Display main content based on analysis type
            if "full_result" in content:
                # Full analysis from CrewAI - this contains the final rewritten thesis after critique
                st.markdown("### 🎯 Final Investment Thesis (After Critique & Rewrite)")
                st.markdown("**This is the final, improved investment thesis that incorporates all critic recommendations:**")
                st.markdown(content["full_result"])
                
                # Show the workflow steps
                st.markdown("---")
                st.markdown("### 🔄 Analysis Workflow")
                
                # Original thesis
                if "original_thesis" in content:
                    with st.expander("📝 Original Thesis (Before Critique)"):
                        st.markdown(content["original_thesis"])
                
                # Critic's recommendations
                if "critique" in content:
                    with st.expander("🔍 Critic's Recommendations"):
                        st.markdown(content["critique"])
                
                # Individual agent results
                if "research" in content:
                    with st.expander("🔍 Research Analysis"):
                        st.markdown(content["research"])
                
                if "sentiment" in content:
                    with st.expander("🧠 Sentiment Analysis"):
                        st.markdown(content["sentiment"])
                
                if "valuation" in content:
                    with st.expander("💰 Valuation Analysis"):
                        st.markdown(content["valuation"])
                        
            elif "content" in content:
                # Single analysis type
                st.markdown("### 📝 Analysis Content")
                st.markdown(content["content"])
            
            # Display models used
            if "models_used" in content:
                st.markdown("### 🤖 Models Used")
                for model in content["models_used"]:
                    st.write(f"• {model}")
        else:
            # If content is a string, display it directly
            st.markdown("### 📝 Analysis Content")
            st.markdown(str(content))
    
    def render_details_tab(self, content):
        """Render details tab"""
        st.markdown("### 📊 Detailed Analysis")
        
        if isinstance(content, dict):
            if "full_result" in content:
                # Full analysis from CrewAI - show the individual components instead of repeating final thesis
                st.markdown("### 🔄 Analysis Workflow Components")
                st.info("**Note:** The final investment thesis is shown in the Summary tab above. Here are the individual analysis components:")
                
                # Show the analysis workflow
                st.markdown("---")
                st.markdown("### 🔄 Complete Analysis Workflow")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if "research" in content:
                        st.markdown("#### 🔍 Research Agent")
                        st.markdown(content["research"])
                    
                    if "sentiment" in content:
                        st.markdown("#### 🧠 Sentiment Agent")
                        st.markdown(content["sentiment"])
                
                with col2:
                    if "valuation" in content:
                        st.markdown("#### 💰 Valuation Agent")
                        st.markdown(content["valuation"])
                    
                    if "original_thesis" in content:
                        st.markdown("#### 📝 Original Thesis")
                        st.markdown(content["original_thesis"])
                
                if "critique" in content:
                    st.markdown("#### 🔍 Critic Agent - Recommendations")
                    st.markdown(content["critique"])
                
                if "final_thesis" in content:
                    st.markdown("#### ✅ Final Thesis (After Improvements)")
                    st.markdown(content["final_thesis"])
                    
            elif "content" in content:
                # Single analysis type
                st.markdown(content["content"])
            else:
                # Display all content sections
                for key, value in content.items():
                    if key not in ["company_name", "analysis_type", "models_used", "fallback_count", "confidence_score", "execution_time", "cost_estimate"]:
                        if isinstance(value, str) and value.strip():
                            st.markdown(f"#### {key.title()}")
                            st.markdown(value)
        else:
            st.markdown(str(content))
    
    def render_insights_tab(self, content):
        """Render insights tab"""
        st.markdown("### 🎯 Key Insights")
        
        # Extract insights from content
        insights = []
        
        if isinstance(content, dict):
            # Look for content in different possible locations
            content_text = ""
            
            if "full_result" in content:
                content_text = content["full_result"]
            elif "content" in content:
                content_text = content["content"]
            elif "research" in content:
                content_text = content["research"]
            
            if content_text:
                # Common insight patterns
                insight_patterns = [
                    "key insight",
                    "important finding",
                    "notable",
                    "significant",
                    "recommendation",
                    "conclusion",
                    "key takeaway",
                    "critical",
                    "essential",
                    "crucial"
                ]
                
                lines = content_text.split('\n')
                for line in lines:
                    line_lower = line.lower()
                    if any(pattern in line_lower for pattern in insight_patterns):
                        insights.append(line.strip())
        
        if insights:
            for insight in insights[:10]:  # Limit to 10 insights
                st.markdown(f"• {insight}")
        else:
            st.info("No specific insights extracted. Check the full analysis content in the Details tab.")
    
    def render_metrics_tab(self, content):
        """Render metrics tab"""
        st.markdown("### 📈 Performance Metrics")
        
        if isinstance(content, dict):
            # Display execution metrics
            col1, col2 = st.columns(2)
            
            with col1:
                if "execution_time" in content:
                    st.metric("Execution Time", f"{content['execution_time']:.2f}s")
                
                if "cost_estimate" in content:
                    st.metric("Cost Estimate", f"${content['cost_estimate']:.4f}")
            
            with col2:
                if "fallback_count" in content:
                    st.metric("Fallbacks Used", content["fallback_count"])
                
                if "confidence_score" in content:
                    st.metric("Confidence Score", f"{content['confidence_score']:.2f}")
            
            # Display model usage
            if "models_used" in content:
                st.markdown("#### 🤖 Model Usage")
                for model in content["models_used"]:
                    st.write(f"• {model}")
        
        # Create a simple performance chart
        if self.analysis_history:
            st.markdown("#### 📊 Analysis History")
            
            # Prepare data for chart
            history_data = []
            for analysis in self.analysis_history[-10:]:  # Last 10 analyses
                history_data.append({
                    "Company": analysis.request.company_name,
                    "Type": analysis.request.analysis_type,
                    "Time": analysis.execution_time,
                    "Confidence": analysis.confidence_score
                })
            
            if history_data:
                df = pd.DataFrame(history_data)
                
                # Create performance chart
                fig = go.Figure(data=go.Scatter(x=df.index, y=df['Time'], mode='lines+markers'))
                fig.update_layout(
                    title="Analysis Execution Times",
                    xaxis_title="Analysis #",
                    yaxis_title="Execution Time (seconds)"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def load_market_highlights(self):
        """Load market highlights once and cache them for 2 minutes"""
        # Check if cache is still valid (2 minutes)
        if (st.session_state.market_highlights_loaded and 
            st.session_state.market_highlights_data is not None and
            st.session_state.market_highlights_timestamp):
            
            cache_age = datetime.now() - st.session_state.market_highlights_timestamp
            if cache_age.total_seconds() < 120:  # 2 minutes cache
                return st.session_state.market_highlights_data
        
        try:
            with st.spinner("📊 Loading market highlights with optimized scanner..."):
                market_data = self.system.get_market_insights(days_back=3)  # Reduced to 3 days for speed
            
            if "error" not in market_data:
                st.session_state.market_highlights_data = market_data
                st.session_state.market_highlights_timestamp = datetime.now()
                st.session_state.market_highlights_loaded = True
                print("✅ Market highlights loaded and cached (2 min)")
            else:
                print(f"❌ Market highlights error: {market_data['error']}")
                return None
        except Exception as e:
            print(f"❌ Could not load market highlights: {e}")
            return None
        
        return st.session_state.market_highlights_data
    
    def render_market_discovery_section(self):
        """Render the optimized market discovery section with top 3 performers and sectors"""
        st.markdown("## 📈 Market Highlights")
        
        # Load market highlights (cached)
        market_data = self.load_market_highlights()
        
        if market_data is None:
            st.error("❌ Could not load market highlights")
            return
        
        # Show cache status and performance info
        if st.session_state.market_highlights_timestamp:
            cache_age = datetime.now() - st.session_state.market_highlights_timestamp
            st.caption(f"📊 Data loaded: {cache_age.seconds} seconds ago | ⚡ Optimized for speed | 🚀 ~32s scan time | 📈 Real NSE indices")
        
        # Add refresh button with better styling
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Refresh", help="Update market highlights with latest data", type="primary"):
                st.session_state.market_highlights_loaded = False
                st.session_state.market_highlights_data = None
                st.rerun()
        
        with col2:
            st.caption("💡 Click refresh to get the latest market data using our advanced scanner with real NSE sectoral indices")
        
        # Top performing discovered stocks
        top_stocks = market_data.get('top_performing_stocks', [])
        
        if top_stocks:
            st.markdown("### 🥇 Top 3 Discovered Performers")
            
            # Create a more attractive layout for stocks
            cols = st.columns(3)
            
            for i, stock in enumerate(top_stocks[:3]):
                with cols[i]:
                    direction = "📈" if stock['price_change_pct'] > 0 else "📉"
                    stock_symbol = stock['symbol'].replace('.NS', '').replace('.BO', '')
                    
                    # Improved color coding with better contrast
                    if stock['price_change_pct'] > 0:
                        color = "#28a745"  # Green
                        bg_color = "#1a1a1a"  # Dark background for black theme
                        border_color = "#28a745"  # Green border
                    else:
                        color = "#dc3545"  # Red
                        bg_color = "#1a1a1a"  # Dark background for black theme
                        border_color = "#dc3545"  # Red border
                    
                    # Always use rupees for Indian stocks
                    price_symbol = "₹"
                    
                    # Better category display - show source type instead of "Unknown"
                    category = "Today's Gainer" if stock['price_change_pct'] > 0 else "Today's Loser"
                    
                    st.markdown(f"""
                        <div style="padding: 1rem; border: 2px solid {border_color}; border-radius: 15px; text-align: center; background-color: {bg_color}; margin: 5px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                            <h3 style="margin: 0; color: {color}; font-size: 1.3rem; font-weight: bold; text-align: center;">{stock_symbol}</h3>
                            <p style="font-weight: bold; margin: 6px 0; color: #ffffff; font-size: 0.9rem; text-align: center;">{stock['name']}</p>
                            <p style="font-size: 1.5rem; font-weight: bold; color: {color}; margin: 8px 0; text-align: center;">
                                {direction} {stock['price_change_pct']:+.2f}%
                            </p>
                            <p style="font-size: 1rem; margin: 6px 0; color: #ffffff; font-weight: 600; text-align: center;">{price_symbol}{stock['current_price']:,.2f}</p>
                            <p style="font-size: 0.8rem; color: #cccccc; margin: 6px 0; font-weight: 500; text-align: center;">{category}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No stocks discovered. This might be due to:")
            st.markdown("""
            - **Market scanner optimization in progress**
            - **Network connectivity issues**
            - **API rate limits**
            
            Try clicking **🔄 Refresh** to retry the discovery process.
            """)
        
        # Top performing discovered sectors
        top_sectors = market_data.get('top_performing_sectors', [])
        if top_sectors:
            st.markdown("### 🏆 Top Performing NSE Sectoral Indices")
            
            # Create sector cards similar to stocks
            sector_cols = st.columns(3)
            
            for i, sector in enumerate(top_sectors[:3]):
                with sector_cols[i]:
                    direction = "📈" if sector['price_change_pct'] > 0 else "📉"
                    sector_name = sector['name'].replace(' Sector', '').replace(' Index', '').replace(' (Overall Market)', '')
                    
                    # Improved color coding with better contrast
                    if sector['price_change_pct'] > 0:
                        color = "#28a745"  # Green
                        bg_color = "#1a1a1a"  # Dark background for black theme
                        border_color = "#28a745"  # Green border
                    else:
                        color = "#dc3545"  # Red
                        bg_color = "#1a1a1a"  # Dark background for black theme
                        border_color = "#dc3545"  # Red border
                    
                    # Better volatility display - show market status instead of 0.00%
                    volatility = sector.get('volatility', 0)
                    if volatility is None or pd.isna(volatility) or volatility == 0:
                        volatility_text = "Live Market Data"
                    else:
                        volatility_text = f"Volatility: {volatility:.2f}%"
                    
                    st.markdown(f"""
                        <div style="padding: 1rem; border: 2px solid {border_color}; border-radius: 15px; text-align: center; background-color: {bg_color}; margin: 5px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                            <h3 style="margin: 0; color: {color}; font-size: 1.3rem; font-weight: bold; text-align: center;">{sector_name}</h3>
                            <p style="font-size: 1.5rem; font-weight: bold; color: {color}; margin: 8px 0; text-align: center;">
                                {direction} {sector['price_change_pct']:+.2f}%
                            </p>
                            <p style="font-size: 1rem; margin: 6px 0; color: #ffffff; font-weight: 600; text-align: center;">₹{sector['current_price']:,.2f}</p>
                            <p style="font-size: 0.8rem; color: #cccccc; margin: 6px 0; font-weight: 500; text-align: center;">{volatility_text}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Add sector performance chart
            if len(top_sectors) > 1:
                st.markdown("#### 📊 NSE Sectoral Indices Performance Chart")
                sector_data = []
                for sector in top_sectors[:5]:
                    sector_data.append({
                        "Sector": sector['name'].replace(' Sector', '').replace(' Index', '').replace(' (Overall Market)', ''),
                        "Performance": sector['price_change_pct'],
                        "Volatility": sector.get('volatility', 0)
                    })
                
                if sector_data:
                    df_sectors = pd.DataFrame(sector_data)
                    
                    # Create bar chart with dark theme styling
                    fig = go.Figure(data=go.Bar(
                        x=df_sectors['Sector'], 
                        y=df_sectors['Performance'], 
                        marker_color=df_sectors['Performance'].apply(lambda x: '#28a745' if x > 0 else '#dc3545'),
                        text=df_sectors['Performance'].apply(lambda x: f'{x:+.2f}%'),
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title={
                            'text': "NSE Sectoral Indices Performance Overview",
                            'font': {'color': '#ffffff', 'size': 16}
                        },
                        xaxis_title="Sector",
                        yaxis_title="Performance (%)",
                        height=400,
                        showlegend=False,
                        plot_bgcolor='#1a1a1a',  # Dark background matching cards
                        paper_bgcolor='#000000',  # Pitch black background
                        font={'color': '#ffffff'},  # White text
                        xaxis={
                            'gridcolor': '#333333',
                            'tickfont': {'color': '#ffffff'}
                        },
                        yaxis={
                            'gridcolor': '#333333',
                            'tickfont': {'color': '#ffffff'}
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No sectors discovered. This might be due to:")
            st.markdown("""
            - **Market scanner optimization in progress**
            - **Network connectivity issues**
            - **API rate limits**
            
            Try clicking **🔄 Refresh** to retry the discovery process.
            """)
        
        # Add market insights if available
        market_insights = market_data.get('market_insights', {})
        if market_insights:
            st.markdown("### 💡 Market Insights")
            
            # Display insights in a nice format
            col1, col2 = st.columns(2)
            
            with col1:
                sentiment = market_insights.get('market_sentiment', 'neutral')
                sentiment_emoji = {"bullish": "📈", "bearish": "📉", "neutral": "➡️"}.get(sentiment, "➡️")
                st.metric("Market Sentiment", f"{sentiment_emoji} {sentiment.title()}")
            
            with col2:
                risk_level = market_insights.get('risk_level', 'medium')
                risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(risk_level, "🟡")
                st.metric("Risk Level", f"{risk_emoji} {risk_level.title()}")
            
            # Show key observations
            key_observations = market_insights.get('key_observations', [])
            if key_observations:
                st.markdown("#### 🔍 Key Observations")
                for observation in key_observations[:3]:  # Show top 3
                    st.markdown(f"• {observation}")
        
        # Add a separator before the analysis form
        st.markdown("---")
    
    def render_history(self):
        """Render analysis history"""
        if not self.system:
            return
        
        st.markdown("## 📚 Analysis History")
        
        # Add controls for history management
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            history_limit = st.selectbox(
                "Show last N analyses:",
                [10, 25, 50, 100],
                index=0,
                help="Number of recent analyses to display"
            )
        
        with col2:
            if st.button("🔄 Refresh History"):
                # Just show a success message - the history will be refreshed on the next render
                st.success("✅ History refreshed!")
        
        with col3:
            if st.button("🗑️ Clear History"):
                self.system.clear_history()
                st.success("🗑️ History cleared!")
        
        try:
            history = self.system.get_analysis_history(limit=history_limit)
            
            if history:
                # Add a summary
                st.info(f"📊 Showing {len(history)} most recent analyses")
                
                # Add search functionality
                search_term = st.text_input(
                    "🔍 Search by company name:",
                    placeholder="Enter company name to filter...",
                    help="Filter analyses by company name"
                )
                
                # Filter history based on search
                if search_term:
                    filtered_history = [h for h in history if search_term.lower() in h['company_name'].lower()]
                    st.info(f"🔍 Found {len(filtered_history)} analyses for '{search_term}'")
                else:
                    filtered_history = history
                
                # Display as a table with better formatting
                st.dataframe(
                    filtered_history,
                    column_config={
                        "company_name": st.column_config.TextColumn(
                            "Company",
                            width="medium"
                        ),
                        "analysis_type": st.column_config.SelectboxColumn(
                            "Type",
                            width="small",
                            options=["full", "research", "sentiment", "valuation", "thesis"]
                        ),
                        "status": st.column_config.TextColumn(
                            "Status",
                            width="small"
                        ),
                        "execution_time": st.column_config.NumberColumn(
                            "Time (s)",
                            format="%.2f",
                            width="small"
                        ),
                        "confidence_score": st.column_config.NumberColumn(
                            "Confidence",
                            format="%.2f",
                            width="small"
                        ),
                        "timestamp": st.column_config.DatetimeColumn(
                            "Timestamp",
                            format="DD/MM/YYYY HH:mm",
                            width="medium"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Add detailed view section
                st.markdown("### 📋 Detailed Analysis View")
                
                # Create tabs for different viewing options
                tab1, tab2 = st.tabs(["🎯 View by Analysis", "🏢 View by Company"])
                
                with tab1:
                    # Select analysis to view
                    if filtered_history:
                        analysis_options = [f"{h['company_name']} - {h['analysis_type']} ({h['timestamp'][:10]})" for h in filtered_history]
                        selected_analysis = st.selectbox(
                            "Select analysis to view details:",
                            analysis_options,
                            help="Choose an analysis to view its complete results"
                        )
                        
                        if selected_analysis:
                            # Find the selected analysis
                            selected_index = analysis_options.index(selected_analysis)
                            selected_history_item = filtered_history[selected_index]
                            
                            # Get the full analysis details using the actual analysis ID
                            # We need to find the actual ID in the full history
                            full_history = self.system.get_analysis_history(limit=1000)  # Get all history
                            actual_analysis_id = None
                            
                            # Find the matching analysis in full history
                            for i, full_item in enumerate(full_history):
                                if (full_item['company_name'] == selected_history_item['company_name'] and
                                    full_item['analysis_type'] == selected_history_item['analysis_type'] and
                                    full_item['timestamp'] == selected_history_item['timestamp']):
                                    actual_analysis_id = i
                                    break
                            
                            if actual_analysis_id is not None:
                                full_analysis = self.system.get_analysis_by_id(actual_analysis_id)
                                
                                if full_analysis:
                                    st.success(f"📋 Showing complete analysis for {full_analysis['company_name']}")
                                    self.render_analysis_details(full_analysis)
                                else:
                                    st.warning("⚠️ Could not retrieve full analysis details")
                            else:
                                st.warning("⚠️ Could not find the selected analysis in full history")
                
                with tab2:
                    # Company search and view
                    company_search = st.text_input(
                        "🏢 Enter company name:",
                        placeholder="e.g., Apple Inc., Tesla",
                        help="View all analyses for a specific company"
                    )
                    
                    if company_search:
                        company_analyses = self.system.get_analysis_by_company(company_search)
                        
                        if company_analyses:
                            st.success(f"📊 Found {len(company_analyses)} analyses for {company_search}")
                            
                            # Display company analyses
                            for analysis in company_analyses:
                                with st.expander(f"📋 {analysis['analysis_type'].title()} Analysis - {analysis['timestamp'][:10]}"):
                                    self.render_analysis_details(analysis)
                        else:
                            st.info(f"📝 No analyses found for '{company_search}'")
                
                # Add some statistics
                st.markdown("### 📈 History Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    successful = len([h for h in history if h['status'] == 'success'])
                    st.metric("Successful", successful)
                    
                with col2:
                    avg_time = sum(h['execution_time'] for h in history) / len(history) if history else 0
                    st.metric("Avg Time", f"{avg_time:.1f}s")
                
                with col3:
                    avg_confidence = sum(h['confidence_score'] for h in history) / len(history) if history else 0
                    st.metric("Avg Confidence", f"{avg_confidence:.2f}")
                
                with col4:
                    unique_companies = len(set(h['company_name'] for h in history))
                    st.metric("Companies", unique_companies)
            else:
                st.info("No analysis history available yet. Run your first analysis to see history here!")
                
        except Exception as e:
            st.error(f"Could not load history: {e}")
            st.info("Try refreshing the page or running a new analysis.")
    
    def render_analysis_details(self, analysis: Dict[str, Any]):
        """Render detailed analysis results"""
        st.markdown(f"#### 📊 Analysis Details for {analysis['company_name']}")
        
        # Debug information (can be removed later)
        if st.checkbox("🔧 Show Debug Info", help="Show debug information about the analysis"):
            st.json(analysis)
        
        # Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Company:** {analysis['company_name']}")
            st.info(f"**Type:** {analysis['analysis_type'].title()}")
                
        with col2:
            st.info(f"**Status:** {analysis['status'].title()}")
            st.info(f"**Execution Time:** {analysis['execution_time']:.2f}s")
                
        with col3:
            st.info(f"**Confidence:** {analysis['confidence_score']:.2f}")
            st.info(f"**Date:** {analysis['timestamp'][:10]}")
        
        # Models used
        if analysis.get('models_used'):
            st.markdown("**🤖 Models Used:**")
            for model in analysis['models_used']:
                st.write(f"• {model}")
        
        # Analysis content
        if analysis.get('content'):
            st.markdown("#### 📝 Analysis Content")
            
            # Show content structure info
            content = analysis['content']
            if isinstance(content, dict):
                st.info(f"📋 Content sections available: {list(content.keys())}")
            
            # Create tabs for different content sections
            if isinstance(content, dict):
                if "full_result" in content:
                    # Full analysis from CrewAI
                    st.markdown("##### 🎯 Final Investment Thesis")
                    st.markdown(content["full_result"])
                    
                    # Show individual components in expanders
                    if "original_thesis" in content:
                        with st.expander("📝 Original Thesis"):
                            st.markdown(content["original_thesis"])
                    
                    if "critique" in content:
                        with st.expander("🔍 Critic's Recommendations"):
                            st.markdown(content["critique"])
                    
                    if "research" in content:
                        with st.expander("🔍 Research Analysis"):
                            st.markdown(content["research"])
                    
                    if "sentiment" in content:
                        with st.expander("🧠 Sentiment Analysis"):
                            st.markdown(content["sentiment"])
                    
                    if "valuation" in content:
                        with st.expander("💰 Valuation Analysis"):
                            st.markdown(content["valuation"])
                
                elif "content" in content:
                    # Single analysis type
                    st.markdown(content["content"])
                else:
                    # Display all content sections
                    for key, value in content.items():
                        if isinstance(value, str) and value.strip():
                            with st.expander(f"📋 {key.title()}"):
                                st.markdown(value)
            else:
                # If content is a string
                st.markdown(str(content))
        else:
            st.warning("⚠️ No analysis content available")
        
        # Metadata
        if analysis.get('metadata'):
            with st.expander("🔧 Analysis Metadata"):
                st.json(analysis['metadata'])
    
    def render_system_status(self):
        """Render system status"""
        if not self.system:
            return
        
        st.markdown("## 🔧 System Status")
        
        try:
            status = self.system.get_system_status()
            
            # System status
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🚀 System Information")
                st.info(f"**Status:** {status['system_status']}")
                st.info(f"**CrewAI Available:** {status['crewai_available']}")
                st.info(f"**Tools Available:** {status['tools_available']}")
                st.info(f"**History Count:** {status['analysis_history_count']}")
                
            with col2:
                st.markdown("### 📊 Performance Metrics")
                st.info(f"**Total Analyses:** {status['metrics']['total_analyses']}")
                st.info(f"**Successful:** {status['metrics']['successful_analyses']}")
                st.info(f"**Failed:** {status['metrics']['failed_analyses']}")
                st.info(f"**Avg Time:** {status['metrics']['average_execution_time']:.2f}s")
            
            # Model usage
            st.markdown("### 🤖 Model Usage")
            if status['metrics']['model_usage']:
                model_df = pd.DataFrame([
                    {"Model": model, "Usage": count}
                    for model, count in status['metrics']['model_usage'].items()
                ])
                st.bar_chart(model_df.set_index("Model"))
            else:
                st.info("No model usage data available")
            
        except Exception as e:
            st.warning(f"Could not load system status: {e}")
    
    def render_market_overview(self):
        """Render the full dynamic market overview tab"""
        st.markdown("## 📈 Dynamic Market Overview")
        
        # Add refresh button for market data
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info("🔍 Dynamically discovering trending stocks and sectors...")
                        
        with col2:
            if st.button("🔄 Refresh Market Data", help="Update dynamic market data"):
                st.session_state.market_highlights_loaded = False
                st.session_state.market_highlights_data = None
                st.rerun()
        
        # Get market insights (use cached data if available, otherwise load fresh)
        if self.system:
            try:
                # Use cached data if available, otherwise load fresh
                if st.session_state.market_highlights_loaded and st.session_state.market_highlights_data:
                    market_data = st.session_state.market_highlights_data
                    st.info("📊 Using cached market data (click refresh to update)")
                else:
                    with st.spinner("📊 Dynamically discovering market data..."):
                        market_data = self.system.get_market_insights(days_back=5)
                
                if "error" in market_data:
                    st.error(f"❌ Market data error: {market_data['error']}")
                    return
                
                # Display market summary
                st.markdown("### 📊 Dynamic Market Discovery Summary")
                st.info(f"**Scan Date:** {market_data.get('scan_date', 'Unknown')}")
                st.info(f"**Days Analyzed:** {market_data.get('days_analyzed', 5)}")
                st.info(f"**Discovery Method:** {market_data.get('discovery_method', 'Dynamic Scanner')}")
                
                # Discovery statistics
                discovery_stats = market_data.get('discovery_stats', {})
                if discovery_stats:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Stocks Analyzed", discovery_stats.get('stocks_analyzed', 0))
                    
                    with col2:
                        st.metric("Sectors Analyzed", discovery_stats.get('sectors_analyzed', 0))
                    
                    with col3:
                        st.metric("Indices Analyzed", discovery_stats.get('indices_analyzed', 0))
                
                # Market insights
                insights = market_data.get('market_insights', {})
                if insights:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        sentiment = insights.get('market_sentiment', 'neutral')
                        sentiment_emoji = "📈" if sentiment == 'bullish' else "📉" if sentiment == 'bearish' else "➡️"
                        st.metric("Market Sentiment", f"{sentiment_emoji} {sentiment.title()}")
                    
                    with col2:
                        risk_level = insights.get('risk_level', 'medium')
                        risk_emoji = "🟢" if risk_level == 'low' else "🟡" if risk_level == 'medium' else "🔴"
                        st.metric("Risk Level", f"{risk_emoji} {risk_level.title()}")
                    
                    with col3:
                        trending_sectors = insights.get('trending_sectors', [])
                        st.metric("Trending Sectors", len(trending_sectors))
                
                # Top performing discovered stocks
                top_stocks = market_data.get('top_performing_stocks', [])
                if top_stocks:
                    st.markdown("### 🏆 Top Performing Discovered Stocks")
                    
                    # Create a dataframe for better display
                    stock_data = []
                    for stock in top_stocks[:10]:
                        stock_symbol = stock['symbol'].replace('.NS', '')  # Remove .NS suffix
                        stock_data.append({
                            "Symbol": stock_symbol,
                            "Name": stock['name'][:30] + "..." if len(stock['name']) > 30 else stock['name'],
                            "Sector": stock['sector'],
                            "Price": f"₹{stock['current_price']}",  # Always use rupees
                            "Change": f"{stock['price_change_pct']:+.2f}%",
                            "Volatility": f"{stock['volatility']:.1f}%",
                            "Score": f"{stock['performance_score']:.1f}"
                        })
                    
                    if stock_data:
                        df_stocks = pd.DataFrame(stock_data)
                        
                        # Color code the change column
                        def color_change(val):
                            if '+' in val:
                                return 'color: green'
                            elif '-' in val:
                                return 'color: red'
                            return ''
                        
                        styled_df = df_stocks.style.applymap(color_change, subset=['Change'])
                        st.dataframe(styled_df, use_container_width=True, hide_index=True)
                        
                        # Show top 3 stocks in cards
                        st.markdown("### 🥇 Top 3 Discovered Performers")
                        cols = st.columns(3)
                        
                        for i, stock in enumerate(top_stocks[:3]):
                            with cols[i]:
                                direction = "📈" if stock['price_change_pct'] > 0 else "📉"
                                stock_symbol = stock['symbol'].replace('.NS', '')
                                st.markdown(f"""
                                <div style="padding: 1rem; border: 1px solid #333333; border-radius: 10px; text-align: center; background-color: #1a1a1a; color: #ffffff;">
                                    <h4 style="color: #ffffff;">{stock_symbol}</h4>
                                    <p style="color: #ffffff;"><strong>{stock['name']}</strong></p>
                                    <p style="font-size: 1.5rem; color: {'#28a745' if stock['price_change_pct'] > 0 else '#dc3545'};">
                                        {direction} {stock['price_change_pct']:+.2f}%
                                    </p>
                                    <p style="color: #ffffff;">₹{stock['current_price']}</p>
                                    <p style="color: #cccccc;"><small>{stock['sector']}</small></p>
                                </div>
                                """, unsafe_allow_html=True)
                
                # Top performing discovered sectors
                top_sectors = market_data.get('top_performing_sectors', [])
                if top_sectors:
                    st.markdown("### 🏆 Top Performing Discovered Sectors")
                    
                    # Create sector chart
                    sector_data = []
                    for sector in top_sectors[:5]:
                        sector_data.append({
                            "Sector": sector['name'],
                            "Performance": sector['price_change_pct'],
                            "Volatility": sector['volatility']
                        })
                    
                    if sector_data:
                        df_sectors = pd.DataFrame(sector_data)
                        
                        # Create bar chart
                        fig = go.Figure(data=go.Bar(x=df_sectors['Sector'], y=df_sectors['Performance'], marker_color=df_sectors['Performance']))
                        fig.update_layout(
                            title="Discovered Sector Performance (Last 5 Days)",
                            xaxis_title="Sector",
                            yaxis_title="Performance (%)",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display sector table
                        st.dataframe(df_sectors, use_container_width=True, hide_index=True)
                
                # Market insights
                if insights.get('key_observations'):
                    st.markdown("### 🔍 Key Market Observations")
                    for observation in insights['key_observations']:
                        st.info(f"• {observation}")
                
                # Market summary
                if market_data.get('market_summary'):
                    with st.expander("📋 Detailed Market Discovery Summary"):
                        st.markdown(market_data['market_summary'])
                
            except Exception as e:
                st.error(f"❌ Could not load dynamic market data: {e}")
                st.info("Please try refreshing the market data or check your internet connection.")
        else:
            st.warning("⚠️ System not available for market data")

    def run(self):
        """Main application runner"""
        # Render header
        self.render_header()
        
        # Render sidebar and get configuration
        config = self.render_sidebar()
        
        # Main content area
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Analysis", "📈 Markets", "📚 History", "🔧 Status", "ℹ️ About"])
        
        with tab1:
            # Render market discovery content at the top of analysis tab
            self.render_market_discovery_section()
            
            # Render analysis form
            form_data = self.render_analysis_form(config)
            
            # Handle analysis execution
            if form_data["run_analysis"] and form_data["company_name"]:
                company_name = form_data["company_name"].strip()
                
                if company_name:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Run async analysis with engaging progress
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        result = loop.run_until_complete(
                            self.run_analysis_with_progress(company_name, config, form_data, progress_bar, status_text)
                        )
                        
                        # Add to history
                        if result:
                            self.analysis_history.append(result)
                        
                        # Update metrics after analysis
                        self.update_metrics_after_analysis(result)
                        
                        progress_bar.progress(100)
                        status_text.text("🎉 Analysis complete! Results ready below.")
                        
                        # Clear any previous error messages
                        st.empty()
                        
                        # Render results
                        self.render_analysis_results(result)
                        
                    except Exception as e:
                        # Clear progress indicators
                        progress_bar.progress(0)
                        status_text.text("❌ Analysis failed")
                        
                        # Show error in a clean way
                        st.error(f"❌ Analysis failed: {str(e)}")
                        
                        # Don't show the error again in results
                        result = None
                    
                    finally:
                        # Clean up
                        if 'loop' in locals():
                            loop.close()
                else:
                    st.warning("⚠️ Please enter a company name")
        
        with tab2:
            self.render_market_overview()
        
        with tab3:
            self.render_history()
        
        with tab4:
            self.render_system_status()
        
        with tab5:
            self.render_about()

    def render_about(self):
        """Render about section"""
        st.markdown("## ℹ️ About IntelliVest AI")
        
        st.markdown("""
        ### 🚀 Advanced Investment Analysis System
        
        **IntelliVest AI** is a sophisticated agentic AI system that provides comprehensive investment analysis 
        using advanced AI models, real-time data, and parallel processing optimization.
        
        ### 🎯 Key Features
        
        - **🤖 Agentic AI Framework**: CrewAI with 5 specialized agents
        - **🧠 Advanced Fallback System**: Multi-LLM orchestration with intelligent routing
        - **⚡ Parallel Processing**: High-speed concurrent data gathering and analysis
        - **🛠️ Custom Tools**: 6 investment tools with real data access
        - **📊 Real-time Monitoring**: Comprehensive metrics and analytics
        - **🚀 Performance Optimized**: 3.3x faster execution with parallel processing
        
        ### 🏗️ System Architecture
        
        - **Primary Model**: Gemini 2.5 Flash
        - **Fallback Models**: Groq DeepSeek R1, Llama 3.3-70B, and more
        - **Parallel Workers**: Configurable concurrent processing
        - **Advanced Tools**: Web crawling, financial data, sentiment analysis
        
        ### 📈 Performance
        
        - **Speed Improvement**: 3.3x faster than traditional methods
        - **Success Rate**: 100% in production tests
        - **Confidence Score**: 0.82 average across all analysis types
        - **Execution Time**: ~39 seconds for comprehensive analyses
        
        ### 🔧 Technical Stack
        
        - **CrewAI**: Multi-agent orchestration
        - **LangChain**: Tool integration and LLM management
        - **Streamlit**: Web interface
        - **Parallel Processing**: ThreadPoolExecutor for high-speed operations
        - **Advanced Fallback**: Multi-LLM intelligent routing
        
        ---
        
        **🎉 IntelliVest AI - Transforming Investment Analysis with Advanced AI and Parallel Processing**
        """)

def main():
    """Main function to run the Streamlit app"""
    app = IntelliVestStreamlitApp()
    app.run()

if __name__ == "__main__":
    main() 