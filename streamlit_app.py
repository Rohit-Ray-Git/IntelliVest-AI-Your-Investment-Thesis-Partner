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
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our core systems
from production_integration import ProductionIntelliVestAI, AnalysisRequest, AnalysisResult
from tools.rag_system import RAGSystem
from llm.advanced_fallback_system import TaskType
from financial_facts import get_random_fact

# Import RAG system
from components.qa_interface import render_qa_tab

# Import reportlab for PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Import additional utilities
import re

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
        
        # Initialize RAG system
        try:
            self.rag_system = RAGSystem()
        except Exception as e:
            st.error(f"❌ RAG System initialization failed: {e}")
            self.rag_system = None
        
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
    
    def store_analysis_in_rag(self, result):
        """Store analysis results in RAG system for Q&A"""
        if not self.rag_system or not result:
            print("⚠️ RAG system or result not available")
            return False
        
        try:
            # Extract company name from result
            company_name = result.request.company_name
            print(f"📝 Storing analysis for {company_name} in RAG system...")
            
            # Prepare report content
            report_content = ""
            
            # Get the content
            content = result.content
            
            # Add content based on its structure
            if isinstance(content, dict):
                # Add summary
                if 'summary' in content:
                    report_content += f"SUMMARY:\n{content['summary']}\n\n"
                
                # Add detailed analysis
                if 'detailed_analysis' in content:
                    report_content += f"DETAILED ANALYSIS:\n{content['detailed_analysis']}\n\n"
                
                # Add investment thesis
                if 'investment_thesis' in content:
                    report_content += f"INVESTMENT THESIS:\n{content['investment_thesis']}\n\n"
                
                # Add insights
                if 'insights' in content:
                    report_content += f"KEY INSIGHTS:\n{content['insights']}\n\n"
                
                # Add metrics
                if 'metrics' in content:
                    report_content += f"FINANCIAL METRICS:\n{content['metrics']}\n\n"
                
                # Add full result if available
                if 'full_result' in content:
                    report_content += f"FULL ANALYSIS:\n{content['full_result']}\n\n"
                
                # Add individual components
                if 'research' in content:
                    report_content += f"RESEARCH ANALYSIS:\n{content['research']}\n\n"
                
                if 'sentiment' in content:
                    report_content += f"SENTIMENT ANALYSIS:\n{content['sentiment']}\n\n"
                
                if 'valuation' in content:
                    report_content += f"VALUATION ANALYSIS:\n{content['valuation']}\n\n"
                
                if 'critique' in content:
                    report_content += f"CRITIQUE:\n{content['critique']}\n\n"
                
                # Add any other content sections
                for key, value in content.items():
                    if key not in ['summary', 'detailed_analysis', 'investment_thesis', 'insights', 'metrics', 'full_result', 'research', 'sentiment', 'valuation', 'critique']:
                        if isinstance(value, str) and value.strip():
                            report_content += f"{key.upper()}:\n{value}\n\n"
            else:
                # If content is a string, use it directly
                report_content += f"ANALYSIS CONTENT:\n{content}\n\n"
            
            # Validate that we have meaningful content
            if not report_content.strip():
                print(f"⚠️ No meaningful content found for {company_name}")
                return False
            
            print(f"📝 Prepared {len(report_content)} characters of content for {company_name}")
            
            # Prepare metadata
            report_metadata = {
                'analysis_type': result.request.analysis_type,
                'timestamp': datetime.now().isoformat(),
                'execution_time': result.execution_time,
                'confidence_score': result.confidence_score,
                'status': result.status,
                'source': 'intellivest_ai',
                'company_name': company_name
            }
            
            # Store in RAG system
            report_id = self.rag_system.store_report(company_name, report_content, report_metadata)
            
            if report_id:
                print(f"✅ Successfully stored {company_name} in RAG system with ID: {report_id}")
                # Set current company in RAG system
                self.rag_system.current_company = company_name
                return True
            else:
                print(f"❌ Failed to store {company_name} in RAG system")
                return False
                
        except Exception as e:
            print(f"❌ Error storing analysis in RAG system: {e}")
            return False
            
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
        
        # Get company name
        company_name = result.request.company_name if hasattr(result.request, 'company_name') else "Unknown Company"
        
        # Display company name prominently at the top
        st.markdown(f"## **{company_name}**")
        st.markdown("---")
        
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
            
            # Add report download section
            self.render_report_download_section(result)
            
            # 🆕 IMMEDIATE RAG APPLICATION AND Q&A SUGGESTION
            self.render_immediate_rag_suggestion(result)
        elif result.status == "error":
            st.info("Analysis completed with errors. Please check the error message above.")
    
    def render_immediate_rag_suggestion(self, result):
        """Render immediate RAG application and Q&A suggestion after analysis"""
        if not result or result.status != "success":
            return
        
        st.markdown("---")
        st.markdown("## 🤖 AI-Powered Q&A System")
        
        # Check if RAG system is available
        if not self.rag_system:
            st.warning("⚠️ Q&A system is not available. Please check the system status.")
            return
        
        # Check if analysis was stored in RAG
        company_name = result.request.company_name
        
        # Try to store the analysis in RAG if not already done
        rag_stored = False
        if self.rag_system.current_company != company_name:
            with st.spinner("🤖 Storing analysis in Q&A system..."):
                rag_stored = self.store_analysis_in_rag(result)
        else:
            rag_stored = True
        
        if rag_stored:
            # Create a success message with Q&A suggestion
            st.success(f"""
            ✅ **Analysis Successfully Stored in Q&A System!**
            
            Your comprehensive analysis for **{company_name}** has been processed and is now available for interactive questioning.
            
            🎯 **What you can do now:**
            - Ask specific questions about {company_name}'s financial performance
            - Get detailed insights about risks and opportunities
            - Understand the investment thesis better
            - Explore competitive advantages and market position
            
            💡 **Navigate to the "Q&A" tab** to start asking questions about {company_name}!
            """)
            
            # Add a direct link to Q&A tab with better styling
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; margin: 1rem 0;">
                <h3>🚀 Ready to Explore Your Analysis?</h3>
                <p style="margin: 0.5rem 0;">Click the <strong>"Q&A"</strong> tab above to start asking questions about your analysis!</p>
                <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.9;">
                    💡 Try questions like: "What are the main risks?", "What's the growth outlook?", "How does it compare to competitors?"
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show some suggested questions
            if self.rag_system.current_company == company_name:
                suggested_questions = self.rag_system.get_suggested_questions()
                if suggested_questions:
                    st.markdown("### 💡 Suggested Questions to Ask:")
                    for i, question in enumerate(suggested_questions[:4]):
                        st.markdown(f"• **{question}**")
            
            # Add a quick Q&A preview
            st.markdown("### 🎯 Quick Q&A Preview")
            st.markdown("""
            Your analysis is now ready for interactive questioning. The AI system can answer questions about:
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                📊 **Financial Analysis**
                • Key metrics and ratios
                • Revenue and growth trends
                • Profitability analysis
                • Cash flow patterns
                """)
            
            with col2:
                st.markdown("""
                🎯 **Investment Insights**
                • Risk assessment
                • Competitive advantages
                • Market position
                • Growth opportunities
                """)
        else:
            st.warning(f"""
            ⚠️ **Analysis could not be stored in Q&A system**
            
            The analysis for {company_name} was completed successfully, but there was an issue storing it in the Q&A system.
            You can still view the analysis results above, but interactive Q&A features may not be available.
            
            💡 **Try refreshing the page or running the analysis again.**
            """)
    
    def render_report_download_section(self, result):
        """Render the report download section"""
        st.markdown("---")
        st.markdown("## 📥 Download Report")
        
        # Create download options - only PDF
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("📄 Download PDF Report", type="primary", use_container_width=True):
                self.download_pdf_report(result)
        
        # Add report customization options
        with st.expander("⚙️ Report Customization Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                include_metrics = st.checkbox("Include Performance Metrics", value=True)
                include_workflow = st.checkbox("Include Analysis Workflow", value=True)
            
            with col2:
                include_insights = st.checkbox("Include Key Insights", value=True)
                include_risks = st.checkbox("Include Risk Assessment", value=True)
            
            # Custom report generation
            if st.button("🔄 Generate Custom Report", type="secondary"):
                self.generate_custom_report(result, {
                    'include_metrics': include_metrics,
                    'include_workflow': include_workflow,
                    'include_insights': include_insights,
                    'include_risks': include_risks
                })
    
    def download_pdf_report(self, result):
        """Generate and download PDF report"""
        try:
            with st.spinner("📄 Generating PDF report..."):
                pdf_content = self.generate_pdf_content(result)
                
                # Create a temporary file
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='w') as tmp_file:
                    tmp_file.write(pdf_content)
                    tmp_file_path = tmp_file.name
                
                # Read the file and create download button
                with open(tmp_file_path, 'rb') as f:
                    pdf_bytes = f.read()
                
                # Clean up temporary file
                os.unlink(tmp_file_path)
                
                # Create download button
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"investment_analysis_{result.request.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                
                st.success("✅ PDF report generated successfully!")
                    
        except Exception as e:
            st.error(f"❌ Error generating PDF report: {e}")
    
    def generate_custom_report(self, result, options):
        """Generate a custom report based on user preferences"""
        try:
            with st.spinner("🔄 Generating custom report..."):
                custom_content = self.generate_custom_content(result, options)
                
                # Create download button
                st.download_button(
                    label="📥 Download Custom Report",
                    data=custom_content,
                    file_name=f"custom_analysis_{result.request.company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    type="primary"
                )
                
                st.success("✅ Custom report generated successfully!")
                
        except Exception as e:
            st.error(f"❌ Error generating custom report: {e}")
    
    def generate_pdf_content(self, result):
        """Generate PDF content for the report using reportlab with rich formatting"""
        try:
            from io import BytesIO
            
            # Create a buffer to store the PDF
            buffer = BytesIO()
            
            # Create the PDF document
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Create custom styles with rich formatting
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=20,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.darkblue,
                fontName='Helvetica-Bold',
                borderWidth=2,
                borderColor=colors.darkblue,
                borderPadding=10,
                backColor=colors.lightblue
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=15,
                spaceBefore=20,
                textColor=colors.darkblue,
                fontName='Helvetica-Bold',
                leftIndent=10,
                borderWidth=1,
                borderColor=colors.grey,
                borderPadding=5,
                backColor=colors.lightgrey
            )
            
            subheading_style = ParagraphStyle(
                'CustomSubHeading',
                parent=styles['Heading3'],
                fontSize=14,
                spaceAfter=10,
                spaceBefore=15,
                textColor=colors.darkgreen,
                fontName='Helvetica-Bold',
                leftIndent=15
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                leading=14,
                alignment=TA_JUSTIFY,
                fontName='Helvetica'
            )
            
            bullet_style = ParagraphStyle(
                'CustomBullet',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6,
                leading=14,
                alignment=TA_LEFT,
                fontName='Helvetica',
                leftIndent=20
            )
            
            highlight_style = ParagraphStyle(
                'CustomHighlight',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                leading=14,
                alignment=TA_LEFT,
                fontName='Helvetica-Bold',
                textColor=colors.darkred,
                backColor=colors.lightyellow,
                borderWidth=1,
                borderColor=colors.darkred,
                borderPadding=5
            )
            
            # Build the story (content)
            story = []
            
            # Title with rich formatting
            story.append(Paragraph("🚀 INTELLIVEST AI - INVESTMENT ANALYSIS REPORT", title_style))
            story.append(Spacer(1, 20))
            
            # Report metadata in a formatted table
            content = result.content
            company_name = result.request.company_name
            analysis_type = result.request.analysis_type
            execution_time = result.execution_time
            confidence_score = result.confidence_score
            
            metadata_data = [
                ['📊 Report Generated', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
                ['🏢 Company Analyzed', company_name],
                ['📈 Analysis Type', analysis_type.title()],
                ['⚡ Execution Time', f"{execution_time:.2f} seconds"],
                ['🎯 Confidence Score', f"{confidence_score:.2f}"],
                ['✅ Status', 'SUCCESS' if result.status == 'success' else 'ERROR']
            ]
            
            metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(metadata_table)
            story.append(Spacer(1, 25))
            
            # Executive Summary with rich formatting
            story.append(Paragraph("📋 EXECUTIVE SUMMARY", heading_style))
            story.append(Spacer(1, 15))
            
            if isinstance(content, dict):
                if "full_result" in content:
                    # Process the full result with better content parsing
                    story.extend(self._process_investment_thesis_content(content['full_result'], subheading_style, normal_style, bullet_style))
                    story.append(Spacer(1, 20))
                    
                    # Individual components with enhanced formatting
                    if "research" in content:
                        story.append(Paragraph("🔍 RESEARCH ANALYSIS", subheading_style))
                        story.extend(self._process_content_paragraphs(content['research'], normal_style, bullet_style))
                        story.append(Spacer(1, 15))
                    
                    if "sentiment" in content:
                        story.append(Paragraph("🧠 SENTIMENT ANALYSIS", subheading_style))
                        story.extend(self._process_content_paragraphs(content['sentiment'], normal_style, bullet_style))
                        story.append(Spacer(1, 15))
                    
                    if "valuation" in content:
                        story.append(Paragraph("💰 VALUATION ANALYSIS", subheading_style))
                        story.extend(self._process_content_paragraphs(content['valuation'], normal_style, bullet_style))
                        story.append(Spacer(1, 15))
                    
                    if "critique" in content:
                        story.append(Paragraph("🔍 CRITIC'S RECOMMENDATIONS", subheading_style))
                        story.extend(self._process_content_paragraphs(content['critique'], normal_style, bullet_style))
                        story.append(Spacer(1, 15))
                
                elif "content" in content:
                    story.append(Paragraph("📝 ANALYSIS CONTENT", subheading_style))
                    story.extend(self._process_content_paragraphs(content['content'], normal_style, bullet_style))
                    story.append(Spacer(1, 15))
                
                # Models used in a formatted table
                if "models_used" in content:
                    story.append(Paragraph("🤖 MODELS USED", subheading_style))
                    models_data = [[f"• {model}"] for model in content['models_used']]
                    models_table = Table(models_data, colWidths=[5*inch])
                    models_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgreen),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ]))
                    story.append(models_table)
                    story.append(Spacer(1, 15))
            
                else:
                    story.append(Paragraph("📝 ANALYSIS CONTENT", subheading_style))
                    story.extend(self._process_content_paragraphs(str(content), normal_style, bullet_style))
                    story.append(Spacer(1, 15))
            
            # Report metadata with enhanced formatting
            story.append(Paragraph("📊 REPORT METADATA", heading_style))
            
            metadata_detailed_data = [
                ['🔢 Analysis ID', str(id(result))],
                ['⏰ Timestamp', datetime.now().isoformat()],
                ['🔄 System Version', 'IntelliVest AI v2.0'],
                ['🤖 Generated By', 'Advanced AI-Powered Investment Analysis System']
            ]
            
            metadata_detailed_table = Table(metadata_detailed_data, colWidths=[2*inch, 3*inch])
            metadata_detailed_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            story.append(metadata_detailed_table)
            story.append(Spacer(1, 20))
            
            # Footer with enhanced formatting
            footer_text = """
            <para align="center">
            <b>This report was generated by IntelliVest AI, an advanced AI-powered investment analysis system.</b><br/>
            For questions or support, please contact the system administrator.<br/><br/>
            <i>© 2024 IntelliVest AI. All rights reserved.</i>
            </para>
            """
            story.append(Paragraph(footer_text, normal_style))
            
            # Build the PDF
            doc.build(story)
            
            # Get the PDF content
            pdf_content = buffer.getvalue()
            buffer.close()
            
            return pdf_content
            
        except Exception as e:
            # Fallback to simple text-based PDF
            return self.generate_simple_pdf_content(result)
    
    def _process_investment_thesis_content(self, content, subheading_style, normal_style, bullet_style):
        """Process investment thesis content with proper formatting"""
        story_elements = []
        
        # Split content into lines and process each line
        lines = content.split('\n')
        current_section = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for main section headers (numbered sections like "1. Executive Summary")
            if re.match(r'^\d+\.\s+[A-Z]', line):
                current_section = line
                story_elements.append(Paragraph(line, subheading_style))
                story_elements.append(Spacer(1, 10))
            
            # Check for subsection headers (like "Key Risk Factors:")
            elif re.match(r'^[A-Z][^:]*:$', line) or line.startswith('**') and line.endswith('**'):
                # Remove markdown formatting
                clean_line = line.replace('**', '').replace('*', '')
                story_elements.append(Paragraph(clean_line, subheading_style))
                story_elements.append(Spacer(1, 8))
            
            # Check for bullet points
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                story_elements.append(Paragraph(line, bullet_style))
                story_elements.append(Spacer(1, 4))
            
            # Check for numbered lists
            elif re.match(r'^\d+\.\s+', line):
                story_elements.append(Paragraph(line, bullet_style))
                story_elements.append(Spacer(1, 4))
            
            # Regular paragraph content
            else:
                # Handle bold text within paragraphs
                formatted_line = self._format_bold_text(line)
                story_elements.append(Paragraph(formatted_line, normal_style))
                story_elements.append(Spacer(1, 6))
        
        return story_elements
    
    def _process_content_paragraphs(self, content, normal_style, bullet_style):
        """Process regular content paragraphs"""
        story_elements = []
        
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Check if it's a bullet point
            if para.startswith('•') or para.startswith('-') or para.startswith('*'):
                story_elements.append(Paragraph(para, bullet_style))
                story_elements.append(Spacer(1, 4))
        else:
                # Handle bold text within paragraphs
                formatted_para = self._format_bold_text(para)
                story_elements.append(Paragraph(formatted_para, normal_style))
                story_elements.append(Spacer(1, 6))
        
        return story_elements
    
    def _format_bold_text(self, text):
        """Format bold text in paragraphs"""
        # Convert markdown bold to HTML bold
        text = text.replace('**', '<b>').replace('**', '</b>')
        text = text.replace('*', '<i>').replace('*', '</i>')
        return text
    
    def generate_simple_pdf_content(self, result):
        """Generate simple text-based PDF content as fallback"""
        content = self.generate_text_content(result)
        
        # Simple PDF-like formatting
        pdf_content = f"""
%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length {len(content)}
>>
stream
{content}
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
{len(content) + 300}
%%EOF
"""
        return pdf_content
    
    def generate_text_content(self, result):
        """Generate text content for the report with enhanced formatting"""
        try:
            content = result.content
            company_name = result.request.company_name
            analysis_type = result.request.analysis_type
            execution_time = result.execution_time
            confidence_score = result.confidence_score
            
            report_text = f"""
{'='*100}
                    🚀 INTELLIVEST AI - INVESTMENT ANALYSIS REPORT
{'='*100}

📊 REPORT METADATA
{'-'*50}
📅 Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
🏢 Company Analyzed: {company_name}
📈 Analysis Type: {analysis_type.title()}
⚡ Execution Time: {execution_time:.2f} seconds
🎯 Confidence Score: {confidence_score:.2f}
✅ Status: {'SUCCESS' if result.status == 'success' else 'ERROR'}

{'='*100}
                            📋 EXECUTIVE SUMMARY
{'='*100}

"""
            
            if isinstance(content, dict):
                if "full_result" in content:
                    report_text += f"""
🎯 FINAL INVESTMENT THESIS
{'-'*50}
{content['full_result']}

"""
                    # Add individual components if available
                    if "research" in content:
                        report_text += f"""
🔍 RESEARCH ANALYSIS
{'-'*50}
{content['research']}

"""
                    
                    if "sentiment" in content:
                        report_text += f"""
🧠 SENTIMENT ANALYSIS
{'-'*50}
{content['sentiment']}

"""
                    
                    if "valuation" in content:
                        report_text += f"""
💰 VALUATION ANALYSIS
{'-'*50}
{content['valuation']}

"""
                    
                    if "critique" in content:
                        report_text += f"""
🔍 CRITIC'S RECOMMENDATIONS
{'-'*50}
{content['critique']}

"""
                
                elif "content" in content:
                    report_text += f"""
📝 ANALYSIS CONTENT
{'-'*50}
{content['content']}

"""
                
                # Add models used if available
                if "models_used" in content:
                    report_text += f"""
🤖 MODELS USED
{'-'*50}
"""
                    for model in content['models_used']:
                        report_text += f"• {model}\n"
                    report_text += "\n"
            
            else:
                report_text += f"""
📝 ANALYSIS CONTENT
{'-'*50}
{str(content)}

"""
            
            report_text += f"""
{'='*100}
                            📊 REPORT METADATA
{'='*100}

🔢 Analysis ID: {id(result)}
⏰ Timestamp: {datetime.now().isoformat()}
🔄 System Version: IntelliVest AI v2.0
🤖 Generated By: Advanced AI-Powered Investment Analysis System

{'='*100}
                            📋 REPORT FOOTER
{'='*100}

This report was generated by IntelliVest AI, an advanced AI-powered investment analysis system.
For questions or support, please contact the system administrator.

© 2024 IntelliVest AI. All rights reserved.

{'='*100}
                            END OF REPORT
{'='*100}
"""
            
            return report_text
            
        except Exception as e:
            return f"Error generating text report: {e}"
    
    def generate_custom_content(self, result, options):
        """Generate custom content based on user preferences"""
        try:
            content = result.content
            company_name = result.request.company_name
            analysis_type = result.request.analysis_type
            
            custom_text = f"""
{'='*80}
                    INTELLIVEST AI - CUSTOM ANALYSIS REPORT
{'='*80}

Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
Company Analyzed: {company_name}
Analysis Type: {analysis_type.title()}

{'='*80}
                            CUSTOM REPORT
{'='*80}

"""
            
            if isinstance(content, dict):
                if "full_result" in content:
                    custom_text += f"""
FINAL INVESTMENT THESIS:
{content['full_result']}

"""
                
                # Include metrics if requested
                if options.get('include_metrics', True):
                    custom_text += f"""
PERFORMANCE METRICS:
- Execution Time: {result.execution_time:.2f} seconds
- Confidence Score: {result.confidence_score:.2f}
- Status: {result.status.title()}

"""
                
                # Include workflow if requested
                if options.get('include_workflow', True):
                    if "research" in content:
                        custom_text += f"""
RESEARCH ANALYSIS:
{content['research']}

"""
                    
                    if "sentiment" in content:
                        custom_text += f"""
SENTIMENT ANALYSIS:
{content['sentiment']}

"""
                    
                    if "valuation" in content:
                        custom_text += f"""
VALUATION ANALYSIS:
{content['valuation']}

"""
                
                # Include insights if requested
                if options.get('include_insights', True):
                    if "critique" in content:
                        custom_text += f"""
CRITIC'S INSIGHTS:
{content['critique']}

"""
                
                # Include risks if requested
                if options.get('include_risks', True):
                    custom_text += f"""
RISK ASSESSMENT:
This analysis includes comprehensive risk assessment as part of the investment thesis.
Please refer to the main thesis for detailed risk analysis and mitigation strategies.

"""
            
            custom_text += f"""
{'='*80}
                            CUSTOM REPORT END
{'='*80}

Report customized based on user preferences:
- Include Metrics: {options.get('include_metrics', True)}
- Include Workflow: {options.get('include_workflow', True)}
- Include Insights: {options.get('include_insights', True)}
- Include Risks: {options.get('include_risks', True)}

Generated by IntelliVest AI Custom Report Generator
"""
            
            return custom_text
            
        except Exception as e:
            return f"Error generating custom report: {e}"
    
    def download_pdf_report_from_history(self, analysis):
        """Download PDF report from historical analysis"""
        try:
            with st.spinner("📄 Generating PDF report from history..."):
                # Create a mock result object for the historical analysis
                class MockResult:
                    def __init__(self, analysis_data):
                        self.content = analysis_data.get('content', {})
                        self.request = type('obj', (object,), {
                            'company_name': analysis_data.get('company_name', 'Unknown'),
                            'analysis_type': analysis_data.get('analysis_type', 'full')
                        })
                        self.execution_time = analysis_data.get('execution_time', 0.0)
                        self.confidence_score = analysis_data.get('confidence_score', 0.0)
                        self.status = analysis_data.get('status', 'success')
                
                mock_result = MockResult(analysis)
                pdf_content = self.generate_pdf_content(mock_result)
                
                # Create download button
                st.download_button(
                    label="📄 Download Historical PDF Report",
                    data=pdf_content,
                    file_name=f"historical_analysis_{analysis.get('company_name', 'Unknown').replace(' ', '_')}_{analysis.get('timestamp', datetime.now().strftime('%Y%m%d_%H%M%S'))[:10]}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                
                st.success("✅ Historical PDF report generated successfully!")
                
        except Exception as e:
            st.error(f"❌ Error generating historical PDF report: {e}")
    
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
    
    def _llm_callback(self, prompt: str) -> str:
        """LLM callback for RAG system"""
        try:
            if self.system and hasattr(self.system, 'fallback_system'):
                # Use the fallback system for LLM calls - same as main analysis
                import asyncio
                
                # Create a new event loop if one doesn't exist
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Run the async method using the same system as main analysis
                result = loop.run_until_complete(
                    self.system.fallback_system.execute_with_fallback(
                        prompt, 
                        task_type=TaskType.GENERAL,  # Use general task type for Q&A
                        max_fallbacks=3
                    )
                )
                
                if result and hasattr(result, 'content'):
                    return result.content
                else:
                    return "I couldn't generate a response. Please try again."
            else:
                return "LLM system not available. Please check the system status."
        except Exception as e:
            print(f"❌ LLM callback error: {e}")
            return f"Error generating response: {str(e)}"
    
    def _web_search_callback(self, query: str) -> List[Dict[str, Any]]:
        """Web search callback for RAG system"""
        try:
            if self.system and hasattr(self.system, 'web_search'):
                return self.system.web_search(query)
            else:
                return []
        except Exception as e:
            return []
    
    def render_summary_tab(self, content):
        """Render summary tab - showing only the final report"""
        st.markdown("### 📋 Analysis Summary")
        
        if isinstance(content, dict):
            # Get company name
            company_name = content.get("company_name", "Unknown Company")
            
            # Display company name in bold at the top
            st.markdown(f"## **{company_name}**")
            st.markdown("---")
            
            # Display main content based on analysis type
            if "full_result" in content:
                # Full analysis from CrewAI - this contains the final rewritten thesis after critique
                st.markdown("### 🎯 Final Investment Thesis")
                st.markdown("**Complete analysis report after critique and rewrite:**")
                st.markdown(content["full_result"])
                
            elif "final_thesis" in content:
                # Alternative field name for final thesis
                st.markdown("### 🎯 Final Investment Thesis")
                st.markdown("**Complete analysis report:**")
                st.markdown(content["final_thesis"])
                
            elif "thesis" in content:
                # Fallback to thesis field
                st.markdown("### 🎯 Investment Thesis")
                st.markdown("**Complete analysis report:**")
                st.markdown(content["thesis"])
                
            else:
                # If no final thesis found, show the entire content
                st.markdown("### 📊 Complete Analysis Report")
                for key, value in content.items():
                    if isinstance(value, str) and value.strip():
                        if key not in ['company_name', 'analysis_type']:
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            st.markdown(value)
                            st.markdown("---")
                
        elif isinstance(content, str):
            # If content is a string, display it directly
            st.markdown("### 📊 Analysis Report")
            st.markdown(content)
            
        else:
            st.warning("⚠️ No analysis content available to display.")
    
    def render_details_tab(self, content):
        """Render details tab - showing only the final report details"""
        st.markdown("### 📊 Detailed Analysis")
        
        if isinstance(content, dict):
            if "full_result" in content:
                # Show only the final result with better formatting
                st.markdown("### 🎯 Complete Investment Analysis")
                st.markdown("**This is the comprehensive final analysis report:**")
                st.markdown(content["full_result"])
                
            elif "final_thesis" in content:
                # Alternative field name for final thesis
                st.markdown("### 🎯 Complete Investment Analysis")
                st.markdown("**This is the comprehensive final analysis report:**")
                st.markdown(content["final_thesis"])
                    
            elif "thesis" in content:
                # Fallback to thesis field
                st.markdown("### 🎯 Complete Investment Analysis")
                st.markdown("**This is the comprehensive final analysis report:**")
                st.markdown(content["thesis"])
                
            elif "content" in content:
                # Single analysis type
                st.markdown("### 📊 Analysis Content")
                st.markdown(content["content"])
            else:
                # Display all content sections (excluding metadata)
                for key, value in content.items():
                    if key not in ["company_name", "analysis_type", "models_used", "fallback_count", "confidence_score", "execution_time", "cost_estimate"]:
                        if isinstance(value, str) and value.strip():
                            st.markdown(f"#### {key.replace('_', ' ').title()}")
                            st.markdown(value)
                            st.markdown("---")
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
        
        # Professional header with gradient styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem; font-weight: 700;">
                📈 Market Highlights
            </h1>
            <p style="color: white; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                Real-time NSE market data and sectoral indices
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load market highlights (cached)
        market_data = self.load_market_highlights()
        
        if market_data is None:
            st.error("❌ Could not load market highlights")
            return
        
        # Enhanced status information with better alignment
        if st.session_state.market_highlights_timestamp:
            cache_age = datetime.now() - st.session_state.market_highlights_timestamp
            
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.05); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        border-left: 5px solid #17a2b8;
                        margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.1rem;">📊</span>
                        <span style="font-weight: 600; color: #495057;">Data loaded: {cache_age.seconds} seconds ago</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.1rem;">⚡</span>
                        <span style="font-weight: 600; color: #28a745;">Optimized for speed</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.1rem;">🚀</span>
                        <span style="font-weight: 600; color: #007bff;">~32s scan time</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.1rem;">📈</span>
                        <span style="font-weight: 600; color: #dc3545;">Real NSE indices</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Top performing discovered stocks
        top_stocks = market_data.get('top_performing_stocks', [])
        
        if top_stocks:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 2rem 0 1rem 0;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <h2 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 600; text-align: center;">
                    🥇 Top 3 Discovered Performers
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a more attractive layout for stocks with better alignment
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
                        <div style="padding: 1.5rem; border: 2px solid {border_color}; border-radius: 15px; text-align: center; background-color: {bg_color}; margin: 5px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.3); transition: transform 0.2s;">
                            <h3 style="margin: 0; color: {color}; font-size: 1.5rem; font-weight: bold; text-align: center;">{stock_symbol}</h3>
                            <p style="font-weight: bold; margin: 8px 0; color: #ffffff; font-size: 1rem; text-align: center; line-height: 1.4;">{stock['name']}</p>
                            <p style="font-size: 1.8rem; font-weight: bold; color: {color}; margin: 12px 0; text-align: center;">
                                {direction} {stock['price_change_pct']:+.2f}%
                            </p>
                            <p style="font-size: 1.2rem; margin: 8px 0; color: #ffffff; font-weight: 600; text-align: center;">{price_symbol}{stock['current_price']:,.2f}</p>
                            <p style="font-size: 0.9rem; color: #cccccc; margin: 8px 0; font-weight: 500; text-align: center;">{category}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No stocks discovered. This might be due to:")
            st.markdown("""
            - **Market scanner optimization in progress**
            - **Network connectivity issues**
            - **API rate limits**
            
            Try refreshing the page to retry the discovery process.
            """)
        
        # Top performing discovered sectors
        top_sectors = market_data.get('top_performing_sectors', [])
        if top_sectors:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 2rem 0 1rem 0;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <h2 style="color: white; margin: 0; font-size: 1.5rem; font-weight: 600; text-align: center;">
                    🏆 Top Performing NSE Sectoral Indices
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Create sector cards similar to stocks with better alignment
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
                        <div style="padding: 1.5rem; border: 2px solid {border_color}; border-radius: 15px; text-align: center; background-color: {bg_color}; margin: 5px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.3); transition: transform 0.2s;">
                            <h3 style="margin: 0; color: {color}; font-size: 1.5rem; font-weight: bold; text-align: center;">{sector_name}</h3>
                            <p style="font-size: 1.8rem; font-weight: bold; color: {color}; margin: 12px 0; text-align: center;">
                                {direction} {sector['price_change_pct']:+.2f}%
                            </p>
                            <p style="font-size: 1.2rem; margin: 8px 0; color: #ffffff; font-weight: 600; text-align: center;">₹{sector['current_price']:,.2f}</p>
                            <p style="font-size: 0.9rem; color: #cccccc; margin: 8px 0; font-weight: 500; text-align: center;">{volatility_text}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Add sector performance chart with enhanced styling
            if len(top_sectors) > 1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; 
                            border-radius: 12px; 
                            margin: 2rem 0 1rem 0;
                            box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                    <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                        📊 NSE Sectoral Indices Performance Chart
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
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
                            'font': {'color': '#ffffff', 'size': 18, 'weight': 'bold'},
                            'x': 0.5,
                            'xanchor': 'center'
                        },
                        xaxis_title="Sector",
                        yaxis_title="Performance (%)",
                        height=450,
                        showlegend=False,
                        plot_bgcolor='#1a1a1a',  # Dark background matching cards
                        paper_bgcolor='#000000',  # Pitch black background
                        font={'color': '#ffffff'},  # White text
                        xaxis={
                            'gridcolor': '#333333',
                            'tickfont': {'color': '#ffffff', 'size': 12},
                            'title': {'font': {'color': '#ffffff', 'size': 14, 'weight': 'bold'}}
                        },
                        yaxis={
                            'gridcolor': '#333333',
                            'tickfont': {'color': '#ffffff', 'size': 12},
                            'title': {'font': {'color': '#ffffff', 'size': 14, 'weight': 'bold'}}
                        },
                        margin=dict(l=60, r=60, t=80, b=60)
                    )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No sectors discovered. This might be due to:")
            st.markdown("""
            - **Market scanner optimization in progress**
            - **Network connectivity issues**
            - **API rate limits**
            
            Try refreshing the page to retry the discovery process.
            """)
        
        # Add a separator before the analysis form
        st.markdown("---")
    
    def render_history(self):
        """Render analysis history with professional styling"""
        if not self.system:
            return
        
        # Professional header with gradient styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem; font-weight: 700;">
                📚 Analysis History
            </h1>
            <p style="color: white; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                Comprehensive view of all your investment analyses
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced controls section with better styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                ⚙️ History Management
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced controls with better layout
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            history_limit = st.selectbox(
                "📊 Show last N analyses:",
                [10, 25, 50, 100],
                index=0,
                help="Number of recent analyses to display",
                key="history_limit_selector"
            )
        
        with col2:
            if st.button("🔄 Refresh History", key="refresh_history", use_container_width=True):
                st.success("✅ History refreshed!")
        
        with col3:
            if st.button("🗑️ Clear History", key="clear_history", use_container_width=True):
                self.system.clear_history()
                st.success("🗑️ History cleared!")
        
        try:
            history = self.system.get_analysis_history(limit=history_limit)
            
            if history:
                # Enhanced summary with better styling
                st.markdown(f"""
                <div style="background: rgba(40, 167, 69, 0.1); 
                            padding: 1rem; 
                            border-radius: 8px; 
                            margin: 1rem 0;
                            border-left: 4px solid #28a745;">
                    <h4 style="margin: 0; color: #28a745; font-size: 1.1rem;">📊 Analysis Summary</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #495057;">Showing {len(history)} most recent analyses</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced search functionality
                search_term = st.text_input(
                    "🔍 Search by company name:",
                    placeholder="Enter company name to filter analyses...",
                    help="Filter analyses by company name",
                    key="history_search_input"
                )
                
                # Filter history based on search with enhanced feedback
                if search_term:
                    filtered_history = [h for h in history if search_term.lower() in h['company_name'].lower()]
                    st.markdown(f"""
                    <div style="background: rgba(0, 123, 255, 0.1); 
                                padding: 1rem; 
                                border-radius: 8px; 
                                margin: 1rem 0;
                                border-left: 4px solid #007bff;">
                        <h4 style="margin: 0; color: #007bff; font-size: 1.1rem;">🔍 Search Results</h4>
                        <p style="margin: 0.5rem 0 0 0; color: #495057;">Found {len(filtered_history)} analyses for '{search_term}'</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    filtered_history = history
                
                # Enhanced table display with better styling
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 1.5rem; 
                            border-radius: 12px; 
                            margin: 2rem 0 1rem 0;
                            box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                    <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                        📋 Analysis Overview Table
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
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
                
                # Enhanced detailed view section
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; 
                            border-radius: 12px; 
                            margin: 2rem 0 1rem 0;
                            box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                    <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                        📋 Detailed Analysis View
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Select analysis to view with enhanced styling
                if filtered_history:
                    analysis_options = [f"{h['company_name']} - {h['analysis_type']} ({h['timestamp'][:10]})" for h in filtered_history]
                    selected_analysis = st.selectbox(
                        "📊 Select analysis to view details:",
                        analysis_options,
                        help="Choose an analysis to view its complete results",
                        key="analysis_detail_selector"
                    )
                    
                    if selected_analysis:
                        # Find the selected analysis
                        selected_index = analysis_options.index(selected_analysis)
                        selected_history_item = filtered_history[selected_index]
                        
                        # Get the full analysis details using the actual analysis ID
                        full_history = self.system.get_analysis_history(limit=1000)
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
                                st.markdown(f"""
                                <div style="background: rgba(40, 167, 69, 0.1); 
                                            padding: 1rem; 
                                            border-radius: 8px; 
                                            margin: 1rem 0;
                                            border-left: 4px solid #28a745;">
                                    <h4 style="margin: 0; color: #28a745; font-size: 1.1rem;">📋 Analysis Details</h4>
                                    <p style="margin: 0.5rem 0 0 0; color: #495057;">Showing complete analysis for {full_analysis['company_name']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                self.render_analysis_details(full_analysis)
                                
                                # Enhanced download options section
                                st.markdown("""
                                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                            padding: 1.5rem; 
                                            border-radius: 12px; 
                                            margin: 2rem 0 1rem 0;
                                            box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                                    <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                                        📥 Download Historical Report
                                    </h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns([1, 1, 1])
                                
                                with col1:
                                    if st.button(f"📄 PDF Report", key=f"pdf_{actual_analysis_id}", help="Download PDF report", use_container_width=True):
                                        self.download_pdf_report_from_history(full_analysis)
                                
                                with col2:
                                    if st.button(f"📝 Word Report", key=f"word_{actual_analysis_id}", help="Download Word report", use_container_width=True):
                                        self.download_word_report_from_history(full_analysis)
                                
                                with col3:
                                    if st.button(f"📋 Text Report", key=f"text_{actual_analysis_id}", help="Download text report", use_container_width=True):
                                        self.download_text_report_from_history(full_analysis)
                            else:
                                st.warning("⚠️ Could not retrieve full analysis details")
                        else:
                            st.warning("⚠️ Could not find the selected analysis in full history")
                
                # Enhanced statistics section
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; 
                            border-radius: 12px; 
                            margin: 2rem 0 1rem 0;
                            box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                    <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                        📈 History Statistics
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    successful = len([h for h in history if h['status'] == 'success'])
                    st.metric("✅ Successful", successful)
                
                with col2:
                    avg_time = sum(h['execution_time'] for h in history) / len(history) if history else 0
                    st.metric("⏱️ Avg Time", f"{avg_time:.1f}s")
                
                with col3:
                    avg_confidence = sum(h['confidence_score'] for h in history) / len(history) if history else 0
                    st.metric("🎯 Avg Confidence", f"{avg_confidence:.2f}")
                
                with col4:
                    unique_companies = len(set(h['company_name'] for h in history))
                    st.metric("🏢 Companies", unique_companies)
            else:
                st.markdown("""
                <div style="background: rgba(255, 193, 7, 0.1); 
                            padding: 2rem; 
                            border-radius: 12px; 
                            margin: 2rem 0;
                            border-left: 4px solid #ffc107;">
                    <h4 style="margin: 0; color: #856404; font-size: 1.3rem;">📝 No Analysis History</h4>
                    <p style="margin: 1rem 0 0 0; color: #495057; font-size: 1.1rem;">
                        No analysis history available yet. Run your first analysis to see history here!
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Could not load history: {e}")
            st.info("Try refreshing the page or running a new analysis.")
    
    def render_analysis_details(self, analysis: Dict[str, Any]):
        """Render detailed analysis results with professional styling"""
        
        # Professional header for analysis details
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin: 1rem 0;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                📊 Analysis Details for {analysis['company_name']}
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Debug information (can be removed later)
        if st.checkbox("🔧 Show Debug Info", help="Show debug information about the analysis"):
            st.json(analysis)
        
        # Analysis content section (moved to top)
        if analysis.get('content'):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 2rem 0 1rem 0;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 600;">📝 Analysis Content</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Show content structure info
            content = analysis['content']
            if isinstance(content, dict):
                st.markdown(f"""
                <div style="background: rgba(40, 167, 69, 0.1); 
                            padding: 1rem; 
                            border-radius: 8px; 
                            margin: 1rem 0;
                            border-left: 4px solid #28a745;">
                    <h5 style="margin: 0; color: #28a745; font-size: 1rem;">📋 Content Sections Available</h5>
                    <p style="margin: 0.5rem 0 0 0; color: #495057;">{', '.join(list(content.keys()))}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Create tabs for different content sections
            if isinstance(content, dict):
                if "full_result" in content:
                    # Full analysis from CrewAI
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 1.5rem; 
                                border-radius: 12px; 
                                margin: 1rem 0;
                                box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                        <h5 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 600;">🎯 Final Investment Thesis</h5>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("### 🎯 Complete Investment Analysis")
                    st.markdown("**This is the comprehensive final analysis report:**")
                    st.markdown(content["final_thesis"])
                    
                    # Show individual components in expanders with enhanced styling
                    if "original_thesis" in content:
                        with st.expander("📝 Original Thesis", expanded=False):
                            st.markdown(content["original_thesis"])
                    
                    if "critique" in content:
                        with st.expander("🔍 Critic's Recommendations", expanded=False):
                            st.markdown(content["critique"])
                    
        # Enhanced basic info section (moved to end)
        st.markdown("""
        <div style="background: rgba(0,0,0,0.05); 
                    padding: 1.5rem; 
                    border-radius: 10px; 
                    margin: 2rem 0 1rem 0;
                    border-left: 5px solid #17a2b8;">
            <h4 style="margin: 0; color: #17a2b8; font-size: 1.1rem; font-weight: 600;">📋 Analysis Information</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(40, 167, 69, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 4px solid #28a745;">
                <p style="margin: 0; font-weight: 600; color: #28a745;">🏢 Company</p>
                <p style="margin: 0.3rem 0 0 0; color: #495057;">{analysis['company_name']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(0, 123, 255, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 4px solid #007bff;">
                <p style="margin: 0; font-weight: 600; color: #007bff;">📊 Type</p>
                <p style="margin: 0.3rem 0 0 0; color: #495057;">{analysis['analysis_type'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
                        
        with col2:
            st.markdown(f"""
            <div style="background: rgba(255, 193, 7, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 4px solid #ffc107;">
                <p style="margin: 0; font-weight: 600; color: #856404;">📈 Status</p>
                <p style="margin: 0.3rem 0 0 0; color: #495057;">{analysis['status'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(220, 53, 69, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 4px solid #dc3545;">
                <p style="margin: 0; font-weight: 600; color: #dc3545;">⏱️ Execution Time</p>
                <p style="margin: 0.3rem 0 0 0; color: #495057;">{analysis['execution_time']:.2f}s</p>
            </div>
            """, unsafe_allow_html=True)
                
        with col3:
            st.markdown(f"""
            <div style="background: rgba(102, 16, 242, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 4px solid #6610f2;">
                <p style="margin: 0; font-weight: 600; color: #6610f2;">🎯 Confidence</p>
                <p style="margin: 0.3rem 0 0 0; color: #495057;">{analysis['confidence_score']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: rgba(108, 117, 125, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 0.5rem 0;
                        border-left: 4px solid #6c757d;">
                <p style="margin: 0; font-weight: 600; color: #6c757d;">📅 Date</p>
                <p style="margin: 0.3rem 0 0 0; color: #495057;">{analysis['timestamp'][:10]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Models used section (moved to end)
        if analysis.get('models_used'):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 2rem 0 1rem 0;
                        box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 600;">🤖 Models Used</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for model in analysis['models_used']:
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.03); 
                            padding: 0.8rem; 
                            border-radius: 8px; 
                            margin: 0.3rem 0;
                            border-left: 3px solid #007bff;">
                    <p style="margin: 0; color: #007bff; font-weight: 500;">• {model}</p>
                </div>
                """, unsafe_allow_html=True)
    
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
            if st.button("🔄 Refresh Market Data", help="Update dynamic market data", key="refresh_market_data"):
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
    
    def render_combined_qa_section(self):
        """Render combined Q&A section with company loading and question answering"""
        st.markdown("### 🤖 Q&A System for Historical Analyses")
        st.markdown("Load a company from your analysis history and ask questions about it.")
        
        if not self.rag_system:
            st.warning("⚠️ Q&A system is not available. Please check the system status.")
            return
        
        # Create two columns for the interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 🏢 Step 1: Load Company")
            
            # Get available companies from history
            try:
                history = self.system.get_analysis_history(limit=1000)
                if not history:
                    st.info("📝 No analysis history available. Run your first analysis to use this feature.")
                    return
                
                # Get unique companies
                companies = list(set([h['company_name'] for h in history]))
                companies.sort()
                
                # Company selection
                selected_company = st.selectbox(
                    "Select a company to ask questions about:",
                    companies,
                    help="Choose a company from your analysis history",
                    key="combined_qa_company_selector"
                )
                
                if selected_company:
                    # Get analyses for this company using the correct method
                    company_analyses = self.system.get_analysis_by_company(selected_company)
                    
                    if not company_analyses:
                        st.warning(f"⚠️ No analyses found for {selected_company}")
                        return
                    
                    st.success(f"📊 Found {len(company_analyses)} analyses for {selected_company}")
                    
                    # Show analysis summary
                    with st.expander(f"📋 Analysis Summary for {selected_company}"):
                        for analysis in company_analyses:
                            st.markdown(f"""
                            **{analysis['analysis_type'].title()} Analysis** - {analysis['timestamp'][:10]}
                            - Status: {analysis['status']}
                            - Confidence: {analysis['confidence_score']:.2f}
                            - Execution Time: {analysis['execution_time']:.2f}s
                            """)
                    
                    # Load company data into RAG system
                    if st.button(f"🤖 Load {selected_company} into Q&A System", type="primary", key="combined_load_company"):
                        with st.spinner(f"Loading {selected_company} data into Q&A system..."):
                            try:
                                success = self.load_company_into_rag(selected_company, company_analyses)
                                
                                if success:
                                    # Ensure both session state and RAG system are synchronized
                                    st.session_state['loaded_company'] = selected_company
                                    st.session_state['company_loaded'] = True
                                    st.session_state['show_company_selector'] = False
                                    
                                    # Double-check that RAG system has the correct company
                                    if self.rag_system:
                                        success = self.rag_system.set_current_company(selected_company)
                                        if success:
                                            print(f"🔧 Synchronized RAG system current_company to: {selected_company}")
                                        else:
                                            print(f"⚠️ Warning: Could not verify company data for {selected_company}")
                                    
                                    st.success(f"✅ {selected_company} loaded into Q&A system!")
                                    # Don't use st.rerun() - it causes full system reload
                                    # The UI will update automatically through session state
                            
                            except Exception as e:
                                st.error(f"❌ Error loading {selected_company} into Q&A system: {str(e)}")
                                st.info("💡 This might be due to empty analysis content or system issues.")
                
            except Exception as e:
                st.error(f"❌ Error loading historical data: {e}")
                st.info("💡 Please try refreshing the page or check if the system is properly initialized.")
        
        with col2:
            st.markdown("#### 🤔 Step 2: Ask Questions")
            
            # Check if a company is loaded using session state
            company_loaded = st.session_state.get('company_loaded', False)
            loaded_company = st.session_state.get('loaded_company', None)
            
            if not company_loaded or not loaded_company:
                st.info("📝 No company loaded. Please load a company first.")
                return
            
            # Verify RAG system has data for this company
            if self.rag_system and self.rag_system.current_company != loaded_company:
                st.warning(f"⚠️ RAG system mismatch. Expected: {loaded_company}, Got: {self.rag_system.current_company}")
                st.info("💡 Please reload the company.")
                return
            
            # Show current company
            st.success(f"📊 Currently loaded: **{loaded_company}**")
            
            # Question input
            question = st.text_area(
                "Ask a question:",
                placeholder="e.g., What are the main risks? What's the growth outlook? How does it compare to competitors?",
                help="Ask any question about the loaded company",
                height=100,
                key="qa_question_input"
            )
            
            # Suggested questions as example text boxes
            suggested_questions = self.rag_system.get_suggested_questions()
            if suggested_questions:
                st.markdown("### 💡 Example Questions You Can Ask:")
                
                # Display suggested questions as example text boxes
                col1, col2 = st.columns(2)
                
                with col1:
                    for i, suggested_q in enumerate(suggested_questions[:2]):
                        st.text_area(
                            f"Example {i+1}:",
                            value=suggested_q,
                            height=80,
                            disabled=True,
                            key=f"qa_example_{i}"
                        )
                
                with col2:
                    for i, suggested_q in enumerate(suggested_questions[2:4]):
                        st.text_area(
                            f"Example {i+3}:",
                            value=suggested_q,
                            height=80,
                            disabled=True,
                            key=f"qa_example_{i+2}"
                        )
            
            # Ask question button
            if st.button("🚀 Ask Question", type="primary", disabled=not question.strip(), key="qa_ask_question"):
                if question.strip():
                    with st.spinner("🤔 Thinking..."):
                        try:
                            # Debug: Check current company status
                            print(f"🔍 Debug - Session state loaded_company: {st.session_state.get('loaded_company')}")
                            print(f"🔍 Debug - RAG system current_company: {self.rag_system.current_company if self.rag_system else 'None'}")
                            
                            # Ensure RAG system has the correct company
                            if self.rag_system and st.session_state.get('loaded_company'):
                                if self.rag_system.current_company != st.session_state.get('loaded_company'):
                                    print(f"🔧 Fixing RAG system current_company from '{self.rag_system.current_company}' to '{st.session_state.get('loaded_company')}'")
                                    success = self.rag_system.set_current_company(st.session_state.get('loaded_company'))
                                    if not success:
                                        st.error(f"❌ Failed to set current company to {st.session_state.get('loaded_company')}")
                                        return
                            
                            # Get answer from RAG system
                            answer_result = self.rag_system.answer_question(
                                question, 
                                self._llm_callback, 
                                self._web_search_callback
                            )
                            
                            # Display answer in full width (outside the columns)
                            st.markdown("---")
                            
                            # Enhanced answer display with professional styling in full width
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                        padding: 2rem; 
                                        border-radius: 15px; 
                                        margin: 2rem 0;
                                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                                <h2 style="color: white; text-align: center; margin: 0; font-size: 2rem; font-weight: 700;">
                                    🤖 AI Answer
                                </h2>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Enhanced source display in full width - Fixed the st.info() issue
                            source_emoji = {
                                'stored_report': '📊',
                                'web_search': '🌐',
                                'no_data': '❌',
                                'error': '⚠️'
                            }.get(answer_result['source'], '📝')
                            
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.08); 
                                        padding: 1.5rem; 
                                        border-radius: 10px; 
                                        border-left: 5px solid #17a2b8;
                                        margin: 1rem 0;">
                                <p style="margin: 0; font-weight: 600; font-size: 1.1rem; color: #000000;">
                                    {source_emoji} <strong>Source:</strong> {answer_result['source'].replace('_', ' ').title()}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Enhanced answer display in full width
                            st.markdown(f"""
                            <div style="background: white; 
                                        padding: 2rem; 
                                        border-radius: 12px; 
                                        border: 2px solid #e0e0e0;
                                        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
                                        margin: 1rem 0;
                                        max-width: 100%;">
                                <div style="line-height: 1.8; color: #000000; font-size: 1.1rem; font-weight: 500;">
                                    {answer_result['answer']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Debug: Also display answer using st.write as fallback
                            st.markdown("### 🔍 Debug: Answer Content")
                            st.write("Answer length:", len(answer_result.get('answer', '')))
                            st.write("Answer preview:", answer_result.get('answer', '')[:200] + "..." if len(answer_result.get('answer', '')) > 200 else answer_result.get('answer', ''))
                            
                            # Alternative display method using st.markdown with explicit styling
                            st.markdown("### 📝 Answer (Alternative Display)")
                            st.markdown(f"""
                            <div style="background: #f8f9fa; 
                                        padding: 1.5rem; 
                                        border-radius: 8px; 
                                        border: 1px solid #dee2e6;
                                        margin: 1rem 0;">
                                <div style="color: #212529; font-size: 1rem; line-height: 1.6;">
                                    {answer_result['answer']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Store question for history
                            self.rag_system.store_question(question, answer_result['answer'], answer_result['confidence'])
                            
                            # Enhanced sources display in full width
                            if answer_result.get('chunks_used'):
                                with st.expander("📄 Sources Used", expanded=False):
                                    for i, chunk in enumerate(answer_result['chunks_used'][:3]):
                                        st.markdown(f"""
                                        <div style="background: rgba(0,0,0,0.05); 
                                                    padding: 1.5rem; 
                                                    border-radius: 10px; 
                                                    margin: 1rem 0;
                                                    border-left: 4px solid #007bff;">
                                            <h5 style="margin: 0; color: #007bff; font-size: 1.1rem;">Source {i+1}</h5>
                                            <p style="margin: 0.8rem 0 0 0; color: #000000; font-style: italic; line-height: 1.6; font-weight: 500;">
                                                {chunk['content'][:300]}...
                                            </p>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                        except Exception as e:
                            st.error(f"❌ Error answering question: {str(e)}")
                            st.info("💡 This might be due to LLM system issues. Please try again.")
                            st.error(f"🔍 Debug: Full error details: {type(e).__name__}: {e}")
            
            # Question history
            question_history = self.rag_system.get_question_history(loaded_company)
            if question_history:
                st.markdown("""
                <div style="background: rgba(40, 167, 69, 0.1); 
                            padding: 1rem; 
                            border-radius: 8px; 
                            margin: 1rem 0;
                            border-left: 4px solid #28a745;">
                    <h4 style="margin: 0; color: #28a745; font-size: 1.1rem;">📚 Recent Questions</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for qa in question_history[:3]:  # Show last 3 questions
                    with st.expander(f"Q: {qa['question'][:50]}...", expanded=False):
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.03); 
                                    padding: 1rem; 
                                    border-radius: 8px; 
                                    margin: 0.5rem 0;">
                            <p style="margin: 0; font-weight: 600; color: #495057;">
                                <strong>Question:</strong> {qa['question']}
                            </p>
                            <p style="margin: 0.5rem 0 0 0; color: #6c757d;">
                                <strong>Answer:</strong> {qa.get('answer', 'No answer stored')}
                            </p>
                            <p style="margin: 0.5rem 0 0 0; color: #999; font-size: 0.8rem;">
                                📅 Asked: {qa['timestamp'][:19] if qa.get('timestamp') else 'Unknown'}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # 4. Clear Data Section
        if st.button("🗑️ Clear Current Company Data", type="secondary", key="qa_clear_data"):
                if loaded_company:
                    self.rag_system.clear_company_data(loaded_company)
                    # Clear session state
                    st.session_state['loaded_company'] = None
                    st.session_state['company_loaded'] = False
                    st.success("✅ Company data cleared!")
        
        # 5. System Statistics Section
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin-top: 2rem;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                📊 Q&A System Statistics
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        if self.rag_system:
            stats = self.rag_system.get_system_stats()
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Reports", stats.get('total_reports', 0))
            
            with col2:
                st.metric("💬 Questions", stats.get('total_questions', 0))
            
            with col3:
                st.metric("🏢 Companies", stats.get('unique_companies', 0))
            
            with col4:
                st.metric("📊 Chunks", stats.get('total_chunks', 0))
    
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
    
    def validate_analysis_content(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and analyze the content structure of an analysis"""
        content = analysis.get('content', {})
        validation_result = {
            'has_content': False,
            'content_type': type(content).__name__,
            'content_keys': [],
            'total_chars': 0,
            'is_valid': False,
            'issues': []
        }
        
        if isinstance(content, dict):
            validation_result['has_content'] = True
            validation_result['content_keys'] = list(content.keys())
            
            # Calculate total characters
            total_chars = 0
            for key, value in content.items():
                if isinstance(value, str):
                    total_chars += len(value)
            
            validation_result['total_chars'] = total_chars
            
            # Check for common content keys
            expected_keys = ['full_result', 'research', 'sentiment', 'valuation', 'critique', 'original_thesis', 'final_thesis']
            found_keys = [key for key in expected_keys if key in content]
            
            if found_keys:
                validation_result['is_valid'] = True
            else:
                validation_result['issues'].append("No expected content keys found")
                
        elif isinstance(content, str):
            validation_result['has_content'] = True
            validation_result['total_chars'] = len(content)
            if len(content) > 100:
                validation_result['is_valid'] = True
            else:
                validation_result['issues'].append("Content too short")
        else:
            validation_result['issues'].append(f"Unexpected content type: {type(content).__name__}")
        
        return validation_result
    
    def load_company_into_rag(self, company_name: str, analyses: List[Dict[str, Any]]) -> bool:
        """Load company analyses into RAG system"""
        try:
            if not self.rag_system:
                print("❌ RAG system not available")
                return False
            
            print(f"📝 Loading {len(analyses)} analyses for {company_name} into RAG system...")
            
            # Clear any previous company data to prevent contamination
            if self.rag_system.current_company and self.rag_system.current_company != company_name:
                print(f"🗑️ Clearing previous company data for {self.rag_system.current_company}")
                self.rag_system.clear_company_data(self.rag_system.current_company)
            
            # Prepare comprehensive report content from all analyses
            report_content = ""
            
            for i, analysis in enumerate(analyses):
                analysis_type = analysis.get('analysis_type', 'unknown')
                content = analysis.get('content', {})
                
                print(f"📋 Processing {analysis_type} analysis {i+1}/{len(analyses)}")
                
                # Add analysis type header
                report_content += f"\n\n=== {analysis_type.upper()} ANALYSIS ===\n"
                
                # Add content based on structure
                if isinstance(content, dict):
                    if 'full_result' in content:
                        report_content += f"FULL RESULT:\n{content['full_result']}\n\n"
                    
                    if 'research' in content:
                        report_content += f"RESEARCH:\n{content['research']}\n\n"
                    
                    if 'sentiment' in content:
                        report_content += f"SENTIMENT:\n{content['sentiment']}\n\n"
                    
                    if 'valuation' in content:
                        report_content += f"VALUATION:\n{content['valuation']}\n\n"
                    
                    if 'critique' in content:
                        report_content += f"CRITIQUE:\n{content['critique']}\n\n"
                    
                    if 'original_thesis' in content:
                        report_content += f"ORIGINAL THESIS:\n{content['original_thesis']}\n\n"
                    
                    if 'final_thesis' in content:
                        report_content += f"FINAL THESIS:\n{content['final_thesis']}\n\n"
                    
                    # Add any other content sections
                    for key, value in content.items():
                        if key not in ['full_result', 'research', 'sentiment', 'valuation', 'critique', 'original_thesis', 'final_thesis']:
                            if isinstance(value, str) and value.strip():
                                report_content += f"{key.upper()}:\n{value}\n\n"
                            elif isinstance(value, dict):
                                # Handle nested dictionaries
                                report_content += f"{key.upper()}:\n"
                                for sub_key, sub_value in value.items():
                                    if isinstance(sub_value, str) and sub_value.strip():
                                        report_content += f"{sub_key}: {sub_value}\n"
                                report_content += "\n"
                else:
                    # If content is a string
                    if isinstance(content, str) and content.strip():
                        report_content += f"CONTENT:\n{content}\n\n"
                    else:
                        print(f"⚠️ Skipping analysis {i+1} - no valid content found")
            
            # Validate that we have meaningful content
            if not report_content.strip():
                print(f"⚠️ No meaningful content found for {company_name}")
                return False
            
            print(f"📝 Prepared {len(report_content)} characters of content for {company_name}")
            
            # Prepare metadata
            report_metadata = {
                'analysis_count': len(analyses),
                'analysis_types': ', '.join([a.get('analysis_type', 'unknown') for a in analyses]),
                'timestamp': datetime.now().isoformat(),
                'source': 'historical_analysis',
                'company_name': company_name,
                'status': 'success'
            }
            
            # Store in RAG system
            report_id = self.rag_system.store_report(company_name, report_content, report_metadata)
            
            if report_id:
                print(f"✅ Successfully loaded {company_name} with {len(analyses)} analyses into RAG system")
                
                # Verify company isolation
                if not self.rag_system.verify_company_isolation(company_name):
                    print(f"⚠️ Warning: Company isolation verification failed for {company_name}")
                
                self.rag_system.current_company = company_name  # Set current company
                return True
            else:
                print(f"❌ Failed to load {company_name} into RAG system")
                return False
                
        except Exception as e:
            print(f"❌ Error loading company into RAG: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self):
        """Main application runner"""
        # Render header
        self.render_header()
        
        # Render sidebar and get configuration
        config = self.render_sidebar()
        
        # Main content area
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Analysis", "📈 Markets", "📚 History", "🤖 Q&A", "🔧 Status"])
        
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
                        
                        # Store analysis in RAG system for Q&A
                        rag_success = self.store_analysis_in_rag(result)
                        if rag_success:
                            print(f"✅ Analysis for {company_name} successfully stored in RAG system")
                        else:
                            print(f"⚠️ Failed to store analysis for {company_name} in RAG system")
                        
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
                        st.info("💡 Please check your input and try again.")
        
        with tab2:
            # Markets tab
            self.render_market_overview()
        
        with tab3:
            # History tab
            self.render_history()
        
        with tab4:
            # Q&A tab
            self.render_qa_tab()
        
        with tab5:
            # Status tab
            self.render_system_status()
            
            # Add About section
            st.markdown("---")
            self.render_about()
    
    def render_qa_tab(self):
        """Render the dedicated Q&A tab with professional styling"""
        
        # Professional header with gradient styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem; font-weight: 700;">
                🤖 AI-Powered Investment Q&A
            </h1>
            <p style="color: white; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                Ask intelligent questions about your investment analyses
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not self.rag_system:
            st.error("⚠️ Q&A system is not available. Please check the system status.")
            return
        
        # Sequential layout - no columns, everything flows in order
        
        # 1. Company Loading Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600;">
                🏢 Load Company Data
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if we have a current company from recent analysis
        current_company = self.rag_system.current_company if self.rag_system else None
        
        if current_company:
            st.markdown(f"""
            <div style="background: rgba(40, 167, 69, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        border-left: 4px solid #28a745;">
                <h4 style="margin: 0; color: #28a745;">📊 Current Company</h4>
                <p style="margin: 0.5rem 0 0 0; font-weight: 600; font-size: 1.1rem;">{current_company}</p>
                <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">💡 You can ask questions about this company directly!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Option to load a different company
            if st.button("🔄 Load Different Company", key="qa_load_different", use_container_width=True):
                st.session_state['show_company_selector'] = True
        else:
            st.info("📝 No company currently loaded. Select a company from your analysis history.")
            st.session_state['show_company_selector'] = True
        
        # Company selector with enhanced styling
        if st.session_state.get('show_company_selector', False):
            try:
                history = self.system.get_analysis_history(limit=1000)
                if not history:
                    st.warning("📝 No analysis history available. Run your first analysis to use this feature.")
                    return
                
                # Get unique companies
                companies = list(set([h['company_name'] for h in history]))
                companies.sort()
                
                # Company selection with better styling
                selected_company = st.selectbox(
                    "Select a company to ask questions about:",
                    companies,
                    help="Choose a company from your analysis history",
                    key="qa_company_selector"
                )
                
                if selected_company:
                    # Get analyses for this company
                    company_analyses = self.system.get_analysis_by_company(selected_company)
                    
                    if not company_analyses:
                        st.error(f"⚠️ No analyses found for {selected_company}")
                        return
                    
                    st.success(f"📊 Found {len(company_analyses)} analyses for {selected_company}")
                    
                    # Enhanced analysis summary with better styling
                    with st.expander(f"📋 Analysis Summary for {selected_company}", expanded=False):
                        for analysis in company_analyses:
                            st.markdown(f"""
                            <div style="background: rgba(0,0,0,0.05); 
                                        padding: 1rem; 
                                        border-radius: 8px; 
                                        margin: 0.5rem 0;
                                        border-left: 3px solid #007bff;">
                                <h5 style="margin: 0; color: #007bff;">{analysis['analysis_type'].title()} Analysis</h5>
                                <p style="margin: 0.3rem 0; color: #666;">📅 {analysis['timestamp'][:10]}</p>
                                <p style="margin: 0.3rem 0;">✅ Status: {analysis['status']}</p>
                                <p style="margin: 0.3rem 0;">🎯 Confidence: {analysis['confidence_score']:.2f}</p>
                                <p style="margin: 0.3rem 0;">⏱️ Execution Time: {analysis['execution_time']:.2f}s</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Enhanced load button with better styling
                    if st.button(f"🤖 Load {selected_company} into Q&A System", type="primary", key="qa_load_company", use_container_width=True):
                        with st.spinner(f"Loading {selected_company} data into Q&A system..."):
                            try:
                                success = self.load_company_into_rag(selected_company, company_analyses)
                                
                                if success:
                                    # Ensure both session state and RAG system are synchronized
                                    st.session_state['loaded_company'] = selected_company
                                    st.session_state['company_loaded'] = True
                                    st.session_state['show_company_selector'] = False
                                    
                                    # Double-check that RAG system has the correct company
                                    if self.rag_system:
                                        success = self.rag_system.set_current_company(selected_company)
                                        if success:
                                            print(f"🔧 Synchronized RAG system current_company to: {selected_company}")
                                        else:
                                            print(f"⚠️ Warning: Could not verify company data for {selected_company}")
                                    
                                    st.success(f"✅ {selected_company} loaded into Q&A system!")
                                    # Don't use st.rerun() - it causes full system reload
                                    # The UI will update automatically through session state
                            
                            except Exception as e:
                                st.error(f"❌ Error loading {selected_company} into Q&A system: {str(e)}")
                                st.info("💡 This might be due to empty analysis content or system issues.")
            
            except Exception as e:
                st.error(f"❌ Error loading historical data: {e}")
                st.info("💡 Please try refreshing the page or check if the system is properly initialized.")
        
        # 2. Question Asking Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin: 2rem 0 1.5rem 0;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600;">
                🤔 Ask Questions
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if a company is loaded using session state
        company_loaded = st.session_state.get('company_loaded', False)
        loaded_company = st.session_state.get('loaded_company', None)
        current_company = self.rag_system.current_company if self.rag_system else None
        
        active_company = loaded_company or current_company
        
        if not active_company:
            st.info("📝 No company loaded. Please load a company first.")
            return
        
        # Enhanced current company display
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; 
                    border-radius: 8px; 
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 600;">
                📊 Currently Loaded
            </h4>
            <p style="color: white; margin: 0.5rem 0 0 0; font-weight: 700; font-size: 1.2rem;">
                {active_company}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced question input with better styling
        question = st.text_area(
            "Ask a question:",
            placeholder="e.g., What are the main risks? What's the growth outlook? How does it compare to competitors?",
            help="Ask any question about the loaded company",
            height=120,
            key="qa_question_input"
        )
        
        # Enhanced suggested questions with better styling
        suggested_questions = self.rag_system.get_suggested_questions()
        if suggested_questions:
            st.markdown("""
            <div style="background: rgba(255, 193, 7, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 1rem 0;
                        border-left: 4px solid #ffc107;">
                <h4 style="margin: 0; color: #856404; font-size: 1.1rem;">💡 Example Questions You Can Ask</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display suggested questions in a more attractive format - full width
            for i, suggested_q in enumerate(suggested_questions[:4]):
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.03); 
                            padding: 1rem; 
                            border-radius: 8px; 
                            margin: 0.5rem 0;
                            border: 1px solid rgba(0,0,0,0.1);">
                    <p style="margin: 0; font-weight: 600; color: #495057;">Example {i+1}:</p>
                    <p style="margin: 0.5rem 0 0 0; color: #6c757d; font-size: 0.9rem;">{suggested_q}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Enhanced ask question button
        if st.button("🚀 Ask Question", type="primary", disabled=not question.strip(), key="qa_ask_question", use_container_width=True):
            if question.strip():
                with st.spinner("🤔 Thinking..."):
                    try:
                        # Debug: Check current company status
                        print(f"🔍 Debug - Session state loaded_company: {st.session_state.get('loaded_company')}")
                        print(f"🔍 Debug - RAG system current_company: {self.rag_system.current_company if self.rag_system else 'None'}")
                        
                        # Ensure RAG system has the correct company
                        if self.rag_system and st.session_state.get('loaded_company'):
                            if self.rag_system.current_company != st.session_state.get('loaded_company'):
                                print(f"🔧 Fixing RAG system current_company from '{self.rag_system.current_company}' to '{st.session_state.get('loaded_company')}'")
                                success = self.rag_system.set_current_company(st.session_state.get('loaded_company'))
                                if not success:
                                    st.error(f"❌ Failed to set current company to {st.session_state.get('loaded_company')}")
                                    return
                        
                        # Get answer from RAG system
                        answer_result = self.rag_system.answer_question(
                            question, 
                            self._llm_callback, 
                            self._web_search_callback
                        )
                        
                        # Display answer in full width (outside the columns)
                        st.markdown("---")
                        
                        # Enhanced answer display with professional styling in full width
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    padding: 2rem; 
                                    border-radius: 15px; 
                                    margin: 2rem 0;
                                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
                            <h2 style="color: white; text-align: center; margin: 0; font-size: 2rem; font-weight: 700;">
                                🤖 AI Answer
                            </h2>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Enhanced source display in full width - Fixed the st.info() issue
                        source_emoji = {
                            'stored_report': '📊',
                            'web_search': '🌐',
                            'no_data': '❌',
                            'error': '⚠️'
                        }.get(answer_result['source'], '📝')
                        
                        st.markdown(f"""
                        <div style="background: rgba(0,0,0,0.08); 
                                    padding: 1.5rem; 
                                    border-radius: 10px; 
                                    border-left: 5px solid #17a2b8;
                                    margin: 1rem 0;">
                            <p style="margin: 0; font-weight: 600; font-size: 1.1rem; color: #000000;">
                                {source_emoji} <strong>Source:</strong> {answer_result['source'].replace('_', ' ').title()}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Enhanced answer display in full width
                        st.markdown(f"""
                        <div style="background: white; 
                                    padding: 2rem; 
                                    border-radius: 12px; 
                                    border: 2px solid #e0e0e0;
                                    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
                                    margin: 1rem 0;
                                    max-width: 100%;">
                            <div style="line-height: 1.8; color: #000000; font-size: 1.1rem; font-weight: 500;">
                                {answer_result['answer']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Debug: Also display answer using st.write as fallback
                        st.markdown("### 🔍 Debug: Answer Content")
                        st.write("Answer length:", len(answer_result.get('answer', '')))
                        st.write("Answer preview:", answer_result.get('answer', '')[:200] + "..." if len(answer_result.get('answer', '')) > 200 else answer_result.get('answer', ''))
                        
                        # Alternative display method using st.markdown with explicit styling
                        st.markdown("### 📝 Answer (Alternative Display)")
                        st.markdown(f"""
                        <div style="background: #f8f9fa; 
                                    padding: 1.5rem; 
                                    border-radius: 8px; 
                                    border: 1px solid #dee2e6;
                                    margin: 1rem 0;">
                            <div style="color: #212529; font-size: 1rem; line-height: 1.6;">
                                {answer_result['answer']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Store question for history
                        self.rag_system.store_question(question, answer_result['answer'], answer_result['confidence'])
                        
                        # Enhanced sources display in full width
                        if answer_result.get('chunks_used'):
                            with st.expander("📄 Sources Used", expanded=False):
                                for i, chunk in enumerate(answer_result['chunks_used'][:3]):
                                    st.markdown(f"""
                                    <div style="background: rgba(0,0,0,0.05); 
                                                padding: 1.5rem; 
                                                border-radius: 10px; 
                                                margin: 1rem 0;
                                                border-left: 4px solid #007bff;">
                                        <h5 style="margin: 0; color: #007bff; font-size: 1.1rem;">Source {i+1}</h5>
                                        <p style="margin: 0.8rem 0 0 0; color: #000000; font-style: italic; line-height: 1.6; font-weight: 500;">
                                            {chunk['content'][:300]}...
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                    except Exception as e:
                        st.error(f"❌ Error answering question: {str(e)}")
                        st.info("💡 This might be due to LLM system issues. Please try again.")
                        st.error(f"🔍 Debug: Full error details: {type(e).__name__}: {e}")
        
        # 3. Question History Section
        question_history = self.rag_system.get_question_history(loaded_company)
        if question_history:
            st.markdown("""
            <div style="background: rgba(40, 167, 69, 0.1); 
                        padding: 1rem; 
                        border-radius: 8px; 
                        margin: 2rem 0 1rem 0;
                        border-left: 4px solid #28a745;">
                <h4 style="margin: 0; color: #28a745; font-size: 1.1rem;">📚 Recent Questions</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for qa in question_history[:3]:  # Show last 3 questions
                with st.expander(f"Q: {qa['question'][:50]}...", expanded=False):
                    st.markdown(f"""
                    <div style="background: rgba(0,0,0,0.03); 
                                padding: 1rem; 
                                border-radius: 8px; 
                                margin: 0.5rem 0;">
                        <p style="margin: 0; font-weight: 600; color: #495057;">
                            <strong>Question:</strong> {qa['question']}
                        </p>
                        <p style="margin: 0.5rem 0 0 0; color: #6c757d;">
                            <strong>Answer:</strong> {qa.get('answer', 'No answer stored')}
                        </p>
                        <p style="margin: 0.5rem 0 0 0; color: #999; font-size: 0.8rem;">
                            📅 Asked: {qa['timestamp'][:19] if qa.get('timestamp') else 'Unknown'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # 4. Clear Data Section
        if st.button("🗑️ Clear Current Company Data", type="secondary", key="qa_clear_data", use_container_width=True):
            if loaded_company:
                self.rag_system.clear_company_data(loaded_company)
                # Clear session state
                st.session_state['loaded_company'] = None
                st.session_state['company_loaded'] = False
                st.success("✅ Company data cleared!")
        
        # 5. System Statistics Section
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin-top: 2rem;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600; text-align: center;">
                📊 Q&A System Statistics
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        if self.rag_system:
            stats = self.rag_system.get_system_stats()
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Reports", stats.get('total_reports', 0))
            
            with col2:
                st.metric("💬 Questions", stats.get('total_questions', 0))
            
            with col3:
                st.metric("🏢 Companies", stats.get('unique_companies', 0))
            
            with col4:
                st.metric("📊 Chunks", stats.get('total_chunks', 0))

def main():
    """Main function to run the Streamlit app"""
    app = IntelliVestStreamlitApp()
    app.run()

if __name__ == "__main__":
    main() 