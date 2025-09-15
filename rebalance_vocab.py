#!/usr/bin/env python3
"""
Script to rebalance vocabulary distribution for better learning progression
"""

import re
import json

def rebalance_vocabulary():
    """Rebalance vocabulary from current 663-46-28-15 to 150-250-200-150"""
    
    # Read the current app.py file
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Execute the vocabulary data to get current structure
    exec_globals = {}
    exec(content.split('class IndonesianLearningApp:')[0], exec_globals)
    current_vocab = exec_globals['VOCABULARY_DATA']
    
    # Collect all words from all levels
    all_words = []
    for level, words in current_vocab.items():
        for word, data in words.items():
            all_words.append((word, data, level))
    
    print(f"Total words collected: {len(all_words)}")
    
    # Categorize words by complexity for redistribution
    absolute_beginner_words = []
    beginner_words = []
    intermediate_words = []
    advanced_words = []
    
    # Core essentials for Absolute Beginner (150 words)
    essential_categories = ['greetings', 'numbers', 'family', 'pronouns', 'basic_verbs']
    essential_words = ['halo', 'terima kasih', 'sama-sama', 'maaf', 'permisi', 'ya', 'tidak', 'baik',
                      'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan', 'sepuluh',
                      'saya', 'kamu', 'dia', 'kami', 'mereka', 'ini', 'itu', 'yang',
                      'ibu', 'ayah', 'anak', 'kakak', 'adik', 'nenek', 'kakek',
                      'makan', 'minum', 'tidur', 'bangun', 'pergi', 'datang', 'pulang']
    
    # Sort words by complexity and frequency
    for word, data, original_level in all_words:
        category = data.get('category', 'general')
        
        # Absolute Beginner: Most essential words
        if (word in essential_words or 
            category in essential_categories or 
            len(absolute_beginner_words) < 150 and category in ['greetings', 'numbers', 'family', 'pronouns']):
            absolute_beginner_words.append((word, data))
        
        # Beginner: Common daily vocabulary
        elif (len(beginner_words) < 250 and 
              category in ['verbs', 'time', 'places', 'transportation', 'questions', 'adjectives', 'colors', 'emotions', 'personal']):
            beginner_words.append((word, data))
        
        # Intermediate: More complex concepts
        elif (len(intermediate_words) < 200 and 
              category in ['food', 'clothing', 'house', 'body', 'animals', 'nature', 'weather', 'activities']):
            intermediate_words.append((word, data))
        
        # Advanced: Specialized vocabulary
        else:
            advanced_words.append((word, data))
    
    # Fill remaining slots if needed
    remaining_words = []
    for word, data, original_level in all_words:
        if not any(word == w[0] for w in absolute_beginner_words + beginner_words + intermediate_words + advanced_words):
            remaining_words.append((word, data))
    
    # Distribute remaining words
    while remaining_words and len(absolute_beginner_words) < 150:
        absolute_beginner_words.append(remaining_words.pop(0))
    while remaining_words and len(beginner_words) < 250:
        beginner_words.append(remaining_words.pop(0))
    while remaining_words and len(intermediate_words) < 200:
        intermediate_words.append(remaining_words.pop(0))
    while remaining_words:
        advanced_words.append(remaining_words.pop(0))
    
    print(f"Rebalanced distribution:")
    print(f"Absolute Beginner: {len(absolute_beginner_words)} words")
    print(f"Beginner: {len(beginner_words)} words")
    print(f"Intermediate: {len(intermediate_words)} words")
    print(f"Advanced: {len(advanced_words)} words")
    print(f"Total: {len(absolute_beginner_words) + len(beginner_words) + len(intermediate_words) + len(advanced_words)} words")
    
    return {
        "Absolute Beginner": dict(absolute_beginner_words),
        "Beginner": dict(beginner_words),
        "Intermediate": dict(intermediate_words),
        "Advanced": dict(advanced_words)
    }

if __name__ == "__main__":
    new_vocab = rebalance_vocabulary()
    
    # Save the rebalanced vocabulary to a JSON file for inspection
    with open('rebalanced_vocab.json', 'w') as f:
        json.dump(new_vocab, f, indent=2, ensure_ascii=False)
    
    print("Rebalanced vocabulary saved to rebalanced_vocab.json")
    print("You can now use this to update the app.py file")
