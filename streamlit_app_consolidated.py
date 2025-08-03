#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Consolidated Streamlit Interface
===================================================

A comprehensive Streamlit UI for IntelliVest AI that combines:
- Real-time agent progress tracking
- Direct integration with production system
- Professional investment thesis reports
- Interactive visualizations
- Live status updates
- Multiple analysis types
- System monitoring
"""

import streamlit as st
import asyncio
import sys
import os
import json
import time
import threading
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

# Import the production system
try:
    from production_integration import ProductionIntelliVestAI, AnalysisRequest, AnalysisResult
    PRODUCTION_SYSTEM_AVAILABLE = True
except ImportError as e:
    st.error(f"Production system not available: {e}")
    PRODUCTION_SYSTEM_AVAILABLE = False

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
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .progress-container {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
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
    
    .agent-waiting {
        background: #fff3cd;
        border-left: 3px solid #ffc107;
    }
    
    .agent-error {
        background: #f8d7da;
        border-left: 3px solid #dc3545;
    }
    
    .analysis-type-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .analysis-type-card:hover {
        border-color: #1f77b4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .analysis-type-card.selected {
        border-color: #1f77b4;
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class ConsolidatedIntelliVestUI:
    """Consolidated IntelliVest AI Streamlit Interface"""
    
    def __init__(self):
        self.intellivest_ai = None
        self.initialize_session_state()
        self.initialize_production_system()
    
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
        if 'selected_analysis_type' not in st.session_state:
            st.session_state.selected_analysis_type = "research"
        if 'system_status' not in st.session_state:
            st.session_state.system_status = {}
    
    def initialize_production_system(self):
        """Initialize the production system"""
        if PRODUCTION_SYSTEM_AVAILABLE:
            try:
                with st.spinner("Initializing IntelliVest AI System..."):
                    self.intellivest_ai = ProductionIntelliVestAI()
                    st.success("✅ Production system initialized successfully!")
            except Exception as e:
                st.error(f"❌ Failed to initialize production system: {e}")
                self.intellivest_ai = None
    
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 IntelliVest AI</h1>
            <p>Your Investment Thesis Partner - Advanced AI-Powered Investment Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with controls"""
        with st.sidebar:
            st.markdown("### 🎯 Analysis Controls")
            
            # Company input
            company_name = st.text_input(
                "Company Name",
                placeholder="e.g., Apple Inc., Tesla, Microsoft",
                help="Enter the company name for analysis"
            )
            
            # Analysis type selection
            st.markdown("### 📊 Analysis Type")
            analysis_types = {
                "research": "🔍 Research Analysis",
                "sentiment": "😊 Sentiment Analysis", 
                "valuation": "💰 Valuation Analysis",
                "thesis": "📝 Thesis Generation",
                "full": "🎯 Full Analysis (All Types)"
            }
            
            selected_type = st.selectbox(
                "Choose Analysis Type",
                options=list(analysis_types.keys()),
                format_func=lambda x: analysis_types[x],
                index=0
            )
            
            st.session_state.selected_analysis_type = selected_type
            
            # Analysis options
            st.markdown("### ⚙️ Options")
            include_tools = st.checkbox("Include Tools", value=True, help="Use custom investment tools")
            use_fallback = st.checkbox("Use Advanced Fallback", value=True, help="Enable multi-LLM fallback system")
            
            # Start analysis button
            st.markdown("---")
            if st.button("🚀 Start Analysis", type="primary", disabled=not company_name or st.session_state.analysis_running):
                if company_name:
                    self.start_analysis(company_name, selected_type, include_tools, use_fallback)
            
            # System status
            if self.intellivest_ai:
                st.markdown("---")
                st.markdown("### 📊 System Status")
                try:
                    status = self.intellivest_ai.get_system_status()
                    st.json(status)
                except Exception as e:
                    st.error(f"Status error: {e}")
    
    def render_system_status(self):
        """Render system status dashboard"""
        if not self.intellivest_ai:
            st.warning("⚠️ Production system not available")
            return
        
        try:
            status = self.intellivest_ai.get_system_status()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("System Status", status.get('system_status', 'Unknown'))
            
            with col2:
                metrics = status.get('metrics', {})
                st.metric("Total Analyses", metrics.get('total_analyses', 0))
            
            with col3:
                st.metric("Success Rate", f"{metrics.get('success_rate', 0):.1f}%")
            
            with col4:
                st.metric("Avg Execution Time", f"{metrics.get('avg_execution_time', 0):.1f}s")
            
            # Model usage
            st.markdown("### 🤖 Model Usage")
            model_usage = status.get('metrics', {}).get('model_usage', {})
            if model_usage:
                model_df = pd.DataFrame(list(model_usage.items()), columns=['Model', 'Usage Count'])
                st.bar_chart(model_df.set_index('Model'))
            
        except Exception as e:
            st.error(f"Error getting system status: {e}")
    
    def render_main_interface(self):
        """Render the main interface"""
        if st.session_state.analysis_running:
            self.render_analysis_progress()
        elif st.session_state.analysis_results:
            self.render_analysis_results()
        else:
            # Welcome screen
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Welcome to IntelliVest AI")
                st.markdown("""
                **IntelliVest AI** is your advanced investment thesis partner powered by:
                - 🤖 **5 Specialized AI Agents** working together
                - 🧠 **8 AI Models** with intelligent fallback system
                - 🛠️ **6 Custom Tools** for real-time data access
                - 📊 **Professional Analysis** with confidence scoring
                
                **Available Analysis Types:**
                - 🔍 **Research Analysis**: Comprehensive company research
                - 😊 **Sentiment Analysis**: Market sentiment and psychology
                - 💰 **Valuation Analysis**: Financial modeling and metrics
                - 📝 **Thesis Generation**: Professional investment thesis
                - 🎯 **Full Analysis**: Complete end-to-end analysis
                """)
            
            with col2:
                st.markdown("### 🚀 Quick Start")
                st.markdown("""
                1. Enter a company name in the sidebar
                2. Select analysis type
                3. Click "Start Analysis"
                4. Watch real-time progress
                5. Review professional results
                """)
                
                # Example companies
                st.markdown("### 💡 Example Companies")
                example_companies = ["Apple Inc.", "Tesla Inc.", "Microsoft Corporation", "Amazon.com Inc."]
                for company in example_companies:
                    if st.button(f"Analyze {company}", key=f"example_{company}"):
                        self.start_analysis(company, "research", True, True)
    
    def render_analysis_progress(self):
        """Render analysis progress"""
        st.markdown("### 🔄 Analysis in Progress")
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Progress log
        with st.expander("📋 Progress Log", expanded=True):
            progress_container = st.container()
        
        # Agent status grid
        st.markdown("### 🤖 Agent Status")
        self.render_agent_status_grid()
        
        # Update progress
        if st.session_state.progress_log:
            progress = min(len(st.session_state.progress_log) / 10, 1.0)
            progress_bar.progress(progress)
            
            with progress_container:
                for i, log_entry in enumerate(st.session_state.progress_log):
                    st.write(f"**{i+1}.** {log_entry}")
        
        # Check if analysis is complete
        if st.session_state.analysis_results:
            st.session_state.analysis_running = False
            st.rerun()
    
    def render_agent_status_grid(self):
        """Render agent status grid"""
        agents = {
            "Research Agent": "🔍",
            "Sentiment Agent": "😊", 
            "Valuation Agent": "💰",
            "Thesis Agent": "📝",
            "Critique Agent": "🔍"
        }
        
        cols = st.columns(len(agents))
        
        for i, (agent_name, emoji) in enumerate(agents.items()):
            with cols[i]:
                self.render_agent_status_card(agent_name, emoji, "waiting")
    
    def render_agent_status_card(self, agent_name: str, emoji: str, status: str):
        """Render individual agent status card"""
        status_colors = {
            "active": "🟢",
            "waiting": "🟡", 
            "completed": "🟢",
            "error": "🔴"
        }
        
        status_emoji = status_colors.get(status, "⚪")
        
        st.markdown(f"""
        <div class="agent-status agent-{status}">
            <span>{emoji} {agent_name}</span>
            <span>{status_emoji}</span>
        </div>
        """, unsafe_allow_html=True)
    
    def render_analysis_results(self):
        """Render analysis results"""
        if not st.session_state.analysis_results:
            return
        
        results = st.session_state.analysis_results
        
        st.markdown("### 📊 Analysis Results")
        
        # Results summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", results.get('status', 'Unknown'))
        
        with col2:
            st.metric("Execution Time", f"{results.get('execution_time', 0):.2f}s")
        
        with col3:
            st.metric("Confidence Score", f"{results.get('confidence_score', 0):.2f}")
        
        # Analysis content
        content = results.get('content', {})
        
        # Research Analysis
        if 'research_analysis' in content:
            self.render_research_analysis(content['research_analysis'])
        
        # Sentiment Analysis
        if 'sentiment_analysis' in content:
            self.render_sentiment_analysis(content['sentiment_analysis'])
        
        # Valuation Analysis
        if 'valuation_analysis' in content:
            self.render_valuation_analysis(content['valuation_analysis'])
        
        # Thesis Analysis
        if 'thesis_analysis' in content:
            self.render_thesis_analysis(content['thesis_analysis'])
        
        # Download results
        st.markdown("---")
        if st.button("📥 Download Results"):
            self.download_results(results)
    
    def render_research_analysis(self, research_data: Dict[str, Any]):
        """Render research analysis results"""
        st.markdown("### 🔍 Research Analysis")
        
        with st.expander("📋 Research Details", expanded=True):
            if 'business_model' in research_data:
                st.markdown("**Business Model:**")
                st.write(research_data['business_model'])
            
            if 'market_position' in research_data:
                st.markdown("**Market Position:**")
                st.write(research_data['market_position'])
            
            if 'competitive_landscape' in research_data:
                st.markdown("**Competitive Landscape:**")
                st.write(research_data['competitive_landscape'])
    
    def render_sentiment_analysis(self, sentiment_data: Dict[str, Any]):
        """Render sentiment analysis results"""
        st.markdown("### 😊 Sentiment Analysis")
        
        with st.expander("📊 Sentiment Details", expanded=True):
            if 'overall_sentiment' in sentiment_data:
                st.markdown("**Overall Sentiment:**")
                sentiment_score = sentiment_data['overall_sentiment']
                
                # Create sentiment gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = sentiment_score * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Sentiment Score (%)"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgray"},
                            {'range': [30, 70], 'color': "gray"},
                            {'range': [70, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            if 'key_insights' in sentiment_data:
                st.markdown("**Key Insights:**")
                st.write(sentiment_data['key_insights'])
    
    def render_valuation_analysis(self, valuation_data: Dict[str, Any]):
        """Render valuation analysis results"""
        st.markdown("### 💰 Valuation Analysis")
        
        with st.expander("📈 Valuation Details", expanded=True):
            if 'financial_metrics' in valuation_data:
                st.markdown("**Financial Metrics:**")
                metrics = valuation_data['financial_metrics']
                
                # Create metrics table
                metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
                st.dataframe(metrics_df, use_container_width=True)
            
            if 'valuation_assessment' in valuation_data:
                st.markdown("**Valuation Assessment:**")
                st.write(valuation_data['valuation_assessment'])
    
    def render_thesis_analysis(self, thesis_data: Dict[str, Any]):
        """Render thesis analysis results"""
        st.markdown("### 📝 Investment Thesis")
        
        with st.expander("📋 Thesis Details", expanded=True):
            if 'thesis_summary' in thesis_data:
                st.markdown("**Thesis Summary:**")
                st.markdown(thesis_data['thesis_summary'])
            
            if 'recommendation' in thesis_data:
                st.markdown("**Recommendation:**")
                recommendation = thesis_data['recommendation']
                
                # Color code recommendation
                if 'buy' in recommendation.lower():
                    st.markdown(f'<div class="status-success">{recommendation}</div>', unsafe_allow_html=True)
                elif 'sell' in recommendation.lower():
                    st.markdown(f'<div class="status-error">{recommendation}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="status-warning">{recommendation}</div>', unsafe_allow_html=True)
            
            if 'risk_assessment' in thesis_data:
                st.markdown("**Risk Assessment:**")
                st.write(thesis_data['risk_assessment'])
    
    def start_analysis(self, company_name: str, analysis_type: str, include_tools: bool, use_fallback: bool):
        """Start the analysis process"""
        if not self.intellivest_ai:
            st.error("❌ Production system not available")
            return
        
        st.session_state.analysis_running = True
        st.session_state.progress_log = []
        st.session_state.analysis_results = None
        
        # Start analysis in a separate thread
        thread = threading.Thread(
            target=self.run_analysis_thread,
            args=(company_name, analysis_type, include_tools, use_fallback)
        )
        thread.start()
        
        st.rerun()
    
    def run_analysis_thread(self, company_name: str, analysis_type: str, include_tools: bool, use_fallback: bool):
        """Run analysis in a separate thread"""
        try:
            self.update_progress(f"🎯 Starting {analysis_type} analysis for {company_name}")
            
            # Create analysis request
            request = AnalysisRequest(
                company_name=company_name,
                analysis_type=analysis_type,
                include_tools=include_tools,
                use_advanced_fallback=use_fallback
            )
            
            self.update_progress("🔄 Initializing analysis components...")
            
            # Run analysis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(self.intellivest_ai.analyze_company(request))
                
                self.update_progress("✅ Analysis completed successfully!")
                
                # Store results
                st.session_state.analysis_results = {
                    'status': result.status,
                    'execution_time': result.execution_time,
                    'confidence_score': result.confidence_score,
                    'content': result.content,
                    'metadata': result.metadata
                }
                
            finally:
                loop.close()
                
        except Exception as e:
            self.update_progress(f"❌ Analysis failed: {str(e)}")
            st.session_state.analysis_running = False
    
    def update_progress(self, message: str):
        """Update progress log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if 'progress_log' not in st.session_state:
            st.session_state.progress_log = []
        
        st.session_state.progress_log.append(log_entry)
    
    def download_results(self, results: Dict[str, Any]):
        """Download analysis results"""
        # Convert results to JSON
        results_json = json.dumps(results, indent=2, default=str)
        
        # Create download button
        st.download_button(
            label="📥 Download Results (JSON)",
            data=results_json,
            file_name=f"intellivest_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def main():
    """Main application function"""
    ui = ConsolidatedIntelliVestUI()
    
    # Render the interface
    ui.render_header()
    ui.render_sidebar()
    ui.render_system_status()
    ui.render_main_interface()

if __name__ == "__main__":
    main() 