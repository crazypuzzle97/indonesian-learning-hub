# 🇮🇩 Indonesian Learning Hub

A comprehensive, interactive Indonesian language learning platform built with Streamlit.

## 🚀 Features

### 📚 Comprehensive Grammar Library
- **5 Major Categories**: Basic Structure, Pronouns & Possession, Verbs & Tenses, Questions & Interrogatives, Numbers & Counting
- **15+ Detailed Topics** with pronunciation guides and practice exercises
- **Interactive Learning** with progress tracking and completion system
- **Smart Search** to find any grammar topic instantly

### 📝 Massive Sentence Database
- **100+ Sentences** across 4 difficulty levels (Beginner, Intermediate, Advanced, Conversational)
- **10+ Categories** including greetings, daily life, family, food, travel, business, and more
- **Rich Metadata** with pronunciation guides, grammar focus, and key words
- **Category Filtering** for organized learning

### 🎯 Interactive Learning Tools
- **Flashcards** with spaced repetition system
- **Interactive Workbook** with multiple exercise types
- **Progress Tracking** with completion metrics and study streaks
- **Quiz System** with immediate feedback
- **Profile Management** with secure PIN-based access

### 📊 Advanced Features
- **Real-time Progress Analytics** with detailed statistics
- **Level-based Content Filtering** for appropriate difficulty
- **Smart Search & Discovery** across all content
- **Modern UI** with responsive design and visual indicators

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start
1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```
4. **Open your browser** to `http://localhost:8501`

### For Sharing with Friends

#### Option 1: Local Network Sharing
1. **Find your IP address**:
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `ip addr`
2. **Run with network access**:
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```
3. **Share the URL**: `http://YOUR_IP:8501`

#### Option 2: Cloud Deployment (Recommended)

**Streamlit Cloud (Free)**
1. **Push to GitHub**:
   - Create a GitHub repository
   - Upload all files
   - Make sure `requirements.txt` is in the root
2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Deploy!

**Heroku (Free tier available)**
1. **Create `Procfile`**:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   heroku create your-app-name
   git push heroku main
   ```

**Railway (Free tier available)**
1. **Connect GitHub** to Railway
2. **Select repository** and deploy
3. **Automatic deployment** with zero configuration

## 📁 Project Structure

```
flashcards-application-cursor/
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── massive_sentence_database.py   # Comprehensive sentence data
├── comprehensive_grammar.py       # Grammar database
├── workbook_system.py             # Interactive workbook logic
├── comprehensive_sentences.py     # Additional sentence data
├── master_vocabulary.py           # Vocabulary database
├── ultimate_vocabulary.py         # Extended vocabulary
├── mega_vocabulary.py             # Large vocabulary set
├── bonus_vocabulary.py            # Additional vocabulary
└── user_data/                     # User progress data (auto-created)
    └── profiles/                  # Individual user profiles
```

## 🎯 Usage Guide

### Getting Started
1. **Create Profile**: Set up your learning profile with a PIN
2. **Choose Level**: Select appropriate difficulty level
3. **Explore Content**: Browse grammar topics and sentences
4. **Practice**: Use flashcards, workbook, and quizzes
5. **Track Progress**: Monitor your learning journey

### Learning Paths
- **Beginner**: Start with basic structure and simple sentences
- **Intermediate**: Progress to complex grammar and conversations
- **Advanced**: Master professional and academic Indonesian
- **Conversational**: Focus on practical communication skills

## 🔧 Technical Details

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **ReportLab**: PDF generation
- **JSON**: Data persistence

### Key Features
- **Session State Management**: Persistent user sessions
- **Profile Isolation**: Secure user data separation
- **Responsive Design**: Works on all devices
- **Error Handling**: Robust error management
- **Performance Optimized**: Efficient data processing

## 🤝 Sharing with Friends

### Method 1: Quick Local Sharing
```bash
# Run with network access
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

# Share this URL with friends on your network
http://YOUR_IP_ADDRESS:8501
```

### Method 2: Cloud Deployment (Best for Sharing)
1. **Streamlit Cloud** (Recommended - Free)
2. **Heroku** (Free tier available)
3. **Railway** (Free tier available)
4. **Google Cloud Run** (Pay-per-use)
5. **AWS** (Various options)

## 📞 Support

If you encounter any issues:
1. Check the terminal for error messages
2. Ensure all dependencies are installed
3. Verify Python version compatibility
4. Check file permissions

## 🎉 Enjoy Learning Indonesian!

This platform is designed to make Indonesian language learning engaging, comprehensive, and effective. Happy learning!

**Selamat belajar! (Happy learning!)** 🇮🇩✨