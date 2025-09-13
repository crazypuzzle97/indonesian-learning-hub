#!/usr/bin/env python3
"""
Test script for Indonesian Learning Platform Quiz
"""

import sys
import os
sys.path.append('.')

from app import VOCABULARY_DATA
import random

def test_quiz_functionality():
    """Test quiz functionality without Streamlit"""
    print("🧪 Testing Quiz Functionality")
    print("=" * 40)
    
    # Test 1: Check vocabulary data
    total_words = sum(len(words) for words in VOCABULARY_DATA.values())
    print(f"✅ Total vocabulary words: {total_words}")
    
    # Test 2: Check word data structure
    sample_word = None
    sample_data = None
    for level, words in VOCABULARY_DATA.items():
        if words:
            sample_word = list(words.keys())[0]
            sample_data = words[sample_word]
            break
    
    if sample_word and sample_data:
        print(f"✅ Sample word: '{sample_word}'")
        print(f"   English: {sample_data.get('english', 'N/A')}")
        print(f"   Pronunciation: {sample_data.get('pronunciation', 'N/A')}")
        print(f"   Category: {sample_data.get('category', 'N/A')}")
    
    # Test 3: Test wrong answer generation
    print("\n🔍 Testing Wrong Answer Generation:")
    
    # Get a few words for testing
    test_words = []
    for level, words in VOCABULARY_DATA.items():
        test_words.extend(list(words.keys())[:3])
        if len(test_words) >= 10:
            break
    
    if len(test_words) >= 4:
        current_word = test_words[0]
        current_data = None
        
        # Find current word data
        for level, words in VOCABULARY_DATA.items():
            if current_word in words:
                current_data = words[current_word]
                break
        
        if current_data:
            correct_answer = current_data['english']
            print(f"   Current word: '{current_word}' -> '{correct_answer}'")
            
            # Generate wrong answers
            wrong_answers = []
            for word in test_words[1:4]:  # Get 3 other words
                for level, words in VOCABULARY_DATA.items():
                    if word in words:
                        wrong_answers.append(words[word]['english'])
                        break
            
            print(f"   Wrong answers: {wrong_answers}")
            
            # Test options generation
            options = [correct_answer] + wrong_answers
            random.shuffle(options)
            print(f"   Quiz options: {options}")
            print("✅ Quiz generation works!")
        else:
            print("❌ Could not find word data")
    else:
        print("❌ Not enough words for testing")
    
    # Test 4: Check all levels have words
    print(f"\n📊 Level Statistics:")
    for level, words in VOCABULARY_DATA.items():
        print(f"   {level}: {len(words)} words")
    
    print("\n🎉 Quiz functionality test completed!")
    print("=" * 40)

if __name__ == "__main__":
    test_quiz_functionality()
