"""
💬 Q&A Interface Component
=========================

Interactive question-answering interface for IntelliVest AI.
Integrates with RAG system for intelligent responses.
"""

import streamlit as st
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

def render_qa_interface(rag_system, llm_callback, web_search_callback=None):
    """Render the Q&A interface"""
    
    # Initialize session state
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>🤔 Ask Questions About Your Investment Analysis</h2>
        <p style="color: #888; font-size: 1.1rem;">
            Get detailed insights about the analyzed company using our intelligent Q&A system
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have a current company
    if not rag_system.current_company:
        st.warning("⚠️ No company analysis available. Please generate an investment analysis first.")
        return
    
    # Company info card
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                        padding: 1rem; border-radius: 10px; color: white;">
                <h4>📊 Currently Analyzing: {rag_system.current_company}</h4>
                <p style="margin: 0; opacity: 0.9;">Ask questions about this company's analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            stats = rag_system.get_system_stats()
            st.metric("📝 Reports", stats.get('total_reports', 0))
        
        with col3:
            st.metric("💬 Questions", stats.get('total_questions', 0))
    
    st.markdown("---")
    
    # Main Q&A interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Question input
        st.markdown("### 💭 Ask Your Question")
        
        # Suggested questions
        suggested_questions = rag_system.get_suggested_questions()
        if suggested_questions:
            st.markdown("**💡 Suggested Questions:**")
            for i, question in enumerate(suggested_questions[:4]):
                if st.button(f"❓ {question}", key=f"suggest_{i}", use_container_width=True):
                    st.session_state.current_question = question
        
        # Question input field
        question = st.text_area(
            "Type your question here:",
            value=st.session_state.current_question,
            placeholder="e.g., What are the main risks facing this company?",
            height=100,
            key="question_input"
        )
        
        # Ask button
        col_ask1, col_ask2, col_ask3 = st.columns([1, 1, 1])
        with col_ask2:
            ask_button = st.button("🚀 Ask Question", use_container_width=True, type="primary")
        
        # Process question
        if ask_button and question.strip():
            with st.spinner("🤔 Analyzing your question..."):
                # Get answer from RAG system
                answer_data = rag_system.answer_question(
                    question.strip(), 
                    llm_callback, 
                    web_search_callback
                )
                
                # Store question in history
                st.session_state.qa_history.append({
                    'question': question.strip(),
                    'answer': answer_data['answer'],
                    'confidence': answer_data['confidence'],
                    'source': answer_data['source'],
                    'timestamp': datetime.now().isoformat(),
                    'company': rag_system.current_company
                })
                
                # Store in RAG system
                rag_system.store_question(
                    question.strip(),
                    answer_data['answer'],
                    answer_data['confidence']
                )
                
                # Clear current question
                st.session_state.current_question = ""
                st.rerun()
    
    with col2:
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        
        if st.session_state.qa_history:
            recent_qa = st.session_state.qa_history[-1]
            
            # Confidence indicator
            confidence = recent_qa['confidence']
            if confidence > 0.8:
                confidence_color = "🟢"
                confidence_text = "High"
            elif confidence > 0.6:
                confidence_color = "🟡"
                confidence_text = "Medium"
            else:
                confidence_color = "🔴"
                confidence_text = "Low"
            
            st.metric("Confidence", f"{confidence_color} {confidence_text}")
            
            # Source indicator
            source_emoji = {
                'stored_report': '📊',
                'web_search': '🌐',
                'no_data': '⚠️',
                'error': '❌'
            }.get(recent_qa['source'], '❓')
            
            st.metric("Source", f"{source_emoji} {recent_qa['source'].replace('_', ' ').title()}")
        
        # System status
        st.markdown("### 🔧 System Status")
        stats = rag_system.get_system_stats()
        
        status_color = "🟢" if stats.get('vector_db_status') == 'healthy' else "🔴"
        st.metric("Vector DB", f"{status_color} {stats.get('vector_db_status', 'Unknown')}")
    
    # Display latest answer
    if st.session_state.qa_history:
        st.markdown("---")
        st.markdown("### 💬 Latest Answer")
        
        latest_qa = st.session_state.qa_history[-1]
        
        # Answer card
        with st.container():
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
                <h4>❓ Question:</h4>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">{latest_qa['question']}</p>
                
                <h4>💡 Answer:</h4>
                <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                    {latest_qa['answer'].replace(chr(10), '<br>')}
                </div>
                
                <div style="margin-top: 1rem; display: flex; justify-content: space-between; opacity: 0.8;">
                    <span>🎯 Confidence: {latest_qa['confidence']:.1%}</span>
                    <span>📊 Source: {latest_qa['source'].replace('_', ' ').title()}</span>
                    <span>⏰ {datetime.fromisoformat(latest_qa['timestamp']).strftime('%H:%M')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Question history
    if len(st.session_state.qa_history) > 1:
        st.markdown("---")
        st.markdown("### 📚 Question History")
        
        # Filter history for current company
        current_company_history = [
            qa for qa in st.session_state.qa_history 
            if qa['company'] == rag_system.current_company
        ]
        
        if current_company_history:
            # Show last 5 questions
            for i, qa in enumerate(current_company_history[-5:]):
                with st.expander(f"❓ {qa['question'][:50]}...", expanded=False):
                    st.markdown(f"**Question:** {qa['question']}")
                    st.markdown(f"**Answer:** {qa['answer']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"🎯 Confidence: {qa['confidence']:.1%}")
                    with col2:
                        st.caption(f"📊 Source: {qa['source'].replace('_', ' ').title()}")
                    with col3:
                        st.caption(f"⏰ {datetime.fromisoformat(qa['timestamp']).strftime('%Y-%m-%d %H:%M')}")
    
    # Clear data option
    st.markdown("---")
    st.markdown("### 🗑️ Data Management")
    
    col_clear1, col_clear2 = st.columns(2)
    
    with col_clear1:
        if st.button("🗑️ Clear Current Company Data", type="secondary"):
            if st.confirm(f"Are you sure you want to clear all data for {rag_system.current_company}?"):
                rag_system.clear_company_data(rag_system.current_company)
                st.session_state.qa_history = [
                    qa for qa in st.session_state.qa_history 
                    if qa['company'] != rag_system.current_company
                ]
                st.success(f"✅ Cleared all data for {rag_system.current_company}")
                st.rerun()
    
    with col_clear2:
        if st.button("🔄 Clear Q&A History", type="secondary"):
            if st.confirm("Are you sure you want to clear the Q&A history?"):
                st.session_state.qa_history = []
                st.success("✅ Cleared Q&A history")
                st.rerun()

def render_qa_tab(rag_system, llm_callback, web_search_callback=None):
    """Render the Q&A tab in the main interface"""
    
    # Custom CSS for Q&A interface
    st.markdown("""
    <style>
    .qa-container {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .qa-question {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .qa-answer {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the Q&A interface
    render_qa_interface(rag_system, llm_callback, web_search_callback) 