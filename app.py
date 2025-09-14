#!/usr/bin/env python3
"""
Simple Indonesian Language Learning App
A straightforward flashcard and vocabulary learning tool for daily practice
"""

import streamlit as st
import pandas as pd
import json
import random
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter, A4
from extended_vocabulary import EXTENDED_VOCABULARY
from mega_vocabulary import MEGA_VOCABULARY
from ultimate_vocabulary import ULTIMATE_VOCABULARY
from master_vocabulary import MASTER_VOCABULARY
from bonus_vocabulary import BONUS_VOCABULARY
from sentences import SENTENCE_DATABASE
from comprehensive_sentences import SENTENCE_DATABASE as COMPREHENSIVE_SENTENCES
from massive_sentence_database import get_massive_sentence_database
from mega_sentence_database import get_mega_sentence_database
from ultimate_sentence_database import get_ultimate_sentence_database
from premium_sentence_database import get_premium_sentence_database, get_extended_premium_sentences
from premium_ui_components import PremiumUI
from workbook_system import WorkbookSystem, WorkbookProgress, EXERCISE_TEMPLATES
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Indonesian Learning Hub",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Indonesian vocabulary database - organized by difficulty level
# Focus on most essential words for absolute beginners
VOCABULARY_DATA = {
    "Absolute Beginner": {
        # Most Essential Greetings & Basic Phrases
        "halo": {"english": "hello", "pronunciation": "ha-lo", "category": "greetings", "example": "Halo, apa kabar?"},
        "terima kasih": {"english": "thank you", "pronunciation": "te-ri-ma ka-sih", "category": "greetings", "example": "Terima kasih banyak!"},
        "sama-sama": {"english": "you're welcome", "pronunciation": "sa-ma sa-ma", "category": "greetings", "example": "Sama-sama!"},
        "maaf": {"english": "sorry", "pronunciation": "ma-af", "category": "greetings", "example": "Maaf, saya terlambat."},
        "permisi": {"english": "excuse me", "pronunciation": "per-mi-si", "category": "greetings", "example": "Permisi, boleh lewat?"},
        "ya": {"english": "yes", "pronunciation": "ya", "category": "greetings", "example": "Ya, saya mengerti."},
        "tidak": {"english": "no", "pronunciation": "ti-dak", "category": "greetings", "example": "Tidak, terima kasih."},
        "baik": {"english": "good/fine", "pronunciation": "ba-ik", "category": "greetings", "example": "Saya baik-baik saja."},
        
        # Essential Numbers 1-10
        "satu": {"english": "one", "pronunciation": "sa-tu", "category": "numbers", "example": "Satu orang"},
        "dua": {"english": "two", "pronunciation": "du-a", "category": "numbers", "example": "Dua buku"},
        "tiga": {"english": "three", "pronunciation": "ti-ga", "category": "numbers", "example": "Tiga apel"},
        "empat": {"english": "four", "pronunciation": "em-pat", "category": "numbers", "example": "Empat kursi"},
        "lima": {"english": "five", "pronunciation": "li-ma", "category": "numbers", "example": "Lima menit"},
        "enam": {"english": "six", "pronunciation": "e-nam", "category": "numbers", "example": "Enam jam"},
        "tujuh": {"english": "seven", "pronunciation": "tu-juh", "category": "numbers", "example": "Tujuh hari"},
        "delapan": {"english": "eight", "pronunciation": "de-la-pan", "category": "numbers", "example": "Delapan bulan"},
        "sembilan": {"english": "nine", "pronunciation": "sem-bi-lan", "category": "numbers", "example": "Sembilan tahun"},
        "sepuluh": {"english": "ten", "pronunciation": "se-pu-luh", "category": "numbers", "example": "Sepuluh orang"},
        
        # Most Important Pronouns
        "saya": {"english": "I/me", "pronunciation": "sa-ya", "category": "pronouns", "example": "Saya belajar bahasa Indonesia."},
        "anda": {"english": "you (formal)", "pronunciation": "an-da", "category": "pronouns", "example": "Anda dari mana?"},
        "kamu": {"english": "you (informal)", "pronunciation": "ka-mu", "category": "pronouns", "example": "Kamu tinggal di mana?"},
        "dia": {"english": "he/she", "pronunciation": "di-a", "category": "pronouns", "example": "Dia teman saya."},
        "kita": {"english": "we/us", "pronunciation": "ki-ta", "category": "pronouns", "example": "Kita pergi bersama."},
        "mereka": {"english": "they/them", "pronunciation": "me-re-ka", "category": "pronouns", "example": "Mereka dari Jakarta."},
        
        # Essential Family Words
        "ibu": {"english": "mother", "pronunciation": "i-bu", "category": "family", "example": "Ibu saya guru."},
        "ayah": {"english": "father", "pronunciation": "a-yah", "category": "family", "example": "Ayah saya dokter."},
        "anak": {"english": "child", "pronunciation": "a-nak", "category": "family", "example": "Anak saya pintar."},
        "keluarga": {"english": "family", "pronunciation": "ke-lu-ar-ga", "category": "family", "example": "Keluarga saya besar."},
        
        # Most Common Verbs
        "ada": {"english": "to be/exist", "pronunciation": "a-da", "category": "verbs", "example": "Ada banyak orang di sini."},
        "makan": {"english": "to eat", "pronunciation": "ma-kan", "category": "verbs", "example": "Saya makan nasi."},
        "minum": {"english": "to drink", "pronunciation": "mi-num", "category": "verbs", "example": "Saya minum air."},
        "pergi": {"english": "to go", "pronunciation": "per-gi", "category": "verbs", "example": "Saya pergi ke sekolah."},
        "datang": {"english": "to come", "pronunciation": "da-tang", "category": "verbs", "example": "Dia datang dari Bandung."},
        "tinggal": {"english": "to live/stay", "pronunciation": "ting-gal", "category": "verbs", "example": "Saya tinggal di Jakarta."},
        "bekerja": {"english": "to work", "pronunciation": "be-ker-ja", "category": "verbs", "example": "Saya bekerja di kantor."},
        "belajar": {"english": "to study/learn", "pronunciation": "be-la-jar", "category": "verbs", "example": "Saya belajar bahasa Indonesia."},
        
        # Essential Objects
        "air": {"english": "water", "pronunciation": "a-ir", "category": "objects", "example": "Saya minum air."},
        "makanan": {"english": "food", "pronunciation": "ma-ka-nan", "category": "objects", "example": "Makanan ini enak."},
        "rumah": {"english": "house", "pronunciation": "ru-mah", "category": "objects", "example": "Rumah saya kecil."},
        "buku": {"english": "book", "pronunciation": "bu-ku", "category": "objects", "example": "Buku ini bagus."},
        "uang": {"english": "money", "pronunciation": "u-ang", "category": "objects", "example": "Saya tidak punya uang."},
        "waktu": {"english": "time", "pronunciation": "wak-tu", "category": "objects", "example": "Waktu sudah malam."},
        
        # Essential Questions
        "apa": {"english": "what", "pronunciation": "a-pa", "category": "questions", "example": "Apa kabar?"},
        "siapa": {"english": "who", "pronunciation": "si-a-pa", "category": "questions", "example": "Siapa nama Anda?"},
        "di mana": {"english": "where", "pronunciation": "di ma-na", "category": "questions", "example": "Di mana toilet?"},
        "kapan": {"english": "when", "pronunciation": "ka-pan", "category": "questions", "example": "Kapan Anda datang?"},
        "berapa": {"english": "how much/many", "pronunciation": "be-ra-pa", "category": "questions", "example": "Berapa harganya?"},
        "bagaimana": {"english": "how", "pronunciation": "ba-gai-ma-na", "category": "questions", "example": "Bagaimana kabarnya?"},
        
        # More Essential Words
        "ini": {"english": "this", "pronunciation": "i-ni", "category": "pronouns", "example": "Ini buku saya."},
        "itu": {"english": "that", "pronunciation": "i-tu", "category": "pronouns", "example": "Itu mobil baru."},
        "di": {"english": "in/at", "pronunciation": "di", "category": "prepositions", "example": "Saya di rumah."},
        "ke": {"english": "to", "pronunciation": "ke", "category": "prepositions", "example": "Saya pergi ke sekolah."},
        "dari": {"english": "from", "pronunciation": "da-ri", "category": "prepositions", "example": "Saya dari Jakarta."},
        "dengan": {"english": "with", "pronunciation": "de-ngan", "category": "prepositions", "example": "Saya pergi dengan teman."},
        "untuk": {"english": "for", "pronunciation": "un-tuk", "category": "prepositions", "example": "Ini untuk Anda."},
        "dan": {"english": "and", "pronunciation": "dan", "category": "conjunctions", "example": "Saya dan dia pergi."},
        "atau": {"english": "or", "pronunciation": "a-tau", "category": "conjunctions", "example": "Teh atau kopi?"},
        "tetapi": {"english": "but", "pronunciation": "te-ta-pi", "category": "conjunctions", "example": "Saya lelah tetapi senang."},
        
        # Time Words
        "sekarang": {"english": "now", "pronunciation": "se-ka-rang", "category": "time", "example": "Sekarang jam berapa?"},
        "kemarin": {"english": "yesterday", "pronunciation": "ke-ma-rin", "category": "time", "example": "Kemarin saya pergi ke pasar."},
        "besok": {"english": "tomorrow", "pronunciation": "be-sok", "category": "time", "example": "Besok saya akan datang."},
        "hari ini": {"english": "today", "pronunciation": "ha-ri i-ni", "category": "time", "example": "Hari ini cuaca bagus."},
        "malam": {"english": "night", "pronunciation": "ma-lam", "category": "time", "example": "Malam ini saya tidur."},
        "pagi": {"english": "morning", "pronunciation": "pa-gi", "category": "time", "example": "Pagi ini saya bangun."},
        "siang": {"english": "afternoon", "pronunciation": "si-ang", "category": "time", "example": "Siang ini panas."},
        
        # Common Adjectives
        "besar": {"english": "big", "pronunciation": "be-sar", "category": "adjectives", "example": "Rumah ini besar."},
        "kecil": {"english": "small", "pronunciation": "ke-cil", "category": "adjectives", "example": "Anak itu kecil."},
        "tinggi": {"english": "tall/high", "pronunciation": "ting-gi", "category": "adjectives", "example": "Orang itu tinggi."},
        "pendek": {"english": "short", "pronunciation": "pen-dek", "category": "adjectives", "example": "Saya pendek."},
        "panjang": {"english": "long", "pronunciation": "pan-jang", "category": "adjectives", "example": "Rambut saya panjang."},
        "pendek": {"english": "short", "pronunciation": "pen-dek", "category": "adjectives", "example": "Jalan ini pendek."},
        "baru": {"english": "new", "pronunciation": "ba-ru", "category": "adjectives", "example": "Mobil ini baru."},
        "lama": {"english": "old", "pronunciation": "la-ma", "category": "adjectives", "example": "Rumah ini lama."},
        "muda": {"english": "young", "pronunciation": "mu-da", "category": "adjectives", "example": "Dia masih muda."},
        "tua": {"english": "old", "pronunciation": "tu-a", "category": "adjectives", "example": "Kakek saya tua."},
        "baik": {"english": "good", "pronunciation": "ba-ik", "category": "adjectives", "example": "Dia orang baik."},
        "buruk": {"english": "bad", "pronunciation": "bu-ruk", "category": "adjectives", "example": "Cuaca buruk hari ini."},
        "enak": {"english": "delicious", "pronunciation": "e-nak", "category": "adjectives", "example": "Makanan ini enak."},
        "mahal": {"english": "expensive", "pronunciation": "ma-hal", "category": "adjectives", "example": "Mobil ini mahal."},
        "murah": {"english": "cheap", "pronunciation": "mu-rah", "category": "adjectives", "example": "Harga ini murah."},
        "mudah": {"english": "easy", "pronunciation": "mu-dah", "category": "adjectives", "example": "Pekerjaan ini mudah."},
        "sulit": {"english": "difficult", "pronunciation": "su-lit", "category": "adjectives", "example": "Pelajaran ini sulit."},
        "cepat": {"english": "fast", "pronunciation": "ce-pat", "category": "adjectives", "example": "Mobil ini cepat."},
        "lambat": {"english": "slow", "pronunciation": "lam-bat", "category": "adjectives", "example": "Kereta ini lambat."},
        "jauh": {"english": "far", "pronunciation": "ja-uh", "category": "adjectives", "example": "Rumah saya jauh."},
        "dekat": {"english": "near", "pronunciation": "de-kat", "category": "adjectives", "example": "Sekolah dekat rumah."},
        "banyak": {"english": "many/much", "pronunciation": "ba-nyak", "category": "adjectives", "example": "Ada banyak orang."},
        "sedikit": {"english": "few/little", "pronunciation": "se-di-kit", "category": "adjectives", "example": "Saya punya sedikit uang."},
        "penuh": {"english": "full", "pronunciation": "pe-nuh", "category": "adjectives", "example": "Gelas ini penuh."},
        "kosong": {"english": "empty", "pronunciation": "ko-song", "category": "adjectives", "example": "Rumah ini kosong."},
        "bersih": {"english": "clean", "pronunciation": "ber-sih", "category": "adjectives", "example": "Rumah ini bersih."},
        "kotor": {"english": "dirty", "pronunciation": "ko-tor", "category": "adjectives", "example": "Pakaian ini kotor."},
        "panas": {"english": "hot", "pronunciation": "pa-nas", "category": "adjectives", "example": "Cuaca hari ini panas."},
        "dingin": {"english": "cold", "pronunciation": "ding-in", "category": "adjectives", "example": "Air ini dingin."},
        "hangat": {"english": "warm", "pronunciation": "hang-at", "category": "adjectives", "example": "Teh ini hangat."},
        "sejuk": {"english": "cool", "pronunciation": "se-juk", "category": "adjectives", "example": "Udara pagi sejuk."},
    },
    
    "Beginner": {
        # Greetings & Basic Phrases
        "selamat pagi": {"english": "good morning", "pronunciation": "se-la-mat pa-gi", "category": "greetings", "example": "Selamat pagi, Bu!"},
        "selamat siang": {"english": "good afternoon", "pronunciation": "se-la-mat si-ang", "category": "greetings", "example": "Selamat siang, Pak!"},
        "selamat malam": {"english": "good evening/night", "pronunciation": "se-la-mat ma-lam", "category": "greetings", "example": "Selamat malam!"},
        "selamat tinggal": {"english": "goodbye", "pronunciation": "se-la-mat ting-gal", "category": "greetings", "example": "Selamat tinggal, sampai jumpa!"},
        "sampai jumpa": {"english": "see you later", "pronunciation": "sam-pai jum-pa", "category": "greetings", "example": "Sampai jumpa besok!"},
        "apa kabar": {"english": "how are you", "pronunciation": "a-pa ka-bar", "category": "greetings", "example": "Apa kabar hari ini?"},
        "kabar baik": {"english": "I'm fine", "pronunciation": "ka-bar ba-ik", "category": "greetings", "example": "Kabar baik, terima kasih."},
        
        # Numbers 11-20
        "sebelas": {"english": "eleven", "pronunciation": "se-be-las", "category": "numbers", "example": "Sebelas jam"},
        "dua belas": {"english": "twelve", "pronunciation": "du-a be-las", "category": "numbers", "example": "Dua belas bulan"},
        "tiga belas": {"english": "thirteen", "pronunciation": "ti-ga be-las", "category": "numbers", "example": "Tiga belas tahun"},
        "empat belas": {"english": "fourteen", "pronunciation": "em-pat be-las", "category": "numbers", "example": "Empat belas hari"},
        "lima belas": {"english": "fifteen", "pronunciation": "li-ma be-las", "category": "numbers", "example": "Lima belas menit"},
        "enam belas": {"english": "sixteen", "pronunciation": "e-nam be-las", "category": "numbers", "example": "Enam belas orang"},
        "tujuh belas": {"english": "seventeen", "pronunciation": "tu-juh be-las", "category": "numbers", "example": "Tujuh belas buku"},
        "delapan belas": {"english": "eighteen", "pronunciation": "de-la-pan be-las", "category": "numbers", "example": "Delapan belas kursi"},
        "sembilan belas": {"english": "nineteen", "pronunciation": "sem-bi-lan be-las", "category": "numbers", "example": "Sembilan belas apel"},
        "dua puluh": {"english": "twenty", "pronunciation": "du-a pu-luh", "category": "numbers", "example": "Dua puluh tahun"},
        
        # Family & People
        "kakak": {"english": "older sibling", "pronunciation": "ka-kak", "category": "family", "example": "Kakak saya mahasiswa."},
        "adik": {"english": "younger sibling", "pronunciation": "a-dik", "category": "family", "example": "Adik saya masih kecil."},
        "nenek": {"english": "grandmother", "pronunciation": "ne-nek", "category": "family", "example": "Nenek saya sudah tua."},
        "kakek": {"english": "grandfather", "pronunciation": "ka-kek", "category": "family", "example": "Kakek saya petani."},
        "teman": {"english": "friend", "pronunciation": "te-man", "category": "people", "example": "Dia teman baik saya."},
        "guru": {"english": "teacher", "pronunciation": "gu-ru", "category": "people", "example": "Guru saya sangat baik."},
        "dokter": {"english": "doctor", "pronunciation": "dok-ter", "category": "people", "example": "Dokter ini terkenal."},
        
        # More Verbs
        "tidur": {"english": "to sleep", "pronunciation": "ti-dur", "category": "verbs", "example": "Saya tidur jam sepuluh."},
        "bangun": {"english": "to wake up", "pronunciation": "bang-un", "category": "verbs", "example": "Saya bangun pagi-pagi."},
        "mandi": {"english": "to take a bath", "pronunciation": "man-di", "category": "verbs", "example": "Saya mandi dua kali sehari."},
        "lihat": {"english": "to see/look", "pronunciation": "li-hat", "category": "verbs", "example": "Saya lihat film bagus."},
        "dengar": {"english": "to hear/listen", "pronunciation": "de-ngar", "category": "verbs", "example": "Saya dengar musik."},
        "bicara": {"english": "to speak/talk", "pronunciation": "bi-ca-ra", "category": "verbs", "example": "Saya bicara bahasa Indonesia."},
        "tahu": {"english": "to know", "pronunciation": "ta-hu", "category": "verbs", "example": "Saya tahu jawabannya."},
        "mau": {"english": "to want", "pronunciation": "ma-u", "category": "verbs", "example": "Saya mau makan nasi."},
        
        # Common Objects
        "mobil": {"english": "car", "pronunciation": "mo-bil", "category": "objects", "example": "Mobil saya biru."},
        "motor": {"english": "motorcycle", "pronunciation": "mo-tor", "category": "objects", "example": "Motor itu mahal."},
        "sepeda": {"english": "bicycle", "pronunciation": "se-pe-da", "category": "objects", "example": "Sepeda saya baru."},
        "meja": {"english": "table", "pronunciation": "me-ja", "category": "objects", "example": "Meja ini besar."},
        "kursi": {"english": "chair", "pronunciation": "kur-si", "category": "objects", "example": "Kursi itu nyaman."},
        "pintu": {"english": "door", "pronunciation": "pin-tu", "category": "objects", "example": "Pintu itu tertutup."},
        "jendela": {"english": "window", "pronunciation": "jen-de-la", "category": "objects", "example": "Jendela ini besar."},
        "lampu": {"english": "lamp/light", "pronunciation": "lam-pu", "category": "objects", "example": "Lampu ini terang."},
        
        # Colors
        "merah": {"english": "red", "pronunciation": "me-rah", "category": "colors", "example": "Bunga ini merah."},
        "biru": {"english": "blue", "pronunciation": "bi-ru", "category": "colors", "example": "Laut itu biru."},
        "hijau": {"english": "green", "pronunciation": "hi-jau", "category": "colors", "example": "Daun itu hijau."},
        "kuning": {"english": "yellow", "pronunciation": "ku-ning", "category": "colors", "example": "Matahari kuning."},
        "hitam": {"english": "black", "pronunciation": "hi-tam", "category": "colors", "example": "Malam hari hitam."},
        "putih": {"english": "white", "pronunciation": "pu-tih", "category": "colors", "example": "Salju itu putih."},
    },
    
    "Intermediate": {
        # Time & Days
        "hari": {"english": "day", "pronunciation": "ha-ri", "category": "time"},
        "minggu": {"english": "week", "pronunciation": "ming-gu", "category": "time"},
        "bulan": {"english": "month", "pronunciation": "bu-lan", "category": "time"},
        "tahun": {"english": "year", "pronunciation": "ta-hun", "category": "time"},
        "senin": {"english": "Monday", "pronunciation": "se-nin", "category": "time"},
        "selasa": {"english": "Tuesday", "pronunciation": "se-la-sa", "category": "time"},
        "rabu": {"english": "Wednesday", "pronunciation": "ra-bu", "category": "time"},
        "kamis": {"english": "Thursday", "pronunciation": "ka-mis", "category": "time"},
        "jumat": {"english": "Friday", "pronunciation": "ju-mat", "category": "time"},
        "sabtu": {"english": "Saturday", "pronunciation": "sab-tu", "category": "time"},
        
        # Colors
        "merah": {"english": "red", "pronunciation": "me-rah", "category": "colors"},
        "biru": {"english": "blue", "pronunciation": "bi-ru", "category": "colors"},
        "hijau": {"english": "green", "pronunciation": "hi-jau", "category": "colors"},
        "kuning": {"english": "yellow", "pronunciation": "ku-ning", "category": "colors"},
        "hitam": {"english": "black", "pronunciation": "hi-tam", "category": "colors"},
        "putih": {"english": "white", "pronunciation": "pu-tih", "category": "colors"},
        
        # Body Parts
        "kepala": {"english": "head", "pronunciation": "ke-pa-la", "category": "body"},
        "mata": {"english": "eye", "pronunciation": "ma-ta", "category": "body"},
        "hidung": {"english": "nose", "pronunciation": "hi-dung", "category": "body"},
        "mulut": {"english": "mouth", "pronunciation": "mu-lut", "category": "body"},
        "tangan": {"english": "hand", "pronunciation": "ta-ngan", "category": "body"},
        "kaki": {"english": "foot/leg", "pronunciation": "ka-ki", "category": "body"},
        
        # More Verbs
        "bekerja": {"english": "to work", "pronunciation": "be-ker-ja", "category": "verbs"},
        "belajar": {"english": "to study/learn", "pronunciation": "be-la-jar", "category": "verbs"},
        "bermain": {"english": "to play", "pronunciation": "ber-ma-in", "category": "verbs"},
        "berbicara": {"english": "to speak/talk", "pronunciation": "ber-bi-ca-ra", "category": "verbs"},
        "membaca": {"english": "to read", "pronunciation": "mem-ba-ca", "category": "verbs"},
        "menulis": {"english": "to write", "pronunciation": "me-nu-lis", "category": "verbs"},
    },
    
    "Advanced": {
        # Abstract Concepts
        "pikiran": {"english": "thought/mind", "pronunciation": "pi-ki-ran", "category": "abstract"},
        "perasaan": {"english": "feeling", "pronunciation": "pe-ra-sa-an", "category": "abstract"},
        "harapan": {"english": "hope", "pronunciation": "ha-ra-pan", "category": "abstract"},
        "impian": {"english": "dream", "pronunciation": "im-pi-an", "category": "abstract"},
        "kenangan": {"english": "memory", "pronunciation": "ke-na-ngan", "category": "abstract"},
        
        # Complex Verbs
        "mempertimbangkan": {"english": "to consider", "pronunciation": "mem-per-tim-bang-kan", "category": "verbs"},
        "mengembangkan": {"english": "to develop", "pronunciation": "me-nge-mbang-kan", "category": "verbs"},
        "menyampaikan": {"english": "to convey/deliver", "pronunciation": "me-nyam-pai-kan", "category": "verbs"},
        "menjelaskan": {"english": "to explain", "pronunciation": "men-je-las-kan", "category": "verbs"},
        "memahami": {"english": "to understand", "pronunciation": "me-ma-ha-mi", "category": "verbs"},
        
        # Professional Terms
        "pekerjaan": {"english": "job/work", "pronunciation": "pe-ker-ja-an", "category": "professional"},
        "perusahaan": {"english": "company", "pronunciation": "pe-ru-sa-ha-an", "category": "professional"},
        "rapat": {"english": "meeting", "pronunciation": "ra-pat", "category": "professional"},
        "proyek": {"english": "project", "pronunciation": "pro-yek", "category": "professional"},
        "tanggung jawab": {"english": "responsibility", "pronunciation": "tang-gung ja-wab", "category": "professional"},
    }
}

# Merge extended vocabulary
VOCABULARY_DATA.update(EXTENDED_VOCABULARY)
VOCABULARY_DATA.update(MEGA_VOCABULARY)
VOCABULARY_DATA.update(ULTIMATE_VOCABULARY)
VOCABULARY_DATA.update(MASTER_VOCABULARY)
VOCABULARY_DATA.update(BONUS_VOCABULARY)

class IndonesianLearningApp:
    def __init__(self):
        self.data_dir = "user_data"
        self.profiles_dir = os.path.join(self.data_dir, "profiles")
        self.workbook_system = WorkbookSystem()
        self.workbook_progress = WorkbookProgress()
        self.ensure_data_directory()
        self.init_session_state()
        
    def get_profile_files(self, profile_name):
        """Get file paths for a specific profile"""
        profile_dir = os.path.join(self.profiles_dir, profile_name)
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
        return {
            'progress': os.path.join(profile_dir, "progress.json"),
            'flashcards': os.path.join(profile_dir, "flashcards.json"),
            'sentences': os.path.join(profile_dir, "sentences.json")
        }
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
    
    def save_progress(self):
        """Save user progress to current profile"""
        if st.session_state.current_profile and st.session_state.current_profile != "Demo":
            self.save_profile_data(st.session_state.current_profile)
        return True
    
    def load_progress(self):
        """Load user progress from current profile"""
        if st.session_state.current_profile and st.session_state.current_profile != "Demo":
            self.load_profile_data(st.session_state.current_profile)
        return None
    
    def save_flashcards(self):
        """Save flashcard data to current profile"""
        if st.session_state.current_profile and st.session_state.current_profile != "Demo":
            self.save_profile_data(st.session_state.current_profile)
        return True
    
    def load_flashcards(self):
        """Load flashcard data from current profile"""
        if st.session_state.current_profile and st.session_state.current_profile != "Demo":
            self.load_profile_data(st.session_state.current_profile)
        return None
        
    def init_session_state(self):
        """Initialize session state variables"""
        # Initialize profile selection
        if 'current_profile' not in st.session_state:
            st.session_state.current_profile = None
            
        if 'user_progress' not in st.session_state:
            # Try to load saved progress
            saved_progress = self.load_progress()
            if saved_progress:
                st.session_state.user_progress = saved_progress
            else:
                st.session_state.user_progress = {
                    'words_learned': set(),
                    'daily_streak': 0,
                    'last_study_date': None,
                    'total_study_time': 0,
                    'flashcard_reviews': {},
                    'quiz_scores': [],
                    'current_level': 'Absolute Beginner',
                    'learned_words_details': {},  # Store detailed info about learned words
                    'weak_words': set(),  # Words that need more practice
                    'mastered_words': set(),  # Words fully mastered
                    'study_sessions': [],  # Track study sessions
                    'total_words_learned': 0
                }
            
        if 'flashcard_data' not in st.session_state:
            # Try to load saved flashcards
            saved_flashcards = self.load_flashcards()
            if saved_flashcards:
                st.session_state.flashcard_data = saved_flashcards
            else:
                st.session_state.flashcard_data = self.init_flashcard_data()
            
        if 'current_card' not in st.session_state:
            st.session_state.current_card = None
            
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
            
        if 'daily_goal' not in st.session_state:
            st.session_state.daily_goal = 20  # Default: 20 words per day
            
    def init_flashcard_data(self):
        """Initialize flashcard data with spaced repetition scheduling"""
        flashcard_data = {}
        for level, words in VOCABULARY_DATA.items():
            for indonesian, details in words.items():
                flashcard_data[indonesian] = {
                    'level': level,
                    'english': details['english'],
                    'pronunciation': details['pronunciation'],
                    'category': details['category'],
                    'next_review': datetime.now(),
                    'interval': 1,  # Days until next review
                    'ease_factor': 2.5,
                    'review_count': 0,
                    'correct_streak': 0
                }
        return flashcard_data
    
    def update_flashcard_schedule(self, word, difficulty):
        """Update flashcard schedule based on spaced repetition algorithm"""
        card = st.session_state.flashcard_data[word]
        card['review_count'] += 1
        
        # Save detailed word information when learned
        if word not in st.session_state.user_progress['learned_words_details']:
            st.session_state.user_progress['learned_words_details'][word] = {
                'first_learned': datetime.now().isoformat(),
                'total_reviews': 0,
                'correct_reviews': 0,
                'difficulty_history': [],
                'last_reviewed': None,
                'mastery_level': 0
            }
            st.session_state.user_progress['total_words_learned'] += 1
        
        # Update word details
        word_details = st.session_state.user_progress['learned_words_details'][word]
        word_details['total_reviews'] += 1
        word_details['last_reviewed'] = datetime.now().isoformat()
        word_details['difficulty_history'].append(difficulty)
        
        if difficulty == 'easy':
            card['correct_streak'] += 1
            card['interval'] = max(1, int(card['interval'] * card['ease_factor']))
            card['ease_factor'] = min(2.5, card['ease_factor'] + 0.1)
            word_details['correct_reviews'] += 1
            word_details['mastery_level'] = min(10, word_details['mastery_level'] + 2)
            
            # Move to mastered if mastery level is high enough
            if word_details['mastery_level'] >= 8:
                st.session_state.user_progress['mastered_words'].add(word)
                if word in st.session_state.user_progress['weak_words']:
                    st.session_state.user_progress['weak_words'].remove(word)
                    
        elif difficulty == 'medium':
            card['correct_streak'] += 1
            card['interval'] = max(1, int(card['interval'] * card['ease_factor'] * 0.8))
            word_details['correct_reviews'] += 1
            word_details['mastery_level'] = min(10, word_details['mastery_level'] + 1)
            
        else:  # hard
            card['correct_streak'] = 0
            card['interval'] = 1
            card['ease_factor'] = max(1.3, card['ease_factor'] - 0.2)
            word_details['mastery_level'] = max(0, word_details['mastery_level'] - 1)
            
            # Add to weak words if mastery level is low
            if word_details['mastery_level'] < 3:
                st.session_state.user_progress['weak_words'].add(word)
                if word in st.session_state.user_progress['mastered_words']:
                    st.session_state.user_progress['mastered_words'].remove(word)
            
        card['next_review'] = datetime.now() + timedelta(days=card['interval'])
        
        # Record study session
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'word': word,
            'difficulty': difficulty,
            'mastery_level': word_details['mastery_level']
        }
        st.session_state.user_progress['study_sessions'].append(session_data)
        
        # Auto-save progress and flashcards
        self.save_progress()
        self.save_flashcards()
        
    def get_due_cards(self, level=None):
        """Get cards that are due for review"""
        now = datetime.now()
        due_cards = []
        
        for word, card in st.session_state.flashcard_data.items():
            if level and card['level'] != level:
                continue
            if card['next_review'] <= now:
                due_cards.append(word)
                
        return due_cards
    
    def update_daily_streak(self):
        """Update daily streak counter"""
        today = datetime.now().date()
        last_date = st.session_state.user_progress.get('last_study_date')
        
        if last_date is None:
            st.session_state.user_progress['daily_streak'] = 1
        elif last_date == today:
            # Already studied today, no change
            pass
        elif last_date == today - timedelta(days=1):
            # Studied yesterday, increment streak
            st.session_state.user_progress['daily_streak'] += 1
        else:
            # Missed days, reset streak
            st.session_state.user_progress['daily_streak'] = 1
            
        st.session_state.user_progress['last_study_date'] = today
    
    def render_dashboard(self):
        """Render the simplified, engaging dashboard"""
        # Clean header
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #2E8B57; font-size: 3rem; margin: 0;'>🇮🇩 Indonesian Hub</h1>
            <p style='color: #666; font-size: 1.2rem; margin: 0.5rem 0;'>Learn Indonesian the fun way!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple progress overview
        learned_words = len(st.session_state.user_progress['words_learned'])
        streak = st.session_state.user_progress.get('study_streak', 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4CAF50, #45a049); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;'>
                <h2 style='margin: 0; font-size: 2.5rem;'>{learned_words}</h2>
                <p style='margin: 0; font-size: 1.1rem;'>Words Learned</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FF6B6B, #ee5a52); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;'>
                <h2 style='margin: 0; font-size: 2.5rem;'>{streak}</h2>
                <p style='margin: 0; font-size: 1.1rem;'>Day Streak</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            level = st.session_state.user_progress.get('current_level', 'Absolute Beginner')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4ECDC4, #44a08d); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;'>
                <h2 style='margin: 0; font-size: 2.5rem;'>{level.split()[0]}</h2>
                <p style='margin: 0; font-size: 1.1rem;'>Current Level</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show total vocabulary count and security status
        total_words = sum(len(level_words) for level_words in VOCABULARY_DATA.values())
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📚 **{total_words} Indonesian words** available for learning!")
        with col2:
            # Security and save status
            if st.session_state.current_profile and st.session_state.current_profile != "Demo":
                profile_files = self.get_profile_files(st.session_state.current_profile)
                if os.path.exists(profile_files['progress']):
                    st.success("🔒 Private & Saved")
                else:
                    st.warning("⚠️ No Saved Data")
            else:
                st.info("🚀 Demo Mode")
        st.markdown("---")
        
        # Quick stats row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Words Learned", 
                len(st.session_state.user_progress['words_learned']),
                delta=None
            )
            
        with col2:
            st.metric(
                "Daily Streak", 
                st.session_state.user_progress['daily_streak'],
                delta=None
            )
            
        with col3:
            due_count = len(self.get_due_cards())
            st.metric("Cards Due", due_count, delta=None)
            
        with col4:
            current_level = st.session_state.user_progress['current_level']
            st.metric("Current Level", current_level, delta=None)
        
        st.markdown("---")
        
        # Progress visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Learning Progress")
            
            # Progress by level
            level_progress = {}
            for level in VOCABULARY_DATA.keys():
                total_words = len(VOCABULARY_DATA[level])
                learned_words = len([w for w in st.session_state.user_progress['words_learned'] 
                                   if w in VOCABULARY_DATA[level]])
                level_progress[level] = (learned_words / total_words) * 100 if total_words > 0 else 0
            
            progress_df = pd.DataFrame(list(level_progress.items()), 
                                     columns=['Level', 'Progress'])
            
            fig = px.bar(progress_df, x='Level', y='Progress', 
                        title='Progress by Level (%)',
                        color='Progress',
                        color_continuous_scale='Viridis')
            fig.update_layout(height=300)
            st.plotly_chart(fig, width='stretch')
            
        with col2:
            st.subheader("🎯 Daily Goals")
            
            # Daily goal progress
            today_reviews = len([w for w in st.session_state.user_progress['words_learned'] 
                               if st.session_state.user_progress.get('last_study_date') == datetime.now().date()])
            
            goal_progress = min(100, (today_reviews / st.session_state.daily_goal) * 100)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = goal_progress,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Today's Progress"},
                delta = {'reference': 100},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 100], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90}}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, width='stretch')
        
        # Learning Progress Details
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Word Mastery Status")
            
            # Show mastery levels
            if st.session_state.user_progress['learned_words_details']:
                mastery_data = []
                for word, details in st.session_state.user_progress['learned_words_details'].items():
                    mastery_data.append({
                        'Word': word,
                        'Mastery Level': details['mastery_level'],
                        'Total Reviews': details['total_reviews'],
                        'Success Rate': f"{(details['correct_reviews']/details['total_reviews']*100):.1f}%" if details['total_reviews'] > 0 else "0%"
                    })
                
                mastery_df = pd.DataFrame(mastery_data)
                mastery_df = mastery_df.sort_values('Mastery Level', ascending=False)
                st.dataframe(mastery_df.head(10), width='stretch')
            else:
                st.info("Start learning words to see your mastery progress!")
        
        with col2:
            st.subheader("🎯 Focus Areas")
            
            # Weak words that need practice
            if st.session_state.user_progress['weak_words']:
                st.warning(f"⚠️ {len(st.session_state.user_progress['weak_words'])} words need more practice:")
                weak_words_list = list(st.session_state.user_progress['weak_words'])[:5]
                for word in weak_words_list:
                    st.write(f"• {word}")
                if len(st.session_state.user_progress['weak_words']) > 5:
                    st.write(f"... and {len(st.session_state.user_progress['weak_words']) - 5} more")
            else:
                st.success("🎉 No weak words! Keep up the great work!")
            
            # Mastered words
            if st.session_state.user_progress['mastered_words']:
                st.success(f"✅ {len(st.session_state.user_progress['mastered_words'])} words mastered!")
                mastered_list = list(st.session_state.user_progress['mastered_words'])[:3]
                for word in mastered_list:
                    st.write(f"• {word}")
                if len(st.session_state.user_progress['mastered_words']) > 3:
                    st.write(f"... and {len(st.session_state.user_progress['mastered_words']) - 3} more")
        
        # Action buttons
        st.markdown("---")
        # Simple, engaging navigation
        st.markdown("---")
        
        # Main learning buttons - large and colorful
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📚 Study Flashcards", use_container_width=True, type="primary"):
                st.session_state.page = 'flashcards'
                st.rerun()
        
        with col2:
            if st.button("⚔️ Battle Friends", use_container_width=True, type="secondary"):
                st.session_state.page = 'battle'
                st.rerun()
        
        # Secondary learning options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧠 Quiz", use_container_width=True):
                st.session_state.page = 'quiz'
                st.rerun()
        
        with col2:
            if st.button("📝 Sentences", use_container_width=True):
                st.session_state.page = 'sentences'
                st.rerun()
        
        with col3:
            if st.button("📖 Grammar", use_container_width=True):
                st.session_state.page = 'study'
                st.rerun()
        
        # Quick access buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.page = 'profile'
                st.rerun()
        
        with col2:
            if st.button("📊 Progress", use_container_width=True):
                st.session_state.page = 'word_database'
                st.rerun()
        
        # Review weak words button
        if st.session_state.user_progress['weak_words']:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Review Weak Words", width='stretch', type="primary"):
                    st.session_state.page = 'review_weak'
                    st.rerun()
    
    def render_flashcards(self):
        """Render simplified flashcard study interface"""
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #2E8B57; font-size: 2.5rem; margin: 0;'>📚 Study Flashcards</h1>
            <p style='color: #666; font-size: 1.1rem; margin: 0.5rem 0;'>Learn Indonesian words with spaced repetition</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple level selector
        selected_level = st.selectbox(
            "Choose your level:",
            options=list(VOCABULARY_DATA.keys()),
            index=list(VOCABULARY_DATA.keys()).index(st.session_state.user_progress['current_level'])
        )
        
        due_cards = self.get_due_cards(selected_level)
        
        if not due_cards:
            st.success("🎉 All cards in this level are up to date! Come back later or try another level.")
            if st.button("← Back to Dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
            return
        
        # Get current card
        if st.session_state.current_card is None or st.session_state.current_card not in due_cards:
            st.session_state.current_card = random.choice(due_cards)
            st.session_state.show_answer = False
        
        current_word = st.session_state.current_card
        card_data = st.session_state.flashcard_data[current_word]
        
        # Simple card display
        st.markdown("---")
        
        # Clean, simple card
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4CAF50, #45a049); padding: 3rem; border-radius: 20px; text-align: center; color: white; margin: 2rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.15);'>
            <h1 style='font-size: 4rem; margin: 0; font-weight: bold;'>{current_word}</h1>
        </div>
        """, unsafe_allow_html=True)
                
        # Answer display
        if st.session_state.show_answer:
            example_text = card_data.get('example', 'No example available')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FF6B6B, #ee5a52); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.15);'>
                <h2 style='font-size: 2.5rem; margin: 0; font-weight: bold;'>{card_data['english']}</h2>
                <p style='font-size: 1.3rem; margin: 0.5rem 0; opacity: 0.9;'>{card_data['pronunciation']}</p>
                <p style='font-size: 1.1rem; margin: 0.5rem 0; opacity: 0.8;'>Category: {card_data['category'].title()}</p>
                <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                    <p style='margin: 0; font-weight: bold;'>Example:</p>
                    <p style='margin: 0.5rem 0 0 0; font-style: italic;'>"{example_text}"</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Simple control buttons
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        with col2:
            if not st.session_state.show_answer:
                if st.button("👁️ Show Answer", use_container_width=True, type="primary"):
                    st.session_state.show_answer = True
                    st.rerun()
            else:
                st.markdown("**Rate difficulty:**")
        
        with col3:
            if st.button("➡️ Next", use_container_width=True, type="secondary"):
                st.session_state.current_card = None
                st.session_state.show_answer = False
                st.rerun()
        
        if st.session_state.show_answer:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("😊 Easy", width='stretch', type="primary"):
                    self.update_flashcard_schedule(current_word, 'easy')
                    st.session_state.user_progress['words_learned'].add(current_word)
                    self.update_daily_streak()
                    st.session_state.current_card = None
                    st.session_state.show_answer = False
                    st.rerun()
                    
            with col2:
                if st.button("🤔 Medium", width='stretch'):
                    self.update_flashcard_schedule(current_word, 'medium')
                    st.session_state.user_progress['words_learned'].add(current_word)
                    self.update_daily_streak()
                    st.session_state.current_card = None
                    st.session_state.show_answer = False
                    st.rerun()
                    
            with col3:
                if st.button("😰 Hard", width='stretch'):
                    self.update_flashcard_schedule(current_word, 'hard')
                    self.update_daily_streak()
                    st.session_state.current_card = None
                    st.session_state.show_answer = False
                    st.rerun()
        
        # Progress info
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 Cards remaining in {selected_level}: {len(due_cards)}")
        with col2:
            st.info(f"🔄 Review #{card_data['review_count'] + 1} for this card")
    
    def render_battle_mode(self):
        """Render social battle mode for competitive learning"""
        st.title("⚔️ Battle Mode")
        st.markdown("**Challenge friends and see who learns more Indonesian words!**")
        
        # Battle statistics
        learned_words = len(st.session_state.user_progress['words_learned'])
        battle_wins = st.session_state.user_progress.get('battle_wins', 0)
        battle_losses = st.session_state.user_progress.get('battle_losses', 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Words Learned", f"{learned_words:,}")
        with col2:
            st.metric("Battles Won", battle_wins)
        with col3:
            st.metric("Win Rate", f"{battle_wins/(battle_wins+battle_losses)*100:.1f}%" if (battle_wins+battle_losses) > 0 else "0%")
        
        st.markdown("---")
        
        # Battle options
        battle_mode = st.radio(
            "Choose Battle Mode:",
            ["🏠 Local Battle", "🌐 Online Battle", "🤖 Practice vs AI", "📊 Leaderboard"],
            horizontal=True
        )
        
        if battle_mode == "🏠 Local Battle":
            self.render_local_battle()
        elif battle_mode == "🌐 Online Battle":
            self.render_online_battle()
        elif battle_mode == "🤖 Practice vs AI":
            self.render_ai_battle()
        elif battle_mode == "📊 Leaderboard":
            self.render_leaderboard()
    
    def render_local_battle(self):
        """Render local multiplayer battle"""
        st.subheader("🏠 Local Battle")
        st.info("Two players can battle on the same device!")
        
        if 'battle_players' not in st.session_state:
            st.session_state.battle_players = {'player1': '', 'player2': ''}
            st.session_state.battle_scores = {'player1': 0, 'player2': 0}
            st.session_state.battle_current_player = 'player1'
            st.session_state.battle_round = 1
            st.session_state.battle_words = []
        
        # Player setup
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Player 1 Name:", value=st.session_state.battle_players['player1'], key="p1_name")
            st.session_state.battle_players['player1'] = st.session_state.p1_name
        
        with col2:
            st.text_input("Player 2 Name:", value=st.session_state.battle_players['player2'], key="p2_name")
            st.session_state.battle_players['player2'] = st.session_state.p2_name
        
        if st.session_state.battle_players['player1'] and st.session_state.battle_players['player2']:
            if st.button("🚀 Start Battle!", type="primary"):
                # Initialize battle with random words
                all_words = []
                for level_words in VOCABULARY_DATA.values():
                    all_words.extend(level_words.keys())
                
                st.session_state.battle_words = random.sample(all_words, min(10, len(all_words)))
                st.session_state.battle_current_word = 0
                st.session_state.battle_round = 1
                st.rerun()
            
            # Battle interface
            if st.session_state.battle_words:
                self.render_battle_interface()
    
    def render_battle_interface(self):
        """Render the actual battle interface"""
        current_word = st.session_state.battle_words[st.session_state.battle_current_word]
        current_player = st.session_state.battle_current_player
        player_name = st.session_state.battle_players[current_player]
        
        st.markdown(f"### Round {st.session_state.battle_round} - {player_name}'s Turn")
        
        # Word display
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FF6B6B, #ee5a52); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;'>
            <h1 style='font-size: 3rem; margin: 0;'>{current_word}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        answer = st.text_input("What does this word mean in English?", key=f"battle_answer_{st.session_state.battle_current_word}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Submit Answer", type="primary"):
                # Check answer
                correct_answer = VOCABULARY_DATA.get('Absolute Beginner', {}).get(current_word, {}).get('english', 'Unknown')
                if answer.lower().strip() == correct_answer.lower().strip():
                    st.session_state.battle_scores[current_player] += 1
                    st.success(f"✅ Correct! +1 point for {player_name}")
                else:
                    st.error(f"❌ Wrong! The answer was: {correct_answer}")
                
                # Move to next word or end battle
                st.session_state.battle_current_word += 1
                if st.session_state.battle_current_word >= len(st.session_state.battle_words):
                    # End battle
                    self.end_battle()
                else:
                    # Switch players
                    st.session_state.battle_current_player = 'player2' if current_player == 'player1' else 'player1'
                    st.session_state.battle_round += 1
                    st.rerun()
        
        with col2:
            if st.button("⏭️ Skip Word"):
                st.session_state.battle_current_word += 1
                if st.session_state.battle_current_word >= len(st.session_state.battle_words):
                    self.end_battle()
                else:
                    st.session_state.battle_current_player = 'player2' if current_player == 'player1' else 'player1'
                    st.session_state.battle_round += 1
                    st.rerun()
        
        # Show current scores
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"{st.session_state.battle_players['player1']}", st.session_state.battle_scores['player1'])
        with col2:
            st.metric(f"{st.session_state.battle_players['player2']}", st.session_state.battle_scores['player2'])
    
    def end_battle(self):
        """End the battle and show results"""
        p1_score = st.session_state.battle_scores['player1']
        p2_score = st.session_state.battle_scores['player2']
        p1_name = st.session_state.battle_players['player1']
        p2_name = st.session_state.battle_players['player2']
        
        st.markdown("## 🏆 Battle Results!")
        
        if p1_score > p2_score:
            winner = p1_name
            st.session_state.user_progress['battle_wins'] = st.session_state.user_progress.get('battle_wins', 0) + 1
        elif p2_score > p1_score:
            winner = p2_name
            st.session_state.user_progress['battle_losses'] = st.session_state.user_progress.get('battle_losses', 0) + 1
        else:
            winner = "It's a tie!"
        
        st.markdown(f"### 🎉 {winner} wins!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"{p1_name}", p1_score)
        with col2:
            st.metric(f"{p2_name}", p2_score)
        
        if st.button("🔄 Play Again"):
            st.session_state.battle_words = []
            st.session_state.battle_current_word = 0
            st.session_state.battle_round = 1
            st.session_state.battle_scores = {'player1': 0, 'player2': 0}
            st.session_state.battle_current_player = 'player1'
            st.rerun()
    
    def render_online_battle(self):
        """Render online battle mode"""
        st.subheader("🌐 Online Battle")
        st.info("Coming soon! Challenge friends from anywhere in the world.")
        
        # Placeholder for online features
        st.markdown("""
        ### Features Coming Soon:
        - 🔗 Share battle links with friends
        - 🌍 Global leaderboards
        - 🏆 Tournaments and competitions
        - 💬 Chat during battles
        - 📱 Mobile-optimized battles
        """)
    
    def render_ai_battle(self):
        """Render AI practice battle"""
        st.subheader("🤖 Practice vs AI")
        st.info("Practice your skills against our AI opponent!")
        
        if st.button("🎯 Start AI Battle", type="primary"):
            st.session_state.page = 'ai_battle'
            st.rerun()
    
    def render_leaderboard(self):
        """Render leaderboard"""
        st.subheader("📊 Global Leaderboard")
        
        # Mock leaderboard data
        leaderboard_data = [
            {"rank": 1, "name": "IndonesianMaster", "words": 1250, "battles_won": 45},
            {"rank": 2, "name": "BaliExplorer", "words": 1100, "battles_won": 38},
            {"rank": 3, "name": "JakartaLearner", "words": 980, "battles_won": 32},
            {"rank": 4, "name": "SurabayaStudent", "words": 850, "battles_won": 28},
            {"rank": 5, "name": "BandungBuddy", "words": 720, "battles_won": 25},
        ]
        
        for player in leaderboard_data:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                st.markdown(f"**#{player['rank']}**")
            with col2:
                st.markdown(f"**{player['name']}**")
            with col3:
                st.markdown(f"{player['words']} words")
            with col4:
                st.markdown(f"{player['battles_won']} wins")

    def render_quiz(self):
        """Render premium quiz interface"""
        st.title("🧠 Enhanced Vocabulary Quiz")
        st.markdown("**Test your Indonesian vocabulary with intelligent questions and detailed feedback**")
        
        # Quiz statistics
        learned_words = len(st.session_state.user_progress['words_learned'])
        quiz_scores = st.session_state.user_progress.get('quiz_scores', [])
        avg_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Words Available", f"{learned_words:,}")
        with col2:
            st.metric("Quizzes Completed", len(quiz_scores))
        with col3:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col4:
            st.metric("Question System", "AI-Powered")
        
        if 'quiz_words' not in st.session_state:
            # Initialize quiz with 10 random words from learned vocabulary
            learned_words = list(st.session_state.user_progress['words_learned'])
            if len(learned_words) < 3:
                st.warning("Learn at least 3 words before taking a quiz!")
                if st.button("← Back to Dashboard"):
                    st.session_state.page = 'dashboard'
                    st.rerun()
                return
            
            # Ensure we have valid words for the quiz
            valid_words = []
            for word in learned_words:
                # Check if word exists in vocabulary data
                word_found = False
                for level, words in VOCABULARY_DATA.items():
                    if word in words:
                        valid_words.append(word)
                        word_found = True
                        break
                if not word_found:
                    st.warning(f"Word '{word}' not found in vocabulary data, skipping...")
            
            if len(valid_words) < 3:
                st.error("Not enough valid words for a quiz. Please learn more words first!")
                if st.button("← Back to Dashboard"):
                    st.session_state.page = 'dashboard'
                    st.rerun()
                return
                
            st.session_state.quiz_words = random.sample(valid_words, min(10, len(valid_words)))
            st.session_state.quiz_current = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = []
        
        current_idx = st.session_state.quiz_current
        
        if current_idx >= len(st.session_state.quiz_words):
            # Quiz complete
            score_percentage = (st.session_state.quiz_score / len(st.session_state.quiz_words)) * 100
            st.session_state.user_progress['quiz_scores'].append(score_percentage)
            
            st.success(f"🎉 Quiz Complete!")
            st.metric("Final Score", f"{st.session_state.quiz_score}/{len(st.session_state.quiz_words)}", 
                     f"{score_percentage:.1f}%")
            
            if score_percentage >= 80:
                st.balloons()
                st.success("Excellent work! 🌟")
            elif score_percentage >= 60:
                st.success("Good job! 👍")
            else:
                st.info("Keep practicing! 💪")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Take Another Quiz"):
                    for key in ['quiz_words', 'quiz_current', 'quiz_score', 'quiz_answers']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            with col2:
                if st.button("← Back to Dashboard"):
                    for key in ['quiz_words', 'quiz_current', 'quiz_score', 'quiz_answers']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.session_state.page = 'dashboard'
                    st.rerun()
            return
        
        # Current question
        current_word = st.session_state.quiz_words[current_idx]
        
        # Get word data from vocabulary or flashcard data
        if current_word in st.session_state.flashcard_data:
            card_data = st.session_state.flashcard_data[current_word]
        else:
            # Find word in vocabulary data
            card_data = None
            for level, words in VOCABULARY_DATA.items():
                if current_word in words:
                    card_data = words[current_word]
                    card_data['level'] = level
                    break
            
            if not card_data:
                st.error(f"Word '{current_word}' not found in vocabulary data!")
                st.session_state.quiz_current += 1
                st.rerun()
                return
        
        st.progress((current_idx + 1) / len(st.session_state.quiz_words))
        st.subheader(f"Question {current_idx + 1} of {len(st.session_state.quiz_words)}")
        
        # Question display with better contrast and styling
        st.markdown(
            f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            '>
                <h2 style='color: white; margin: 0; font-size: 2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                    What does "{current_word}" mean in English?
                </h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                    Choose the correct translation
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Generate multiple choice options
        correct_answer = card_data['english']
        
        # Get wrong answers from same level or any level
        wrong_answers = []
        
        # Try to get words from same level first
        same_level_words = []
        for w, data in st.session_state.flashcard_data.items():
            if data.get('level') == card_data.get('level') and w != current_word:
                same_level_words.append(data['english'])
        
        # If not enough words from same level, get from any level
        if len(same_level_words) < 3:
            all_other_words = []
            for level, words in VOCABULARY_DATA.items():
                for w, data in words.items():
                    if w != current_word and data['english'] != correct_answer:
                        all_other_words.append(data['english'])
            
            # Remove duplicates and add to same_level_words
            same_level_words.extend([w for w in all_other_words if w not in same_level_words])
        
        # Select wrong answers
        wrong_answers = random.sample(same_level_words, min(3, len(same_level_words)))
        
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        # Answer selection with better styling
        st.markdown("### Choose the correct answer:")
        selected_answer = st.radio("", options, key=f"quiz_{current_idx}")
        
        # Add hint button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💡 Get Hint", width='stretch'):
                st.info(f"💡 Hint: The word '{current_word}' is related to '{card_data.get('category', 'general')}' category")
        
        # Submit button with better styling - only proceed if answer is selected
        if st.button("Submit Answer", width='stretch', type="primary"):
            if not selected_answer:
                st.warning("Please select an answer before submitting!")
                return
            if selected_answer == correct_answer:
                st.session_state.quiz_score += 1
                st.markdown(
                    f"""
                    <div style='
                        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                        padding: 1.5rem;
                        border-radius: 10px;
                        text-align: center;
                        margin: 1rem 0;
                        box-shadow: 0 2px 10px rgba(76,175,80,0.3);
                    '>
                        <h3 style='color: white; margin: 0;'>✅ Correct! Well done!</h3>
                        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
                            "{current_word}" means "{correct_answer}"
                        </p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style='
                        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
                        padding: 1.5rem;
                        border-radius: 10px;
                        text-align: center;
                        margin: 1rem 0;
                        box-shadow: 0 2px 10px rgba(244,67,54,0.3);
                    '>
                        <h3 style='color: white; margin: 0;'>❌ Not quite right</h3>
                        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
                            The correct answer is: <strong>"{correct_answer}"</strong>
                        </p>
                        <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                            You selected: "{selected_answer}"
                        </p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            st.session_state.quiz_answers.append({
                'word': current_word,
                'correct': correct_answer,
                'selected': selected_answer,
                'is_correct': selected_answer == correct_answer
            })
            
            # Show result and wait for user to continue
            st.session_state.quiz_current += 1
            
            # Add continue button instead of auto-advance
            if st.session_state.quiz_current < len(st.session_state.quiz_words):
                st.info("⏳ Click 'Continue' to proceed to the next question...")
                if st.button("➡️ Continue to Next Question", width='stretch', type="primary"):
                    st.rerun()
            else:
                st.rerun()
    
    def render_weak_words_review(self):
        """Render enhanced weak words review interface"""
        st.title("🔄 Review Weak Words")
        
        weak_words = list(st.session_state.user_progress['weak_words'])
        
        if not weak_words:
            st.markdown(
                """
                <div style='
                    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    text-align: center;
                    margin: 1rem 0;
                    box-shadow: 0 4px 15px rgba(76,175,80,0.3);
                '>
                    <h2 style='color: white; margin: 0;'>🎉 No weak words to review!</h2>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                        You're doing great! Keep up the excellent work!
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button("← Back to Dashboard", width='stretch'):
                st.session_state.page = 'dashboard'
                st.rerun()
            return
        
        # Enhanced weak words display with priority sorting
        st.subheader(f"🎯 Words that need more practice ({len(weak_words)} total)")
        
        # Sort weak words by priority (mastery level, success rate, last reviewed)
        def calculate_priority(word):
            if word not in st.session_state.user_progress['learned_words_details']:
                return 0
            details = st.session_state.user_progress['learned_words_details'][word]
            mastery = details.get('mastery_level', 0)
            success_rate = details.get('correct_reviews', 0) / max(details.get('total_reviews', 1), 1)
            return (10 - mastery) * 0.6 + (1 - success_rate) * 0.4
        
        weak_words_sorted = sorted(weak_words, key=calculate_priority, reverse=True)
        
        # Show top 10 weak words with enhanced display
        for i, word in enumerate(weak_words_sorted[:10]):
            if word in st.session_state.user_progress['learned_words_details']:
                details = st.session_state.user_progress['learned_words_details'][word]
                
                # Get word data
                card_data = None
                for level, words in VOCABULARY_DATA.items():
                    if word in words:
                        card_data = words[word]
                        break
                
                if not card_data:
                    continue
                
                # Calculate priority score
                priority_score = calculate_priority(word)
                mastery_level = details.get('mastery_level', 0)
                success_rate = details.get('correct_reviews', 0) / max(details.get('total_reviews', 1), 1)
                
                # Color coding based on priority
                if priority_score > 7:
                    priority_color = "#f44336"  # High priority - red
                    priority_text = "🔴 High Priority"
                elif priority_score > 4:
                    priority_color = "#ff9800"  # Medium priority - orange
                    priority_text = "🟡 Medium Priority"
                else:
                    priority_color = "#4CAF50"  # Low priority - green
                    priority_text = "🟢 Low Priority"
                
                with st.expander(f"{i+1}. {word} - {priority_text} (Mastery: {mastery_level}/10)"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📚 Word Details:**")
                        st.write(f"**English:** {card_data['english']}")
                        st.write(f"**Pronunciation:** /{card_data['pronunciation']}/")
                        st.write(f"**Category:** {card_data['category'].title()}")
                        if 'example' in card_data:
                            st.write(f"**Example:** {card_data['example']}")
                    
                    with col2:
                        st.markdown("**📊 Statistics:**")
                        st.write(f"**Total Reviews:** {details.get('total_reviews', 0)}")
                        st.write(f"**Success Rate:** {success_rate:.1%}")
                        st.write(f"**Last Reviewed:** {details.get('last_reviewed', 'Never')[:10] if details.get('last_reviewed') else 'Never'}")
                        
                        # Progress bar for mastery
                        st.progress(mastery_level / 10)
                        st.caption(f"Mastery Progress: {mastery_level}/10")
                    
                    with col3:
                        st.markdown("**🎯 Practice Options:**")
                        
                        # Practice buttons with different modes
                        if st.button(f"📚 Flashcard", key=f"flashcard_{word}", width='stretch'):
                            st.session_state.current_card = word
                            st.session_state.show_answer = False
                            st.session_state.page = 'flashcards'
                            st.rerun()
                        
                        if st.button(f"🧠 Quiz", key=f"quiz_{word}", width='stretch'):
                            st.session_state.quiz_words = [word]
                            st.session_state.quiz_current = 0
                            st.session_state.quiz_score = 0
                            st.session_state.quiz_answers = []
                            st.session_state.page = 'quiz'
                            st.rerun()
                        
                        if st.button(f"✍️ Write", key=f"write_{word}", width='stretch'):
                            st.session_state.practice_word = word
                            st.session_state.practice_mode = 'writing'
                            st.rerun()
        
        if len(weak_words_sorted) > 10:
            st.info(f"📋 ... and {len(weak_words_sorted) - 10} more weak words")
        
        # Enhanced action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Practice All Weak Words", width='stretch', type="primary"):
                st.session_state.weak_words_practice = weak_words_sorted.copy()
                st.session_state.weak_word_index = 0
                st.session_state.page = 'flashcards'
                st.rerun()
        
        with col2:
            if st.button("🧠 Quiz Weak Words", width='stretch'):
                st.session_state.quiz_words = weak_words_sorted[:10]  # Quiz top 10
                st.session_state.quiz_current = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
                st.session_state.page = 'quiz'
                st.rerun()
        
        with col3:
            if st.button("← Back to Dashboard", width='stretch'):
                st.session_state.page = 'dashboard'
                st.rerun()
    
    def render_word_database(self):
        """Render comprehensive word database view"""
        st.title("📊 Word Database")
        
        # Search and filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Search words:", placeholder="Type Indonesian or English word...")
        
        with col2:
            category_filter = st.selectbox("📂 Filter by category:", 
                                         ["All"] + list(set([data['category'] for data in VOCABULARY_DATA.values() for data in data.values()])))
        
        with col3:
            level_filter = st.selectbox("📚 Filter by level:", 
                                      ["All"] + list(VOCABULARY_DATA.keys()))
        
        # Get all learned words
        learned_words = st.session_state.user_progress['learned_words_details']
        
        if not learned_words:
            st.info("No words learned yet! Start studying flashcards to build your database.")
            if st.button("← Back to Dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
            return
        
        # Filter words based on search and filters
        filtered_words = []
        for word, details in learned_words.items():
            # Find the word in vocabulary data
            word_data = None
            for level, words in VOCABULARY_DATA.items():
                if word in words:
                    word_data = words[word]
                    word_level = level
                    break
            
            if not word_data:
                continue
                
            # Apply filters
            if level_filter != "All" and word_level != level_filter:
                continue
                
            if category_filter != "All" and word_data['category'] != category_filter:
                continue
                
            if search_term and search_term.lower() not in word.lower() and search_term.lower() not in word_data['english'].lower():
                continue
                
            filtered_words.append({
                'Indonesian': word,
                'English': word_data['english'],
                'Pronunciation': word_data['pronunciation'],
                'Category': word_data['category'].title(),
                'Level': word_level,
                'Mastery': details['mastery_level'],
                'Reviews': details['total_reviews'],
                'Success Rate': f"{(details['correct_reviews']/details['total_reviews']*100):.1f}%" if details['total_reviews'] > 0 else "0%",
                'Example': word_data.get('example', 'No example available'),
                'Last Reviewed': details['last_reviewed'][:10] if details['last_reviewed'] else 'Never'
            })
        
        # Sort by mastery level (highest first)
        filtered_words.sort(key=lambda x: x['Mastery'], reverse=True)
        
        st.subheader(f"📚 Your Learned Words ({len(filtered_words)} words)")
        
        if filtered_words:
            # Create DataFrame for better display
            df = pd.DataFrame(filtered_words)
            
            # Display with options
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.dataframe(df, width='stretch', height=400)
            
            with col2:
                st.subheader("📊 Quick Stats")
                st.metric("Total Words", len(filtered_words))
                st.metric("Mastered Words", len([w for w in filtered_words if w['Mastery'] >= 8]))
                st.metric("Average Mastery", f"{sum(w['Mastery'] for w in filtered_words)/len(filtered_words):.1f}/10")
                
                # Export options
                st.subheader("📤 Export")
                if st.button("📄 Export to CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"indonesian_words_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                if st.button("📋 Copy to Clipboard"):
                    st.code(df.to_string(index=False), language=None)
                    st.success("Copied to clipboard!")
        else:
            st.warning("No words match your search criteria.")
        
        # Word review options
        st.markdown("---")
        st.subheader("🔄 Review Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Review All Words", width='stretch'):
                st.session_state.page = 'flashcards'
                st.rerun()
        
        with col2:
            if st.button("🎯 Review Weak Words", width='stretch'):
                st.session_state.page = 'review_weak'
                st.rerun()
        
        with col3:
            if st.button("📝 Take Quiz", width='stretch'):
                st.session_state.page = 'quiz'
                st.rerun()
        
        st.markdown("---")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    def render_profile(self):
        """Render user profile page"""
        st.title("👤 User Profile")
        
        # Profile creation/editing
        with st.expander("✏️ Edit Profile", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name:", value=st.session_state.user_progress.get('profile_name', ''))
                email = st.text_input("Email:", value=st.session_state.user_progress.get('profile_email', ''))
                learning_goal = st.text_area("Learning Goal:", value=st.session_state.user_progress.get('learning_goal', ''))
            
            with col2:
                native_language = st.selectbox("Native Language:", 
                                             ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Other"])
                target_language = st.selectbox("Target Language:", 
                                             ["Indonesian", "English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean"])
                daily_goal = st.slider("Daily Word Goal:", 5, 100, st.session_state.daily_goal)
        
        if st.button("💾 Save Profile"):
            st.session_state.user_progress['profile_name'] = name
            st.session_state.user_progress['profile_email'] = email
            st.session_state.user_progress['learning_goal'] = learning_goal
            st.session_state.user_progress['native_language'] = native_language
            st.session_state.user_progress['target_language'] = target_language
            st.session_state.daily_goal = daily_goal
            st.success("Profile saved successfully!")
        
        # Profile display
        st.markdown("---")
        st.subheader("📊 Learning Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Words Learned", len(st.session_state.user_progress['learned_words_details']))
        
        with col2:
            st.metric("Daily Streak", st.session_state.user_progress['daily_streak'])
        
        with col3:
            st.metric("Mastered Words", len(st.session_state.user_progress['mastered_words']))
        
        with col4:
            st.metric("Weak Words", len(st.session_state.user_progress['weak_words']))
        
        # Learning progress chart
        if st.session_state.user_progress['learned_words_details']:
            st.subheader("📈 Learning Progress")
            
            # Create progress data
            progress_data = []
            for word, details in st.session_state.user_progress['learned_words_details'].items():
                progress_data.append({
                    'Word': word,
                    'Mastery Level': details['mastery_level'],
                    'Total Reviews': details['total_reviews'],
                    'Success Rate': (details['correct_reviews']/details['total_reviews']*100) if details['total_reviews'] > 0 else 0
                })
            
            df = pd.DataFrame(progress_data)
            
            # Mastery level distribution
            fig = px.histogram(df, x='Mastery Level', nbins=11, 
                             title='Mastery Level Distribution',
                             labels={'count': 'Number of Words', 'Mastery Level': 'Mastery Level (0-10)'})
            st.plotly_chart(fig, width='stretch')
        
        # Share profile
        st.markdown("---")
        st.subheader("🔗 Share Your Progress")
        
        # Generate shareable profile data
        profile_data = {
            'name': st.session_state.user_progress.get('profile_name', 'Anonymous'),
            'total_words': len(st.session_state.user_progress['learned_words_details']),
            'daily_streak': st.session_state.user_progress['daily_streak'],
            'mastered_words': len(st.session_state.user_progress['mastered_words']),
            'learning_goal': st.session_state.user_progress.get('learning_goal', ''),
            'target_language': st.session_state.user_progress.get('target_language', 'Indonesian'),
            'profile_date': datetime.now().isoformat()
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Copy Profile Link"):
                profile_json = json.dumps(profile_data, indent=2)
                st.code(profile_json, language='json')
                st.success("Profile data copied! Share this with others.")
        
        with col2:
            if st.button("📤 Export Full Profile"):
                full_profile = {
                    'profile': profile_data,
                    'progress': dict(st.session_state.user_progress),
                    'learned_words': list(st.session_state.user_progress['learned_words_details'].keys())
                }
                # Convert sets to lists for JSON serialization
                for key, value in full_profile['progress'].items():
                    if isinstance(value, set):
                        full_profile['progress'][key] = list(value)
                
                profile_json = json.dumps(full_profile, indent=2, default=str)
                st.download_button(
                    label="Download Profile JSON",
                    data=profile_json,
                    file_name=f"indonesian_learning_profile_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        st.markdown("---")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    def render_settings(self):
        """Render settings page"""
        st.title("⚙️ Settings")
        
        st.subheader("🎯 Learning Goals")
        new_goal = st.slider("Daily word goal:", 5, 50, st.session_state.daily_goal)
        if new_goal != st.session_state.daily_goal:
            st.session_state.daily_goal = new_goal
            st.success("Daily goal updated!")
        
        st.subheader("📊 Progress Management")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Export Progress"):
                progress_data = {
                    'user_progress': dict(st.session_state.user_progress),
                    'flashcard_data': {k: {**v, 'next_review': v['next_review'].isoformat()} 
                                     for k, v in st.session_state.flashcard_data.items()},
                    'daily_goal': st.session_state.daily_goal
                }
                progress_data['user_progress']['words_learned'] = list(progress_data['user_progress']['words_learned'])
                if progress_data['user_progress']['last_study_date']:
                    progress_data['user_progress']['last_study_date'] = progress_data['user_progress']['last_study_date'].isoformat()
                
                json_str = json.dumps(progress_data, indent=2)
                st.download_button(
                    label="Download Progress JSON",
                    data=json_str,
                    file_name=f"indonesian_progress_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_file = st.file_uploader("📥 Import Progress", type=['json'])
            if uploaded_file is not None:
                try:
                    progress_data = json.load(uploaded_file)
                    
                    # Restore user progress
                    st.session_state.user_progress = progress_data['user_progress']
                    st.session_state.user_progress['words_learned'] = set(st.session_state.user_progress['words_learned'])
                    if st.session_state.user_progress['last_study_date']:
                        st.session_state.user_progress['last_study_date'] = datetime.fromisoformat(
                            st.session_state.user_progress['last_study_date']).date()
                    
                    # Restore flashcard data
                    for word, data in progress_data['flashcard_data'].items():
                        if word in st.session_state.flashcard_data:
                            st.session_state.flashcard_data[word].update(data)
                            st.session_state.flashcard_data[word]['next_review'] = datetime.fromisoformat(data['next_review'])
                    
                    st.session_state.daily_goal = progress_data.get('daily_goal', 20)
                    st.success("Progress imported successfully!")
                    
                except Exception as e:
                    st.error(f"Error importing progress: {e}")
        
        st.subheader("🔄 Reset Options")
        st.warning("⚠️ These actions cannot be undone!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reset Progress", type="secondary"):
                st.session_state.user_progress = {
                    'words_learned': set(),
                    'daily_streak': 0,
                    'last_study_date': None,
                    'total_study_time': 0,
                    'flashcard_reviews': {},
                    'quiz_scores': [],
                    'current_level': 'Beginner'
                }
                st.success("Progress reset!")
                
        with col2:
            if st.button("Reset Flashcard Schedule", type="secondary"):
                st.session_state.flashcard_data = self.init_flashcard_data()
                st.success("Flashcard schedule reset!")
        
        st.markdown("---")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    def generate_workbook(self):
        """Generate and download PDF workbook"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph("Indonesian Vocabulary Workbook", title_style))
            story.append(Spacer(1, 20))
            
            # Get user's current level words
            current_level = st.session_state.user_progress['current_level']
            level_words = VOCABULARY_DATA[current_level]
            
            # Exercise 1: Vocabulary List
            story.append(Paragraph("Exercise 1: Vocabulary Reference", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            vocab_data = [['Indonesian', 'English', 'Pronunciation']]
            for indo, details in list(level_words.items())[:20]:  # Limit to 20 words
                vocab_data.append([indo, details['english'], details['pronunciation']])
            
            vocab_table = Table(vocab_data)
            vocab_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(vocab_table)
            story.append(Spacer(1, 30))
            
            # Exercise 2: Fill in the blanks
            story.append(Paragraph("Exercise 2: Fill in the Blanks", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            sample_words = random.sample(list(level_words.items()), min(10, len(level_words)))
            for i, (indo, details) in enumerate(sample_words, 1):
                story.append(Paragraph(f"{i}. {details['english']} = _______________", styles['Normal']))
                story.append(Spacer(1, 10))
            
            story.append(Spacer(1, 20))
            
            # Exercise 3: Translation
            story.append(Paragraph("Exercise 3: Translate to English", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            translation_words = random.sample(list(level_words.items()), min(10, len(level_words)))
            for i, (indo, details) in enumerate(translation_words, 1):
                story.append(Paragraph(f"{i}. {indo} = _______________", styles['Normal']))
                story.append(Spacer(1, 10))
            
            # Answer Key
            story.append(Spacer(1, 30))
            story.append(Paragraph("Answer Key", styles['Heading2']))
            story.append(Spacer(1, 10))
            
            story.append(Paragraph("Exercise 2 Answers:", styles['Heading3']))
            for i, (indo, details) in enumerate(sample_words, 1):
                story.append(Paragraph(f"{i}. {indo}", styles['Normal']))
            
            story.append(Spacer(1, 15))
            story.append(Paragraph("Exercise 3 Answers:", styles['Heading3']))
            for i, (indo, details) in enumerate(translation_words, 1):
                story.append(Paragraph(f"{i}. {details['english']}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            # Create download button
            st.download_button(
                label="📖 Download Workbook PDF",
                data=buffer.getvalue(),
                file_name=f"indonesian_workbook_{current_level.lower()}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.success("Workbook generated successfully!")
            
        except Exception as e:
            st.error(f"Error generating workbook: {e}")
    
    def run(self):
        """Main app runner"""
        # Initialize page state
        if 'page' not in st.session_state:
            st.session_state.page = 'dashboard'
        
        # Sidebar navigation with profile info
        with st.sidebar:
            # Profile info and logout
            pin_code = st.session_state.user_progress.get('access_code', 'N/A')
            st.markdown(
                f"""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1rem;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 1rem;
                '>
                    <h3 style='color: white; margin: 0;'>👤 {st.session_state.current_profile}</h3>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                        Your Learning Profile
                    </p>
                    <p style='color: rgba(255,255,255,0.8); margin: 0.3rem 0 0 0; font-size: 0.8rem;'>
                        PIN: {pin_code}
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Logout button
            if st.button("🚪 Logout", width='stretch', type="secondary"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            st.markdown("---")
            
            # Navigation
            st.subheader("Navigation")
            
            pages = {
                'dashboard': '🏠 Dashboard',
                'flashcards': '📚 Flashcards',
                'sentences': '📝 Learn Sentences',
                'workbook': '📖 Workbook',
                'study': '📚 Study Grammar',
                'quiz': '🧠 Quiz',
                'word_database': '📊 Word Database',
                'review_weak': '🔄 Review Weak Words',
                'profile': '👤 Profile',
                'settings': '⚙️ Settings'
            }
            
            for page_key, page_name in pages.items():
                if st.button(page_name, width='stretch'):
                    st.session_state.page = page_key
                    st.rerun()
            
            st.markdown("---")
            st.subheader("📊 Quick Stats")
            st.metric("Words Learned", len(st.session_state.user_progress['words_learned']))
            st.metric("Current Streak", st.session_state.user_progress['daily_streak'])
            
            due_cards = len(self.get_due_cards())
            if due_cards > 0:
                st.warning(f"⏰ {due_cards} cards due for review!")
        
        # Check if profile is selected
        if st.session_state.current_profile is None:
            self.render_profile_selection()
            return
        
        # Render current page
        if st.session_state.page == 'dashboard':
            self.render_dashboard()
        elif st.session_state.page == 'flashcards':
            self.render_flashcards()
        elif st.session_state.page == 'sentences':
            self.render_sentence_learning()
        elif st.session_state.page == 'workbook':
            self.render_workbook()
        elif st.session_state.page == 'study':
            self.render_study_grammar()
        elif st.session_state.page == 'battle':
            self.render_battle_mode()
        elif st.session_state.page == 'quiz':
            self.render_quiz()
        elif st.session_state.page == 'review_weak':
            self.render_weak_words_review()
        elif st.session_state.page == 'word_database':
            self.render_word_database()
        elif st.session_state.page == 'profile':
            self.render_profile()
        elif st.session_state.page == 'settings':
            self.render_settings()
    
    def render_profile_selection(self):
        """Render modern login and profile selection page"""
        # Modern header with gradient
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: -1rem -1rem 3rem -1rem;'>
            <h1 style='color: white; font-size: 4rem; margin: 0; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🇮🇩 Indonesian Hub</h1>
            <p style='color: #f0f0f0; font-size: 1.4rem; margin: 1rem 0; font-weight: 300;'>Your Personal Learning Journey</p>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 15px; margin: 2rem auto; max-width: 600px;'>
                <p style='color: white; margin: 0; font-size: 1.1rem;'>🔒 Secure • Private • Personal</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main content area
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Get existing profiles
            existing_profiles = self.get_existing_profiles()
            
            if existing_profiles:
                # Modern login card
                st.markdown("""
                <div style='background: white; padding: 3rem; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin: 2rem 0; border: 1px solid #e0e0e0;'>
                    <h2 style='text-align: center; color: #333; margin-bottom: 0.5rem; font-size: 2.2rem; font-weight: 600;'>Welcome Back</h2>
                    <p style='text-align: center; color: #666; margin-bottom: 2.5rem; font-size: 1.1rem;'>Sign in to continue your learning journey</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Login form
                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input(
                        "👤 Username", 
                        placeholder="Enter your username...",
                        help="The name you used when creating your profile",
                        key="login_username"
                    )
                    
                    pin_code = st.text_input(
                        "🔐 PIN Code", 
                        placeholder="Enter your 4-digit PIN...",
                        help="Your personal 4-digit PIN code",
                        type="password",
                        max_chars=4,
                        key="login_pin"
                    )
                    
                    col_btn1, col_btn2 = st.columns([1, 1])
                    with col_btn1:
                        login_submitted = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
                    
                    with col_btn2:
                        if st.form_submit_button("🔄 Clear", use_container_width=True):
                            st.rerun()
                    
                    if login_submitted and username and pin_code:
                        if self.authenticate_profile(username, pin_code):
                            st.session_state.current_profile = username
                            self.load_profile_data(username)
                            st.success(f"🎉 Welcome back, {username}! Redirecting to your dashboard...")
                            st.session_state.page = 'dashboard'
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or PIN code. Please check and try again.")
                
                # Current profile info (only if logged in)
                if st.session_state.current_profile:
                    st.markdown("---")
                    st.markdown("### 👤 Your Profile")
                    
                    # Get current profile info
                    current_profile_data = None
                    for profile in existing_profiles:
                        if profile['name'] == st.session_state.current_profile:
                            current_profile_data = profile
                            break
                    
                    if current_profile_data:
                        col_info1, col_info2 = st.columns([2, 1])
                        with col_info1:
                            st.info(f"**{current_profile_data['name']}** • {current_profile_data['words_learned']} words learned")
                        with col_info2:
                            if st.button("🗑️ Delete My Profile", type="secondary", help="Delete your profile"):
                                if self.delete_profile(current_profile_data['name']):
                                    st.success("Profile deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete profile.")
                    
                    st.markdown("---")
                
                # Create new profile section
                st.markdown("""
                <div style='background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 2.5rem; border-radius: 20px; margin: 2rem 0; border-left: 5px solid #667eea;'>
                    <h3 style='color: #333; margin-top: 0; font-size: 1.5rem;'>New to Indonesian Hub?</h3>
                    <p style='color: #666; margin-bottom: 1.5rem; font-size: 1.1rem;'>Create your personal learning profile to start your Indonesian journey!</p>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                # First time user - welcome message
                st.markdown("""
                <div style='background: white; padding: 3rem; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin: 2rem 0; text-align: center; border: 1px solid #e0e0e0;'>
                    <h2 style='color: #333; margin-bottom: 1rem; font-size: 2.2rem; font-weight: 600;'>Welcome to Indonesian Hub!</h2>
                    <p style='color: #666; font-size: 1.2rem; margin-bottom: 2rem; line-height: 1.6;'>Create your profile to start learning Indonesian with personalized progress tracking, flashcards, and social battles.</p>
                    <div style='background: #e3f2fd; padding: 1.5rem; border-radius: 15px; margin: 2rem 0; border-left: 5px solid #2196f3;'>
                        <p style='margin: 0; color: #1565c0; font-size: 1rem; font-weight: 500;'>
                            🔒 <strong>Your Privacy Matters:</strong> All data is stored locally and securely. No information is shared with others.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Create new profile form
            with st.form("create_profile", clear_on_submit=True):
                st.markdown("### ✨ Create Your Profile")
                
                new_name = st.text_input(
                    "👤 Your Name", 
                    max_chars=20,
                    placeholder="Enter your name",
                    help="This will be displayed on your dashboard",
                    key="create_name"
                )
                
                new_pin = st.text_input(
                    "🔐 Create a 4-digit PIN", 
                    type="password", 
                    max_chars=4,
                    placeholder="1234",
                    help="Use this PIN to access your profile",
                    key="create_pin"
                )
                
                # Terms and privacy notice
                st.markdown("""
                <div style='background: #e8f5e8; padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0; border-left: 5px solid #4caf50;'>
                    <p style='margin: 0; color: #2e7d32; font-size: 0.95rem; line-height: 1.5;'>
                        🔒 <strong>Privacy & Security:</strong> Your learning data is stored locally on your device. No information is shared with others or stored on external servers. Your PIN protects your personal progress.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col_create1, col_create2 = st.columns([1, 1])
                with col_create1:
                    create_submitted = st.form_submit_button("🚀 Create My Profile", type="primary", use_container_width=True)
                with col_create2:
                    if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                        st.rerun()
                
                if create_submitted and new_name and new_pin:
                    if len(new_name) < 2:
                        st.error("Name must be at least 2 characters long.")
                    elif len(new_pin) != 4 or not new_pin.isdigit():
                        st.error("PIN must be exactly 4 digits.")
                    elif new_name in [p['name'] for p in existing_profiles]:
                        st.error("Profile name already exists. Please choose a different name.")
                    else:
                        if self.init_new_profile(new_name, new_pin):
                            st.session_state.current_profile = new_name
                            st.session_state.page = 'dashboard'
                            st.success(f"🎉 Profile '{new_name}' created successfully! Welcome to your learning journey!")
                            st.rerun()
                        else:
                            st.error("Failed to create profile. Please try again.")
    
    
    def delete_profile(self, profile_name):
        """Delete a profile with security validation"""
        try:
            # Security check: Only allow deleting the current profile
            if st.session_state.current_profile != profile_name:
                st.error("🔒 Security Error: You can only delete your own profile.")
                return False
            
            profile_files = self.get_profile_files(profile_name)
            
            # Delete all profile files
            for file_type, file_path in profile_files.items():
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Clear session state
            st.session_state.current_profile = None
            st.session_state.user_progress = self.get_default_progress()
            st.session_state.flashcard_data = {}
            
            return True
        except Exception as e:
            st.error(f"Error deleting profile: {e}")
            return False

    def load_profile_data(self, profile_name):
        """Load data for a specific profile with security validation"""
        # Security check: Only allow loading the current profile
        if st.session_state.current_profile != profile_name:
            st.error("🔒 Security Error: You can only access your own profile data.")
            return False
        
        profile_files = self.get_profile_files(profile_name)
        
        # Load progress
        if os.path.exists(profile_files['progress']):
            try:
                with open(profile_files['progress'], 'r') as f:
                    progress_data = json.load(f)
                
                # Validate profile ownership
                if progress_data.get('profile_name') != profile_name:
                    st.error("🔒 Security Error: Profile data mismatch.")
                    return False
                
                # Convert lists back to sets
                for key, value in progress_data.items():
                    if key in ['words_learned', 'weak_words', 'mastered_words'] and isinstance(value, list):
                        progress_data[key] = set(value)
                    elif key == 'last_study_date' and value:
                        try:
                            progress_data[key] = datetime.fromisoformat(value).date()
                        except:
                            progress_data[key] = None
                
                st.session_state.user_progress = progress_data
            except Exception as e:
                st.error(f"Error loading profile progress: {e}")
                return False
        
        # Load flashcards
        if os.path.exists(profile_files['flashcards']):
            try:
                with open(profile_files['flashcards'], 'r') as f:
                    flashcard_data = json.load(f)
                
                # Convert ISO strings back to datetime objects
                for word, data in flashcard_data.items():
                    if 'next_review' in data:
                        try:
                            data['next_review'] = datetime.fromisoformat(data['next_review'])
                        except:
                            data['next_review'] = datetime.now()
                
                st.session_state.flashcard_data = flashcard_data
            except Exception as e:
                st.error(f"Error loading flashcards: {e}")
                return False
        
        return True
    
    
    def authenticate_profile(self, username, pin_code):
        """Authenticate a profile with username and PIN code"""
        try:
            profile_files = self.get_profile_files(username)
            if os.path.exists(profile_files['progress']):
                with open(profile_files['progress'], 'r') as f:
                    data = json.load(f)
                    stored_pin = data.get('access_code', '')  # PIN is stored in access_code field
                    return stored_pin == pin_code
        except:
            pass
        return False
    
    def get_existing_profiles(self):
        """Get list of existing profiles with complete privacy isolation"""
        profiles = []
        if os.path.exists(self.profiles_dir):
            for profile_name in os.listdir(self.profiles_dir):
                profile_path = os.path.join(self.profiles_dir, profile_name)
                if os.path.isdir(profile_path):
                    profile_files = self.get_profile_files(profile_name)
                    if os.path.exists(profile_files['progress']):
                        try:
                            with open(profile_files['progress'], 'r') as f:
                                data = json.load(f)
                                # Only show basic info, no sensitive data
                                profiles.append({
                                    'name': profile_name,
                                    'words_learned': len(data.get('words_learned', [])),
                                    'access_code': data.get('access_code', 'N/A')
                                })
                        except:
                            pass
        return profiles
    
    def init_new_profile(self, profile_name):
        """Initialize a new profile with default data"""
        # Reset to default state
        st.session_state.user_progress = {
            'words_learned': set(),
            'daily_streak': 0,
            'last_study_date': None,
            'total_study_time': 0,
            'flashcard_reviews': {},
            'quiz_scores': [],
            'current_level': 'Absolute Beginner',
            'learned_words_details': {},
            'weak_words': set(),
            'mastered_words': set(),
            'study_sessions': [],
            'total_words_learned': 0,
            'profile_name': profile_name,
            'created_date': datetime.now().isoformat()
        }
        
        st.session_state.flashcard_data = self.init_flashcard_data()
        
        # Save initial data
        self.save_profile_data(profile_name)
    
    def save_profile_data(self, profile_name):
        """Save current session data to profile"""
        profile_files = self.get_profile_files(profile_name)
        
        # Save progress
        try:
            progress_data = dict(st.session_state.user_progress)
            # Convert sets to lists for JSON serialization
            for key, value in progress_data.items():
                if isinstance(value, set):
                    progress_data[key] = list(value)
                elif key == 'last_study_date' and value:
                    progress_data[key] = value.isoformat() if hasattr(value, 'isoformat') else str(value)
            
            with open(profile_files['progress'], 'w') as f:
                json.dump(progress_data, f, indent=2, default=str)
        except Exception as e:
            st.error(f"Error saving profile progress: {e}")
        
        # Save flashcards
        try:
            flashcard_data = {}
            for word, data in st.session_state.flashcard_data.items():
                flashcard_data[word] = dict(data)
                if 'next_review' in flashcard_data[word]:
                    flashcard_data[word]['next_review'] = data['next_review'].isoformat()
            
            with open(profile_files['flashcards'], 'w') as f:
                json.dump(flashcard_data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving flashcards: {e}")
    
    def render_sentence_learning(self):
        """Render premium sentence learning interface with massive database"""
        
        # Get comprehensive sentence database (combining all databases)
        MASSIVE_SENTENCES = get_massive_sentence_database()
        MEGA_SENTENCES = get_mega_sentence_database()
        ULTIMATE_SENTENCES = get_ultimate_sentence_database()
        PREMIUM_SENTENCES = get_premium_sentence_database()
        EXTENDED_SENTENCES = get_extended_premium_sentences()
        
        # Combine all sentence databases for maximum content
        COMBINED_SENTENCES = {}
        all_categories = ["Greetings & Politeness", "Daily Life", "Family & Relationships", "Food & Dining", 
                         "Travel & Transportation", "Shopping & Money", "Work & Education", "Business & Professional", 
                         "Culture & Society", "Technology & Innovation", "Casual & Slang", "Emotions & Feelings",
                         "Technology", "Health", "Education"]
        
        for level in ["Beginner", "Intermediate", "Advanced", "Conversational"]:
            COMBINED_SENTENCES[level] = {}
            for category in all_categories:
                COMBINED_SENTENCES[level][category] = []
                
                # Add sentences from all databases
                for db in [MASSIVE_SENTENCES, MEGA_SENTENCES, ULTIMATE_SENTENCES, PREMIUM_SENTENCES]:
                    if level in db and category in db[level]:
                        COMBINED_SENTENCES[level][category].extend(db[level][category])
                
                # Add extended sentences
                if category in EXTENDED_SENTENCES:
                    COMBINED_SENTENCES[level][category].extend(EXTENDED_SENTENCES[category][:20])  # Add 20 per category per level
        
        MASSIVE_SENTENCES = COMBINED_SENTENCES
        
        # Calculate total sentences
        total_sentences = sum(len(category_sentences) for level_data in MASSIVE_SENTENCES.values() 
                             for category_sentences in level_data.values())
        
        st.title("🇮🇩 Indonesian Sentence Learning")
        st.markdown("**Master Indonesian through 2000+ carefully curated sentences with pronunciation guides, grammar focus, and cultural context**")
        
        # Sentence statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sentences", f"{total_sentences:,}")
        with col2:
            st.metric("Difficulty Levels", "4")
        with col3:
            st.metric("Categories", f"{len(all_categories)}")
        with col4:
            st.metric("Quality", "Premium")
        
        # Level selector with enhanced options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_level = st.selectbox(
                "Choose Difficulty Level:",
                options=list(MASSIVE_SENTENCES.keys()),
                index=0,
                help="Select your current learning level to see appropriate sentences"
            )
        
        with col2:
            # Category filter
            sentences = MASSIVE_SENTENCES[selected_level]
            all_categories = set()
            for category_sentences in sentences.values():
                for sentence in category_sentences:
                    all_categories.add(sentence['category'])
            
            selected_category = st.selectbox(
                "Filter by Category:",
                options=["All"] + sorted(list(all_categories)),
                help="Filter sentences by specific topics"
            )
        
        # Filter sentences by category if selected
        if selected_category != "All":
            filtered_sentences = {}
            for category, sentence_list in sentences.items():
                filtered_sentences[category] = [s for s in sentence_list if s['category'] == selected_category]
            sentences = filtered_sentences
        
        # Flatten all sentences from all categories
        all_sentences = []
        for category, sentence_list in sentences.items():
            for sentence in sentence_list:
                all_sentences.append(sentence)
        
        if not all_sentences:
            st.warning("No sentences available for this level and category.")
            return
        
        # Get current sentence
        if 'current_sentence' not in st.session_state:
            st.session_state.current_sentence = 0
            st.session_state.show_sentence_answer = False
        
        # Ensure current_sentence index is valid
        if st.session_state.current_sentence >= len(all_sentences):
            st.session_state.current_sentence = 0
        
        sentence_data = all_sentences[st.session_state.current_sentence]
        
        # Debug: Check sentence data structure
        if not isinstance(sentence_data, dict):
            st.error(f"Invalid sentence data structure: {type(sentence_data)}")
            return
        
        # Display sentence statistics
        # Display sentence statistics
        if all_sentences:
            difficulty_level = sentence_data.get('difficulty', 1) if 'sentence_data' in locals() else 1
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Available Sentences", f"{len(all_sentences):,}")
            with col2:
                st.metric("Current Level", selected_level)
            with col3:
                st.metric("Category", selected_category)
            with col4:
                st.metric("Difficulty", f"Level {difficulty_level}/3")
        
        st.markdown("---")
        
        # Display enhanced sentence card
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Enhanced sentence display
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            '>
                <h2 style='color: white; margin: 0; font-size: 2.5rem; font-weight: bold;'>{sentence_data['indonesian']}</h2>
                <p style='color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;'>{sentence_data['pronunciation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # English translation
            st.markdown(f"**English:** {sentence_data['english']}")
            
            # Additional information
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.info(f"**Category:** {sentence_data.get('category', 'N/A')}")
                st.info(f"**Grammar Focus:** {sentence_data.get('grammar_focus', 'N/A')}")
            with col_info2:
                st.info(f"**Difficulty:** Level {sentence_data.get('difficulty', 1)}/3")
                if sentence_data.get('cultural_note'):
                    st.info(f"**Cultural Note:** {sentence_data['cultural_note']}")
            
            # Sentence information panel
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("**📚 Grammar Focus:**")
                st.info(f"**{sentence_data['grammar_focus'].replace('_', ' ').title()}**")
                
                st.markdown("**🏷️ Category:**")
                st.success(f"**{sentence_data['category'].replace('_', ' ').title()}**")
            
            with col_info2:
                st.markdown("**🔑 Key Words:**")
                key_words = sentence_data.get('key_words', [])
                for word in key_words:
                    st.caption(f"• {word}")
                
                st.markdown("**📊 Difficulty:**")
                difficulty = sentence_data.get('difficulty', 1)
                st.progress(difficulty / 3)
                st.caption(f"Level {difficulty}/3")
            
            if st.session_state.show_sentence_answer:
                st.markdown(
                    f"""
                    <div style='
                        background: white;
                        padding: 1.5rem;
                        border-radius: 10px;
                        text-align: center;
                        margin: 1rem 0;
                        border: 2px solid #667eea;
                    '>
                        <h3 style='color: #333; margin: 0;'>{sentence_data['english']}</h3>
                        <p style='color: #666; font-style: italic; margin: 0.5rem 0;'>/{sentence_data['pronunciation']}/</p>
                        <p style='color: #888; margin: 0.5rem 0;'>Category: {sentence_data['category'].title()}</p>
                        <p style='color: #888; margin: 0.5rem 0;'>Grammar: {sentence_data['grammar_focus']}</p>
                        <div style='background: #f8f9fa; padding: 1rem; border-radius: 5px; margin: 1rem 0;'>
                            <p style='color: #495057; margin: 0; font-weight: bold;'>Key Words:</p>
                            <p style='color: #6c757d; margin: 0.5rem 0 0 0;'>{', '.join(sentence_data['key_words'])}</p>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        # Control buttons
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("← Back"):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        with col3:
            if not st.session_state.show_sentence_answer:
                if st.button("Show Translation", width='stretch'):
                    st.session_state.show_sentence_answer = True
                    st.rerun()
                # Add Next button even before showing translation
                if st.button("➡️ Next Sentence", width='stretch', type="secondary"):
                    next_index = (st.session_state.current_sentence + 1) % len(all_sentences)
                    st.session_state.current_sentence = next_index
                    st.session_state.show_sentence_answer = False
                    st.rerun()
            else:
                if st.button("➡️ Next Sentence", width='stretch', type="primary"):
                    # Get next sentence
                    next_index = (st.session_state.current_sentence + 1) % len(all_sentences)
                    st.session_state.current_sentence = next_index
                    st.session_state.show_sentence_answer = False
                    st.rerun()
                # Add Previous button
                if st.button("⬅️ Previous", width='stretch', type="secondary"):
                    prev_index = (st.session_state.current_sentence - 1) % len(all_sentences)
                    st.session_state.current_sentence = prev_index
                    st.session_state.show_sentence_answer = False
                    st.rerun()
        
        # Progress info
        st.markdown("---")
        current_index = st.session_state.current_sentence + 1
        st.info(f"📊 Sentence {current_index} of {len(all_sentences)} in {selected_level}")
        
        st.markdown("---")
        st.markdown("**💡 Tip:** Practice these sentences regularly to improve your Indonesian conversation skills!")
    
    def render_study_grammar(self):
        """Render advanced Indonesian grammar study section with interactive features"""
        st.title("📚 Advanced Indonesian Grammar Mastery")
        st.markdown("**Comprehensive grammar learning with interactive exercises, progress tracking, and personalized study plans**")
        
        # Create sidebar for navigation and progress
        with st.sidebar:
            st.markdown("### 🎯 Study Progress")
            if 'grammar_progress' not in st.session_state:
                st.session_state.grammar_progress = {
                    'completed_topics': [],
                    'current_level': 'beginner',
                    'study_streak': 0,
                    'total_study_time': 0
                }
            
            progress = st.session_state.grammar_progress
            st.metric("Completed Topics", len(progress['completed_topics']))
            st.metric("Study Streak", f"{progress['study_streak']} days")
            
            st.markdown("---")
            st.markdown("### 🎚️ Study Level")
            level = st.selectbox(
                "Choose your level:",
                ["beginner", "intermediate", "advanced", "expert"],
                index=["beginner", "intermediate", "advanced", "expert"].index(progress['current_level'])
            )
            if level != progress['current_level']:
                st.session_state.grammar_progress['current_level'] = level
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 🔍 Quick Search")
            search_term = st.text_input("Search grammar topics:", placeholder="e.g., past tense, pronouns")
            
            st.markdown("---")
            st.markdown("### 📊 Study Analytics")
            if st.button("View Detailed Progress"):
                st.session_state.show_grammar_analytics = True
        
        # MASSIVE COMPREHENSIVE GRAMMAR LIBRARY
        grammar_categories = {
            "🏗️ Basic Structure": {
                "level": "beginner",
                "difficulty": 1,
                "description": "Master fundamental sentence patterns and word order",
                "estimated_time": "20 minutes",
                "topics": [
                    {
                        "title": "Subject + Verb + Object (SVO)",
                        "explanation": "Indonesian follows SVO word order like English, but is more flexible. Understanding this basic structure is crucial for building correct sentences.",
                        "detailed_explanation": """
                        **Word Order Rules:**
                        - Subject always comes first
                        - Verb follows immediately after subject
                        - Object comes last
                        - No articles (a, an, the) needed
                        - More flexible than English - can rearrange for emphasis
                        """,
                        "examples": [
                            {"indonesian": "Saya makan nasi", "english": "I eat rice", "pronunciation": "SAH-yah MAH-kan NAH-see"},
                            {"indonesian": "Dia minum kopi", "english": "He/She drinks coffee", "pronunciation": "DEE-ah MEE-noom KOH-pee"},
                            {"indonesian": "Kami belajar bahasa Indonesia", "english": "We learn Indonesian", "pronunciation": "KAH-mee beh-LAH-jar bah-HAH-sah In-do-NEH-see-ah"}
                        ],
                        "key_points": [
                            "Subject comes first",
                            "Verb follows the subject",
                            "Object comes last",
                            "No articles (a, an, the) needed",
                            "Can rearrange for emphasis: Nasi saya makan (Rice I eat)"
                        ],
                        "common_mistakes": [
                            "Putting articles before nouns (❌ a buku → ✅ buku)",
                            "Wrong word order (❌ makan saya nasi → ✅ saya makan nasi)"
                        ],
                        "practice_exercises": [
                            "Translate: 'I drink water'",
                            "Translate: 'She reads books'",
                            "Rearrange: 'makan saya nasi' (correct order)"
                        ]
                    },
                    {
                        "title": "Adjective Placement",
                        "explanation": "Adjectives come AFTER the noun they describe, opposite of English. This is one of the most important differences to remember.",
                        "detailed_explanation": """
                        **Adjective Rules:**
                        - Always placed AFTER the noun
                        - No agreement with gender or number
                        - Can be used as predicate
                        - Can be intensified with 'sangat' (very)
                        """,
                        "examples": [
                            {"indonesian": "rumah besar", "english": "big house", "pronunciation": "ROO-mah BAH-sar"},
                            {"indonesian": "mobil merah", "english": "red car", "pronunciation": "MOH-beel meh-RAH"},
                            {"indonesian": "buku bagus", "english": "good book", "pronunciation": "BOO-koo BAH-goos"},
                            {"indonesian": "Rumah ini besar", "english": "This house is big", "pronunciation": "ROO-mah EE-nee BAH-sar"}
                        ],
                        "key_points": [
                            "Adjective follows noun",
                            "No agreement with gender or number",
                            "Can be used as predicate: Rumah ini besar (This house is big)",
                            "Can be intensified: sangat besar (very big)"
                        ],
                        "common_mistakes": [
                            "Putting adjectives before nouns (❌ besar rumah → ✅ rumah besar)",
                            "Adding gender agreement (❌ rumah besara → ✅ rumah besar)"
                        ],
                        "practice_exercises": [
                            "Translate: 'small house'",
                            "Translate: 'beautiful flower'",
                            "Make sentence: 'This car is expensive'"
                        ]
                    },
                    {
                        "title": "Noun + Adjective Pattern",
                        "explanation": "Learn the most common Indonesian sentence pattern where adjectives follow nouns.",
                        "detailed_explanation": """
                        **Pattern: Noun + Adjective**
                        - This is the most basic Indonesian sentence structure
                        - No verb 'to be' needed
                        - Can be used as complete sentences
                        """,
                        "examples": [
                            {"indonesian": "Rumah besar", "english": "The house is big", "pronunciation": "ROO-mah BAH-sar"},
                            {"indonesian": "Mobil mahal", "english": "The car is expensive", "pronunciation": "MOH-beel mah-HAHL"},
                            {"indonesian": "Buku tebal", "english": "The book is thick", "pronunciation": "BOO-koo teh-BAHL"}
                        ],
                        "key_points": [
                            "No 'to be' verb needed",
                            "Noun + Adjective = complete sentence",
                            "Most common pattern in Indonesian"
                        ],
                        "common_mistakes": [
                            "Adding 'adalah' unnecessarily (❌ Rumah adalah besar → ✅ Rumah besar)"
                        ],
                        "practice_exercises": [
                            "Make sentence: 'The dog is small'",
                            "Make sentence: 'The food is delicious'"
                        ]
                    }
                ]
            },
            "👥 Pronouns & Possession": {
                "level": "beginner",
                "difficulty": 2,
                "description": "Master personal pronouns, possession, and social context",
                "estimated_time": "20 minutes",
                "topics": [
                    {
                        "title": "Personal Pronouns System",
                        "explanation": "Indonesian has a complex pronoun system with formal/informal distinctions and social implications. Master this for proper communication.",
                        "detailed_explanation": """
                        **Formal vs Informal System:**
                        - **Saya** (I) - formal, polite, business
                        - **Aku** (I) - informal, intimate, friends/family
                        - **Anda** (You) - formal, respectful, strangers/elders
                        - **Kamu** (You) - informal, friends/peers
                        - **Dia** (He/She) - neutral, works for both genders
                        - **Kami** (We) - excludes listener
                        - **Kita** (We) - includes listener
                        """,
                        "examples": [
                            {"indonesian": "Saya pergi ke kantor", "english": "I go to the office", "pronunciation": "SAH-yah PER-gee keh KAN-tor", "context": "Formal"},
                            {"indonesian": "Aku suka musik", "english": "I like music", "pronunciation": "AH-koo SOO-kah MOO-seek", "context": "Informal"},
                            {"indonesian": "Anda dari mana?", "english": "Where are you from?", "pronunciation": "Ahn-DAH DAH-ree MAH-nah?", "context": "Formal question"},
                            {"indonesian": "Kamu mau apa?", "english": "What do you want?", "pronunciation": "KAH-moo MAH-oo AH-pah?", "context": "Informal question"}
                        ],
                        "key_points": [
                            "Saya vs Aku: Saya is more polite and formal",
                            "Anda vs Kamu: Anda shows respect and distance",
                            "Dia works for both he and she (no gender distinction)",
                            "Kami excludes listener, Kita includes listener",
                            "Choose based on relationship and context"
                        ],
                        "common_mistakes": [
                            "Using Aku with strangers (❌ Aku mau... → ✅ Saya mau...)",
                            "Using Kamu with elders (❌ Kamu dari mana? → ✅ Anda dari mana?)",
                            "Confusing Kami/Kita (❌ Kami pergi → ✅ Kita pergi, if including listener)"
                        ],
                        "practice_exercises": [
                            "Choose correct pronoun: Talking to your boss (Saya/Aku)",
                            "Choose correct pronoun: Talking to your friend (Anda/Kamu)",
                            "Translate: 'We (including you) are going'"
                        ]
                    },
                    {
                        "title": "Possession & Ownership",
                        "explanation": "Express ownership using possessive pronouns, 'punya', and possessive constructions. Essential for describing relationships and belongings.",
                        "detailed_explanation": """
                        **Possession Methods:**
                        1. **Possessive after noun**: Buku saya (my book)
                        2. **Punya construction**: Saya punya buku (I have a book)
                        3. **Milik construction**: Buku ini milik saya (This book belongs to me)
                        4. **Kepunyaan**: Kepunyaan saya (mine)
                        """,
                        "examples": [
                            {"indonesian": "Buku saya", "english": "My book", "pronunciation": "BOO-koo SAH-yah", "method": "Possessive after noun"},
                            {"indonesian": "Rumah dia", "english": "His/Her house", "pronunciation": "ROO-mah DEE-ah", "method": "Possessive after noun"},
                            {"indonesian": "Saya punya mobil", "english": "I have a car", "pronunciation": "SAH-yah POO-nyah MOH-beel", "method": "Punya construction"},
                            {"indonesian": "Mobil ini milik saya", "english": "This car belongs to me", "pronunciation": "MOH-beel EE-nee MEE-leek SAH-yah", "method": "Milik construction"}
                        ],
                        "key_points": [
                            "Possessive pronouns come AFTER the noun",
                            "Punya means 'to have' or 'to own'",
                            "Milik means 'belongs to'",
                            "No apostrophe needed (unlike English)",
                            "Can combine methods for emphasis"
                        ],
                        "common_mistakes": [
                            "Putting possessive before noun (❌ saya buku → ✅ buku saya)",
                            "Using English apostrophe (❌ buku's saya → ✅ buku saya)",
                            "Confusing punya and milik usage"
                        ],
                        "practice_exercises": [
                            "Translate: 'My house is big'",
                            "Translate: 'She has a beautiful garden'",
                            "Make sentence: 'This book belongs to us'"
                        ]
                    }
                ]
            },
            "🏃 Verbs & Tenses": {
                "level": "beginner",
                "difficulty": 2,
                "description": "Master verb forms, tenses, and temporal expressions",
                "estimated_time": "25 minutes",
                "topics": [
                    {
                        "title": "Present Tense (No Conjugation)",
                        "explanation": "Indonesian verbs don't change form for tense. Use time words and context to indicate when actions happen.",
                        "detailed_explanation": """
                        **Present Tense Rules:**
                        - Verbs never change form
                        - Use time words to indicate when
                        - Context determines meaning
                        - Can express present, present continuous, or habitual actions
                        """,
                        "examples": [
                            {"indonesian": "Saya makan", "english": "I eat / I am eating", "pronunciation": "SAH-yah MAH-kan", "context": "Present"},
                            {"indonesian": "Dia tidur", "english": "He/She sleeps / is sleeping", "pronunciation": "DEE-ah TEE-door", "context": "Present"},
                            {"indonesian": "Kami belajar", "english": "We study / are studying", "pronunciation": "KAH-mee beh-LAH-jar", "context": "Present"}
                        ],
                        "key_points": [
                            "No verb conjugation needed",
                            "Use time words: sekarang (now), setiap hari (every day)",
                            "Context determines exact meaning",
                            "Same form for all subjects"
                        ],
                        "common_mistakes": [
                            "Trying to conjugate verbs (❌ saya makan → ✅ saya makan)",
                            "Adding unnecessary tense markers"
                        ],
                        "practice_exercises": [
                            "Translate: 'I am reading a book'",
                            "Translate: 'She is cooking dinner'",
                            "Make sentence: 'We are studying Indonesian'"
                        ]
                    },
                    {
                        "title": "Past Tense with Time Words",
                        "explanation": "Express past actions using time words like 'kemarin' (yesterday) or 'tadi' (earlier).",
                        "detailed_explanation": """
                        **Past Tense Indicators:**
                        - kemarin (yesterday)
                        - tadi (earlier today)
                        - sudah (already)
                        - pernah (ever, once)
                        - dulu (before, in the past)
                        """,
                        "examples": [
                            {"indonesian": "Saya makan kemarin", "english": "I ate yesterday", "pronunciation": "SAH-yah MAH-kan keh-MAH-reen", "time_word": "kemarin"},
                            {"indonesian": "Dia sudah pergi", "english": "He/She has already gone", "pronunciation": "DEE-ah SOO-dah per-GEE", "time_word": "sudah"},
                            {"indonesian": "Kami pernah ke Bali", "english": "We have been to Bali", "pronunciation": "KAH-mee peh-NAH keh BAH-lee", "time_word": "pernah"}
                        ],
                        "key_points": [
                            "Use time words to indicate past",
                            "Sudah = already (present perfect)",
                            "Pernah = ever, once (experience)",
                            "Dulu = before, in the past"
                        ],
                        "common_mistakes": [
                            "Trying to conjugate verbs for past tense",
                            "Forgetting time words"
                        ],
                        "practice_exercises": [
                            "Translate: 'I went to school yesterday'",
                            "Translate: 'She has already eaten'",
                            "Make sentence: 'We visited Jakarta last week'"
                        ]
                    },
                    {
                        "title": "Future Tense with 'Akan'",
                        "explanation": "Express future actions using 'akan' (will) or time words like 'besok' (tomorrow).",
                        "detailed_explanation": """
                        **Future Tense Markers:**
                        - akan (will)
                        - besok (tomorrow)
                        - nanti (later)
                        - minggu depan (next week)
                        - tahun depan (next year)
                        """,
                        "examples": [
                            {"indonesian": "Saya akan makan", "english": "I will eat", "pronunciation": "SAH-yah AH-kan MAH-kan", "marker": "akan"},
                            {"indonesian": "Dia pergi besok", "english": "He/She will go tomorrow", "pronunciation": "DEE-ah per-GEE beh-SOHK", "marker": "besok"},
                            {"indonesian": "Kami akan belajar nanti", "english": "We will study later", "pronunciation": "KAH-mee AH-kan beh-LAH-jar NAHN-tee", "marker": "nanti"}
                        ],
                        "key_points": [
                            "Akan = will (definite future)",
                            "Time words can replace akan",
                            "Nanti = later (less definite)",
                            "Besok = tomorrow"
                        ],
                        "common_mistakes": [
                            "Using akan with time words unnecessarily",
                            "Confusing akan and nanti"
                        ],
                        "practice_exercises": [
                            "Translate: 'I will go to the market'",
                            "Translate: 'She will call you tomorrow'",
                            "Make sentence: 'We will meet next week'"
                        ]
                    }
                ]
            },
            "❓ Questions & Interrogatives": {
                "level": "beginner",
                "difficulty": 2,
                "description": "Master question formation and interrogative words",
                "estimated_time": "20 minutes",
                "topics": [
                    {
                        "title": "Yes/No Questions",
                        "explanation": "Form yes/no questions by adding 'apakah' or using rising intonation.",
                        "detailed_explanation": """
                        **Yes/No Question Formation:**
                        - Add 'apakah' at the beginning
                        - Use rising intonation
                        - Answer with 'ya' (yes) or 'tidak' (no)
                        """,
                        "examples": [
                            {"indonesian": "Apakah kamu lapar?", "english": "Are you hungry?", "pronunciation": "AH-pah-kah KAH-moo LAH-par?", "answer": "ya/tidak"},
                            {"indonesian": "Apakah dia pergi?", "english": "Did he/she go?", "pronunciation": "AH-pah-kah DEE-ah per-GEE?", "answer": "ya/tidak"},
                            {"indonesian": "Kamu mau makan?", "english": "Do you want to eat?", "pronunciation": "KAH-moo MAH-oo MAH-kan?", "answer": "ya/tidak"}
                        ],
                        "key_points": [
                            "Apakah = formal question marker",
                            "Rising intonation for informal questions",
                            "Ya = yes, Tidak = no",
                            "Bukan = no (for nouns/adjectives)"
                        ],
                        "common_mistakes": [
                            "Using apakah unnecessarily in informal speech",
                            "Confusing ya/tidak and bukan"
                        ],
                        "practice_exercises": [
                            "Make question: 'Are you tired?'",
                            "Make question: 'Is the food delicious?'",
                            "Answer: 'Apakah kamu suka musik?'"
                        ]
                    },
                    {
                        "title": "WH Questions (5W1H)",
                        "explanation": "Master the essential question words: apa, siapa, kapan, di mana, mengapa, bagaimana.",
                        "detailed_explanation": """
                        **Question Words:**
                        - Apa = What
                        - Siapa = Who
                        - Kapan = When
                        - Di mana = Where
                        - Mengapa/Kenapa = Why
                        - Bagaimana = How
                        """,
                        "examples": [
                            {"indonesian": "Apa nama kamu?", "english": "What is your name?", "pronunciation": "AH-pah NAH-mah KAH-moo?", "word": "apa"},
                            {"indonesian": "Siapa itu?", "english": "Who is that?", "pronunciation": "SEE-ah-pah EE-too?", "word": "siapa"},
                            {"indonesian": "Kapan kamu datang?", "english": "When did you come?", "pronunciation": "KAH-pan KAH-moo DAH-tahng?", "word": "kapan"},
                            {"indonesian": "Di mana rumah kamu?", "english": "Where is your house?", "pronunciation": "DEE MAH-nah ROO-mah KAH-moo?", "word": "di mana"},
                            {"indonesian": "Mengapa kamu sedih?", "english": "Why are you sad?", "pronunciation": "Meh-ngah-PAH KAH-moo seh-DEEH?", "word": "mengapa"},
                            {"indonesian": "Bagaimana kabar kamu?", "english": "How are you?", "pronunciation": "Bah-gah-EE-mah KAH-bar KAH-moo?", "word": "bagaimana"}
                        ],
                        "key_points": [
                            "Apa = what (for things)",
                            "Siapa = who (for people)",
                            "Kapan = when (for time)",
                            "Di mana = where (for place)",
                            "Mengapa/Kenapa = why (for reason)",
                            "Bagaimana = how (for manner)"
                        ],
                        "common_mistakes": [
                            "Confusing apa and siapa",
                            "Using di mana incorrectly"
                        ],
                        "practice_exercises": [
                            "Ask: 'What is this?'",
                            "Ask: 'Where do you live?'",
                            "Ask: 'How do you cook rice?'"
                        ]
                    }
                ]
            },
            "🔢 Numbers & Counting": {
                "level": "beginner",
                "difficulty": 2,
                "description": "Master Indonesian numbers, counting, and numerical expressions",
                "estimated_time": "25 minutes",
                "topics": [
                    {
                        "title": "Basic Numbers 1-100",
                        "explanation": "Learn Indonesian numbers from 1 to 100 with proper pronunciation.",
                        "detailed_explanation": """
                        **Number System:**
                        - 1-10: satu, dua, tiga, empat, lima, enam, tujuh, delapan, sembilan, sepuluh
                        - 11-19: add 'belas' (except 11 = sebelas)
                        - 20-99: puluh + unit (except 20 = dua puluh)
                        - 100: seratus
                        """,
                        "examples": [
                            {"indonesian": "satu", "english": "one", "pronunciation": "SAH-too", "number": "1"},
                            {"indonesian": "lima", "english": "five", "pronunciation": "LEE-mah", "number": "5"},
                            {"indonesian": "sepuluh", "english": "ten", "pronunciation": "seh-POO-looh", "number": "10"},
                            {"indonesian": "dua puluh", "english": "twenty", "pronunciation": "DOO-ah POO-looh", "number": "20"},
                            {"indonesian": "seratus", "english": "one hundred", "pronunciation": "seh-RAH-toos", "number": "100"}
                        ],
                        "key_points": [
                            "Satu = one, Dua = two, Tiga = three",
                            "Sepuluh = ten, Seratus = one hundred",
                            "Belas = teen numbers (11-19)",
                            "Puluh = tens (20-90)"
                        ],
                        "common_mistakes": [
                            "Confusing puluh and belas",
                            "Wrong pronunciation of numbers"
                        ],
                        "practice_exercises": [
                            "Count from 1 to 10",
                            "Say: 'twenty-five'",
                            "Say: 'ninety-nine'"
                        ]
                    }
                ]
            },
            "Questions": {
                "icon": "❓",
                "description": "How to ask questions in Indonesian",
                "topics": [
                    {
                        "title": "Yes/No Questions",
                        "explanation": "Add 'apakah' at the beginning or use question intonation.",
                        "examples": [
                            "Apakah Anda lapar? (Are you hungry?)",
                            "Dia pergi? (Is he/she going?)",
                            "Kamu suka kopi? (Do you like coffee?)"
                        ],
                        "key_points": [
                            "Apakah is formal",
                            "Rising intonation for informal",
                            "Answer with 'ya' (yes) or 'tidak' (no)"
                        ]
                    },
                    {
                        "title": "Question Words",
                        "explanation": "Use question words to ask for specific information.",
                        "examples": [
                            "Apa? (What?)",
                            "Siapa? (Who?)",
                            "Di mana? (Where?)",
                            "Kapan? (When?)",
                            "Mengapa? (Why?)",
                            "Bagaimana? (How?)",
                            "Berapa? (How much/many?)"
                        ],
                        "key_points": [
                            "Question word comes first",
                            "No auxiliary verbs needed",
                            "Use question mark at end"
                        ]
                    }
                ]
            },
            "Numbers": {
                "icon": "🔢",
                "description": "Counting and using numbers",
                "topics": [
                    {
                        "title": "Cardinal Numbers",
                        "explanation": "Basic counting from 1 to 100 and beyond.",
                        "examples": [
                            "1-10: satu, dua, tiga, empat, lima, enam, tujuh, delapan, sembilan, sepuluh",
                            "11-20: sebelas, dua belas, tiga belas... dua puluh",
                            "21-30: dua puluh satu, dua puluh dua... tiga puluh",
                            "100: seratus, 1000: seribu"
                        ],
                        "key_points": [
                            "Belas for 11-19",
                            "Puluh for tens",
                            "Ratus for hundreds",
                            "Ribu for thousands"
                        ]
                    },
                    {
                        "title": "Ordinal Numbers",
                        "explanation": "Use 'ke-' prefix to make ordinal numbers.",
                        "examples": [
                            "Pertama (first)",
                            "Kedua (second)",
                            "Ketiga (third)",
                            "Keempat (fourth)",
                            "Kesepuluh (tenth)"
                        ],
                        "key_points": [
                            "Add 'ke-' prefix",
                            "Pertama is irregular",
                            "Used for ranking and order"
                        ]
                    }
                ]
            },
            "Time Expressions": {
                "icon": "⏰",
                "description": "Talking about time and dates",
                "topics": [
                    {
                        "title": "Days of the Week",
                        "explanation": "Days of the week in Indonesian.",
                        "examples": [
                            "Senin (Monday)",
                            "Selasa (Tuesday)",
                            "Rabu (Wednesday)",
                            "Kamis (Thursday)",
                            "Jumat (Friday)",
                            "Sabtu (Saturday)",
                            "Minggu (Sunday)"
                        ],
                        "key_points": [
                            "Capitalize first letter",
                            "Use 'hari' for 'day'",
                            "Hari ini (today), Besok (tomorrow)"
                        ]
                    },
                    {
                        "title": "Time of Day",
                        "explanation": "Expressions for different times of day.",
                        "examples": [
                            "Pagi (morning)",
                            "Siang (noon/afternoon)",
                            "Sore (evening)",
                            "Malam (night)",
                            "Tengah malam (midnight)"
                        ],
                        "key_points": [
                            "Selamat pagi (Good morning)",
                            "Selamat siang (Good afternoon)",
                            "Selamat malam (Good evening/night)"
                        ]
                    }
                ]
            },
            "Prepositions": {
                "icon": "📍",
                "description": "Location and direction words",
                "topics": [
                    {
                        "title": "Location Prepositions",
                        "explanation": "Words to describe where things are located.",
                        "examples": [
                            "Di (at/in/on)",
                            "Ke (to/towards)",
                            "Dari (from)",
                            "Di dalam (inside)",
                            "Di luar (outside)",
                            "Di atas (on top of)",
                            "Di bawah (under/below)"
                        ],
                        "key_points": [
                            "Di for static location",
                            "Ke for movement towards",
                            "Dari for movement from",
                            "Combine with dalam, luar, atas, bawah"
                        ]
                    }
                ]
            },
            "Politeness": {
                "icon": "🙏",
                "description": "Formal and informal language",
                "topics": [
                    {
                        "title": "Formal vs Informal",
                        "explanation": "Indonesian has different levels of formality.",
                        "examples": [
                            "Formal: Saya, Anda, Bapak, Ibu",
                            "Informal: Aku, Kamu, Mas, Mbak",
                            "Formal: Terima kasih (Thank you)",
                            "Informal: Makasih (Thanks)"
                        ],
                        "key_points": [
                            "Use formal with strangers and elders",
                            "Informal with friends and family",
                            "Bapak/Ibu for Mr./Mrs.",
                            "Mas/Mbak for young people"
                        ]
                    },
                    {
                        "title": "Politeness Markers",
                        "explanation": "Words and phrases to be polite.",
                        "examples": [
                            "Tolong (Please - for requests)",
                            "Maaf (Sorry/Excuse me)",
                            "Permisi (Excuse me - to get attention)",
                            "Silakan (Please - offering something)"
                        ],
                        "key_points": [
                            "Tolong for asking favors",
                            "Maaf for apologies",
                            "Permisi to get attention",
                            "Silakan when offering"
                        ]
                    }
                ]
            }
        }
        
        # Main content area with advanced features
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Search and filter functionality
            if search_term:
                st.markdown(f"### 🔍 Search Results for: '{search_term}'")
                filtered_categories = {}
                for cat_name, cat_data in grammar_categories.items():
                    if search_term.lower() in cat_name.lower() or search_term.lower() in cat_data['description'].lower():
                        filtered_categories[cat_name] = cat_data
                    else:
                        for topic in cat_data['topics']:
                            if search_term.lower() in topic['title'].lower() or search_term.lower() in topic['explanation'].lower():
                                if cat_name not in filtered_categories:
                                    filtered_categories[cat_name] = cat_data
                                break
                
                if not filtered_categories:
                    st.warning("No topics found matching your search.")
                    st.markdown("**Try searching for:** pronouns, verbs, tenses, questions, numbers, time, prepositions, politeness")
                else:
                    grammar_categories = filtered_categories
            
            # Level-based filtering
            current_level = st.session_state.grammar_progress['current_level']
            level_order = ['beginner', 'intermediate', 'advanced', 'expert']
            current_level_index = level_order.index(current_level)
            
            # Filter categories by level
            filtered_categories = {}
            for cat_name, cat_data in grammar_categories.items():
                if 'level' in cat_data:
                    cat_level_index = level_order.index(cat_data['level'])
                    if cat_level_index <= current_level_index:
                        filtered_categories[cat_name] = cat_data
            
            if not filtered_categories:
                st.info(f"No topics available for {current_level} level. Try selecting a higher level.")
                return
            
            # Create interactive tabs
            tab_names = list(filtered_categories.keys())
            tabs = st.tabs(tab_names)
            
            for i, (category, content) in enumerate(filtered_categories.items()):
                with tabs[i]:
                    # Category header with progress
                    col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
                    
                    with col_header1:
                        st.markdown(f"### {category}")
                        st.markdown(f"*{content['description']}*")
                    
                    with col_header2:
                        st.metric("Difficulty", f"Level {content['difficulty']}/5")
                    
                    with col_header3:
                        st.metric("Time", content['estimated_time'])
                    
                    # Progress indicator
                    completed_topics = [t for t in content['topics'] if t['title'] in st.session_state.grammar_progress['completed_topics']]
                    progress_percent = len(completed_topics) / len(content['topics']) * 100
                    st.progress(progress_percent / 100)
                    st.caption(f"Progress: {len(completed_topics)}/{len(content['topics'])} topics completed")
                    
                    st.markdown("---")
                    
                    # Topics with interactive features
                    for j, topic in enumerate(content['topics']):
                        is_completed = topic['title'] in st.session_state.grammar_progress['completed_topics']
                        
                        with st.expander(f"{'✅' if is_completed else '📚'} **{topic['title']}**", expanded=(j==0)):
                            # Topic header with completion status
                            col_topic1, col_topic2 = st.columns([3, 1])
                            
                            with col_topic1:
                                st.markdown(f"**{topic['explanation']}**")
                            
                            with col_topic2:
                                if not is_completed:
                                    if st.button(f"Mark Complete", key=f"complete_{i}_{j}"):
                                        st.session_state.grammar_progress['completed_topics'].append(topic['title'])
                                        st.session_state.grammar_progress['study_streak'] += 1
                                        st.success("✅ Topic marked as completed!")
                                        st.rerun()
                                else:
                                    st.success("✅ Completed")
                            
                            # Detailed explanation
                            if 'detailed_explanation' in topic:
                                st.markdown("**📖 Detailed Explanation:**")
                                st.markdown(topic['detailed_explanation'])
                            
                            # Interactive examples with pronunciation
                            st.markdown("**🎯 Examples with Pronunciation:**")
                            for example in topic['examples']:
                                if isinstance(example, dict):
                                    col_ex1, col_ex2, col_ex3 = st.columns([2, 2, 1])
                                    with col_ex1:
                                        st.markdown(f"**Indonesian:** {example['indonesian']}")
                                    with col_ex2:
                                        st.markdown(f"**English:** {example['english']}")
                                    with col_ex3:
                                        if 'pronunciation' in example:
                                            st.markdown(f"*{example['pronunciation']}*")
                                    if 'context' in example:
                                        st.caption(f"Context: {example['context']}")
                                    if 'method' in example:
                                        st.caption(f"Method: {example['method']}")
                                else:
                                    st.info(f"• {example}")
                            
                            # Key points with visual indicators
                            if 'key_points' in topic:
                                st.markdown("**🔑 Key Points to Remember:**")
                                for point in topic['key_points']:
                                    st.success(f"• {point}")
                            
                            # Common mistakes with visual warnings
                            if 'common_mistakes' in topic:
                                st.markdown("**⚠️ Common Mistakes to Avoid:**")
                                for mistake in topic['common_mistakes']:
                                    st.error(f"• {mistake}")
                            
                            # Interactive practice exercises
                            if 'practice_exercises' in topic:
                                st.markdown("**💪 Practice Exercises:**")
                                for exercise in topic['practice_exercises']:
                                    st.info(f"• {exercise}")
                                
                                # Interactive practice section
                                if st.button(f"Start Practice", key=f"practice_{i}_{j}"):
                                    st.session_state.current_practice = {
                                        'category': category,
                                        'topic': topic['title'],
                                        'exercises': topic['practice_exercises']
                                    }
                                    st.rerun()
                            
                            st.markdown("---")
        
        with col2:
            # Quick reference panel
            st.markdown("### 📚 Quick Reference")
            
            # Grammar cheat sheet
            st.markdown("**🔤 Basic Patterns:**")
            st.code("""
Saya makan nasi
(I eat rice)

Rumah besar
(big house)

Saya punya buku
(I have a book)
            """)
            
            # Common phrases
            st.markdown("**💬 Common Phrases:**")
            common_phrases = [
                "Selamat pagi (Good morning)",
                "Terima kasih (Thank you)",
                "Maaf (Sorry)",
                "Tolong (Please)",
                "Permisi (Excuse me)"
            ]
            for phrase in common_phrases:
                st.caption(f"• {phrase}")
            
            # Study tips
            st.markdown("**💡 Study Tips:**")
            st.caption("• Practice daily")
            st.caption("• Use examples")
            st.caption("• Review regularly")
            st.caption("• Focus on patterns")
            
            # Quick quiz button
            if st.button("🧠 Quick Quiz", width='stretch'):
                st.session_state.page = 'quiz'
                st.rerun()
        
        # Practice session modal
        if 'current_practice' in st.session_state and st.session_state.current_practice:
            practice = st.session_state.current_practice
            
            st.markdown("---")
            st.markdown(f"### 💪 Practice Session: {practice['topic']}")
            
            col_prac1, col_prac2 = st.columns([3, 1])
            
            with col_prac1:
                for i, exercise in enumerate(practice['exercises']):
                    st.markdown(f"**Exercise {i+1}:** {exercise}")
                    user_answer = st.text_input(f"Your answer:", key=f"practice_answer_{i}")
                    if st.button(f"Check Answer", key=f"check_{i}"):
                        st.info("Practice completed! Keep studying the examples above.")
            
            with col_prac2:
                if st.button("Close Practice", key="close_practice"):
                    st.session_state.current_practice = None
                    st.rerun()
        
        # Analytics modal
        if st.session_state.get('show_grammar_analytics', False):
            st.markdown("---")
            st.markdown("### 📊 Detailed Study Analytics")
            
            progress = st.session_state.grammar_progress
            
            col_anal1, col_anal2, col_anal3 = st.columns(3)
            
            with col_anal1:
                st.metric("Total Topics Completed", len(progress['completed_topics']))
                st.metric("Current Level", progress['current_level'].title())
            
            with col_anal2:
                st.metric("Study Streak", f"{progress['study_streak']} days")
                st.metric("Completion Rate", f"{len(progress['completed_topics'])}/50 topics")
            
            with col_anal3:
                if st.button("Reset Progress"):
                    st.session_state.grammar_progress = {
                        'completed_topics': [],
                        'current_level': 'beginner',
                        'study_streak': 0,
                        'total_study_time': 0
                    }
                    st.success("Progress reset!")
                    st.rerun()
            
            if st.button("Close Analytics"):
                st.session_state.show_grammar_analytics = False
                st.rerun()
    
    def render_workbook(self):
        """Render comprehensive workbook with interactive exercises"""
        st.title("📖 Interactive Workbook")
        st.markdown("Practice vocabulary, grammar, and sentence construction with interactive exercises!")
        
        # Initialize workbook session state
        if 'workbook_session' not in st.session_state:
            st.session_state.workbook_session = None
        if 'current_exercise' not in st.session_state:
            st.session_state.current_exercise = 0
        if 'exercise_answers' not in st.session_state:
            st.session_state.exercise_answers = {}
        
        # Workbook options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            difficulty = st.selectbox(
                "Select Difficulty Level:",
                options=["beginner", "intermediate", "advanced"],
                index=0
            )
        
        with col2:
            focus_areas = st.multiselect(
                "Choose Focus Areas:",
                options=["vocabulary", "grammar", "conversation", "translation", "fill_blank", "sentence_construction"],
                default=["vocabulary", "grammar", "translation"]
            )
        
        with col3:
            num_exercises = st.slider(
                "Number of Exercises:",
                min_value=5,
                max_value=20,
                value=10
            )
        
        # Create new workbook session
        if st.button("🎯 Start New Workbook Session", type="primary"):
            st.session_state.workbook_session = self.workbook_system.create_workbook_session(
                user_level=difficulty,
                focus_areas=focus_areas,
                num_exercises=num_exercises
            )
            st.session_state.current_exercise = 0
            st.session_state.exercise_answers = {}
            st.success("📚 New workbook session created! Let's start learning!")
            st.rerun()
        
        # Display current session
        if st.session_state.workbook_session:
            session = st.session_state.workbook_session
            exercises = session['exercises']
            
            st.markdown("---")
            st.subheader(f"📚 Workbook Session - {difficulty.title()} Level")
            
            # Progress bar
            progress = st.session_state.current_exercise / len(exercises)
            st.progress(progress)
            st.caption(f"Exercise {st.session_state.current_exercise + 1} of {len(exercises)}")
            
            # Display current exercise
            if st.session_state.current_exercise < len(exercises):
                exercise = exercises[st.session_state.current_exercise]
                self.render_exercise(exercise, st.session_state.current_exercise)
                
                # Navigation buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.session_state.current_exercise > 0:
                        if st.button("⬅️ Previous", width='stretch'):
                            st.session_state.current_exercise -= 1
                            st.rerun()
                
                with col2:
                    if st.button("✅ Submit Answer", type="primary", width='stretch'):
                        self.check_exercise_answer(exercise, st.session_state.current_exercise)
                
                with col3:
                    if st.session_state.current_exercise < len(exercises) - 1:
                        if st.button("➡️ Next", width='stretch'):
                            st.session_state.current_exercise += 1
                            st.rerun()
                    else:
                        if st.button("🏁 Finish Session", width='stretch'):
                            self.finish_workbook_session()
            else:
                self.finish_workbook_session()
        
        # Display workbook progress
        if st.session_state.workbook_session:
            st.markdown("---")
            st.subheader("📊 Your Progress")
            progress_summary = self.workbook_progress.get_progress_summary()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Exercises Completed", progress_summary.get('total_exercises', 0))
            
            with col2:
                st.metric("Average Score", f"{progress_summary.get('average_score', 0):.1f}%")
            
            with col3:
                st.metric("Weak Areas", progress_summary.get('weak_areas', 0))
            
            with col4:
                st.metric("Strengths", progress_summary.get('strengths', 0))
    
    def render_exercise(self, exercise, exercise_index):
        """Render individual exercise"""
        exercise_type = exercise['type']
        
        st.markdown(f"### {EXERCISE_TEMPLATES[exercise_type]['icon']} {EXERCISE_TEMPLATES[exercise_type]['title']}")
        st.markdown(f"**{EXERCISE_TEMPLATES[exercise_type]['description']}**")
        
        if exercise_type == "fill_in_blank":
            self.render_fill_in_blank_exercise(exercise, exercise_index)
        elif exercise_type == "translation":
            self.render_translation_exercise(exercise, exercise_index)
        elif exercise_type == "vocabulary_matching":
            self.render_vocabulary_matching_exercise(exercise, exercise_index)
        elif exercise_type == "sentence_construction":
            self.render_sentence_construction_exercise(exercise, exercise_index)
        elif exercise_type == "grammar_focus":
            self.render_grammar_focus_exercise(exercise, exercise_index)
        elif exercise_type == "conversation_practice":
            self.render_conversation_practice_exercise(exercise, exercise_index)
    
    def render_fill_in_blank_exercise(self, exercise, exercise_index):
        """Render fill-in-the-blank exercise"""
        st.markdown(f"**Complete the sentence:**")
        st.markdown(f"*{exercise['sentence']}*")
        
        if 'hint' in exercise:
            with st.expander("💡 Hint"):
                st.markdown(exercise['hint'])
        
        # Create input fields for blanks
        answers = {}
        for key, answer in exercise['answers'].items():
            blank_num = key.split('_')[1]
            user_answer = st.text_input(
                f"Blank {blank_num}:",
                key=f"blank_{exercise_index}_{blank_num}",
                placeholder="Enter your answer..."
            )
            answers[key] = user_answer
        
        st.session_state.exercise_answers[exercise_index] = answers
    
    def render_translation_exercise(self, exercise, exercise_index):
        """Render translation exercise"""
        st.markdown(f"**{exercise['instruction']}**")
        st.markdown(f"**{exercise['source_text']}**")
        
        if exercise['direction'] == 'indonesian_to_english':
            user_answer = st.text_area(
                "Your English translation:",
                key=f"translation_{exercise_index}",
                placeholder="Enter your translation here...",
                height=100
            )
        else:
            user_answer = st.text_area(
                "Your Indonesian translation:",
                key=f"translation_{exercise_index}",
                placeholder="Enter your translation here...",
                height=100
            )
        
        if 'pronunciation' in exercise and exercise['pronunciation']:
            with st.expander("🔊 Pronunciation Guide"):
                st.markdown(f"*{exercise['pronunciation']}*")
        
        st.session_state.exercise_answers[exercise_index] = user_answer
    
    def render_vocabulary_matching_exercise(self, exercise, exercise_index):
        """Render vocabulary matching exercise"""
        st.markdown(f"**{exercise['instruction']}**")
        
        pairs = exercise['pairs']
        indonesian_words = [pair['indonesian'] for pair in pairs]
        english_words = [pair['english'] for pair in pairs]
        
        # Create matching interface
        st.markdown("**Indonesian Words:**")
        for i, word in enumerate(indonesian_words):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"{i+1}. {word}")
            with col2:
                match = st.selectbox(
                    f"Match {i+1}:",
                    options=[""] + english_words,
                    key=f"match_{exercise_index}_{i}"
                )
        
        st.session_state.exercise_answers[exercise_index] = {
            "matches": [st.session_state.get(f"match_{exercise_index}_{i}", "") for i in range(len(indonesian_words))]
        }
    
    def render_sentence_construction_exercise(self, exercise, exercise_index):
        """Render sentence construction exercise"""
        st.markdown(f"**{exercise['instruction']}**")
        
        if 'pattern_explanation' in exercise:
            st.info(f"**Grammar Pattern:** {exercise['pattern_explanation']}")
        
        if 'example' in exercise:
            st.markdown(f"**Example:** {exercise['example']}")
        
        user_sentence = st.text_area(
            "Your sentence:",
            key=f"sentence_{exercise_index}",
            placeholder="Construct your sentence here...",
            height=100
        )
        
        st.session_state.exercise_answers[exercise_index] = user_sentence
    
    def render_grammar_focus_exercise(self, exercise, exercise_index):
        """Render grammar focus exercise"""
        st.markdown(f"**Grammar Topic: {exercise['topic']}**")
        
        if 'examples' in exercise:
            st.markdown("**Examples:**")
            for example in exercise['examples']:
                st.markdown(f"- {example}")
        
        practice_type = st.selectbox(
            "Choose practice type:",
            options=exercise['practice_sentences'],
            key=f"practice_type_{exercise_index}"
        )
        
        user_response = st.text_area(
            "Your response:",
            key=f"grammar_{exercise_index}",
            placeholder="Write your response here...",
            height=150
        )
        
        st.session_state.exercise_answers[exercise_index] = {
            "practice_type": practice_type,
            "response": user_response
        }
    
    def render_conversation_practice_exercise(self, exercise, exercise_index):
        """Render conversation practice exercise"""
        st.markdown(f"**Scenario: {exercise['scenario']}**")
        
        if 'key_phrases' in exercise:
            st.markdown("**Key Phrases to Use:**")
            for phrase in exercise['key_phrases']:
                st.markdown(f"- {phrase}")
        
        user_conversation = st.text_area(
            "Write your conversation:",
            key=f"conversation_{exercise_index}",
            placeholder="Write your conversation here...",
            height=200
        )
        
        st.session_state.exercise_answers[exercise_index] = user_conversation
    
    def check_exercise_answer(self, exercise, exercise_index):
        """Check exercise answer and provide feedback"""
        user_answer = st.session_state.exercise_answers.get(exercise_index, "")
        
        if exercise['type'] == "fill_in_blank":
            self.check_fill_in_blank_answer(exercise, user_answer, exercise_index)
        elif exercise['type'] == "translation":
            self.check_translation_answer(exercise, user_answer, exercise_index)
        elif exercise['type'] == "vocabulary_matching":
            self.check_vocabulary_matching_answer(exercise, user_answer, exercise_index)
        elif exercise['type'] == "sentence_construction":
            self.check_sentence_construction_answer(exercise, user_answer, exercise_index)
        elif exercise['type'] == "grammar_focus":
            self.check_grammar_focus_answer(exercise, user_answer, exercise_index)
        elif exercise['type'] == "conversation_practice":
            self.check_conversation_practice_answer(exercise, user_answer, exercise_index)
        else:
            st.info("✅ Answer recorded! Great job practicing!")
    
    def check_fill_in_blank_answer(self, exercise, user_answer, exercise_index):
        """Check fill-in-the-blank answers with enhanced feedback"""
        correct_answers = exercise['answers']
        score = 0
        total = len(correct_answers)
        
        st.markdown("### 📝 Fill-in-the-Blank Review")
        
        # Show the original sentence with blanks
        sentence = exercise.get('sentence', '')
        st.markdown(f"**Original sentence:** {sentence}")
        
        for key, correct_answer in correct_answers.items():
            user_answer = user_answers.get(key, "").strip().lower()
            correct = correct_answer.lower()
            blank_num = key.split('_')[1]
            
            if user_answer == correct:
                st.success(f"✅ Blank {blank_num}: **{user_answer}** ✓ (Correct!)")
                score += 1
            else:
                st.error(f"❌ Blank {blank_num}: **{user_answer}** ✗")
                st.info(f"   **Correct answer:** {correct_answer}")
                if exercise.get('hints', {}).get(key):
                    st.info(f"   **Hint:** {exercise['hints'][key]}")
        
        percentage = (score / total) * 100
        
        # Show overall feedback
        if percentage == 100:
            st.success("🎉 Perfect! All blanks filled correctly!")
        elif percentage >= 70:
            st.warning(f"⚠️ Good effort! You got {score}/{total} correct. Review the mistakes above.")
        else:
            st.error(f"❌ Keep practicing! You got {score}/{total} correct. Study the solutions above.")
        
        st.markdown(f"**Final Score: {score}/{total} ({percentage:.1f}%)**")
        
        # Record progress
        self.workbook_progress.record_exercise_completion(
            f"fill_blank_{exercise_index}",
            percentage,
            0  # Time not tracked for now
        )
    
    def check_translation_answer(self, exercise, user_answer, exercise_index):
        """Check translation answers with enhanced feedback"""
        correct_answer = exercise['correct_answer'].lower()
        user_lower = user_answer.lower().strip()
        
        st.markdown("### 📝 Translation Review")
        
        # Show the original text
        if exercise.get('direction') == 'indonesian_to_english':
            st.markdown(f"**Indonesian:** {exercise['source']}")
        else:
            st.markdown(f"**English:** {exercise['source']}")
        
        # Show user's answer
        st.markdown(f"**Your answer:** {user_answer}")
        
        # Simple similarity check (could be improved with more sophisticated matching)
        if user_lower == correct_answer:
            st.success("✅ Perfect translation!")
            score = 100
        elif any(word in user_lower for word in correct_answer.split()):
            st.warning("⚠️ Partially correct! You're on the right track.")
            st.info(f"**Correct answer:** {exercise['correct_answer']}")
            st.info(f"**Explanation:** You got some words right! Try to match the complete sentence structure.")
            score = 70
        else:
            st.error("❌ Not quite right. Here's the solution:")
            st.info(f"**Correct answer:** {exercise['correct_answer']}")
            if exercise.get('pronunciation'):
                st.info(f"**Pronunciation:** {exercise['pronunciation']}")
            if exercise.get('grammar_focus'):
                st.info(f"**Grammar focus:** {exercise['grammar_focus']}")
            score = 30
        
        st.markdown(f"**Score: {score}%**")
        
        # Record progress
        self.workbook_progress.record_exercise_completion(
            f"translation_{exercise_index}",
            score,
            0
        )
    
    def check_vocabulary_matching_answer(self, exercise, user_answer, exercise_index):
        """Check vocabulary matching answers with enhanced feedback"""
        pairs = exercise['pairs']
        matches = user_answer.get('matches', [])
        
        score = 0
        total = len(pairs)
        
        st.markdown("### 📝 Vocabulary Matching Review")
        
        for i, pair in enumerate(pairs):
            user_match = matches[i] if i < len(matches) else ""
            correct_english = pair['english']
            
            if user_match == correct_english:
                st.success(f"✅ **{pair['indonesian']}** → **{correct_english}** ✓")
                score += 1
            else:
                st.error(f"❌ **{pair['indonesian']}** → **{user_match}** ✗")
                st.info(f"   **Correct answer:** {correct_english}")
                if pair.get('pronunciation'):
                    st.info(f"   **Pronunciation:** {pair['pronunciation']}")
                if pair.get('example'):
                    st.info(f"   **Example:** {pair['example']}")
        
        percentage = (score / total) * 100
        
        # Show overall feedback
        if percentage == 100:
            st.success("🎉 Excellent! All vocabulary matches are correct!")
        elif percentage >= 70:
            st.warning(f"⚠️ Good job! You matched {score}/{total} correctly. Review the mistakes above.")
        else:
            st.error(f"❌ Keep studying! You matched {score}/{total} correctly. Check the solutions above.")
        
        st.markdown(f"**Final Score: {score}/{total} ({percentage:.1f}%)**")
        
        # Record progress
        self.workbook_progress.record_exercise_completion(
            f"matching_{exercise_index}",
            percentage,
            0
        )
    
    def check_sentence_construction_answer(self, exercise, user_answer, exercise_index):
        """Check sentence construction answers with enhanced feedback"""
        st.markdown("### 📝 Sentence Construction Review")
        
        # Show the pattern and example
        pattern = exercise.get('pattern', {})
        st.markdown(f"**Pattern:** {pattern.get('pattern', '')}")
        st.markdown(f"**Example:** {pattern.get('example', '')}")
        
        # Show user's answer
        st.markdown(f"**Your sentence:** {user_answer}")
        
        # Simple scoring based on key words
        key_words = exercise.get('key_words', [])
        user_words = user_answer.lower().split()
        matches = sum(1 for word in key_words if word.lower() in user_words)
        
        if matches >= len(key_words) * 0.8:
            st.success("✅ Great sentence construction!")
            score = 100
        elif matches >= len(key_words) * 0.5:
            st.warning("⚠️ Good effort! Try to include more key words.")
            st.info(f"**Key words to include:** {', '.join(key_words)}")
            score = 70
        else:
            st.error("❌ Keep practicing! Include more key words in your sentence.")
            st.info(f"**Key words to include:** {', '.join(key_words)}")
            st.info(f"**Example sentence:** {pattern.get('example', '')}")
            score = 30
        
        st.markdown(f"**Score: {score}%**")
        
        # Record progress
        self.workbook_progress.record_exercise_completion(
            f"sentence_construction_{exercise_index}",
            score,
            0
        )
    
    def check_grammar_focus_answer(self, exercise, user_answer, exercise_index):
        """Check grammar focus answers with enhanced feedback"""
        st.markdown("### 📝 Grammar Focus Review")
        
        # Show the grammar topic
        topic = exercise.get('topic', '')
        st.markdown(f"**Grammar Topic:** {topic}")
        
        # Show user's answer
        if user_answer and user_answer.strip():
            st.markdown(f"**Your answer:** {user_answer}")
        else:
            st.warning("⚠️ No answer provided - showing complete solution below")
        
        # Show examples and explanations
        examples = exercise.get('examples', [])
        if examples:
            st.markdown("**Examples:**")
            for example in examples:
                st.info(f"• {example}")
        
        explanation = exercise.get('explanation', '')
        if explanation:
            st.markdown(f"**Explanation:** {explanation}")
        
        # Show practice instructions
        practice_type = exercise.get('practice_type', '')
        if practice_type:
            st.markdown(f"**Practice:** {practice_type}")
        
        # Show complete solution
        st.markdown("**Complete Solution:**")
        st.success("📚 Study the examples and explanation above to master this grammar topic!")
        
        # Show additional resources
        if exercise.get('key_points'):
            st.markdown("**Key Points to Remember:**")
            for point in exercise['key_points']:
                st.info(f"• {point}")
        
        # Only give score if user actually answered
        if user_answer and user_answer.strip():
            st.info("✅ Grammar practice completed! Review the examples and explanation above.")
            score = 80
        else:
            st.warning("⚠️ Complete the exercise next time to get a score!")
            score = 0
        
        st.markdown(f"**Score: {score}%**")
        
        # Record progress
        self.workbook_progress.record_exercise_completion(
            f"grammar_focus_{exercise_index}",
            score,
            0
        )
    
    def check_conversation_practice_answer(self, exercise, user_answer, exercise_index):
        """Check conversation practice answers with enhanced feedback"""
        st.markdown("### 📝 Conversation Practice Review")
        
        # Show the scenario
        scenario = exercise.get('scenario', '')
        st.markdown(f"**Scenario:** {scenario}")
        
        # Show user's response
        st.markdown(f"**Your response:** {user_answer}")
        
        # Show key phrases
        key_phrases = exercise.get('key_phrases', [])
        if key_phrases:
            st.markdown("**Key phrases to practice:**")
            for phrase in key_phrases:
                st.info(f"• {phrase}")
        
        # Show additional tips
        tips = exercise.get('tips', [])
        if tips:
            st.markdown("**Conversation tips:**")
            for tip in tips:
                st.info(f"• {tip}")
        
        # Always give positive feedback for conversation practice
        st.success("✅ Great conversation practice! Keep practicing these phrases.")
        score = 85  # Always give good score for conversation practice
        
        st.markdown(f"**Score: {score}%**")
        
        # Record progress
        self.workbook_progress.record_exercise_completion(
            f"conversation_practice_{exercise_index}",
            score,
            0
        )
    
    def finish_workbook_session(self):
        """Finish workbook session and show summary"""
        st.markdown("---")
        st.subheader("🎉 Workbook Session Complete!")
        
        progress_summary = self.workbook_progress.get_progress_summary()
        
        st.markdown("### 📊 Session Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Exercises Completed", progress_summary.get('total_exercises', 0))
        
        with col2:
            st.metric("Average Score", f"{progress_summary.get('average_score', 0):.1f}%")
        
        with col3:
            st.metric("Completion Rate", progress_summary.get('completion_rate', '0%'))
        
        if progress_summary.get('weak_areas', 0) > 0:
            st.warning(f"🔍 You have {progress_summary['weak_areas']} areas to focus on. Keep practicing!")
        
        if progress_summary.get('strengths', 0) > 0:
            st.success(f"💪 Great job! You have {progress_summary['strengths']} strong areas!")
        
        if st.button("🔄 Start New Session", type="primary"):
            st.session_state.workbook_session = None
            st.session_state.current_exercise = 0
            st.session_state.exercise_answers = {}
            st.rerun()

# Run the app
if __name__ == "__main__":
    app = IndonesianLearningApp()
    app.run()
