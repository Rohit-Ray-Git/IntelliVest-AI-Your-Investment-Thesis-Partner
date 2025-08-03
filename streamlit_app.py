#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Professional Streamlit Interface
===================================================

A professional Streamlit UI for IntelliVest AI that provides:
- Real-time operation tracking
- Professional investment thesis reports
- Interactive analysis options
- Beautiful visualizations
"""

import streamlit as st
import asyncio
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

# Page configuration
st.set_page_config(
    page_title="IntelliVest AI - Investment Thesis Partner",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .progress-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .report-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .agent-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
    }
    
    .agent-active {
        background: #d4edda;
        border-left: 3px solid #28a745;
    }
    
    .agent-completed {
        background: #cce5ff;
        border-left: 3px solid #007bff;
    }
    
    .agent-pending {
        background: #fff3cd;
        border-left: 3px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

class IntelliVestStreamlitUI:
    """Professional Streamlit UI for IntelliVest AI"""
    
    def __init__(self):
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'analysis_running' not in st.session_state:
            st.session_state.analysis_running = False
        if 'current_step' not in st.session_state:
            st.session_state.current_step = ""
        if 'progress_log' not in st.session_state:
            st.session_state.progress_log = []
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = None
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
            
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 IntelliVest AI</h1>
            <p>Your Professional Investment Thesis Partner</p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Analysis type selection
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Full Analysis", "Research Only", "Sentiment Only", "Valuation Only", "Thesis Only"],
                help="Choose the type of analysis to perform"
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                use_advanced_fallback = st.checkbox(
                    "Use Advanced Fallback System",
                    value=True,
                    help="Enable multi-LLM fallback for better reliability"
                )
                
                max_fallbacks = st.slider(
                    "Max Fallbacks",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="Maximum number of AI model fallbacks"
                )
                
                include_tools = st.checkbox(
                    "Include Custom Tools",
                    value=True,
                    help="Use specialized investment analysis tools"
                )
            
            # System status
            st.header("📊 System Status")
            self.render_system_status()
            
    def render_system_status(self):
        """Render system status in sidebar"""
        try:
            # Import and check system status
            from production_integration import ProductionIntelliVestAI
            system = ProductionIntelliVestAI()
            status = system.get_system_status()
            
            # Display status metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Models Available", status.get('models_available', 0))
            with col2:
                st.metric("Fallback System", "✅ Active" if status.get('fallback_active') else "❌ Inactive")
                
            # Health indicators
            st.subheader("Health Status")
            for model, health in status.get('model_health', {}).items():
                if health:
                    st.success(f"✅ {model}")
                else:
                    st.error(f"❌ {model}")
                    
        except Exception as e:
            st.error(f"System status unavailable: {str(e)}")
            
    def render_main_interface(self):
        """Render the main interface"""
        # Input section
        st.header("📈 Investment Analysis")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            company_name = st.text_input(
                "Company Name or Stock Symbol",
                placeholder="e.g., Apple, AAPL, Tesla, TSLA",
                help="Enter the company name or stock symbol to analyze"
            )
        with col2:
            st.write("")
            st.write("")
            analyze_button = st.button(
                "🚀 Start Analysis",
                type="primary",
                disabled=st.session_state.analysis_running
            )
            
        # Analysis progress
        if st.session_state.analysis_running:
            self.render_analysis_progress()
            
        # Results display
        if st.session_state.analysis_results:
            self.render_analysis_results()
            
        # Handle analysis button click
        if analyze_button and company_name and not st.session_state.analysis_running:
            self.start_analysis(company_name)
            
    def render_analysis_progress(self):
        """Render real-time analysis progress"""
        st.header("🔄 Analysis in Progress")
        
        # Progress bar
        progress_bar = st.progress(0)
        
        # Status indicators
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Step", st.session_state.current_step)
        with col2:
            if st.session_state.start_time:
                elapsed = time.time() - st.session_state.start_time
                st.metric("Elapsed Time", f"{elapsed:.1f}s")
        with col3:
            st.metric("Steps Completed", len([log for log in st.session_state.progress_log if "✅" in log]))
            
        # Progress log
        st.subheader("📋 Progress Log")
        progress_container = st.container()
        
        with progress_container:
            for log_entry in st.session_state.progress_log:
                if "✅" in log_entry:
                    st.success(log_entry)
                elif "⚠️" in log_entry:
                    st.warning(log_entry)
                elif "❌" in log_entry:
                    st.error(log_entry)
                else:
                    st.info(log_entry)
                    
        # Agent status
        st.subheader("🤖 Agent Status")
        self.render_agent_status()
        
    def render_agent_status(self):
        """Render agent status indicators"""
        agents = [
            ("Research Agent", "🔍"),
            ("Sentiment Agent", "😊"),
            ("Valuation Agent", "💰"),
            ("Thesis Agent", "📈"),
            ("Critique Agent", "🔍"),
            ("Rewrite Agent", "✏️")
        ]
        
        for agent_name, emoji in agents:
            status = self.get_agent_status(agent_name)
            if status == "active":
                st.markdown(f"""
                <div class="agent-status agent-active">
                    {emoji} {agent_name} - Active
                </div>
                """, unsafe_allow_html=True)
            elif status == "completed":
                st.markdown(f"""
                <div class="agent-status agent-completed">
                    {emoji} {agent_name} - Completed
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="agent-status agent-pending">
                    {emoji} {agent_name} - Pending
                </div>
                """, unsafe_allow_html=True)
                
    def get_agent_status(self, agent_name: str) -> str:
        """Get the current status of an agent"""
        if not st.session_state.progress_log:
            return "pending"
            
        # Simple logic based on progress log
        log_text = " ".join(st.session_state.progress_log).lower()
        agent_lower = agent_name.lower()
        
        if "completed" in log_text and agent_lower in log_text:
            return "completed"
        elif agent_lower in log_text:
            return "active"
        else:
            return "pending"
            
    def render_analysis_results(self):
        """Render the final analysis results"""
        st.header("📊 Investment Thesis Report")
        
        results = st.session_state.analysis_results
        
        # Executive Summary
        with st.expander("📋 Executive Summary", expanded=True):
            st.markdown("""
            <div class="report-section">
                <h3>Investment Thesis Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if results.get('thesis'):
                st.markdown(results['thesis'])
            else:
                st.warning("Thesis not available")
                
        # Detailed Analysis Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔍 Research Analysis", 
            "😊 Sentiment Analysis", 
            "💰 Valuation Analysis", 
            "🔍 Critique & Validation",
            "📈 Final Thesis"
        ])
        
        with tab1:
            self.render_research_analysis(results)
            
        with tab2:
            self.render_sentiment_analysis(results)
            
        with tab3:
            self.render_valuation_analysis(results)
            
        with tab4:
            self.render_critique_analysis(results)
            
        with tab5:
            self.render_final_thesis(results)
            
    def render_research_analysis(self, results: Dict[str, Any]):
        """Render research analysis results"""
        st.subheader("🔍 Research Analysis")
        
        if results.get('research_data'):
            research = results['research_data']
            
            # Company Overview
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Company Overview**")
                if research.get('business_analysis'):
                    st.write(research['business_analysis'])
                    
            with col2:
                st.markdown("**Market Position**")
                if research.get('market_position'):
                    st.write(research['market_position'])
                    
            # Financial Data
            if research.get('financial_data'):
                st.subheader("📊 Financial Data")
                try:
                    financial_df = pd.DataFrame(research['financial_data'])
                    st.dataframe(financial_df)
                except:
                    st.json(research['financial_data'])
                    
            # Risk Factors
            if research.get('risk_factors'):
                st.subheader("⚠️ Risk Factors")
                for risk in research['risk_factors']:
                    st.write(f"• {risk}")
                    
        else:
            st.warning("Research data not available")
            
    def render_sentiment_analysis(self, results: Dict[str, Any]):
        """Render sentiment analysis results"""
        st.subheader("😊 Sentiment Analysis")
        
        if results.get('sentiment_data'):
            sentiment = results['sentiment_data']
            
            # Sentiment Overview
            col1, col2, col3 = st.columns(3)
            with col1:
                overall_sentiment = sentiment.get('overall_sentiment', 'neutral')
                sentiment_score = sentiment.get('sentiment_score', 0.5)
                
                # Create sentiment gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=sentiment_score * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Overall Sentiment"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 33], 'color': "lightgray"},
                            {'range': [33, 66], 'color': "gray"},
                            {'range': [66, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                st.markdown("**News Sentiment**")
                st.write(sentiment.get('news_sentiment', 'N/A'))
                
            with col3:
                st.markdown("**Market Mood**")
                st.write(sentiment.get('market_mood', 'N/A'))
                
            # Detailed Sentiment Breakdown
            st.subheader("📊 Sentiment Breakdown")
            sentiment_metrics = {
                'News Sentiment': sentiment.get('news_sentiment', 'N/A'),
                'Social Sentiment': sentiment.get('social_sentiment', 'N/A'),
                'Analyst Sentiment': sentiment.get('analyst_sentiment', 'N/A'),
                'Institutional Sentiment': sentiment.get('institutional_sentiment', 'N/A')
            }
            
            sentiment_df = pd.DataFrame(list(sentiment_metrics.items()), 
                                      columns=['Metric', 'Sentiment'])
            st.dataframe(sentiment_df)
            
        else:
            st.warning("Sentiment data not available")
            
    def render_valuation_analysis(self, results: Dict[str, Any]):
        """Render valuation analysis results"""
        st.subheader("💰 Valuation Analysis")
        
        if results.get('valuation_data'):
            valuation = results['valuation_data']
            
            # Valuation Summary
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**DCF Valuation**")
                dcf = valuation.get('dcf_valuation', {})
                st.metric("Fair Value", dcf.get('fair_value', 'N/A'))
                st.metric("Confidence", dcf.get('confidence', 'N/A'))
                
            with col2:
                st.markdown("**Relative Valuation**")
                relative = valuation.get('relative_valuation', {})
                if relative.get('ratios'):
                    st.json(relative['ratios'])
                    
            # Comparable Analysis
            if valuation.get('comparable_analysis'):
                st.subheader("📊 Comparable Analysis")
                comp = valuation['comparable_analysis']
                if comp.get('peer_comparison'):
                    st.write(comp['peer_comparison'])
                    
        else:
            st.warning("Valuation data not available")
            
    def render_critique_analysis(self, results: Dict[str, Any]):
        """Render critique analysis results"""
        st.subheader("🔍 Critique & Validation")
        
        if results.get('critique_data'):
            critique = results['critique_data']
            
            # Critique Summary
            st.markdown("**Thesis Validation**")
            if critique.get('thesis_validation'):
                st.write(critique['thesis_validation'])
                
            # Strengths and Weaknesses
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Strengths**")
                if critique.get('strengths'):
                    for strength in critique['strengths']:
                        st.success(f"✅ {strength}")
                        
            with col2:
                st.markdown("**Weaknesses**")
                if critique.get('weaknesses'):
                    for weakness in critique['weaknesses']:
                        st.error(f"❌ {weakness}")
                        
        else:
            st.warning("Critique data not available")
            
    def render_final_thesis(self, results: Dict[str, Any]):
        """Render the final revised thesis"""
        st.subheader("📈 Final Investment Thesis")
        
        # Original Thesis
        with st.expander("📋 Original Thesis"):
            if results.get('thesis'):
                st.markdown(results['thesis'])
            else:
                st.warning("Original thesis not available")
                
        # Revised Thesis
        st.markdown("**✏️ Revised Thesis (Based on Critique)**")
        if results.get('revised_thesis'):
            st.markdown(results['revised_thesis'])
        else:
            st.warning("Revised thesis not available")
            
        # Download options
        st.subheader("📥 Download Report")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Download as PDF"):
                st.info("PDF download feature coming soon!")
        with col2:
            if st.button("📊 Download as JSON"):
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(results, indent=2),
                    file_name=f"intellivest_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
    def start_analysis(self, company_name: str):
        """Start the investment analysis"""
        st.session_state.analysis_running = True
        st.session_state.start_time = time.time()
        st.session_state.progress_log = []
        st.session_state.current_step = "Initializing..."
        st.session_state.analysis_results = None
        
        # Run analysis in background
        asyncio.run(self.run_analysis_async(company_name))
        
    async def run_analysis_async(self, company_name: str):
        """Run the analysis asynchronously"""
        try:
            # Import the production system
            from production_integration import ProductionIntelliVestAI, AnalysisRequest
            
            # Initialize system
            self.update_progress("🚀 Initializing IntelliVest AI system...")
            system = ProductionIntelliVestAI()
            
            # Create analysis request
            request = AnalysisRequest(
                company_name=company_name,
                analysis_type="full",
                include_tools=True,
                use_advanced_fallback=True,
                max_fallbacks=3
            )
            
            # Run analysis
            self.update_progress("🔍 Starting comprehensive analysis...")
            result = await system.analyze_company(request)
            
            # Store results
            st.session_state.analysis_results = result.content
            st.session_state.analysis_running = False
            self.update_progress("✅ Analysis completed successfully!")
            
        except Exception as e:
            st.session_state.analysis_running = False
            self.update_progress(f"❌ Analysis failed: {str(e)}")
            st.error(f"Analysis failed: {str(e)}")
            
    def update_progress(self, message: str):
        """Update progress log"""
        st.session_state.progress_log.append(message)
        st.session_state.current_step = message
        time.sleep(0.1)  # Small delay for UI updates

def main():
    """Main application function"""
    # Initialize UI
    ui = IntelliVestStreamlitUI()
    
    # Render interface
    ui.render_header()
    ui.render_sidebar()
    ui.render_main_interface()

if __name__ == "__main__":
    main() 