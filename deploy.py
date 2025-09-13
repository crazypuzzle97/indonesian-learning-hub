#!/usr/bin/env python3
"""
Deployment script for Lumen Journal Indonesian Learning Platform
"""

import subprocess
import sys
import os
import socket

def get_local_ip():
    """Get the local IP address for network sharing"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import reportlab
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_local():
    """Run the application locally"""
    print("🚀 Starting Lumen Journal locally...")
    print("📍 Local URL: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")

def run_network():
    """Run the application with network access for sharing"""
    local_ip = get_local_ip()
    print("🚀 Starting Lumen Journal with network access...")
    print(f"📍 Local URL: http://localhost:8501")
    print(f"🌐 Network URL: http://{local_ip}:8501")
    print("📱 Share the network URL with friends on the same network!")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")

def show_deployment_options():
    """Show deployment options"""
    print("\n🌐 DEPLOYMENT OPTIONS FOR SHARING:")
    print("=" * 50)
    
    print("\n1️⃣ STREAMLIT CLOUD (Recommended - Free)")
    print("   • Go to: https://share.streamlit.io")
    print("   • Connect GitHub account")
    print("   • Upload your code")
    print("   • Deploy with one click!")
    
    print("\n2️⃣ HEROKU (Free tier available)")
    print("   • Create Procfile: web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0")
    print("   • Deploy with: git push heroku main")
    
    print("\n3️⃣ RAILWAY (Free tier available)")
    print("   • Connect GitHub to Railway")
    print("   • Select repository and deploy")
    print("   • Automatic deployment!")
    
    print("\n4️⃣ LOCAL NETWORK SHARING")
    print("   • Run: python deploy.py --network")
    print("   • Share the network URL with friends")

def main():
    """Main deployment function"""
    print("🇮🇩 INDONESIAN LEARNING HUB")
    print("=" * 60)
    
    if not check_dependencies():
        return
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--network":
            run_network()
        elif sys.argv[1] == "--help":
            print("\n📖 USAGE:")
            print("  python deploy.py              # Run locally")
            print("  python deploy.py --network    # Run with network access")
            print("  python deploy.py --deploy     # Show deployment options")
            print("  python deploy.py --help       # Show this help")
        elif sys.argv[1] == "--deploy":
            show_deployment_options()
        else:
            print(f"❌ Unknown option: {sys.argv[1]}")
            print("Use --help for available options")
    else:
        print("\n🎯 CHOOSE AN OPTION:")
        print("1. Run locally (localhost only)")
        print("2. Run with network access (share with friends)")
        print("3. Show deployment options")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_local()
        elif choice == "2":
            run_network()
        elif choice == "3":
            show_deployment_options()
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()