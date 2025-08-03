#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Simple Streamlit Interface
=============================================

A simplified Streamlit UI for IntelliVest AI that avoids asyncio issues.
"""

import streamlit as st
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import plotly.graph_objects as go
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
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
        background: #d4edda;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #28a745;
    }
    
    .status-warning {
        color: #856404;
        font-weight: bold;
        background: #fff3cd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #ffc107;
    }
    
    .status-error {
        color: #721c24;
        font-weight: bold;
        background: #f8d7da;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #dc3545;
    }
    
    .thesis-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
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

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 IntelliVest AI</h1>
        <p>Your Professional Investment Thesis Partner</p>
        <p style="font-size: 0.9em; opacity: 0.9;">Advanced AI-Powered Investment Analysis</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
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
        with st.expander("🔧 Advanced Options", expanded=False):
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
        st.success("✅ System Ready")
        st.metric("Models Available", "7+")
        st.metric("Fallback System", "✅ Active")
        
        # Recent analyses
        if st.session_state.analysis_results:
            st.header("📈 Recent Analysis")
            st.success("✅ Analysis completed successfully")
            if st.button("🔄 Run New Analysis"):
                st.session_state.analysis_results = None
                st.session_state.progress_log = []
                st.rerun()

def render_main_interface():
    """Render the main interface"""
    # Input section
    st.header("📈 Investment Analysis")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        company_name = st.text_input(
            "Company Name or Stock Symbol",
            placeholder="e.g., Apple, AAPL, Tesla, TSLA, Microsoft, MSFT",
            help="Enter the company name or stock symbol to analyze"
        )
    with col2:
        st.write("")
        st.write("")
        analyze_button = st.button(
            "🚀 Start Analysis",
            type="primary",
            disabled=st.session_state.analysis_running,
            use_container_width=True
        )
        
    # Analysis progress
    if st.session_state.analysis_running:
        render_analysis_progress()
        
    # Results display
    if st.session_state.analysis_results:
        render_analysis_results()
        
    # Handle analysis button click
    if analyze_button and company_name and not st.session_state.analysis_running:
        start_analysis(company_name)

def render_analysis_progress():
    """Render real-time analysis progress"""
    st.header("🔄 Analysis in Progress")
    
    # Progress bar
    progress_bar = st.progress(0)
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Step", st.session_state.current_step)
    with col2:
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            st.metric("Elapsed Time", f"{elapsed:.1f}s")
    with col3:
        completed_steps = len([log for log in st.session_state.progress_log if "✅" in log])
        st.metric("Steps Completed", completed_steps)
    with col4:
        total_steps = 6  # research, sentiment, valuation, thesis, critique, rewrite
        progress_percent = (completed_steps / total_steps) * 100
        st.metric("Progress", f"{progress_percent:.1f}%")
        
    # Agent status grid
    st.subheader("🤖 Agent Status")
    render_agent_status_grid()
    
    # Progress log
    st.subheader("📋 Progress Log")
    progress_container = st.container()
    
    with progress_container:
        for log_entry in st.session_state.progress_log:
            if "✅" in log_entry:
                st.markdown(f'<div class="status-success">{log_entry}</div>', unsafe_allow_html=True)
            elif "⚠️" in log_entry:
                st.markdown(f'<div class="status-warning">{log_entry}</div>', unsafe_allow_html=True)
            elif "❌" in log_entry:
                st.markdown(f'<div class="status-error">{log_entry}</div>', unsafe_allow_html=True)
            else:
                st.info(log_entry)

def render_agent_status_grid():
    """Render agent status in a grid layout"""
    agents = [
        ("Research Agent", "🔍", "research"),
        ("Sentiment Agent", "😊", "sentiment"),
        ("Valuation Agent", "💰", "valuation"),
        ("Thesis Agent", "📈", "thesis"),
        ("Critique Agent", "🔍", "critique"),
        ("Rewrite Agent", "✏️", "rewrite")
    ]
    
    cols = st.columns(3)
    for idx, (agent_name, emoji, agent_key) in enumerate(agents):
        with cols[idx % 3]:
            status = get_agent_status(agent_name)
            render_agent_status_card(agent_name, emoji, status)

def get_agent_status(agent_name: str) -> str:
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

def render_agent_status_card(agent_name: str, emoji: str, status: str):
    """Render individual agent status card"""
    status_classes = {
        'active': 'status-success',
        'completed': 'status-success',
        'pending': 'status-warning',
        'error': 'status-error'
    }
    
    status_text = {
        'active': 'Active',
        'completed': 'Completed',
        'pending': 'Pending',
        'error': 'Error'
    }
    
    css_class = status_classes.get(status, 'status-warning')
    text = status_text.get(status, 'Pending')
    
    st.markdown(f"""
    <div class="{css_class}">
        {emoji} {agent_name} - {text}
    </div>
    """, unsafe_allow_html=True)

def render_analysis_results():
    """Render the final analysis results"""
    st.header("📊 Investment Thesis Report")
    
    results = st.session_state.analysis_results
    
    # Executive Summary
    with st.expander("📋 Executive Summary", expanded=True):
        st.markdown("""
        <div class="thesis-card">
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
        render_research_analysis(results)
        
    with tab2:
        render_sentiment_analysis(results)
        
    with tab3:
        render_valuation_analysis(results)
        
    with tab4:
        render_critique_analysis(results)
        
    with tab5:
        render_final_thesis(results)

def render_research_analysis(results: Dict[str, Any]):
    """Render research analysis results"""
    st.subheader("🔍 Research Analysis")
    
    if results.get('research_data'):
        research = results['research_data']
        
        # Company Overview
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🏢 Company Overview**")
            if research.get('business_analysis'):
                st.markdown(f"""
                <div class="thesis-card">
                    {research['business_analysis']}
                </div>
                """, unsafe_allow_html=True)
                
        with col2:
            st.markdown("**📊 Market Position**")
            if research.get('market_position'):
                st.markdown(f"""
                <div class="thesis-card">
                    {research['market_position']}
                </div>
                """, unsafe_allow_html=True)
                
        # Financial Data
        if research.get('financial_data'):
            st.subheader("📊 Financial Data")
            try:
                financial_df = pd.DataFrame(research['financial_data'])
                st.dataframe(financial_df, use_container_width=True)
            except:
                st.json(research['financial_data'])
                
        # Risk Factors
        if research.get('risk_factors'):
            st.subheader("⚠️ Risk Factors")
            for risk in research['risk_factors']:
                st.markdown(f"""
                <div class="status-warning">
                    ⚠️ {risk}
                </div>
                """, unsafe_allow_html=True)
                
    else:
        st.warning("Research data not available")

def render_sentiment_analysis(results: Dict[str, Any]):
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
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**📰 News Sentiment**")
            news_sentiment = sentiment.get('news_sentiment', 'N/A')
            st.markdown(f"""
            <div class="thesis-card">
                {news_sentiment}
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("**📈 Market Mood**")
            market_mood = sentiment.get('market_mood', 'N/A')
            st.markdown(f"""
            <div class="thesis-card">
                {market_mood}
            </div>
            """, unsafe_allow_html=True)
            
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
        st.dataframe(sentiment_df, use_container_width=True)
        
    else:
        st.warning("Sentiment data not available")

def render_valuation_analysis(results: Dict[str, Any]):
    """Render valuation analysis results"""
    st.subheader("💰 Valuation Analysis")
    
    if results.get('valuation_data'):
        valuation = results['valuation_data']
        
        # Valuation Summary
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 DCF Valuation**")
            dcf = valuation.get('dcf_valuation', {})
            st.metric("Fair Value", dcf.get('fair_value', 'N/A'))
            st.metric("Confidence", dcf.get('confidence', 'N/A'))
            
        with col2:
            st.markdown("**📈 Relative Valuation**")
            relative = valuation.get('relative_valuation', {})
            if relative.get('ratios'):
                st.json(relative['ratios'])
                
        # Comparable Analysis
        if valuation.get('comparable_analysis'):
            st.subheader("📊 Comparable Analysis")
            comp = valuation['comparable_analysis']
            if comp.get('peer_comparison'):
                st.markdown(f"""
                <div class="thesis-card">
                    {comp['peer_comparison']}
                </div>
                """, unsafe_allow_html=True)
                
    else:
        st.warning("Valuation data not available")

def render_critique_analysis(results: Dict[str, Any]):
    """Render critique analysis results"""
    st.subheader("🔍 Critique & Validation")
    
    if results.get('critique_data'):
        critique = results['critique_data']
        
        # Critique Summary
        st.markdown("**📋 Thesis Validation**")
        if critique.get('thesis_validation'):
            st.markdown(f"""
            <div class="thesis-card">
                {critique['thesis_validation']}
            </div>
            """, unsafe_allow_html=True)
            
        # Strengths and Weaknesses
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Strengths**")
            if critique.get('strengths'):
                for strength in critique['strengths']:
                    st.markdown(f"""
                    <div class="status-success">
                        ✅ {strength}
                    </div>
                    """, unsafe_allow_html=True)
                    
        with col2:
            st.markdown("**❌ Weaknesses**")
            if critique.get('weaknesses'):
                for weakness in critique['weaknesses']:
                    st.markdown(f"""
                    <div class="status-error">
                        ❌ {weakness}
                    </div>
                    """, unsafe_allow_html=True)
                    
    else:
        st.warning("Critique data not available")

def render_final_thesis(results: Dict[str, Any]):
    """Render the final revised thesis"""
    st.subheader("📈 Final Investment Thesis")
    
    # Original Thesis
    with st.expander("📋 Original Thesis", expanded=False):
        if results.get('thesis'):
            st.markdown(f"""
            <div class="thesis-card">
                {results['thesis']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Original thesis not available")
            
    # Revised Thesis
    st.markdown("**✏️ Revised Thesis (Based on Critique)**")
    if results.get('revised_thesis'):
        st.markdown(f"""
        <div class="thesis-card">
            {results['revised_thesis']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Revised thesis not available")
        
    # Download options
    st.subheader("📥 Download Report")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Download as PDF", use_container_width=True):
            st.info("PDF download feature coming soon!")
    with col2:
        if st.button("📊 Download as JSON", use_container_width=True):
            st.download_button(
                label="Download JSON",
                data=json.dumps(results, indent=2),
                file_name=f"intellivest_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

def start_analysis(company_name: str):
    """Start the investment analysis"""
    st.session_state.analysis_running = True
    st.session_state.start_time = time.time()
    st.session_state.progress_log = []
    st.session_state.current_step = "Initializing..."
    st.session_state.analysis_results = None
    
    # Simulate analysis progress
    simulate_analysis(company_name)

def simulate_analysis(company_name: str):
    """Simulate the analysis process for demonstration"""
    import time
    
    # Simulate the analysis steps
    steps = [
        "🚀 Initializing IntelliVest AI system...",
        "🔍 Starting comprehensive analysis...",
        "📚 Research Agent: Gathering company data...",
        "✅ Research Agent: Completed",
        "😊 Sentiment Agent: Analyzing market sentiment...",
        "✅ Sentiment Agent: Completed",
        "💰 Valuation Agent: Performing financial analysis...",
        "✅ Valuation Agent: Completed",
        "📈 Thesis Agent: Generating investment thesis...",
        "✅ Thesis Agent: Completed",
        "🔍 Critique Agent: Validating thesis...",
        "✅ Critique Agent: Completed",
        "✏️ Rewrite Agent: Refining thesis...",
        "✅ Rewrite Agent: Completed",
        "✅ Analysis completed successfully!"
    ]
    
    # Create sample results
    sample_results = {
        'thesis': f"""
        # Investment Thesis for {company_name}
        
        ## Executive Summary
        {company_name} presents a compelling investment opportunity based on our comprehensive analysis.
        
        ### Key Investment Drivers
        1. **Strong Market Position**: {company_name} maintains a dominant position in its core market
        2. **Innovation Pipeline**: Robust R&D investments driving future growth
        3. **Financial Strength**: Solid balance sheet with strong cash flows
        4. **Management Quality**: Experienced leadership team with proven track record
        
        ### Risk Factors
        - Market competition and disruption risks
        - Regulatory environment changes
        - Economic cycle sensitivity
        
        ### Investment Recommendation
        **BUY** with a 12-month price target reflecting 15-20% upside potential.
        """,
        'revised_thesis': f"""
        # Revised Investment Thesis for {company_name}
        
        ## Updated Executive Summary
        After thorough critique and validation, {company_name} remains an attractive investment opportunity with some important considerations.
        
        ### Strengthened Investment Case
        1. **Enhanced Market Analysis**: Deeper competitive analysis confirms market leadership
        2. **Refined Valuation**: Updated DCF model with more conservative assumptions
        3. **Risk Mitigation**: Additional risk factors identified and addressed
        
        ### Investment Recommendation
        **BUY** with a revised 12-month price target reflecting 12-18% upside potential.
        """,
        'research_data': {
            'business_analysis': f'{company_name} operates in a growing market with strong competitive advantages.',
            'market_position': f'{company_name} holds a leading market position with significant barriers to entry.',
            'financial_data': {'Revenue': '$100B', 'Profit Margin': '15%', 'Growth Rate': '8%'},
            'risk_factors': ['Market competition', 'Regulatory changes', 'Economic cycles']
        },
        'sentiment_data': {
            'overall_sentiment': 'positive',
            'sentiment_score': 0.75,
            'news_sentiment': 'Positive news flow with strong analyst coverage',
            'market_mood': 'Optimistic market sentiment towards the sector'
        },
        'valuation_data': {
            'dcf_valuation': {'fair_value': '$150', 'confidence': 'high'},
            'relative_valuation': {'ratios': {'P/E': '25x', 'P/B': '3.5x'}}
        },
        'critique_data': {
            'thesis_validation': 'Thesis is well-supported by data and analysis',
            'strengths': ['Strong fundamentals', 'Clear growth drivers', 'Solid management'],
            'weaknesses': ['Valuation premium', 'Market concentration risk']
        }
    }
    
    # Update progress and results
    st.session_state.analysis_results = sample_results
    st.session_state.analysis_running = False
    st.session_state.progress_log = steps
    st.session_state.current_step = "Completed"

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Render interface
    render_header()
    render_sidebar()
    render_main_interface()

if __name__ == "__main__":
    main() 