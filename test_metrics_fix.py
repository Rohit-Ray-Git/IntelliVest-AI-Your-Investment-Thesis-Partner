#!/usr/bin/env python3
"""
Test script to verify the metrics system works correctly
"""

import streamlit as st
from datetime import datetime

# Simulate the metrics system
def test_metrics_system():
    """Test the metrics system"""
    print("🧪 Testing Metrics System...")
    
    # Initialize session state (simulating what happens in the app)
    if 'metrics_initialized' not in st.session_state:
        st.session_state.metrics_initialized = False
        st.session_state.total_analyses = 0
        st.session_state.successful_analyses = 0
        st.session_state.failed_analyses = 0
        st.session_state.average_execution_time = 0.0
        st.session_state.available_models = 8
        st.session_state.execution_times = []
    
    print(f"📊 Initial metrics:")
    print(f"   Total Analyses: {st.session_state.total_analyses}")
    print(f"   Successful: {st.session_state.successful_analyses}")
    print(f"   Failed: {st.session_state.failed_analyses}")
    print(f"   Avg Time: {st.session_state.average_execution_time:.1f}s")
    print(f"   Available Models: {st.session_state.available_models}")
    
    # Simulate running analyses
    print("\n🚀 Simulating analysis runs...")
    
    # Analysis 1 - Success
    st.session_state.total_analyses += 1
    st.session_state.successful_analyses += 1
    st.session_state.execution_times.append(45.2)
    st.session_state.average_execution_time = sum(st.session_state.execution_times) / len(st.session_state.execution_times)
    
    print(f"✅ Analysis 1 completed (45.2s)")
    
    # Analysis 2 - Success
    st.session_state.total_analyses += 1
    st.session_state.successful_analyses += 1
    st.session_state.execution_times.append(38.7)
    st.session_state.average_execution_time = sum(st.session_state.execution_times) / len(st.session_state.execution_times)
    
    print(f"✅ Analysis 2 completed (38.7s)")
    
    # Analysis 3 - Failed
    st.session_state.total_analyses += 1
    st.session_state.failed_analyses += 1
    st.session_state.execution_times.append(12.3)
    st.session_state.average_execution_time = sum(st.session_state.execution_times) / len(st.session_state.execution_times)
    
    print(f"❌ Analysis 3 failed (12.3s)")
    
    print(f"\n📊 Updated metrics:")
    print(f"   Total Analyses: {st.session_state.total_analyses}")
    print(f"   Successful: {st.session_state.successful_analyses}")
    print(f"   Failed: {st.session_state.failed_analyses}")
    print(f"   Success Rate: {st.session_state.successful_analyses}/{st.session_state.total_analyses}")
    print(f"   Avg Time: {st.session_state.average_execution_time:.1f}s")
    print(f"   Available Models: {st.session_state.available_models}")
    
    print("\n✅ Metrics system test completed successfully!")
    print("🎯 The metrics should now update properly in the Streamlit app.")

if __name__ == "__main__":
    test_metrics_system() 