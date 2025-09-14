# PREMIUM UI COMPONENTS - SIMPLIFIED VERSION
# Advanced UI components for Indonesian Learning Hub

import streamlit as st

class PremiumUI:
    """Premium UI components with modern design and animations"""
    
    @staticmethod
    def custom_css():
        """Inject premium CSS for enhanced UI"""
        st.markdown("""
        <style>
        /* Premium Design System */
        .premium-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
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
        
        .premium-stats {
            display: flex;
            justify-content: space-around;
            background: linear-gradient(45deg, #06D6A0, #FFD23F);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
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
        
        .premium-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .premium-sentence-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #FF6B35;
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
            background: linear-gradient(90deg, #FF6B35, #FFD23F);
        }
        
        .premium-sentence-indonesian {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }
        
        .premium-sentence-english {
            font-size: 1.2rem;
            color: #7F8C8D;
            margin-bottom: 1rem;
            font-style: italic;
        }
        
        .premium-sentence-pronunciation {
            background: linear-gradient(45deg, #004E89, #FF6B35);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 1rem;
        }
        
        .premium-tag {
            background: rgba(255,107,53,0.1);
            color: #FF6B35;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-right: 0.5rem;
            display: inline-block;
            margin-bottom: 0.5rem;
        }
        
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
            <div style="margin-top: 1rem;">
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
            <div style="background: #f0f0f0; border-radius: 25px; height: 8px; overflow: hidden; margin: 1rem 0;">
                <div style="background: linear-gradient(90deg, #06D6A0, #FFD23F); height: 100%; border-radius: 25px; width: {percentage}%; transition: width 0.6s ease;"></div>
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
                    <div style="font-size: 2rem; font-weight: 700; color: #FF6B35;">
                        {metric['value']}
                    </div>
                    <div style="color: #7F8C8D; font-size: 0.9rem; text-transform: uppercase; margin-top: 0.5rem;">
                        {metric['label']}
                    </div>
                </div>
                """, unsafe_allow_html=True)