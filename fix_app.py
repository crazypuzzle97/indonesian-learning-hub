#!/usr/bin/env python3
"""
Quick fix script for Indonesian Learning Platform
"""

import os
import re

def fix_use_container_width():
    """Fix deprecated use_container_width warnings"""
    print("🔧 Fixing deprecated use_container_width warnings...")
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Replace use_container_width=True with width='stretch'
    content = content.replace('use_container_width=True', "width='stretch'")
    
    # Replace use_container_width=False with width='content' (if any)
    content = content.replace('use_container_width=False', "width='content'")
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed use_container_width warnings")

def check_app_health():
    """Check if the app is healthy"""
    print("🏥 Checking app health...")
    
    try:
        # Test imports
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        import io
        import json
        import random
        from datetime import datetime, timedelta
        
        print("✅ All imports successful")
        
        # Test vocabulary data
        from app import VOCABULARY_DATA
        total_words = sum(len(words) for words in VOCABULARY_DATA.values())
        print(f"✅ Vocabulary data loaded: {total_words} words")
        
        # Test sentence data
        from sentences import SENTENCE_DATABASE
        total_sentences = sum(len(sentences) for sentences in SENTENCE_DATABASE.values())
        print(f"✅ Sentence data loaded: {total_sentences} sentences")
        
        print("🎉 App is healthy and ready to run!")
        return True
        
    except Exception as e:
        print(f"❌ App health check failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🇮🇩 Indonesian Learning Platform - Quick Fix")
    print("=" * 50)
    
    # Fix warnings
    fix_use_container_width()
    
    # Check health
    if check_app_health():
        print("\n🚀 Ready to run!")
        print("Run: streamlit run app.py")
        print("Or: python share.py")
    else:
        print("\n❌ Issues found. Please check the errors above.")

if __name__ == "__main__":
    main()
