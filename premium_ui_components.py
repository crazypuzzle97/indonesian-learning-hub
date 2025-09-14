# PREMIUM UI COMPONENTS
# Advanced UI components for Indonesian Learning Hub

import streamlit as st

class PremiumUI:
    """Premium UI components with modern design and animations"""
    
    @staticmethod
    def custom_css():
        """Inject premium CSS for enhanced UI"""
        st.markdown("""
        <style>
        /* Premium Color Scheme */
        :root {
            --primary-color: #FF6B35;
            --secondary-color: #004E89;
            --accent-color: #FFD23F;
            --success-color: #06D6A0;
            --warning-color: #F18F01;
            --error-color: #C73E1D;
            --text-primary: #2C3E50;
            --text-secondary: #7F8C8D;
            --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-shadow: 0 10px 30px rgba(0,0,0,0.1);
            --border-radius: 12px;
        }
        
        /* Premium App Header */
        .premium-header {
            background: var(--background-gradient);
            padding: 2rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: var(--card-shadow);
            animation: slideInDown 0.6s ease-out;
        }
        
        .premium-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .premium-header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin: 0.5rem 0 0 0;
        }
        
        /* Premium Cards */
        .premium-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
            border: 1px solid rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        /* Premium Statistics */
        .premium-stats {
            display: flex;
            justify-content: space-around;
            background: linear-gradient(45deg, var(--success-color), var(--accent-color));
            padding: 1.5rem;
            border-radius: var(--border-radius);
            margin: 1rem 0;
            color: white;
            box-shadow: var(--card-shadow);
        }
        
        .premium-stat-item {
            text-align: center;
            flex: 1;
        }
        
        .premium-stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            display: block;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .premium-stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Premium Buttons */
        .premium-button {
            background: linear-gradient(45deg, var(--primary-color), var(--warning-color));
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: var(--border-radius);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255,107,53,0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .premium-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255,107,53,0.4);
        }
        
        /* Premium Progress Bar */
        .premium-progress {
            background: #f0f0f0;
            border-radius: 25px;
            height: 8px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .premium-progress-fill {
            background: linear-gradient(90deg, var(--success-color), var(--accent-color));
            height: 100%;
            border-radius: 25px;
            transition: width 0.6s ease;
            animation: shimmer 2s infinite;
        }
        
        /* Premium Sentence Card */
        .premium-sentence-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: var(--card-shadow);
            border-left: 5px solid var(--primary-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .premium-sentence-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        }
        
        .premium-sentence-indonesian {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }
        
        .premium-sentence-english {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            font-style: italic;
        }
        
        .premium-sentence-pronunciation {
            background: linear-gradient(45deg, var(--secondary-color), var(--primary-color));
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 1rem;
        }
        
        .premium-sentence-meta {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .premium-tag {
            background: rgba(255,107,53,0.1);
            color: var(--primary-color);
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        /* Animations */
        @keyframes slideInDown {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        @keyframes fadeInUp {
            from {
                transform: translateY(30px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        @keyframes shimmer {
            0% { background-position: -200px 0; }
            100% { background-position: 200px 0; }
        }
        
        /* Premium Quiz Interface */
        .premium-quiz-container {
            background: white;
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--card-shadow);
            margin: 1rem 0;
        }
        
        .premium-quiz-question {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .premium-quiz-option {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: var(--border-radius);
            padding: 1rem 1.5rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1.1rem;
        }
        
        .premium-quiz-option:hover {
            background: rgba(255,107,53,0.1);
            border-color: var(--primary-color);
            transform: translateX(5px);
        }
        
        .premium-quiz-option.selected {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
        
        .premium-quiz-option.correct {
            background: var(--success-color);
            color: white;
            border-color: var(--success-color);
        }
        
        .premium-quiz-option.incorrect {
            background: var(--error-color);
            color: white;
            border-color: var(--error-color);
        }
        
        /* Premium Loading Animation */
        .premium-loader {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .premium-header h1 {
                font-size: 2rem;
            }
            
            .premium-sentence-indonesian {
                font-size: 1.5rem;
            }
            
            .premium-stats {
                flex-direction: column;
                gap: 1rem;
            }
        }
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {
            .premium-card {
                background: #2c3e50;
                color: white;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def premium_header(title, subtitle, stats=None):
        """Create premium header with statistics"""
        PremiumUI.custom_css()
        
        st.markdown(f"""
        <div class="premium-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if stats:
            stats_html = "<div class='premium-stats'>"
            for stat in stats:
                stats_html += f"""
                <div class='premium-stat-item'>
                    <span class='premium-stat-number'>{stat['number']}</span>
                    <span class='premium-stat-label'>{stat['label']}</span>
                </div>
                """
            stats_html += "</div>"
            st.markdown(stats_html, unsafe_allow_html=True)
    
    @staticmethod
    def premium_sentence_card(sentence_data):
        """Create premium sentence display card"""
        cultural_note = sentence_data.get('cultural_note', '')
        cultural_html = f"<div class='premium-tag'>💡 {cultural_note}</div>" if cultural_note else ""
        
        st.markdown(f"""
        <div class="premium-sentence-card">
            <div class="premium-sentence-indonesian">{sentence_data['indonesian']}</div>
            <div class="premium-sentence-english">{sentence_data['english']}</div>
            <div class="premium-sentence-pronunciation">🔊 {sentence_data['pronunciation']}</div>
            <div class="premium-sentence-meta">
                <div class="premium-tag">📚 {sentence_data['category']}</div>
                <div class="premium-tag">⚡ Level {sentence_data['difficulty']}</div>
                <div class="premium-tag">🎯 {sentence_data['grammar_focus']}</div>
                {cultural_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def premium_progress_bar(progress, total, label="Progress"):
        """Create premium animated progress bar"""
        percentage = (progress / total * 100) if total > 0 else 0
        
        st.markdown(f"""
        <div class="premium-card">
            <h4>{label}: {progress}/{total} ({percentage:.1f}%)</h4>
            <div class="premium-progress">
                <div class="premium-progress-fill" style="width: {percentage}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def premium_metric_cards(metrics):
        """Create premium metric display cards"""
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.markdown(f"""
                <div class="premium-card" style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: 700; color: var(--primary-color);">
                        {metric['value']}
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem; text-transform: uppercase;">
                        {metric['label']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
