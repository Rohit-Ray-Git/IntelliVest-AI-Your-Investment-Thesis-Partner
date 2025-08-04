#!/usr/bin/env python3
"""
🚀 IntelliVest AI - Streamlit Web Interface
===========================================

Advanced Investment Analysis with Parallel Processing
Professional UI with real-time analysis capabilities
"""

import streamlit as st
import asyncio
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configure LiteLLM environment variables before importing production system
from dotenv import load_dotenv
load_dotenv()

# Set up LiteLLM environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# Import our production system
from production_integration import ProductionIntelliVestAI, AnalysisRequest

# Page configuration
st.set_page_config(
    page_title="IntelliVest AI - Investment Analysis",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
    
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    
    .stProgress > div > div > div > div {
        background-color: #667eea;
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
</style>
""", unsafe_allow_html=True)

class IntelliVestStreamlitApp:
    """Main Streamlit application class"""
    
    def __init__(self):
        """Initialize the Streamlit app"""
        self.system = None
        self.analysis_history = []
        
        # Initialize session state for metrics
        if 'metrics_initialized' not in st.session_state:
            st.session_state.metrics_initialized = False
            st.session_state.total_analyses = 0
            st.session_state.successful_analyses = 0
            st.session_state.failed_analyses = 0
            st.session_state.average_execution_time = 0.0
            st.session_state.available_models = 8
            st.session_state.execution_times = []
            st.session_state.metrics_updated = False  # Flag to track metrics updates
        
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
        st.session_state.total_analyses += 1
        
        if result and result.status == "success":
            st.session_state.successful_analyses += 1
        else:
            st.session_state.failed_analyses += 1
        
        if result and hasattr(result, 'execution_time'):
            st.session_state.execution_times.append(result.execution_time)
            # Calculate average execution time
            if st.session_state.execution_times:
                st.session_state.average_execution_time = sum(st.session_state.execution_times) / len(st.session_state.execution_times)
    
    def update_metrics_from_system(self):
        """Update session state metrics from system status"""
        if self.system:
            try:
                status = self.system.get_system_status()
                metrics = status.get('metrics', {})
                
                # Store old values for comparison
                old_total = st.session_state.total_analyses
                old_successful = st.session_state.successful_analyses
                
                # Update metrics
                st.session_state.total_analyses = metrics.get('total_analyses', 0)
                st.session_state.successful_analyses = metrics.get('successful_analyses', 0)
                st.session_state.failed_analyses = metrics.get('failed_analyses', 0)
                st.session_state.average_execution_time = metrics.get('average_execution_time', 0.0)
                
                # Get available models from fallback system
                fallback_status = status.get('advanced_fallback_status', {})
                st.session_state.available_models = fallback_status.get('available_models', 8)
                
                st.session_state.metrics_initialized = True
                
                # Check if metrics changed
                if (old_total != st.session_state.total_analyses or 
                    old_successful != st.session_state.successful_analyses):
                    print(f"📊 Metrics updated: {old_total}→{st.session_state.total_analyses} analyses, {old_successful}→{st.session_state.successful_analyses} successful")
                else:
                    print("📊 Metrics refreshed (no changes)")
                    
            except Exception as e:
                print(f"⚠️ Could not update metrics from system: {e}")
                st.error(f"⚠️ Could not update metrics: {e}")
        else:
            st.warning("⚠️ System not available for metrics update")
    
    def render_metrics(self):
        """Render system metrics"""
        # Show success message if metrics were just updated
        if st.session_state.metrics_updated:
            st.success("✅ Metrics updated from system!")
        
        # Add refresh button
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 0.5])
        
        with col1:
            st.metric(
                "Total Analyses",
                st.session_state.total_analyses,
                help="Total number of analyses performed"
            )
        
        with col2:
            total = st.session_state.total_analyses
            successful = st.session_state.successful_analyses
            success_rate = f"{successful}/{total}" if total > 0 else "0/0"
            st.metric(
                "Success Rate",
                success_rate,
                help="Successful vs total analyses"
            )
        
        with col3:
            st.metric(
                "Avg Execution Time",
                f"{st.session_state.average_execution_time:.1f}s",
                help="Average execution time per analysis"
            )
        
        with col4:
            st.metric(
                "Available Models",
                st.session_state.available_models,
                help="Number of available AI models"
            )
        
        with col5:
            if st.button("🔄", help="Refresh metrics from system"):
                # Set flag to update metrics
                st.session_state.metrics_updated = True
                # Update metrics from system
                self.update_metrics_from_system()
                # Reset the flag
                st.session_state.metrics_updated = False
        
        # Add a small reset option for testing
        if st.session_state.total_analyses > 0:
            if st.button("🗑️ Reset Metrics", help="Reset all metrics to zero"):
                st.session_state.total_analyses = 0
                st.session_state.successful_analyses = 0
                st.session_state.failed_analyses = 0
                st.session_state.average_execution_time = 0.0
                st.session_state.execution_times = []
                st.success("��️ Metrics reset!")
    
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 IntelliVest AI</h1>
            <h3>Your Investment Thesis Partner</h3>
            <p>Advanced AI-Powered Investment Analysis with Parallel Processing</p>
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
        
        # Company input
        company_name = st.text_input(
            "🏢 Company Name or Symbol",
            placeholder="e.g., Apple Inc., AAPL, Tesla, TSLA",
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
    
    async def run_analysis_async(self, company_name: str, config: Dict, form_data: Dict):
        """Run analysis asynchronously"""
        try:
            # Create analysis request
            request = AnalysisRequest(
                company_name=company_name,
                analysis_type=config["analysis_type"],
                include_tools=config["include_tools"],
                use_advanced_fallback=config["use_advanced_fallback"],
                max_fallbacks=config["max_fallbacks"],
                budget_limit=form_data["budget_limit"]
            )
            
            # Run analysis
            result = await self.system.analyze_company(request)
            
            return result
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
            return None
    
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
            # Don't show error again - it was already shown in the main area
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
            elif "research" in content and "sentiment" in content and "valuation" in content:
                # Full analysis with separate sections
                st.markdown("### 📝 Analysis Sections")
                
                if content.get("research"):
                    st.markdown("#### 🔍 Research Analysis")
                    st.markdown(content["research"])
                
                if content.get("sentiment"):
                    st.markdown("#### 🧠 Sentiment Analysis")
                    st.markdown(content["sentiment"])
                
                if content.get("valuation"):
                    st.markdown("#### 💰 Valuation Analysis")
                    st.markdown(content["valuation"])
                
                if content.get("thesis"):
                    st.markdown("#### 📝 Investment Thesis")
                    st.markdown(content["thesis"])
                
                if content.get("critique"):
                    st.markdown("#### 🔍 Thesis Critique")
                    st.markdown(content["critique"])
            
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
                # Full analysis from CrewAI - show the complete detailed result
                st.markdown("### 🎯 Final Investment Thesis (Complete)")
                st.markdown(content["full_result"])
                
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
        else:
            # If content is a string
            content_text = str(content)
            lines = content_text.split('\n')
            for line in lines:
                line_lower = line.lower()
                if any(pattern in line_lower for pattern in ["key", "important", "significant", "recommendation", "conclusion"]):
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
                fig = px.line(
                    df,
                    x=df.index,
                    y="Time",
                    title="Analysis Execution Times",
                    labels={"Time": "Execution Time (seconds)", "index": "Analysis #"}
                )
                st.plotly_chart(fig, use_container_width=True)
    
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
    
    def run(self):
        """Main application runner"""
        # Render header
        self.render_header()
        
        # Render sidebar and get configuration
        config = self.render_sidebar()
        
        # Render metrics
        self.render_metrics()
        
        # Main content area
        tab1, tab2, tab3, tab4 = st.tabs(["🚀 Analysis", "📚 History", "🔧 Status", "ℹ️ About"])
        
        with tab1:
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
                        # Run analysis
                        status_text.text("🚀 Starting analysis...")
                        progress_bar.progress(10)
                        
                        # Run async analysis
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        status_text.text("📊 Gathering data...")
                        progress_bar.progress(30)
                        
                        result = loop.run_until_complete(
                            self.run_analysis_async(company_name, config, form_data)
                        )
                        
                        progress_bar.progress(80)
                        status_text.text("📝 Processing results...")
                        
                        # Add to history
                        if result:
                            self.analysis_history.append(result)
                        
                        # Update metrics after analysis
                        self.update_metrics_after_analysis(result)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        
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
            self.render_history()
        
        with tab3:
            self.render_system_status()
        
        with tab4:
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