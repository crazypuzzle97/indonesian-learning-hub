#!/usr/bin/env python3
"""
Quick sharing script for Indonesian Learning Platform
"""

import subprocess
import socket
import webbrowser
import time

def get_network_ip():
    """Get the local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    print("🇮🇩 Indonesian Learning Platform - Quick Share")
    print("=" * 50)
    
    # Get network IP
    network_ip = get_network_ip()
    local_url = "http://localhost:8501"
    network_url = f"http://{network_ip}:8501"
    
    print(f"📱 Local URL: {local_url}")
    print(f"🌐 Network URL: {network_url}")
    print("=" * 50)
    
    # Start the app
    print("🚀 Starting the app...")
    print("📋 Share these URLs with others:")
    print(f"   • For you: {local_url}")
    print(f"   • For others on same WiFi: {network_url}")
    print("=" * 50)
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Open browser
    try:
        webbrowser.open(local_url)
    except:
        pass
    
    # Start Streamlit
    try:
        subprocess.run([
            "streamlit", "run", "app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped. Goodbye!")

if __name__ == "__main__":
    main()
