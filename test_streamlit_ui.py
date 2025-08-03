#!/usr/bin/env python3
"""
🧪 Test Script for IntelliVest AI Streamlit UI
=============================================

This script tests the basic functionality of the Streamlit UI components.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append('.')

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ dotenv imported successfully")
    except ImportError as e:
        print(f"❌ dotenv import failed: {e}")
        return False
    
    return True

def test_streamlit_app():
    """Test if the Streamlit app can be loaded"""
    print("\n🔍 Testing Streamlit app loading...")
    
    try:
        # Test basic app
        with open('streamlit_app.py', 'r') as f:
            content = f.read()
        print("✅ Basic Streamlit app file exists and readable")
        
        # Test enhanced app
        with open('streamlit_app_enhanced.py', 'r') as f:
            content = f.read()
        print("✅ Enhanced Streamlit app file exists and readable")
        
        return True
    except FileNotFoundError as e:
        print(f"❌ Streamlit app file not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading Streamlit app: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n🔍 Testing environment configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for required API keys
        google_key = os.getenv("GOOGLE_API_KEY")
        groq_key = os.getenv("GROQ_API_KEY")
        
        if google_key:
            print("✅ Google API key configured")
        else:
            print("⚠️ Google API key not configured")
            
        if groq_key:
            print("✅ Groq API key configured")
        else:
            print("⚠️ Groq API key not configured")
            
        return True
    else:
        print("⚠️ .env file not found")
        return False

def test_plotly_chart():
    """Test if Plotly charts can be created"""
    print("\n🔍 Testing Plotly chart creation...")
    
    try:
        import plotly.graph_objects as go
        
        # Create a simple gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=75,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Test Gauge"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "lightgray"},
                    {'range': [33, 66], 'color': "gray"},
                    {'range': [66, 100], 'color': "lightgreen"}
                ]
            }
        ))
        
        print("✅ Plotly gauge chart created successfully")
        return True
    except Exception as e:
        print(f"❌ Plotly chart creation failed: {e}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("🧪 IntelliVest AI - Streamlit UI Test")
    print("="*60)
    
    # Run all tests
    tests = [
        test_imports,
        test_streamlit_app,
        test_environment,
        test_plotly_chart
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Summary
    print("="*60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Streamlit UI is ready to use.")
        print("\n🚀 To launch the UI:")
        print("   python launch_streamlit.py")
        print("   or")
        print("   streamlit run streamlit_app_enhanced.py --server.port 8503")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    print("="*60)

if __name__ == "__main__":
    main() 