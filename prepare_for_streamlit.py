#!/usr/bin/env python3
"""
Prepare Lumen Journal for Streamlit Cloud deployment
"""

import os
import shutil
import subprocess
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        '.streamlit/config.toml'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present!")
    return True

def check_dependencies():
    """Check if requirements.txt has all dependencies"""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_deps = ['streamlit', 'pandas', 'plotly', 'reportlab']
        missing_deps = []
        
        for dep in required_deps:
            if dep not in content:
                missing_deps.append(dep)
        
        if missing_deps:
            print("❌ Missing dependencies in requirements.txt:")
            for dep in missing_deps:
                print(f"   - {dep}")
            return False
        
        print("✅ All dependencies specified!")
        return True
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# User data (will be created at runtime)
user_data/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore file")

def show_deployment_instructions():
    """Show deployment instructions"""
    print("\n🚀 STREAMLIT CLOUD DEPLOYMENT INSTRUCTIONS:")
    print("=" * 60)
    
    print("\n1️⃣ CREATE GITHUB REPOSITORY:")
    print("   • Go to github.com and create a new repository")
    print("   • Name: lumen-journal-indonesian")
    print("   • Make it PUBLIC (required for free Streamlit Cloud)")
    print("   • Don't initialize with README (we already have one)")
    
    print("\n2️⃣ UPLOAD YOUR CODE:")
    print("   • Upload all files to your GitHub repository")
    print("   • Or use git commands:")
    print("     git init")
    print("     git add .")
    print("     git commit -m 'Initial commit'")
    print("     git remote add origin https://github.com/YOUR_USERNAME/lumen-journal-indonesian.git")
    print("     git push -u origin main")
    
    print("\n3️⃣ DEPLOY ON STREAMLIT CLOUD:")
    print("   • Go to share.streamlit.io")
    print("   • Sign in with GitHub")
    print("   • Click 'New app'")
    print("   • Repository: YOUR_USERNAME/lumen-journal-indonesian")
    print("   • Branch: main")
    print("   • Main file path: app.py")
    print("   • Click 'Deploy!'")
    
    print("\n4️⃣ SHARE YOUR APP:")
    print("   • Your app will be at: https://YOUR_APP_NAME.streamlit.app")
    print("   • Share this URL with friends worldwide!")

def main():
    """Main preparation function"""
    print("🇮🇩 INDONESIAN LEARNING HUB - STREAMLIT CLOUD PREPARATION")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ app.py not found! Please run this script from the project directory.")
        return
    
    print("\n🔍 CHECKING FILES...")
    if not check_files():
        print("\n❌ Please fix missing files before deploying!")
        return
    
    print("\n🔍 CHECKING DEPENDENCIES...")
    if not check_dependencies():
        print("\n❌ Please fix requirements.txt before deploying!")
        return
    
    print("\n📝 CREATING .GITIGNORE...")
    create_gitignore()
    
    print("\n✅ PREPARATION COMPLETE!")
    print("Your project is ready for Streamlit Cloud deployment!")
    
    show_deployment_instructions()
    
    print("\n🎉 READY TO DEPLOY!")
    print("Follow the instructions above to deploy your Indonesian learning platform!")

if __name__ == "__main__":
    main()
