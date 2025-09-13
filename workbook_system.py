"""
Interactive Workbook System for Indonesian Learning
Comprehensive practice exercises for vocabulary and sentence construction
"""

import random
from datetime import datetime

class WorkbookSystem:
    def __init__(self):
        self.exercise_types = [
            "fill_in_blank",
            "translation",
            "sentence_construction", 
            "vocabulary_matching",
            "grammar_focus",
            "conversation_practice"
        ]
        
    def generate_fill_in_blank_exercise(self, sentence_data, difficulty_level=1):
        """Generate fill-in-the-blank exercises"""
        exercises = []
        
        # Extract key words from sentence
        key_words = sentence_data.get('key_words', [])
        indonesian = sentence_data['indonesian']
        
        if len(key_words) < 2:
            return None
            
        # Choose 1-2 words to blank out based on difficulty
        words_to_blank = random.sample(key_words, min(difficulty_level, len(key_words)))
        
        # Create blanked sentence
        blanked_sentence = indonesian
        answers = {}
        
        for i, word in enumerate(words_to_blank):
            blank_placeholder = f"___{i+1}___"
            blanked_sentence = blanked_sentence.replace(word, blank_placeholder)
            answers[f"blank_{i+1}"] = word
        
        exercise = {
            "type": "fill_in_blank",
            "sentence": blanked_sentence,
            "answers": answers,
            "hint": f"Key words: {', '.join(key_words)}",
            "difficulty": difficulty_level,
            "grammar_focus": sentence_data.get('grammar_focus', ''),
            "category": sentence_data.get('category', '')
        }
        
        return exercise
    
    def generate_translation_exercise(self, sentence_data, direction="indonesian_to_english"):
        """Generate translation exercises"""
        if direction == "indonesian_to_english":
            source = sentence_data['indonesian']
            target = sentence_data['english']
            instruction = "Translate this Indonesian sentence to English:"
        else:
            source = sentence_data['english']
            target = sentence_data['indonesian']
            instruction = "Translate this English sentence to Indonesian:"
        
        exercise = {
            "type": "translation",
            "direction": direction,
            "source_text": source,
            "correct_answer": target,
            "instruction": instruction,
            "pronunciation": sentence_data.get('pronunciation', ''),
            "difficulty": sentence_data.get('difficulty', 1),
            "grammar_focus": sentence_data.get('grammar_focus', ''),
            "category": sentence_data.get('category', '')
        }
        
        return exercise
    
    def generate_sentence_construction_exercise(self, vocabulary_words, grammar_pattern):
        """Generate sentence construction exercises"""
        # Provide words and ask user to construct a sentence
        exercise = {
            "type": "sentence_construction",
            "vocabulary_words": vocabulary_words,
            "grammar_pattern": grammar_pattern,
            "instruction": f"Construct a sentence using these words: {', '.join(vocabulary_words)}",
            "pattern_explanation": grammar_pattern.get('grammar_focus', ''),
            "example": grammar_pattern.get('example', ''),
            "difficulty": grammar_pattern.get('difficulty', 1)
        }
        
        return exercise
    
    def generate_vocabulary_matching_exercise(self, word_pairs, difficulty_level=1):
        """Generate vocabulary matching exercises"""
        # Shuffle the pairs
        shuffled_pairs = word_pairs.copy()
        random.shuffle(shuffled_pairs)
        
        # Create options (correct + distractors)
        indonesian_words = [pair['indonesian'] for pair in shuffled_pairs]
        english_words = [pair['english'] for pair in shuffled_pairs]
        
        # Add some distractors for higher difficulty
        if difficulty_level > 1:
            distractors = [
                {"indonesian": "rumah", "english": "house"},
                {"indonesian": "makan", "english": "eat"},
                {"indonesian": "minum", "english": "drink"},
                {"indonesian": "pergi", "english": "go"}
            ]
            # Add 2-3 distractors
            distractors_to_add = random.sample(distractors, min(3, len(distractors)))
            for distractor in distractors_to_add:
                if distractor not in shuffled_pairs:
                    shuffled_pairs.append(distractor)
        
        exercise = {
            "type": "vocabulary_matching",
            "pairs": shuffled_pairs,
            "instruction": "Match the Indonesian words with their English translations",
            "difficulty": difficulty_level
        }
        
        return exercise
    
    def generate_grammar_focus_exercise(self, grammar_topic, sentence_examples):
        """Generate grammar-focused exercises"""
        exercise = {
            "type": "grammar_focus",
            "topic": grammar_topic,
            "examples": sentence_examples,
            "instruction": f"Study the grammar pattern: {grammar_topic}",
            "practice_sentences": [
                "Complete the following sentences using the correct grammar pattern:",
                "Identify the grammar pattern in these sentences:",
                "Transform these sentences using the new grammar pattern:"
            ]
        }
        
        return exercise
    
    def generate_conversation_practice(self, scenario, key_phrases):
        """Generate conversation practice exercises"""
        exercise = {
            "type": "conversation_practice",
            "scenario": scenario,
            "key_phrases": key_phrases,
            "instruction": f"Practice a conversation about: {scenario}",
            "suggested_responses": [
                "How would you respond in this situation?",
                "What questions would you ask?",
                "How would you express your opinion?"
            ]
        }
        
        return exercise
    
    def create_workbook_session(self, user_level="beginner", focus_areas=None, num_exercises=10):
        """Create a complete workbook session with continuous exercises"""
        if focus_areas is None:
            focus_areas = ["vocabulary", "grammar", "conversation", "translation"]
        
        session = {
            "session_id": f"workbook_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "user_level": user_level,
            "focus_areas": focus_areas,
            "exercises": [],
            "created_at": datetime.now().isoformat()
        }
        
        # Generate multiple exercises per focus area
        exercises_per_area = max(1, num_exercises // len(focus_areas))
        remaining_exercises = num_exercises % len(focus_areas)
        
        for i, area in enumerate(focus_areas):
            # Add extra exercise to some areas if there are remaining exercises
            area_exercises = exercises_per_area + (1 if i < remaining_exercises else 0)
            
            for j in range(area_exercises):
                if area == "vocabulary":
                    # Add vocabulary matching exercises
                    session["exercises"].append(self.generate_vocabulary_matching_exercise(
                        self.get_vocabulary_pairs(user_level), 
                        self.get_difficulty_for_level(user_level)
                    ))
                elif area == "grammar":
                    # Add grammar focus exercises
                    session["exercises"].append(self.generate_grammar_focus_exercise(
                        self.get_grammar_topic(user_level),
                        self.get_grammar_examples(user_level)
                    ))
                elif area == "conversation":
                    # Add conversation practice
                    session["exercises"].append(self.generate_conversation_practice(
                        self.get_conversation_scenario(user_level),
                        self.get_key_phrases(user_level)
                    ))
                elif area == "translation":
                    # Add translation exercises
                    session["exercises"].append(self.generate_translation_exercise(
                        self.get_sample_sentence(user_level),
                        "indonesian_to_english" if j % 2 == 0 else "english_to_indonesian"
                    ))
                elif area == "fill_blank":
                    # Add fill-in-the-blank exercises
                    session["exercises"].append(self.generate_fill_in_blank_exercise(
                        self.get_sample_sentence(user_level),
                        self.get_difficulty_for_level(user_level)
                    ))
                elif area == "sentence_construction":
                    # Add sentence construction exercises
                    session["exercises"].append(self.generate_sentence_construction_exercise(
                        self.get_vocabulary_words(user_level),
                        self.get_grammar_pattern(user_level)
                    ))
        
        # Shuffle exercises for variety
        random.shuffle(session["exercises"])
        
        return session
    
    def get_vocabulary_pairs(self, level):
        """Get vocabulary pairs based on level"""
        pairs = {
            "beginner": [
                {"indonesian": "makan", "english": "eat"},
                {"indonesian": "minum", "english": "drink"},
                {"indonesian": "tidur", "english": "sleep"},
                {"indonesian": "bekerja", "english": "work"},
                {"indonesian": "belajar", "english": "study"}
            ],
            "intermediate": [
                {"indonesian": "mengunjungi", "english": "visit"},
                {"indonesian": "membantu", "english": "help"},
                {"indonesian": "menjelaskan", "english": "explain"},
                {"indonesian": "mengundang", "english": "invite"},
                {"indonesian": "menyelesaikan", "english": "complete"}
            ],
            "advanced": [
                {"indonesian": "mengembangkan", "english": "develop"},
                {"indonesian": "menganalisis", "english": "analyze"},
                {"indonesian": "mengimplementasikan", "english": "implement"},
                {"indonesian": "mengoptimalkan", "english": "optimize"},
                {"indonesian": "mengintegrasikan", "english": "integrate"}
            ]
        }
        return pairs.get(level, pairs["beginner"])
    
    def get_grammar_topic(self, level):
        """Get grammar topic based on level"""
        topics = {
            "beginner": "Basic sentence structure (Subject + Verb + Object)",
            "intermediate": "Past tense with 'sudah' and 'telah'",
            "advanced": "Complex sentence structures and passive voice"
        }
        return topics.get(level, topics["beginner"])
    
    def get_grammar_examples(self, level):
        """Get grammar examples based on level"""
        examples = {
            "beginner": [
                "Saya makan nasi",
                "Dia minum kopi",
                "Kami belajar bahasa Indonesia"
            ],
            "intermediate": [
                "Saya sudah makan",
                "Dia telah pergi",
                "Kami sudah selesai belajar"
            ],
            "advanced": [
                "Buku itu dibaca oleh siswa",
                "Rumah ini dibangun tahun lalu",
                "Masalah ini harus diselesaikan segera"
            ]
        }
        return examples.get(level, examples["beginner"])
    
    def get_conversation_scenario(self, level):
        """Get conversation scenario based on level"""
        scenarios = {
            "beginner": "Introducing yourself and asking basic questions",
            "intermediate": "Ordering food at a restaurant and asking for directions",
            "advanced": "Discussing cultural topics and expressing complex opinions"
        }
        return scenarios.get(level, scenarios["beginner"])
    
    def get_key_phrases(self, level):
        """Get key phrases based on level"""
        phrases = {
            "beginner": [
                "Halo, nama saya...",
                "Apa kabar?",
                "Terima kasih"
            ],
            "intermediate": [
                "Permisi, di mana...",
                "Bolehkah saya...",
                "Menurut saya..."
            ],
            "advanced": [
                "Saya berpendapat bahwa...",
                "Dari sudut pandang saya...",
                "Hal ini menunjukkan bahwa..."
            ]
        }
        return phrases.get(level, phrases["beginner"])
    
    def get_difficulty_for_level(self, level):
        """Get difficulty number based on level"""
        difficulty_map = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3
        }
        return difficulty_map.get(level, 1)
    
    def get_sample_sentence(self, level):
        """Get sample sentence for exercises"""
        sample_sentences = {
            "beginner": {
                "indonesian": "Saya makan nasi gudeg di restoran.",
                "english": "I eat nasi gudeg at the restaurant.",
                "pronunciation": "SAH-yah MAH-kan NAH-see GOO-deg dee reh-STOR-an",
                "category": "Food",
                "grammar_focus": "Basic sentence structure",
                "key_words": ["makan", "nasi gudeg", "restoran"],
                "difficulty": 1
            },
            "intermediate": {
                "indonesian": "Saya sedang mempersiapkan presentasi untuk rapat besok.",
                "english": "I am preparing a presentation for tomorrow's meeting.",
                "pronunciation": "SAH-yah seh-DAHNG meh-per-see-AH-pan preh-sen-TAH-see oon-TOOK RAH-pat beh-SOK",
                "category": "Work",
                "grammar_focus": "Present continuous, future planning",
                "key_words": ["mempersiapkan", "presentasi", "rapat"],
                "difficulty": 2
            },
            "advanced": {
                "indonesian": "Teknologi telah mengubah cara kita berkomunikasi dengan orang lain.",
                "english": "Technology has changed the way we communicate with others.",
                "pronunciation": "Tek-NOH-lo-gee teh-LAH mehng-OO-bah CHAH-rah KEE-tah ber-ko-moo-NEE-ka-see deh-NGAN OR-ang LAH-in",
                "category": "Technology",
                "grammar_focus": "Past perfect, technology impact",
                "key_words": ["teknologi", "mengubah", "berkomunikasi"],
                "difficulty": 3
            }
        }
        return sample_sentences.get(level, sample_sentences["beginner"])
    
    def get_vocabulary_words(self, level):
        """Get vocabulary words for sentence construction"""
        words = {
            "beginner": ["saya", "makan", "nasi", "di", "rumah"],
            "intermediate": ["saya", "sedang", "belajar", "bahasa", "Indonesia", "untuk", "ujian"],
            "advanced": ["teknologi", "telah", "mengubah", "cara", "berkomunikasi", "dengan", "orang", "lain"]
        }
        return words.get(level, words["beginner"])
    
    def get_grammar_pattern(self, level):
        """Get grammar pattern for sentence construction"""
        patterns = {
            "beginner": {
                "pattern": "Saya [verb] [object] [location]",
                "example": "Saya makan nasi di rumah",
                "translation": "I eat rice at home",
                "grammar_focus": "Subject + Verb + Object + Location",
                "difficulty": 1
            },
            "intermediate": {
                "pattern": "Saya [adverb] [verb] [object] [purpose]",
                "example": "Saya sedang belajar bahasa Indonesia untuk ujian",
                "translation": "I am studying Indonesian language for the exam",
                "grammar_focus": "Present continuous + purpose",
                "difficulty": 2
            },
            "advanced": {
                "pattern": "[Subject] [auxiliary] [verb] [object] [manner]",
                "example": "Teknologi telah mengubah cara berkomunikasi dengan orang lain",
                "translation": "Technology has changed the way of communicating with others",
                "grammar_focus": "Past perfect + complex object",
                "difficulty": 3
            }
        }
        return patterns.get(level, patterns["beginner"])

# Exercise templates for different types
EXERCISE_TEMPLATES = {
    "fill_in_blank": {
        "title": "Fill in the Blank",
        "description": "Complete the sentence with the correct word",
        "icon": "✏️"
    },
    "translation": {
        "title": "Translation Practice", 
        "description": "Translate between Indonesian and English",
        "icon": "🔄"
    },
    "sentence_construction": {
        "title": "Sentence Building",
        "description": "Construct sentences using given words",
        "icon": "🏗️"
    },
    "vocabulary_matching": {
        "title": "Vocabulary Matching",
        "description": "Match Indonesian words with English translations",
        "icon": "🔗"
    },
    "grammar_focus": {
        "title": "Grammar Practice",
        "description": "Focus on specific grammar patterns",
        "icon": "📚"
    },
    "conversation_practice": {
        "title": "Conversation Practice",
        "description": "Practice real-life conversations",
        "icon": "💬"
    }
}

# Progress tracking for workbook
class WorkbookProgress:
    def __init__(self):
        self.completed_exercises = []
        self.scores = {}
        self.weak_areas = []
        self.strengths = []
    
    def record_exercise_completion(self, exercise_id, score, time_taken):
        """Record completion of an exercise"""
        self.completed_exercises.append({
            "exercise_id": exercise_id,
            "score": score,
            "time_taken": time_taken,
            "completed_at": datetime.now().isoformat()
        })
        
        # Update scores
        self.scores[exercise_id] = score
        
        # Identify weak areas
        if score < 70:  # Below 70% is considered weak
            self.weak_areas.append(exercise_id)
        elif score >= 90:  # Above 90% is considered strong
            self.strengths.append(exercise_id)
    
    def get_progress_summary(self):
        """Get overall progress summary"""
        total_exercises = len(self.completed_exercises)
        if total_exercises == 0:
            return {"message": "No exercises completed yet"}
        
        average_score = sum(self.scores.values()) / len(self.scores)
        
        return {
            "total_exercises": total_exercises,
            "average_score": round(average_score, 2),
            "weak_areas": len(self.weak_areas),
            "strengths": len(self.strengths),
            "completion_rate": f"{(total_exercises / 10) * 100:.1f}%"  # Assuming 10 exercises per session
        }
