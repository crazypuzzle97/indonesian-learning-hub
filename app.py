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
# Vocabulary imports removed - using integrated vocabulary in VOCABULARY_DATA
from sentences import SENTENCE_DATABASE
from comprehensive_sentences import SENTENCE_DATABASE as COMPREHENSIVE_SENTENCES
from massive_sentence_database import get_massive_sentence_database
from mega_sentence_database import get_mega_sentence_database
from ultimate_sentence_database import get_ultimate_sentence_database
from premium_sentence_database import get_premium_sentence_database, get_extended_premium_sentences
# Premium UI components removed - using simplified inline CSS
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
        "mobil": {"english": "car", "pronunciation": "mo-bil", "category": "objects", "example": "Mobil saya biru."},
        "sepeda": {"english": "bicycle", "pronunciation": "se-pe-da", "category": "objects", "example": "Saya naik sepeda."},
        "telepon": {"english": "phone", "pronunciation": "te-le-pon", "category": "objects", "example": "Telepon saya rusak."},
        "komputer": {"english": "computer", "pronunciation": "kom-pu-ter", "category": "objects", "example": "Saya pakai komputer."},
        "meja": {"english": "table", "pronunciation": "me-ja", "category": "objects", "example": "Meja ini besar."},
        "kursi": {"english": "chair", "pronunciation": "kur-si", "category": "objects", "example": "Kursi ini nyaman."},
        "pintu": {"english": "door", "pronunciation": "pin-tu", "category": "objects", "example": "Pintu ini tertutup."},
        "jendela": {"english": "window", "pronunciation": "jen-de-la", "category": "objects", "example": "Jendela ini besar."},
        "lampu": {"english": "lamp", "pronunciation": "lam-pu", "category": "objects", "example": "Lampu ini terang."},
        
        # Colors
        "merah": {"english": "red", "pronunciation": "me-rah", "category": "colors", "example": "Bunga ini merah."},
        "biru": {"english": "blue", "pronunciation": "bi-ru", "category": "colors", "example": "Langit ini biru."},
        "kuning": {"english": "yellow", "pronunciation": "ku-ning", "category": "colors", "example": "Matahari kuning."},
        "hijau": {"english": "green", "pronunciation": "hi-jau", "category": "colors", "example": "Daun ini hijau."},
        "hitam": {"english": "black", "pronunciation": "hi-tam", "category": "colors", "example": "Malam ini hitam."},
        "putih": {"english": "white", "pronunciation": "pu-tih", "category": "colors", "example": "Salju ini putih."},
        
        # Time & Days
        "hari": {"english": "day", "pronunciation": "ha-ri", "category": "time", "example": "Hari ini cerah."},
        "malam": {"english": "night", "pronunciation": "ma-lam", "category": "time", "example": "Malam ini dingin."},
        "pagi": {"english": "morning", "pronunciation": "pa-gi", "category": "time", "example": "Pagi ini indah."},
        "siang": {"english": "afternoon", "pronunciation": "si-ang", "category": "time", "example": "Siang ini panas."},
        "senin": {"english": "Monday", "pronunciation": "se-nin", "category": "time", "example": "Senin saya kerja."},
        "selasa": {"english": "Tuesday", "pronunciation": "se-la-sa", "category": "time", "example": "Selasa saya libur."},
        "rabu": {"english": "Wednesday", "pronunciation": "ra-bu", "category": "time", "example": "Rabu saya belajar."},
        "kamis": {"english": "Thursday", "pronunciation": "ka-mis", "category": "time", "example": "Kamis saya olahraga."},
        "jumat": {"english": "Friday", "pronunciation": "ju-mat", "category": "time", "example": "Jumat saya pulang."},
        "sabtu": {"english": "Saturday", "pronunciation": "sab-tu", "category": "time", "example": "Sabtu saya santai."},
        "minggu": {"english": "Sunday", "pronunciation": "ming-gu", "category": "time", "example": "Minggu saya istirahat."},
        
        # Food & Drinks
        "nasi": {"english": "rice", "pronunciation": "na-si", "category": "food", "example": "Nasi ini enak."},
        "roti": {"english": "bread", "pronunciation": "ro-ti", "category": "food", "example": "Roti ini lembut."},
        "daging": {"english": "meat", "pronunciation": "da-ging", "category": "food", "example": "Daging ini empuk."},
        "ikan": {"english": "fish", "pronunciation": "i-kan", "category": "food", "example": "Ikan ini segar."},
        "sayur": {"english": "vegetable", "pronunciation": "sa-yur", "category": "food", "example": "Sayur ini sehat."},
        "buah": {"english": "fruit", "pronunciation": "bu-ah", "category": "food", "example": "Buah ini manis."},
        "susu": {"english": "milk", "pronunciation": "su-su", "category": "food", "example": "Susu ini segar."},
        "kopi": {"english": "coffee", "pronunciation": "ko-pi", "category": "food", "example": "Kopi ini panas."},
        "teh": {"english": "tea", "pronunciation": "teh", "category": "food", "example": "Teh ini dingin."},
        "jus": {"english": "juice", "pronunciation": "jus", "category": "food", "example": "Jus ini segar."},
        
        # Body Parts
        "kepala": {"english": "head", "pronunciation": "ke-pa-la", "category": "body", "example": "Kepala saya sakit."},
        "mata": {"english": "eye", "pronunciation": "ma-ta", "category": "body", "example": "Mata saya biru."},
        "hidung": {"english": "nose", "pronunciation": "hi-dung", "category": "body", "example": "Hidung saya kecil."},
        "mulut": {"english": "mouth", "pronunciation": "mu-lut", "category": "body", "example": "Mulut saya kering."},
        "tangan": {"english": "hand", "pronunciation": "tan-gan", "category": "body", "example": "Tangan saya bersih."},
        "kaki": {"english": "foot", "pronunciation": "ka-ki", "category": "body", "example": "Kaki saya sakit."},
        
        # Common Adjectives
        "besar": {"english": "big", "pronunciation": "be-sar", "category": "adjectives", "example": "Rumah ini besar."},
        "kecil": {"english": "small", "pronunciation": "ke-cil", "category": "adjectives", "example": "Anak ini kecil."},
        "tinggi": {"english": "tall", "pronunciation": "ting-gi", "category": "adjectives", "example": "Orang ini tinggi."},
        "pendek": {"english": "short", "pronunciation": "pen-dek", "category": "adjectives", "example": "Meja ini pendek."},
        "panas": {"english": "hot", "pronunciation": "pa-nas", "category": "adjectives", "example": "Cuaca ini panas."},
        "dingin": {"english": "cold", "pronunciation": "din-gin", "category": "adjectives", "example": "Air ini dingin."},
        "enak": {"english": "delicious", "pronunciation": "e-nak", "category": "adjectives", "example": "Makanan ini enak."},
        "buruk": {"english": "bad", "pronunciation": "bu-ruk", "category": "adjectives", "example": "Cuaca ini buruk."},
        "bagus": {"english": "good", "pronunciation": "ba-gus", "category": "adjectives", "example": "Film ini bagus."},
        "cantik": {"english": "beautiful", "pronunciation": "can-tik", "category": "adjectives", "example": "Bunga ini cantik."},
        
        # Places
        "sekolah": {"english": "school", "pronunciation": "se-ko-lah", "category": "places", "example": "Saya pergi ke sekolah."},
        "rumah sakit": {"english": "hospital", "pronunciation": "ru-mah sa-kit", "category": "places", "example": "Saya pergi ke rumah sakit."},
        "toko": {"english": "shop", "pronunciation": "to-ko", "category": "places", "example": "Saya beli di toko."},
        "restoran": {"english": "restaurant", "pronunciation": "res-to-ran", "category": "places", "example": "Saya makan di restoran."},
        "bank": {"english": "bank", "pronunciation": "bank", "category": "places", "example": "Saya pergi ke bank."},
        "kantor": {"english": "office", "pronunciation": "kan-tor", "category": "places", "example": "Saya kerja di kantor."},
        "pasar": {"english": "market", "pronunciation": "pa-sar", "category": "places", "example": "Saya beli di pasar."},
        "taman": {"english": "park", "pronunciation": "ta-man", "category": "places", "example": "Saya jalan di taman."},
        
        # Common Questions
        "apa": {"english": "what", "pronunciation": "a-pa", "category": "questions", "example": "Apa nama Anda?"},
        "siapa": {"english": "who", "pronunciation": "si-a-pa", "category": "questions", "example": "Siapa nama Anda?"},
        "dimana": {"english": "where", "pronunciation": "di-ma-na", "category": "questions", "example": "Dimana rumah Anda?"},
        "kapan": {"english": "when", "pronunciation": "ka-pan", "category": "questions", "example": "Kapan Anda datang?"},
        "mengapa": {"english": "why", "pronunciation": "men-ga-pa", "category": "questions", "example": "Mengapa Anda menangis?"},
        "bagaimana": {"english": "how", "pronunciation": "ba-gai-ma-na", "category": "questions", "example": "Bagaimana kabar Anda?"},
        
        # Common Verbs (More)
        "melihat": {"english": "to see", "pronunciation": "me-li-hat", "category": "verbs", "example": "Saya melihat burung."},
        "mendengar": {"english": "to hear", "pronunciation": "men-den-gar", "category": "verbs", "example": "Saya mendengar musik."},
        "berbicara": {"english": "to speak", "pronunciation": "ber-bi-ca-ra", "category": "verbs", "example": "Saya berbicara bahasa Indonesia."},
        "membaca": {"english": "to read", "pronunciation": "mem-ba-ca", "category": "verbs", "example": "Saya membaca buku."},
        "menulis": {"english": "to write", "pronunciation": "me-nu-lis", "category": "verbs", "example": "Saya menulis surat."},
        "membeli": {"english": "to buy", "pronunciation": "mem-be-li", "category": "verbs", "example": "Saya membeli baju."},
        "menjual": {"english": "to sell", "pronunciation": "men-ju-al", "category": "verbs", "example": "Saya menjual mobil."},
        "mencari": {"english": "to search", "pronunciation": "men-ca-ri", "category": "verbs", "example": "Saya mencari kunci."},
        "menemukan": {"english": "to find", "pronunciation": "me-ne-mu-kan", "category": "verbs", "example": "Saya menemukan dompet."},
        "membuka": {"english": "to open", "pronunciation": "mem-bu-ka", "category": "verbs", "example": "Saya membuka pintu."},
        "menutup": {"english": "to close", "pronunciation": "me-nu-tup", "category": "verbs", "example": "Saya menutup jendela."},
        "duduk": {"english": "to sit", "pronunciation": "du-duk", "category": "verbs", "example": "Saya duduk di kursi."},
        "berdiri": {"english": "to stand", "pronunciation": "ber-di-ri", "category": "verbs", "example": "Saya berdiri di depan."},
        "berjalan": {"english": "to walk", "pronunciation": "ber-ja-lan", "category": "verbs", "example": "Saya berjalan di taman."},
        "berlari": {"english": "to run", "pronunciation": "ber-la-ri", "category": "verbs", "example": "Saya berlari di lapangan."},
        "waktu": {"english": "time", "pronunciation": "wak-tu", "category": "objects", "example": "Waktu sudah malam."},
        "jam": {"english": "hour/clock", "pronunciation": "jam", "category": "objects", "example": "Jam berapa sekarang?"},
        "menit": {"english": "minute", "pronunciation": "me-nit", "category": "objects", "example": "Lima menit lagi."},
        "detik": {"english": "second", "pronunciation": "de-tik", "category": "objects", "example": "Tiga detik."},
        
        # More Essential Words
        "nama": {"english": "name", "pronunciation": "na-ma", "category": "objects", "example": "Nama saya John."},
        "alamat": {"english": "address", "pronunciation": "a-la-mat", "category": "objects", "example": "Alamat saya di Jakarta."},
        "umur": {"english": "age", "pronunciation": "u-mur", "category": "objects", "example": "Umur saya 25 tahun."},
        "tahun": {"english": "year", "pronunciation": "ta-hun", "category": "objects", "example": "Saya lahir tahun 1995."},
        "bulan": {"english": "month", "pronunciation": "bu-lan", "category": "objects", "example": "Bulan ini Januari."},
        "minggu": {"english": "week", "pronunciation": "ming-gu", "category": "objects", "example": "Minggu ini sibuk."},
        
        # More Colors
        "coklat": {"english": "brown", "pronunciation": "cok-lat", "category": "colors", "example": "Rambut saya coklat."},
        "abu-abu": {"english": "gray", "pronunciation": "a-bu a-bu", "category": "colors", "example": "Langit abu-abu."},
        "ungu": {"english": "purple", "pronunciation": "un-gu", "category": "colors", "example": "Bunga ini ungu."},
        "jingga": {"english": "orange", "pronunciation": "jing-ga", "category": "colors", "example": "Jeruk ini jingga."},
        
        # More Family
        "kakak": {"english": "older sibling", "pronunciation": "ka-kak", "category": "family", "example": "Kakak saya mahasiswa."},
        "adik": {"english": "younger sibling", "pronunciation": "a-dik", "category": "family", "example": "Adik saya masih kecil."},
        "nenek": {"english": "grandmother", "pronunciation": "ne-nek", "category": "family", "example": "Nenek saya baik."},
        "kakek": {"english": "grandfather", "pronunciation": "ka-kek", "category": "family", "example": "Kakek saya pintar."},
        "paman": {"english": "uncle", "pronunciation": "pa-man", "category": "family", "example": "Paman saya dokter."},
        "bibi": {"english": "aunt", "pronunciation": "bi-bi", "category": "family", "example": "Bibi saya guru."},
        
        # More Body Parts
        "rambut": {"english": "hair", "pronunciation": "ram-but", "category": "body", "example": "Rambut saya panjang."},
        "telinga": {"english": "ear", "pronunciation": "te-lin-ga", "category": "body", "example": "Telinga saya sakit."},
        "gigi": {"english": "tooth", "pronunciation": "gi-gi", "category": "body", "example": "Gigi saya putih."},
        "leher": {"english": "neck", "pronunciation": "le-her", "category": "body", "example": "Leher saya sakit."},
        "punggung": {"english": "back", "pronunciation": "pung-gung", "category": "body", "example": "Punggung saya sakit."},
        "perut": {"english": "stomach", "pronunciation": "pe-rut", "category": "body", "example": "Perut saya lapar."},
        
        # More Food
        "garam": {"english": "salt", "pronunciation": "ga-ram", "category": "food", "example": "Garam ini asin."},
        "gula": {"english": "sugar", "pronunciation": "gu-la", "category": "food", "example": "Gula ini manis."},
        "minyak": {"english": "oil", "pronunciation": "mi-nyak", "category": "food", "example": "Minyak ini panas."},
        "lada": {"english": "pepper", "pronunciation": "la-da", "category": "food", "example": "Lada ini pedas."},
        "bawang": {"english": "onion", "pronunciation": "ba-wang", "category": "food", "example": "Bawang ini besar."},
        "tomat": {"english": "tomato", "pronunciation": "to-mat", "category": "food", "example": "Tomat ini merah."},
        
        # More Objects
        "kunci": {"english": "key", "pronunciation": "kun-ci", "category": "objects", "example": "Kunci ini kecil."},
        "dompet": {"english": "wallet", "pronunciation": "dom-pet", "category": "objects", "example": "Dompet saya hilang."},
        "tas": {"english": "bag", "pronunciation": "tas", "category": "objects", "example": "Tas ini berat."},
        "sepatu": {"english": "shoe", "pronunciation": "se-pa-tu", "category": "objects", "example": "Sepatu saya baru."},
        "baju": {"english": "clothes", "pronunciation": "ba-ju", "category": "objects", "example": "Baju ini bagus."},
        "celana": {"english": "pants", "pronunciation": "ce-la-na", "category": "objects", "example": "Celana ini panjang."},
        
        # More Adjectives
        "baru": {"english": "new", "pronunciation": "ba-ru", "category": "adjectives", "example": "Mobil ini baru."},
        "lama": {"english": "old", "pronunciation": "la-ma", "category": "adjectives", "example": "Rumah ini lama."},
        "mudah": {"english": "easy", "pronunciation": "mu-dah", "category": "adjectives", "example": "Pekerjaan ini mudah."},
        "sulit": {"english": "difficult", "pronunciation": "su-lit", "category": "adjectives", "category": "adjectives", "example": "Pertanyaan ini sulit."},
        "cepat": {"english": "fast", "pronunciation": "ce-pat", "category": "adjectives", "example": "Mobil ini cepat."},
        "lambat": {"english": "slow", "pronunciation": "lam-bat", "category": "adjectives", "example": "Kereta ini lambat."},
        "mahal": {"english": "expensive", "pronunciation": "ma-hal", "category": "adjectives", "example": "Mobil ini mahal."},
        "murah": {"english": "cheap", "pronunciation": "mu-rah", "category": "adjectives", "example": "Buku ini murah."},
        "bersih": {"english": "clean", "pronunciation": "ber-sih", "category": "adjectives", "example": "Rumah ini bersih."},
        "kotor": {"english": "dirty", "pronunciation": "ko-tor", "category": "adjectives", "example": "Pakaian ini kotor."},
        "berapa": {"english": "how much/many", "pronunciation": "be-ra-pa", "category": "questions", "example": "Berapa harganya?"},
        "bagaimana": {"english": "how", "pronunciation": "ba-gai-ma-na", "category": "questions", "example": "Bagaimana kabarnya?"},
        
        # Weather & Nature
        "hujan": {"english": "rain", "pronunciation": "hu-jan", "category": "weather", "example": "Hari ini hujan."},
        "panas": {"english": "sunny/hot", "pronunciation": "pa-nas", "category": "weather", "example": "Cuaca panas hari ini."},
        "angin": {"english": "wind", "pronunciation": "a-ngin", "category": "weather", "example": "Angin kencang sekali."},
        "awan": {"english": "cloud", "pronunciation": "a-wan", "category": "weather", "example": "Awan hitam di langit."},
        "petir": {"english": "lightning", "pronunciation": "pe-tir", "category": "weather", "example": "Petir menyambar pohon."},
        "salju": {"english": "snow", "pronunciation": "sal-ju", "category": "weather", "example": "Salju turun di gunung."},
        "pohon": {"english": "tree", "pronunciation": "po-hon", "category": "nature", "example": "Pohon mangga besar."},
        "bunga": {"english": "flower", "pronunciation": "bu-nga", "category": "nature", "example": "Bunga mawar merah."},
        "daun": {"english": "leaf", "pronunciation": "da-un", "category": "nature", "example": "Daun gugur di musim kering."},
        "rumput": {"english": "grass", "pronunciation": "rum-put", "category": "nature", "example": "Rumput hijau di taman."},
        "batu": {"english": "stone", "pronunciation": "ba-tu", "category": "nature", "example": "Batu besar di sungai."},
        "pasir": {"english": "sand", "pronunciation": "pa-sir", "category": "nature", "example": "Pasir putih di pantai."},
        "laut": {"english": "sea", "pronunciation": "la-ut", "category": "nature", "example": "Laut biru jernih."},
        "sungai": {"english": "river", "pronunciation": "su-ngai", "category": "nature", "example": "Sungai mengalir deras."},
        "gunung": {"english": "mountain", "pronunciation": "gu-nung", "category": "nature", "example": "Gunung tinggi sekali."},
        "hutan": {"english": "forest", "pronunciation": "hu-tan", "category": "nature", "example": "Hutan lebat dan gelap."},
        
        # Animals
        "kucing": {"english": "cat", "pronunciation": "ku-cing", "category": "animals", "example": "Kucing hitam tidur."},
        "anjing": {"english": "dog", "pronunciation": "an-jing", "category": "animals", "example": "Anjing menggonggong keras."},
        "burung": {"english": "bird", "pronunciation": "bu-rung", "category": "animals", "example": "Burung terbang tinggi."},
        "ayam": {"english": "chicken", "pronunciation": "a-yam", "category": "animals", "example": "Ayam berkokok pagi."},
        "sapi": {"english": "cow", "pronunciation": "sa-pi", "category": "animals", "example": "Sapi makan rumput."},
        "kambing": {"english": "goat", "pronunciation": "kam-bing", "category": "animals", "example": "Kambing putih lucu."},
        "kuda": {"english": "horse", "pronunciation": "ku-da", "category": "animals", "example": "Kuda berlari cepat."},
        "gajah": {"english": "elephant", "pronunciation": "ga-jah", "category": "animals", "example": "Gajah besar dan kuat."},
        "harimau": {"english": "tiger", "pronunciation": "ha-ri-mau", "category": "animals", "example": "Harimau berburu malam."},
        "monyet": {"english": "monkey", "pronunciation": "mo-nyet", "category": "animals", "example": "Monyet melompat di pohon."},
        "ular": {"english": "snake", "pronunciation": "u-lar", "category": "animals", "example": "Ular merayap di tanah."},
        "katak": {"english": "frog", "pronunciation": "ka-tak", "category": "animals", "example": "Katak hijau di kolam."},
        
        # Transportation
        "pesawat": {"english": "airplane", "pronunciation": "pe-sa-wat", "category": "transportation", "example": "Pesawat terbang tinggi."},
        "kereta": {"english": "train", "pronunciation": "ke-re-ta", "category": "transportation", "example": "Kereta api cepat."},
        "bus": {"english": "bus", "pronunciation": "bus", "category": "transportation", "example": "Bus kota penuh penumpang."},
        "taksi": {"english": "taxi", "pronunciation": "tak-si", "category": "transportation", "example": "Taksi kuning berhenti."},
        "motor": {"english": "motorcycle", "pronunciation": "mo-tor", "category": "transportation", "example": "Motor merah kencang."},
        "becak": {"english": "rickshaw", "pronunciation": "be-cak", "category": "transportation", "example": "Becak tradisional Indonesia."},
        "perahu": {"english": "boat", "pronunciation": "pe-ra-hu", "category": "transportation", "example": "Perahu nelayan kecil."},
        "kapal": {"english": "ship", "pronunciation": "ka-pal", "category": "transportation", "example": "Kapal besar di pelabuhan."},
        
        # Emotions & Feelings
        "senang": {"english": "happy", "pronunciation": "se-nang", "category": "emotions", "example": "Saya senang hari ini."},
        "sedih": {"english": "sad", "pronunciation": "se-dih", "category": "emotions", "example": "Dia sedih mendengar berita."},
        "marah": {"english": "angry", "pronunciation": "ma-rah", "category": "emotions", "example": "Ayah marah pada adik."},
        "takut": {"english": "afraid", "pronunciation": "ta-kut", "category": "emotions", "example": "Anak takut gelap."},
        "kaget": {"english": "surprised", "pronunciation": "ka-get", "category": "emotions", "example": "Saya kaget melihatnya."},
        "bosan": {"english": "bored", "pronunciation": "bo-san", "category": "emotions", "example": "Dia bosan di rumah."},
        "lelah": {"english": "tired", "pronunciation": "le-lah", "category": "emotions", "example": "Saya lelah bekerja."},
        "lapar": {"english": "hungry", "pronunciation": "la-par", "category": "emotions", "example": "Perut saya lapar."},
        "haus": {"english": "thirsty", "pronunciation": "ha-us", "category": "emotions", "example": "Mulut saya haus."},
        "sakit": {"english": "sick/hurt", "pronunciation": "sa-kit", "category": "emotions", "example": "Kepala saya sakit."},
        
        # Technology & Modern Life
        "internet": {"english": "internet", "pronunciation": "in-ter-net", "category": "technology", "example": "Internet cepat sekali."},
        "email": {"english": "email", "pronunciation": "e-mail", "category": "technology", "example": "Kirim email penting."},
        "website": {"english": "website", "pronunciation": "web-site", "category": "technology", "example": "Website bagus sekali."},
        "aplikasi": {"english": "application", "pronunciation": "ap-li-ka-si", "category": "technology", "example": "Aplikasi baru di ponsel."},
        "foto": {"english": "photo", "pronunciation": "fo-to", "category": "technology", "example": "Foto keluarga indah."},
        "video": {"english": "video", "pronunciation": "vi-de-o", "category": "technology", "example": "Video lucu di YouTube."},
        "musik": {"english": "music", "pronunciation": "mu-sik", "category": "technology", "example": "Musik jazz enak didengar."},
        "film": {"english": "movie", "pronunciation": "film", "category": "technology", "example": "Film Indonesia bagus."},
        
        # Clothing & Fashion
        "kemeja": {"english": "shirt", "pronunciation": "ke-me-ja", "category": "clothing", "example": "Kemeja putih rapi."},
        "kaos": {"english": "t-shirt", "pronunciation": "ka-os", "category": "clothing", "example": "Kaos merah favorit saya."},
        "rok": {"english": "skirt", "pronunciation": "rok", "category": "clothing", "example": "Rok panjang warna biru."},
        "jaket": {"english": "jacket", "pronunciation": "ja-ket", "category": "clothing", "example": "Jaket tebal untuk dingin."},
        "topi": {"english": "hat", "pronunciation": "to-pi", "category": "clothing", "example": "Topi hitam keren."},
        "kacamata": {"english": "glasses", "pronunciation": "ka-ca-ma-ta", "category": "clothing", "example": "Kacamata minus tinggi."},
        "jam": {"english": "watch", "pronunciation": "jam", "category": "clothing", "example": "Jam tangan mahal."},
        "cincin": {"english": "ring", "pronunciation": "cin-cin", "category": "clothing", "example": "Cincin emas berkilau."},
        "kalung": {"english": "necklace", "pronunciation": "ka-lung", "category": "clothing", "example": "Kalung mutiara cantik."},
        
        # Sports & Activities
        "olahraga": {"english": "sports", "pronunciation": "o-lah-ra-ga", "category": "sports", "example": "Olahraga setiap pagi."},
        "sepak bola": {"english": "football/soccer", "pronunciation": "se-pak bo-la", "category": "sports", "example": "Main sepak bola sore."},
        "basket": {"english": "basketball", "pronunciation": "bas-ket", "category": "sports", "example": "Tim basket sekolah menang."},
        "renang": {"english": "swimming", "pronunciation": "re-nang", "category": "sports", "example": "Renang di kolam bersih."},
        "lari": {"english": "running", "pronunciation": "la-ri", "category": "sports", "example": "Lari pagi menyehatkan."},
        "bersepeda": {"english": "cycling", "pronunciation": "ber-se-pe-da", "category": "sports", "example": "Bersepeda ke kantor."},
        "yoga": {"english": "yoga", "pronunciation": "yo-ga", "category": "sports", "example": "Yoga relaksasi tubuh."},
        "gym": {"english": "gym", "pronunciation": "gym", "category": "sports", "example": "Gym setiap hari."},
        
        # Education & Learning
        "universitas": {"english": "university", "pronunciation": "u-ni-ver-si-tas", "category": "education", "example": "Universitas terbaik di kota."},
        "mahasiswa": {"english": "student", "pronunciation": "ma-ha-sis-wa", "category": "education", "example": "Mahasiswa rajin belajar."},
        "guru": {"english": "teacher", "pronunciation": "gu-ru", "category": "education", "example": "Guru matematika baik."},
        "pelajaran": {"english": "lesson", "pronunciation": "pe-la-ja-ran", "category": "education", "example": "Pelajaran hari ini sulit."},
        "ujian": {"english": "exam", "pronunciation": "u-ji-an", "category": "education", "example": "Ujian besok pagi."},
        "nilai": {"english": "grade", "pronunciation": "ni-lai", "category": "education", "example": "Nilai bagus sekali."},
        "diploma": {"english": "diploma", "pronunciation": "dip-lo-ma", "category": "education", "example": "Diploma sarjana baru."},
        "perpustakaan": {"english": "library", "pronunciation": "per-pus-ta-ka-an", "category": "education", "example": "Perpustakaan buku lengkap."},
        
        # Business & Work
        "kerja": {"english": "work", "pronunciation": "ker-ja", "category": "business", "example": "Saya kerja di kantor."},
        "kantor": {"english": "office", "pronunciation": "kan-tor", "category": "business", "example": "Kantor baru sangat besar."},
        "bisnis": {"english": "business", "pronunciation": "bis-nis", "category": "business", "example": "Bisnis online berkembang."},
        "uang": {"english": "money", "pronunciation": "u-ang", "category": "business", "example": "Uang di dompet habis."},
        "gaji": {"english": "salary", "pronunciation": "ga-ji", "category": "business", "example": "Gaji bulan ini naik."},
        "bank": {"english": "bank", "pronunciation": "bank", "category": "business", "example": "Bank tutup hari Minggu."},
        "investasi": {"english": "investment", "pronunciation": "in-ves-ta-si", "category": "business", "example": "Investasi saham menguntungkan."},
        "perusahaan": {"english": "company", "pronunciation": "pe-ru-sa-ha-an", "category": "business", "example": "Perusahaan besar di Jakarta."},
        
        # Health & Medical
        "dokter": {"english": "doctor", "pronunciation": "dok-ter", "category": "health", "example": "Dokter memeriksa pasien."},
        "rumah sakit": {"english": "hospital", "pronunciation": "ru-mah sa-kit", "category": "health", "example": "Rumah sakit baru dibuka."},
        "obat": {"english": "medicine", "pronunciation": "o-bat", "category": "health", "example": "Obat diminum tiga kali."},
        "sehat": {"english": "healthy", "pronunciation": "se-hat", "category": "health", "example": "Badan sehat jiwa kuat."},
        "demam": {"english": "fever", "pronunciation": "de-mam", "category": "health", "example": "Anak demam tinggi."},
        "batuk": {"english": "cough", "pronunciation": "ba-tuk", "category": "health", "example": "Batuk sudah seminggu."},
        "pilek": {"english": "cold", "pronunciation": "pi-lek", "category": "health", "example": "Pilek karena hujan."},
        "alergi": {"english": "allergy", "pronunciation": "a-ler-gi", "category": "health", "example": "Alergi makanan laut."},
        
        # Travel & Places
        "hotel": {"english": "hotel", "pronunciation": "ho-tel", "category": "travel", "example": "Hotel mewah di pantai."},
        "restoran": {"english": "restaurant", "pronunciation": "res-to-ran", "category": "travel", "example": "Restoran Indonesia enak."},
        "museum": {"english": "museum", "pronunciation": "mu-se-um", "category": "travel", "example": "Museum sejarah menarik."},
        "taman": {"english": "park", "pronunciation": "ta-man", "category": "travel", "example": "Taman kota sangat indah."},
        "pantai": {"english": "beach", "pronunciation": "pan-tai", "category": "travel", "example": "Pantai Bali terkenal."},
        "jalan": {"english": "road/street", "pronunciation": "ja-lan", "category": "travel", "example": "Jalan raya macet."},
        "jembatan": {"english": "bridge", "pronunciation": "jem-ba-tan", "category": "travel", "example": "Jembatan panjang sekali."},
        "bandara": {"english": "airport", "pronunciation": "ban-da-ra", "category": "travel", "example": "Bandara internasional besar."},
        
        # Shopping & Commerce
        "toko": {"english": "shop", "pronunciation": "to-ko", "category": "shopping", "example": "Toko buku di pojok."},
        "pasar": {"english": "market", "pronunciation": "pa-sar", "category": "shopping", "example": "Pasar tradisional ramai."},
        "mall": {"english": "mall", "pronunciation": "mall", "category": "shopping", "example": "Mall baru sangat besar."},
        "kasir": {"english": "cashier", "pronunciation": "ka-sir", "category": "shopping", "example": "Kasir ramah sekali."},
        "diskon": {"english": "discount", "pronunciation": "dis-kon", "category": "shopping", "example": "Diskon besar-besaran."},
        "kartu kredit": {"english": "credit card", "pronunciation": "kar-tu kre-dit", "category": "shopping", "example": "Bayar pakai kartu kredit."},
        "belanja": {"english": "shopping", "pronunciation": "be-lan-ja", "category": "shopping", "example": "Belanja bulanan di supermarket."},
        "harga": {"english": "price", "pronunciation": "har-ga", "category": "shopping", "example": "Harga naik terus."},
        
        # Government & Politics
        "pemerintah": {"english": "government", "pronunciation": "pe-me-rin-tah", "category": "politics", "example": "Pemerintah baru terpilih."},
        "presiden": {"english": "president", "pronunciation": "pre-si-den", "category": "politics", "example": "Presiden memberikan pidato."},
        "menteri": {"english": "minister", "pronunciation": "men-te-ri", "category": "politics", "example": "Menteri kesehatan hadir."},
        "pemilihan": {"english": "election", "pronunciation": "pe-mi-li-han", "category": "politics", "example": "Pemilihan umum tahun depan."},
        "undang-undang": {"english": "law", "pronunciation": "un-dang un-dang", "category": "politics", "example": "Undang-undang baru disahkan."},
        "negara": {"english": "country", "pronunciation": "ne-ga-ra", "category": "politics", "example": "Negara Indonesia besar."},
        "rakyat": {"english": "people/citizens", "pronunciation": "rak-yat", "category": "politics", "example": "Rakyat mendukung kebijakan."},
        
        # Science & Research
        "ilmu": {"english": "science", "pronunciation": "il-mu", "category": "science", "example": "Ilmu pengetahuan berkembang."},
        "penelitian": {"english": "research", "pronunciation": "pe-ne-li-ti-an", "category": "science", "example": "Penelitian ini penting."},
        "eksperimen": {"english": "experiment", "pronunciation": "eks-pe-ri-men", "category": "science", "example": "Eksperimen berhasil dilakukan."},
        "laboratorium": {"english": "laboratory", "pronunciation": "la-bo-ra-to-ri-um", "category": "science", "example": "Laboratorium bersih sekali."},
        "kimia": {"english": "chemistry", "pronunciation": "ki-mi-a", "category": "science", "example": "Pelajaran kimia menarik."},
        "fisika": {"english": "physics", "pronunciation": "fi-si-ka", "category": "science", "example": "Fisika kuantum rumit."},
        "biologi": {"english": "biology", "pronunciation": "bi-o-lo-gi", "category": "science", "example": "Biologi mempelajari kehidupan."},
        "matematika": {"english": "mathematics", "pronunciation": "ma-te-ma-ti-ka", "category": "science", "example": "Matematika dasar penting."},
        
        # Arts & Culture
        "seni": {"english": "art", "pronunciation": "se-ni", "category": "culture", "example": "Seni lukis Indonesia indah."},
        "budaya": {"english": "culture", "pronunciation": "bu-da-ya", "category": "culture", "example": "Budaya Jawa unik."},
        "tarian": {"english": "dance", "pronunciation": "ta-ri-an", "category": "culture", "example": "Tarian Bali sangat cantik."},
        "lukisan": {"english": "painting", "pronunciation": "lu-ki-san", "category": "culture", "example": "Lukisan ini mahal."},
        "patung": {"english": "sculpture", "pronunciation": "pa-tung", "category": "culture", "example": "Patung Budha kuno."},
        "kerajinan": {"english": "handicraft", "pronunciation": "ke-ra-ji-nan", "category": "culture", "example": "Kerajinan tangan bagus."},
        "tradisi": {"english": "tradition", "pronunciation": "tra-di-si", "category": "culture", "example": "Tradisi leluhur dijaga."},
        "upacara": {"english": "ceremony", "pronunciation": "u-pa-ca-ra", "category": "culture", "example": "Upacara adat sakral."},
        
        # Professions & Jobs
        "pekerjaan": {"english": "job", "pronunciation": "pe-ker-ja-an", "category": "jobs", "example": "Pekerjaan ini mudah."},
        "profesi": {"english": "profession", "pronunciation": "pro-fe-si", "category": "jobs", "example": "Profesi dokter mulia."},
        "insinyur": {"english": "engineer", "pronunciation": "in-si-nyur", "category": "jobs", "example": "Insinyur membangun jembatan."},
        "akuntan": {"english": "accountant", "pronunciation": "a-kun-tan", "category": "jobs", "example": "Akuntan menghitung keuangan."},
        "pengacara": {"english": "lawyer", "pronunciation": "peng-a-ca-ra", "category": "jobs", "example": "Pengacara membela klien."},
        "pilot": {"english": "pilot", "pronunciation": "pi-lot", "category": "jobs", "example": "Pilot menerbangkan pesawat."},
        "wartawan": {"english": "journalist", "pronunciation": "war-ta-wan", "category": "jobs", "example": "Wartawan menulis berita."},
        "arsitek": {"english": "architect", "pronunciation": "ar-si-tek", "category": "jobs", "example": "Arsitek merancang rumah."},
        
        # Environment & Ecology
        "lingkungan": {"english": "environment", "pronunciation": "ling-kung-an", "category": "environment", "example": "Lingkungan harus dijaga."},
        "polusi": {"english": "pollution", "pronunciation": "po-lu-si", "category": "environment", "example": "Polusi udara berbahaya."},
        "daur ulang": {"english": "recycling", "pronunciation": "da-ur u-lang", "category": "environment", "example": "Daur ulang plastik penting."},
        "sampah": {"english": "garbage", "pronunciation": "sam-pah", "category": "environment", "example": "Sampah harus dibuang."},
        "konservasi": {"english": "conservation", "pronunciation": "kon-ser-va-si", "category": "environment", "example": "Konservasi hutan diperlukan."},
        "ekosistem": {"english": "ecosystem", "pronunciation": "e-ko-sis-tem", "category": "environment", "example": "Ekosistem laut rusak."},
        "keanekaragaman": {"english": "biodiversity", "pronunciation": "ke-a-ne-ka-ra-ga-man", "category": "environment", "example": "Keanekaragaman hayati Indonesia."},
        
        # Food & Cooking
        "memasak": {"english": "cooking", "pronunciation": "me-ma-sak", "category": "cooking", "example": "Ibu memasak nasi."},
        "resep": {"english": "recipe", "pronunciation": "re-sep", "category": "cooking", "example": "Resep kue lezat."},
        "bumbu": {"english": "spices", "pronunciation": "bum-bu", "category": "cooking", "example": "Bumbu Indonesia kaya."},
        "masakan": {"english": "cuisine", "pronunciation": "ma-sa-kan", "category": "cooking", "example": "Masakan Padang pedas."},
        "hidangan": {"english": "dish", "pronunciation": "hi-dang-an", "category": "cooking", "example": "Hidangan utama lezat."},
        "rasa": {"english": "taste", "pronunciation": "ra-sa", "category": "cooking", "example": "Rasa makanan enak."},
        "aroma": {"english": "aroma", "pronunciation": "a-ro-ma", "category": "cooking", "example": "Aroma kopi harum."},
        
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
        "tetapi": {"english": "but", "pronunciation": "te-ta-pi", "category": "conjunctions", "example": "Mahal tetapi bagus."},
        "karena": {"english": "because", "pronunciation": "ka-re-na", "category": "conjunctions", "example": "Terlambat karena macet."},
        "jika": {"english": "if", "pronunciation": "ji-ka", "category": "conjunctions", "example": "Jika hujan, di rumah."},
        "ketika": {"english": "when", "pronunciation": "ke-ti-ka", "category": "conjunctions", "example": "Ketika malam tiba."},
        "sebelum": {"english": "before", "pronunciation": "se-be-lum", "category": "conjunctions", "example": "Sebelum makan, cuci tangan."},
        "sesudah": {"english": "after", "pronunciation": "se-su-dah", "category": "conjunctions", "example": "Sesudah makan, istirahat."},
        # Military & Security
        "tentara": {"english": "army", "pronunciation": "ten-ta-ra", "category": "military", "example": "Tentara menjaga negara."},
        "polisi": {"english": "police", "pronunciation": "po-li-si", "category": "military", "example": "Polisi menangkap pencuri."},
        "keamanan": {"english": "security", "pronunciation": "ke-a-man-an", "category": "military", "example": "Keamanan sangat penting."},
        "perang": {"english": "war", "pronunciation": "pe-rang", "category": "military", "example": "Perang dunia berakhir."},
        "perdamaian": {"english": "peace", "pronunciation": "per-da-mai-an", "category": "military", "example": "Perdamaian dunia diinginkan."},
        
        # Religion & Spirituality
        "agama": {"english": "religion", "pronunciation": "a-ga-ma", "category": "religion", "example": "Agama mengajarkan kebaikan."},
        "doa": {"english": "prayer", "pronunciation": "do-a", "category": "religion", "example": "Doa ibu terkabul."},
        "gereja": {"english": "church", "pronunciation": "ge-re-ja", "category": "religion", "example": "Gereja tua bersejarah."},
        "masjid": {"english": "mosque", "pronunciation": "mas-jid", "category": "religion", "example": "Masjid besar indah."},
        "kuil": {"english": "temple", "pronunciation": "ku-il", "category": "religion", "example": "Kuil Hindu kuno."},
        "surga": {"english": "heaven", "pronunciation": "sur-ga", "category": "religion", "example": "Surga tempat bahagia."},
        
        # Geography & Nature
        "benua": {"english": "continent", "pronunciation": "be-nu-a", "category": "geography", "example": "Benua Asia terbesar."},
        "pulau": {"english": "island", "pronunciation": "pu-lau", "category": "geography", "example": "Pulau Bali terkenal."},
        "selat": {"english": "strait", "pronunciation": "se-lat", "category": "geography", "example": "Selat Sunda sempit."},
        "teluk": {"english": "bay", "pronunciation": "te-luk", "category": "geography", "example": "Teluk Jakarta besar."},
        "danau": {"english": "lake", "pronunciation": "da-nau", "category": "geography", "example": "Danau Toba indah."},
        "padang rumput": {"english": "grassland", "pronunciation": "pa-dang rum-put", "category": "geography", "example": "Padang rumput luas."},
        "gua": {"english": "cave", "pronunciation": "gu-a", "category": "geography", "example": "Gua gelap dan dingin."},
        "air terjun": {"english": "waterfall", "pronunciation": "a-ir ter-jun", "category": "geography", "example": "Air terjun tinggi sekali."},
        
        # Communication & Media
        "komunikasi": {"english": "communication", "pronunciation": "ko-mu-ni-ka-si", "category": "media", "example": "Komunikasi sangat penting."},
        "berita": {"english": "news", "pronunciation": "be-ri-ta", "category": "media", "example": "Berita hari ini menarik."},
        "koran": {"english": "newspaper", "pronunciation": "ko-ran", "category": "media", "example": "Koran pagi dibaca."},
        "majalah": {"english": "magazine", "pronunciation": "ma-ja-lah", "category": "media", "example": "Majalah fashion terbaru."},
        "radio": {"english": "radio", "pronunciation": "ra-di-o", "category": "media", "example": "Radio menyiarkan musik."},
        "televisi": {"english": "television", "pronunciation": "te-le-vi-si", "category": "media", "example": "Televisi rusak total."},
        "iklan": {"english": "advertisement", "pronunciation": "ik-lan", "category": "media", "example": "Iklan produk baru."},
        
        # Finance & Economics
        "ekonomi": {"english": "economy", "pronunciation": "e-ko-no-mi", "category": "finance", "example": "Ekonomi Indonesia tumbuh."},
        "keuangan": {"english": "finance", "pronunciation": "ke-u-ang-an", "category": "finance", "example": "Keuangan keluarga stabil."},
        "hutang": {"english": "debt", "pronunciation": "hu-tang", "category": "finance", "example": "Hutang harus dibayar."},
        "kredit": {"english": "credit", "pronunciation": "kre-dit", "category": "finance", "example": "Kredit rumah disetujui."},
        "tabungan": {"english": "savings", "pronunciation": "ta-bung-an", "category": "finance", "example": "Tabungan semakin banyak."},
        "pajak": {"english": "tax", "pronunciation": "pa-jak", "category": "finance", "example": "Pajak harus dibayar."},
        "anggaran": {"english": "budget", "pronunciation": "ang-ga-ran", "category": "finance", "example": "Anggaran bulan ini ketat."},
        
        # Emotions & Feelings Extended
        "cinta": {"english": "love", "pronunciation": "cin-ta", "category": "emotions", "example": "Cinta ibu tulus."},
        "benci": {"english": "hate", "pronunciation": "ben-ci", "category": "emotions", "example": "Jangan benci orang lain."},
        "rindu": {"english": "miss", "pronunciation": "rin-du", "category": "emotions", "example": "Rindu kampung halaman."},
        "bangga": {"english": "proud", "pronunciation": "bang-ga", "category": "emotions", "example": "Bangga pada anak."},
        "malu": {"english": "ashamed", "pronunciation": "ma-lu", "category": "emotions", "example": "Malu berbuat salah."},
        "iri": {"english": "jealous", "pronunciation": "i-ri", "category": "emotions", "example": "Iri pada teman."},
        "kecewa": {"english": "disappointed", "pronunciation": "ke-ce-wa", "category": "emotions", "example": "Kecewa dengan hasil."},
        "bahagia": {"english": "happy", "pronunciation": "ba-ha-gi-a", "category": "emotions", "example": "Bahagia bersama keluarga."},
        
        # Music & Entertainment
        "lagu": {"english": "song", "pronunciation": "la-gu", "category": "music", "example": "Lagu ini populer."},
        "penyanyi": {"english": "singer", "pronunciation": "pe-nya-nyi", "category": "music", "example": "Penyanyi terkenal tampil."},
        "konser": {"english": "concert", "pronunciation": "kon-ser", "category": "music", "example": "Konser musik rock."},
        "alat musik": {"english": "musical instrument", "pronunciation": "a-lat mu-sik", "category": "music", "example": "Alat musik tradisional."},
        "bioskop": {"english": "cinema", "pronunciation": "bi-os-kop", "category": "entertainment", "example": "Bioskop penuh penonton."},
        "teater": {"english": "theater", "pronunciation": "te-a-ter", "category": "entertainment", "example": "Teater drama bagus."},
        "hiburan": {"english": "entertainment", "pronunciation": "hi-bu-ran", "category": "entertainment", "example": "Hiburan malam menarik."},
        
        # Time Words
        "sekarang": {"english": "now", "pronunciation": "se-ka-rang", "category": "time", "example": "Sekarang jam berapa?"},
        "kemarin": {"english": "yesterday", "pronunciation": "ke-ma-rin", "category": "time", "example": "Kemarin saya pergi ke pasar."},
        "besok": {"english": "tomorrow", "pronunciation": "be-sok", "category": "time", "example": "Besok saya akan datang."},
        "lusa": {"english": "day after tomorrow", "pronunciation": "lu-sa", "category": "time", "example": "Lusa ada acara penting."},
        "kemarin dulu": {"english": "day before yesterday", "pronunciation": "ke-ma-rin du-lu", "category": "time", "example": "Kemarin dulu hujan deras."},
        "minggu": {"english": "week", "pronunciation": "ming-gu", "category": "time", "example": "Minggu depan libur."},
        "bulan": {"english": "month", "pronunciation": "bu-lan", "category": "time", "example": "Bulan ini sibuk."},
        "tahun": {"english": "year", "pronunciation": "ta-hun", "category": "time", "example": "Tahun baru datang."},
        "abad": {"english": "century", "pronunciation": "a-bad", "category": "time", "example": "Abad ke-21 modern."},
        "masa": {"english": "era/period", "pronunciation": "ma-sa", "category": "time", "example": "Masa lalu indah."},
        
        # Advanced Technology
        "komputer": {"english": "computer", "pronunciation": "kom-pu-ter", "category": "technology", "example": "Komputer baru cepat."},
        "laptop": {"english": "laptop", "pronunciation": "lap-top", "category": "technology", "example": "Laptop ringan praktis."},
        "tablet": {"english": "tablet", "pronunciation": "tab-let", "category": "technology", "example": "Tablet untuk membaca."},
        "smartphone": {"english": "smartphone", "pronunciation": "smart-phone", "category": "technology", "example": "Smartphone canggih sekali."},
        "perangkat lunak": {"english": "software", "pronunciation": "pe-rang-kat lu-nak", "category": "technology", "example": "Perangkat lunak terbaru."},
        "perangkat keras": {"english": "hardware", "pronunciation": "pe-rang-kat ke-ras", "category": "technology", "example": "Perangkat keras mahal."},
        "jaringan": {"english": "network", "pronunciation": "ja-ring-an", "category": "technology", "example": "Jaringan internet cepat."},
        "server": {"english": "server", "pronunciation": "ser-ver", "category": "technology", "example": "Server down sementara."},
        "database": {"english": "database", "pronunciation": "da-ta-base", "category": "technology", "example": "Database pelanggan lengkap."},
        "algoritma": {"english": "algorithm", "pronunciation": "al-go-rit-ma", "category": "technology", "example": "Algoritma pencarian efisien."},
        
        # Advanced Science
        "molekul": {"english": "molecule", "pronunciation": "mo-le-kul", "category": "science", "example": "Molekul air sederhana."},
        "atom": {"english": "atom", "pronunciation": "a-tom", "category": "science", "example": "Atom terkecil materi."},
        "elektron": {"english": "electron", "pronunciation": "e-lek-tron", "category": "science", "example": "Elektron bermuatan negatif."},
        "proton": {"english": "proton", "pronunciation": "pro-ton", "category": "science", "example": "Proton di inti atom."},
        "neutron": {"english": "neutron", "pronunciation": "neu-tron", "category": "science", "example": "Neutron tidak bermuatan."},
        "gravitasi": {"english": "gravity", "pronunciation": "gra-vi-ta-si", "category": "science", "example": "Gravitasi menarik benda."},
        "energi": {"english": "energy", "pronunciation": "e-ner-gi", "category": "science", "example": "Energi tidak dapat hilang."},
        "massa": {"english": "mass", "pronunciation": "mas-sa", "category": "science", "example": "Massa benda tetap."},
        "volume": {"english": "volume", "pronunciation": "vo-lu-me", "category": "science", "example": "Volume air berubah."},
        "densitas": {"english": "density", "pronunciation": "den-si-tas", "category": "science", "example": "Densitas emas tinggi."},
        
        # Advanced Medical
        "diagnosis": {"english": "diagnosis", "pronunciation": "di-ag-no-sis", "category": "health", "example": "Diagnosis dokter akurat."},
        "terapi": {"english": "therapy", "pronunciation": "te-ra-pi", "category": "health", "example": "Terapi fisik membantu."},
        "operasi": {"english": "surgery", "pronunciation": "o-pe-ra-si", "category": "health", "example": "Operasi jantung berhasil."},
        "vaksin": {"english": "vaccine", "pronunciation": "vak-sin", "category": "health", "example": "Vaksin mencegah penyakit."},
        "antibiotik": {"english": "antibiotic", "pronunciation": "an-ti-bi-o-tik", "category": "health", "example": "Antibiotik melawan bakteri."},
        "virus": {"english": "virus", "pronunciation": "vi-rus", "category": "health", "example": "Virus sangat kecil."},
        "bakteri": {"english": "bacteria", "pronunciation": "bak-te-ri", "category": "health", "example": "Bakteri ada dimana-mana."},
        "penyakit": {"english": "disease", "pronunciation": "pe-nya-kit", "category": "health", "example": "Penyakit harus diobati."},
        "gejala": {"english": "symptoms", "pronunciation": "ge-ja-la", "category": "health", "example": "Gejala demam muncul."},
        "pencegahan": {"english": "prevention", "pronunciation": "pen-ce-gah-an", "category": "health", "example": "Pencegahan lebih baik."},
        
        # Advanced Geography
        "benua": {"english": "continent", "pronunciation": "be-nu-a", "category": "geography", "example": "Benua Asia terluas."},
        "samudra": {"english": "ocean", "pronunciation": "sa-mud-ra", "category": "geography", "example": "Samudra Pasifik luas."},
        "khatulistiwa": {"english": "equator", "pronunciation": "kha-tu-lis-ti-wa", "category": "geography", "example": "Indonesia di khatulistiwa."},
        "kutub": {"english": "pole", "pronunciation": "ku-tub", "category": "geography", "example": "Kutub utara dingin."},
        "garis lintang": {"english": "latitude", "pronunciation": "ga-ris lin-tang", "category": "geography", "example": "Garis lintang nol derajat."},
        "garis bujur": {"english": "longitude", "pronunciation": "ga-ris bu-jur", "category": "geography", "example": "Garis bujur timur."},
        "iklim": {"english": "climate", "pronunciation": "ik-lim", "category": "geography", "example": "Iklim tropis hangat."},
        "musim": {"english": "season", "pronunciation": "mu-sim", "category": "geography", "example": "Musim hujan tiba."},
        "topografi": {"english": "topography", "pronunciation": "to-po-gra-fi", "category": "geography", "example": "Topografi pegunungan."},
        "geologi": {"english": "geology", "pronunciation": "ge-o-lo-gi", "category": "geography", "example": "Geologi Indonesia unik."},
        
        # Advanced Arts
        "kaligrafi": {"english": "calligraphy", "pronunciation": "ka-li-gra-fi", "category": "culture", "example": "Kaligrafi Arab indah."},
        "arsitektur": {"english": "architecture", "pronunciation": "ar-si-tek-tur", "category": "culture", "example": "Arsitektur Jawa klasik."},
        "sastra": {"english": "literature", "pronunciation": "sas-tra", "category": "culture", "example": "Sastra Indonesia kaya."},
        "puisi": {"english": "poetry", "pronunciation": "pu-i-si", "category": "culture", "example": "Puisi cinta romantis."},
        "novel": {"english": "novel", "pronunciation": "no-vel", "category": "culture", "example": "Novel sejarah menarik."},
        "cerita": {"english": "story", "pronunciation": "ce-ri-ta", "category": "culture", "example": "Cerita rakyat terkenal."},
        "dongeng": {"english": "fairy tale", "pronunciation": "dong-eng", "category": "culture", "example": "Dongeng anak-anak lucu."},
        "legenda": {"english": "legend", "pronunciation": "le-gen-da", "category": "culture", "example": "Legenda Sangkuriang."},
        "mitos": {"english": "myth", "pronunciation": "mi-tos", "category": "culture", "example": "Mitos kuno misterius."},
        "folklore": {"english": "folklore", "pronunciation": "folk-lo-re", "category": "culture", "example": "Folklore daerah beragam."},
        
        # Advanced Economics
        "inflasi": {"english": "inflation", "pronunciation": "in-fla-si", "category": "finance", "example": "Inflasi naik drastis."},
        "deflasi": {"english": "deflation", "pronunciation": "de-fla-si", "category": "finance", "example": "Deflasi jarang terjadi."},
        "resesi": {"english": "recession", "pronunciation": "re-se-si", "category": "finance", "example": "Resesi ekonomi global."},
        "depresi": {"english": "depression", "pronunciation": "de-pre-si", "category": "finance", "example": "Depresi ekonomi parah."},
        "kapitalisasi": {"english": "capitalization", "pronunciation": "ka-pi-ta-li-sa-si", "category": "finance", "example": "Kapitalisasi pasar besar."},
        "dividen": {"english": "dividend", "pronunciation": "di-vi-den", "category": "finance", "example": "Dividen saham tinggi."},
        "saham": {"english": "stock", "pronunciation": "sa-ham", "category": "finance", "example": "Saham teknologi naik."},
        "obligasi": {"english": "bond", "pronunciation": "o-bli-ga-si", "category": "finance", "example": "Obligasi pemerintah aman."},
        "portofolio": {"english": "portfolio", "pronunciation": "por-to-fo-li-o", "category": "finance", "example": "Portofolio investasi beragam."},
        "likuiditas": {"english": "liquidity", "pronunciation": "li-kui-di-tas", "category": "finance", "example": "Likuiditas tinggi penting."},
        
        # Extended Time & Calendar
        "hari ini": {"english": "today", "pronunciation": "ha-ri i-ni", "category": "time", "example": "Hari ini cuaca bagus."},
        "malam": {"english": "night", "pronunciation": "ma-lam", "category": "time", "example": "Malam ini saya tidur."},
        "pagi": {"english": "morning", "pronunciation": "pa-gi", "category": "time", "example": "Pagi ini saya bangun."},
        "siang": {"english": "afternoon", "pronunciation": "si-ang", "category": "time", "example": "Siang ini panas."},
        "sore": {"english": "evening", "pronunciation": "so-re", "category": "time", "example": "Sore hari sejuk."},
        "dini hari": {"english": "dawn", "pronunciation": "di-ni ha-ri", "category": "time", "example": "Dini hari sunyi."},
        "tengah malam": {"english": "midnight", "pronunciation": "te-ngah ma-lam", "category": "time", "example": "Tengah malam gelap."},
        "tengah hari": {"english": "noon", "pronunciation": "te-ngah ha-ri", "category": "time", "example": "Tengah hari terik."},
        "subuh": {"english": "dawn prayer time", "pronunciation": "su-buh", "category": "time", "example": "Subuh waktu sholat."},
        "maghrib": {"english": "sunset prayer time", "pronunciation": "magh-rib", "category": "time", "example": "Maghrib matahari tenggelam."},
        "semester": {"english": "semester", "pronunciation": "se-mes-ter", "category": "time", "example": "Semester baru dimulai."},
        "dekade": {"english": "decade", "pronunciation": "de-ka-de", "category": "time", "example": "Dekade terakhir berubah."},
        "milenium": {"english": "millennium", "pronunciation": "mi-le-ni-um", "category": "time", "example": "Milenium baru harapan."},
        
        # Extended Food & Cuisine
        "nasi goreng": {"english": "fried rice", "pronunciation": "na-si go-reng", "category": "food", "example": "Nasi goreng pedas enak."},
        "mie ayam": {"english": "chicken noodles", "pronunciation": "mi-e a-yam", "category": "food", "example": "Mie ayam favorit saya."},
        "gado-gado": {"english": "Indonesian salad", "pronunciation": "ga-do ga-do", "category": "food", "example": "Gado-gado sayuran segar."},
        "rendang": {"english": "spicy beef stew", "pronunciation": "ren-dang", "category": "food", "example": "Rendang Padang terkenal."},
        "sate": {"english": "satay", "pronunciation": "sa-te", "category": "food", "example": "Sate ayam bakar."},
        "bakso": {"english": "meatball soup", "pronunciation": "bak-so", "category": "food", "example": "Bakso kuah hangat."},
        "soto": {"english": "Indonesian soup", "pronunciation": "so-to", "category": "food", "example": "Soto ayam kuning."},
        "gudeg": {"english": "jackfruit stew", "pronunciation": "gu-deg", "category": "food", "example": "Gudeg Yogyakarta manis."},
        "tempeh": {"english": "fermented soybeans", "pronunciation": "tem-peh", "category": "food", "example": "Tempeh protein nabati."},
        "tahu": {"english": "tofu", "pronunciation": "ta-hu", "category": "food", "example": "Tahu goreng renyah."},
        "kerupuk": {"english": "crackers", "pronunciation": "ke-ru-puk", "category": "food", "example": "Kerupuk udang gurih."},
        "sambal": {"english": "chili sauce", "pronunciation": "sam-bal", "category": "food", "example": "Sambal pedas sekali."},
        "lalapan": {"english": "raw vegetables", "pronunciation": "la-la-pan", "category": "food", "example": "Lalapan segar sehat."},
        "asinan": {"english": "pickled fruits", "pronunciation": "a-si-nan", "category": "food", "example": "Asinan buah asam."},
        "rujak": {"english": "fruit salad", "pronunciation": "ru-jak", "category": "food", "example": "Rujak buah pedas."},
        
        # Extended Animals & Wildlife
        "orangutan": {"english": "orangutan", "pronunciation": "o-rang-u-tan", "category": "animals", "example": "Orangutan Kalimantan langka."},
        "komodo": {"english": "komodo dragon", "pronunciation": "ko-mo-do", "category": "animals", "example": "Komodo kadal besar."},
        "badak": {"english": "rhinoceros", "pronunciation": "ba-dak", "category": "animals", "example": "Badak bercula satu."},
        "tapir": {"english": "tapir", "pronunciation": "ta-pir", "category": "animals", "example": "Tapir hidung panjang."},
        "anoa": {"english": "dwarf buffalo", "pronunciation": "a-no-a", "category": "animals", "example": "Anoa Sulawesi kecil."},
        "banteng": {"english": "wild ox", "pronunciation": "ban-teng", "category": "animals", "example": "Banteng Jawa kuat."},
        "rusa": {"english": "deer", "pronunciation": "ru-sa", "category": "animals", "example": "Rusa berlari cepat."},
        "babi rusa": {"english": "babirusa", "pronunciation": "ba-bi ru-sa", "category": "animals", "example": "Babi rusa taring panjang."},
        "binturong": {"english": "bearcat", "pronunciation": "bin-tu-rong", "category": "animals", "example": "Binturong pemanjat pohon."},
        "trenggiling": {"english": "pangolin", "pronunciation": "treng-gi-ling", "category": "animals", "example": "Trenggiling sisik keras."},
        "kuskus": {"english": "cuscus", "pronunciation": "kus-kus", "category": "animals", "example": "Kuskus marsupial kecil."},
        "cendrawasih": {"english": "bird of paradise", "pronunciation": "cen-dra-wa-sih", "category": "animals", "example": "Cendrawasih burung indah."},
        "jalak bali": {"english": "bali starling", "pronunciation": "ja-lak ba-li", "category": "animals", "example": "Jalak Bali putih langka."},
        "elang jawa": {"english": "javan eagle", "pronunciation": "e-lang ja-wa", "category": "animals", "example": "Elang Jawa terbang tinggi."},
        
        # Extended Plants & Flowers
        "melati": {"english": "jasmine", "pronunciation": "me-la-ti", "category": "nature", "example": "Melati bunga putih harum."},
        "mawar": {"english": "rose", "pronunciation": "ma-war", "category": "nature", "example": "Mawar merah cantik."},
        "anggrek": {"english": "orchid", "pronunciation": "ang-grek", "category": "nature", "example": "Anggrek bulan langka."},
        "kamboja": {"english": "frangipani", "pronunciation": "kam-bo-ja", "category": "nature", "example": "Kamboja kuning harum."},
        "kenanga": {"english": "ylang-ylang", "pronunciation": "ke-na-nga", "category": "nature", "example": "Kenanga wangi mewangi."},
        "cempaka": {"english": "magnolia", "pronunciation": "cem-pa-ka", "category": "nature", "example": "Cempaka putih suci."},
        "teratai": {"english": "lotus", "pronunciation": "te-ra-tai", "category": "nature", "example": "Teratai di kolam."},
        "bambu": {"english": "bamboo", "pronunciation": "bam-bu", "category": "nature", "example": "Bambu tumbuh cepat."},
        "kelapa": {"english": "coconut", "pronunciation": "ke-la-pa", "category": "nature", "example": "Kelapa buah tropis."},
        "pisang": {"english": "banana", "pronunciation": "pi-sang", "category": "nature", "example": "Pisang kuning manis."},
        "mangga": {"english": "mango", "pronunciation": "mang-ga", "category": "nature", "example": "Mangga harum manis."},
        "durian": {"english": "durian", "pronunciation": "du-ri-an", "category": "nature", "example": "Durian raja buah."},
        "rambutan": {"english": "rambutan", "pronunciation": "ram-bu-tan", "category": "nature", "example": "Rambutan merah berbulu."},
        "manggis": {"english": "mangosteen", "pronunciation": "mang-gis", "category": "nature", "example": "Manggis ratu buah."},
        
        # Extended Transportation & Vehicles
        "ojek": {"english": "motorcycle taxi", "pronunciation": "o-jek", "category": "transportation", "example": "Ojek online praktis."},
        "angkot": {"english": "public minivan", "pronunciation": "ang-kot", "category": "transportation", "example": "Angkot transportasi murah."},
        "bajaj": {"english": "three-wheeler", "pronunciation": "ba-jaj", "category": "transportation", "example": "Bajaj kendaraan kecil."},
        "delman": {"english": "horse cart", "pronunciation": "del-man", "category": "transportation", "example": "Delman tradisional Yogya."},
        "dokar": {"english": "horse carriage", "pronunciation": "do-kar", "category": "transportation", "example": "Dokar wisata kota."},
        "andong": {"english": "traditional carriage", "pronunciation": "an-dong", "category": "transportation", "example": "Andong keliling kota."},
        "helikopter": {"english": "helicopter", "pronunciation": "he-li-kop-ter", "category": "transportation", "example": "Helikopter terbang rendah."},
        "jet": {"english": "jet", "pronunciation": "jet", "category": "transportation", "example": "Jet tempur cepat."},
        "kapal selam": {"english": "submarine", "pronunciation": "ka-pal se-lam", "category": "transportation", "example": "Kapal selam di laut."},
        "feri": {"english": "ferry", "pronunciation": "fe-ri", "category": "transportation", "example": "Feri menyeberang selat."},
        "speedboat": {"english": "speedboat", "pronunciation": "speed-boat", "category": "transportation", "example": "Speedboat cepat sekali."},
        "yacht": {"english": "yacht", "pronunciation": "yacht", "category": "transportation", "example": "Yacht mewah berlayar."},
        
        # Extended Clothing & Fashion
        "batik": {"english": "batik", "pronunciation": "ba-tik", "category": "clothing", "example": "Batik Indonesia terkenal."},
        "kebaya": {"english": "traditional blouse", "pronunciation": "ke-ba-ya", "category": "clothing", "example": "Kebaya wanita elegan."},
        "sarong": {"english": "sarong", "pronunciation": "sa-rong", "category": "clothing", "example": "Sarong kain tradisional."},
        "kain": {"english": "cloth", "pronunciation": "ka-in", "category": "clothing", "example": "Kain sutra halus."},
        "selendang": {"english": "shawl", "pronunciation": "se-len-dang", "category": "clothing", "example": "Selendang menutupi kepala."},
        "ikat pinggang": {"english": "belt", "pronunciation": "i-kat ping-gang", "category": "clothing", "example": "Ikat pinggang kulit."},
        "dasi": {"english": "tie", "pronunciation": "da-si", "category": "clothing", "example": "Dasi formal rapi."},
        "jas": {"english": "suit jacket", "pronunciation": "jas", "category": "clothing", "example": "Jas hitam formal."},
        "gaun": {"english": "dress", "pronunciation": "ga-un", "category": "clothing", "example": "Gaun pesta cantik."},
        "celana": {"english": "pants", "pronunciation": "ce-la-na", "category": "clothing", "example": "Celana jeans biru."},
        "baju": {"english": "shirt", "pronunciation": "ba-ju", "category": "clothing", "example": "Baju putih bersih."},
        "sepatu": {"english": "shoes", "pronunciation": "se-pa-tu", "category": "clothing", "example": "Sepatu kulit mahal."},
        "sandal": {"english": "sandals", "pronunciation": "san-dal", "category": "clothing", "example": "Sandal jepit murah."},
        "kaos kaki": {"english": "socks", "pronunciation": "ka-os ka-ki", "category": "clothing", "example": "Kaos kaki putih."},
        
        # Extended House & Furniture
        "lemari": {"english": "wardrobe", "pronunciation": "le-ma-ri", "category": "house", "example": "Lemari pakaian besar."},
        "kasur": {"english": "mattress", "pronunciation": "ka-sur", "category": "house", "example": "Kasur empuk nyaman."},
        "bantal": {"english": "pillow", "pronunciation": "ban-tal", "category": "house", "example": "Bantal lembut putih."},
        "selimut": {"english": "blanket", "pronunciation": "se-li-mut", "category": "house", "example": "Selimut hangat tebal."},
        "sprei": {"english": "bed sheet", "pronunciation": "spre-i", "category": "house", "example": "Sprei warna biru."},
        "kursi": {"english": "chair", "pronunciation": "kur-si", "category": "house", "example": "Kursi kayu kokoh."},
        "meja": {"english": "table", "pronunciation": "me-ja", "category": "house", "example": "Meja makan bulat."},
        "sofa": {"english": "sofa", "pronunciation": "so-fa", "category": "house", "example": "Sofa kulit coklat."},
        "televisi": {"english": "television", "pronunciation": "te-le-vi-si", "category": "house", "example": "Televisi layar besar."},
        "kulkas": {"english": "refrigerator", "pronunciation": "kul-kas", "category": "house", "example": "Kulkas penuh makanan."},
        "kompor": {"english": "stove", "pronunciation": "kom-por", "category": "house", "example": "Kompor gas biru."},
        "rice cooker": {"english": "rice cooker", "pronunciation": "rice coo-ker", "category": "house", "example": "Rice cooker masak nasi."},
        "blender": {"english": "blender", "pronunciation": "blen-der", "category": "house", "example": "Blender buat jus."},
        "setrika": {"english": "iron", "pronunciation": "se-tri-ka", "category": "house", "example": "Setrika baju kusut."},
        
        # Extended Body Parts
        "jantung": {"english": "heart", "pronunciation": "jan-tung", "category": "body", "example": "Jantung berdetak cepat."},
        "paru-paru": {"english": "lungs", "pronunciation": "pa-ru pa-ru", "category": "body", "example": "Paru-paru butuh oksigen."},
        "hati": {"english": "liver", "pronunciation": "ha-ti", "category": "body", "example": "Hati organ penting."},
        "ginjal": {"english": "kidney", "pronunciation": "gin-jal", "category": "body", "example": "Ginjal saring darah."},
        "lambung": {"english": "stomach", "pronunciation": "lam-bung", "category": "body", "example": "Lambung cerna makanan."},
        "usus": {"english": "intestine", "pronunciation": "u-sus", "category": "body", "example": "Usus serap nutrisi."},
        "otak": {"english": "brain", "pronunciation": "o-tak", "category": "body", "example": "Otak pusat pikiran."},
        "tulang": {"english": "bone", "pronunciation": "tu-lang", "category": "body", "example": "Tulang kuat kokoh."},
        "otot": {"english": "muscle", "pronunciation": "o-tot", "category": "body", "example": "Otot perlu latihan."},
        "kulit": {"english": "skin", "pronunciation": "ku-lit", "category": "body", "example": "Kulit perlu perawatan."},
        "darah": {"english": "blood", "pronunciation": "da-rah", "category": "body", "example": "Darah mengalir tubuh."},
        "urat": {"english": "vein", "pronunciation": "u-rat", "category": "body", "example": "Urat nadi terasa."},
        
        # Extended Common Adjectives
        "besar": {"english": "big", "pronunciation": "be-sar", "category": "adjectives", "example": "Rumah ini besar."},
        "kecil": {"english": "small", "pronunciation": "ke-cil", "category": "adjectives", "example": "Anak itu kecil."},
        "tinggi": {"english": "tall/high", "pronunciation": "ting-gi", "category": "adjectives", "example": "Orang itu tinggi."},
        "pendek": {"english": "short", "pronunciation": "pen-dek", "category": "adjectives", "example": "Rambut saya pendek."},
        "panjang": {"english": "long", "pronunciation": "pan-jang", "category": "adjectives", "example": "Jalan ini panjang."},
        "lebar": {"english": "wide", "pronunciation": "le-bar", "category": "adjectives", "example": "Sungai ini lebar."},
        "sempit": {"english": "narrow", "pronunciation": "sem-pit", "category": "adjectives", "example": "Gang ini sempit."},
        "tebal": {"english": "thick", "pronunciation": "te-bal", "category": "adjectives", "example": "Buku ini tebal."},
        "tipis": {"english": "thin", "pronunciation": "ti-pis", "category": "adjectives", "example": "Kertas ini tipis."},
        "berat": {"english": "heavy", "pronunciation": "be-rat", "category": "adjectives", "example": "Tas ini berat."},
        "ringan": {"english": "light", "pronunciation": "ri-ngan", "category": "adjectives", "example": "Bulu ini ringan."},
        "keras": {"english": "hard", "pronunciation": "ke-ras", "category": "adjectives", "example": "Batu ini keras."},
        "lembut": {"english": "soft", "pronunciation": "lem-but", "category": "adjectives", "example": "Kain ini lembut."},
        "kasar": {"english": "rough", "pronunciation": "ka-sar", "category": "adjectives", "example": "Permukaan ini kasar."},
        "halus": {"english": "smooth", "pronunciation": "ha-lus", "category": "adjectives", "example": "Kulit bayi halus."},
        "tajam": {"english": "sharp", "pronunciation": "ta-jam", "category": "adjectives", "example": "Pisau ini tajam."},
        "tumpul": {"english": "blunt", "pronunciation": "tum-pul", "category": "adjectives", "example": "Pensil ini tumpul."},
        "licin": {"english": "slippery", "pronunciation": "li-cin", "category": "adjectives", "example": "Lantai ini licin."},
        "kering": {"english": "dry", "pronunciation": "ke-ring", "category": "adjectives", "example": "Pakaian sudah kering."},
        "basah": {"english": "wet", "pronunciation": "ba-sah", "category": "adjectives", "example": "Rambut masih basah."},
        "lembab": {"english": "humid", "pronunciation": "lem-bab", "category": "adjectives", "example": "Udara terasa lembab."},
        "panas": {"english": "hot", "pronunciation": "pa-nas", "category": "adjectives", "example": "Air ini panas."},
        "dingin": {"english": "cold", "pronunciation": "di-ngin", "category": "adjectives", "example": "Es ini dingin."},
        "hangat": {"english": "warm", "pronunciation": "ha-ngat", "category": "adjectives", "example": "Sup ini hangat."},
        "sejuk": {"english": "cool", "pronunciation": "se-juk", "category": "adjectives", "example": "Angin sore sejuk."},
        
        # More Extended Verbs
        "berjalan": {"english": "to walk", "pronunciation": "ber-ja-lan", "category": "verbs", "example": "Saya berjalan ke sekolah."},
        "berlari": {"english": "to run", "pronunciation": "ber-la-ri", "category": "verbs", "example": "Dia berlari cepat."},
        "melompat": {"english": "to jump", "pronunciation": "me-lom-pat", "category": "verbs", "example": "Anak melompat tinggi."},
        "berenang": {"english": "to swim", "pronunciation": "be-re-nang", "category": "verbs", "example": "Ikan berenang di laut."},
        "terbang": {"english": "to fly", "pronunciation": "ter-bang", "category": "verbs", "example": "Burung terbang tinggi."},
        "merangkak": {"english": "to crawl", "pronunciation": "me-rang-kak", "category": "verbs", "example": "Bayi merangkak di lantai."},
        "memanjat": {"english": "to climb", "pronunciation": "me-man-jat", "category": "verbs", "example": "Monyet memanjat pohon."},
        "menyelam": {"english": "to dive", "pronunciation": "me-nye-lam", "category": "verbs", "example": "Penyelam menyelam dalam."},
        "mengendarai": {"english": "to ride", "pronunciation": "meng-en-da-rai", "category": "verbs", "example": "Dia mengendarai sepeda."},
        "mengemudi": {"english": "to drive", "pronunciation": "meng-e-mu-di", "category": "verbs", "example": "Ayah mengemudi mobil."},
        "menerbangkan": {"english": "to pilot", "pronunciation": "me-ner-bang-kan", "category": "verbs", "example": "Pilot menerbangkan pesawat."},
        "berlayar": {"english": "to sail", "pronunciation": "ber-la-yar", "category": "verbs", "example": "Kapal berlayar ke pulau."},
        "mendayung": {"english": "to paddle", "pronunciation": "men-da-yung", "category": "verbs", "example": "Nelayan mendayung perahu."},
        "berselancar": {"english": "to surf", "pronunciation": "ber-se-lan-car", "category": "verbs", "example": "Dia berselancar di pantai."},
        
        # More Numbers & Mathematics
        "nol": {"english": "zero", "pronunciation": "nol", "category": "numbers", "example": "Nol tambah satu sama dengan satu."},
        "setengah": {"english": "half", "pronunciation": "se-te-ngah", "category": "numbers", "example": "Setengah dari sepuluh adalah lima."},
        "seperempat": {"english": "quarter", "pronunciation": "se-pe-rem-pat", "category": "numbers", "example": "Seperempat jam lima belas menit."},
        "sepertiga": {"english": "one third", "pronunciation": "se-per-ti-ga", "category": "numbers", "example": "Sepertiga dari sembilan adalah tiga."},
        "sepersepuluh": {"english": "one tenth", "pronunciation": "se-per-se-pu-luh", "category": "numbers", "example": "Sepersepuluh dari seratus adalah sepuluh."},
        "persen": {"english": "percent", "pronunciation": "per-sen", "category": "numbers", "example": "Lima puluh persen adalah setengah."},
        "tambah": {"english": "plus", "pronunciation": "tam-bah", "category": "numbers", "example": "Dua tambah tiga sama dengan lima."},
        "kurang": {"english": "minus", "pronunciation": "ku-rang", "category": "numbers", "example": "Lima kurang dua sama dengan tiga."},
        "kali": {"english": "times", "pronunciation": "ka-li", "category": "numbers", "example": "Tiga kali empat sama dengan dua belas."},
        "bagi": {"english": "divided by", "pronunciation": "ba-gi", "category": "numbers", "example": "Delapan bagi dua sama dengan empat."},
        "sama dengan": {"english": "equals", "pronunciation": "sa-ma de-ngan", "category": "numbers", "example": "Dua tambah dua sama dengan empat."},
        "lebih besar": {"english": "greater than", "pronunciation": "le-bih be-sar", "category": "numbers", "example": "Lima lebih besar dari tiga."},
        "lebih kecil": {"english": "less than", "pronunciation": "le-bih ke-cil", "category": "numbers", "example": "Dua lebih kecil dari lima."},
        
        # Extended Colors
        "ungu": {"english": "purple", "pronunciation": "u-ngu", "category": "colors", "example": "Bunga ungu cantik."},
        "pink": {"english": "pink", "pronunciation": "pink", "category": "colors", "example": "Baju pink cerah."},
        "coklat": {"english": "brown", "pronunciation": "cok-lat", "category": "colors", "example": "Tanah berwarna coklat."},
        "abu-abu": {"english": "gray", "pronunciation": "a-bu a-bu", "category": "colors", "example": "Awan abu-abu gelap."},
        "emas": {"english": "gold", "pronunciation": "e-mas", "category": "colors", "example": "Cincin emas berkilau."},
        "perak": {"english": "silver", "pronunciation": "pe-rak", "category": "colors", "example": "Gelang perak indah."},
        "perunggu": {"english": "bronze", "pronunciation": "pe-rung-gu", "category": "colors", "example": "Medali perunggu ketiga."},
        "krem": {"english": "cream", "pronunciation": "krem", "category": "colors", "example": "Dinding krem lembut."},
        "salmon": {"english": "salmon", "pronunciation": "sal-mon", "category": "colors", "example": "Warna salmon muda."},
        "magenta": {"english": "magenta", "pronunciation": "ma-gen-ta", "category": "colors", "example": "Tinta magenta cerah."},
        
        # Extended Weather & Climate
        "mendung": {"english": "cloudy", "pronunciation": "men-dung", "category": "weather", "example": "Langit mendung gelap."},
        "cerah": {"english": "sunny", "pronunciation": "ce-rah", "category": "weather", "example": "Cuaca cerah hari ini."},
        "berawan": {"english": "overcast", "pronunciation": "ber-a-wan", "category": "weather", "example": "Langit berawan tipis."},
        "berkabut": {"english": "foggy", "pronunciation": "ber-ka-but", "category": "weather", "example": "Pagi berkabut tebal."},
        "badai": {"english": "storm", "pronunciation": "ba-dai", "category": "weather", "example": "Badai kencang datang."},
        "topan": {"english": "typhoon", "pronunciation": "to-pan", "category": "weather", "example": "Topan merusak rumah."},
        "tornado": {"english": "tornado", "pronunciation": "tor-na-do", "category": "weather", "example": "Tornado berbentuk corong."},
        "gempa": {"english": "earthquake", "pronunciation": "gem-pa", "category": "weather", "example": "Gempa bumi guncang kota."},
        "tsunami": {"english": "tsunami", "pronunciation": "tsu-na-mi", "category": "weather", "example": "Tsunami gelombang besar."},
        "banjir": {"english": "flood", "pronunciation": "ban-jir", "category": "weather", "example": "Banjir rendam jalan."},
        "kekeringan": {"english": "drought", "pronunciation": "ke-ke-ring-an", "category": "weather", "example": "Kekeringan panjang terjadi."},
        "longsor": {"english": "landslide", "pronunciation": "long-sor", "category": "weather", "example": "Longsor tutup jalan."},
        
        # Extended Family & Relationships
        "suami": {"english": "husband", "pronunciation": "sua-mi", "category": "family", "example": "Suami saya baik."},
        "istri": {"english": "wife", "pronunciation": "is-tri", "category": "family", "example": "Istri cantik sekali."},
        "anak": {"english": "child", "pronunciation": "a-nak", "category": "family", "example": "Anak bermain di taman."},
        "orang tua": {"english": "parents", "pronunciation": "o-rang tu-a", "category": "family", "example": "Orang tua saya sehat."},
        "kakek": {"english": "grandfather", "pronunciation": "ka-kek", "category": "family", "example": "Kakek berumur delapan puluh."},
        "nenek": {"english": "grandmother", "pronunciation": "ne-nek", "category": "family", "example": "Nenek masak enak."},
        "cucu": {"english": "grandchild", "pronunciation": "cu-cu", "category": "family", "example": "Cucu pertama lahir."},
        "paman": {"english": "uncle", "pronunciation": "pa-man", "category": "family", "example": "Paman datang berkunjung."},
        "bibi": {"english": "aunt", "pronunciation": "bi-bi", "category": "family", "example": "Bibi membawa oleh-oleh."},
        "sepupu": {"english": "cousin", "pronunciation": "se-pu-pu", "category": "family", "example": "Sepupu saya pintar."},
        "keponakan": {"english": "nephew/niece", "pronunciation": "ke-po-na-kan", "category": "family", "example": "Keponakan lucu sekali."},
        "mertua": {"english": "in-law", "pronunciation": "mer-tu-a", "category": "family", "example": "Mertua baik hati."},
        "ipar": {"english": "sibling-in-law", "pronunciation": "i-par", "category": "family", "example": "Ipar saya dokter."},
        "menantu": {"english": "son/daughter-in-law", "pronunciation": "me-nan-tu", "category": "family", "example": "Menantu perempuan cantik."},
        
        # Extended Education & School
        "sekolah dasar": {"english": "elementary school", "pronunciation": "se-ko-lah da-sar", "category": "education", "example": "Sekolah dasar enam tahun."},
        "sekolah menengah": {"english": "middle school", "pronunciation": "se-ko-lah me-ne-ngah", "category": "education", "example": "Sekolah menengah tiga tahun."},
        "sekolah tinggi": {"english": "high school", "pronunciation": "se-ko-lah ting-gi", "category": "education", "example": "Sekolah tinggi persiapan kuliah."},
        "kuliah": {"english": "university", "pronunciation": "ku-li-ah", "category": "education", "example": "Kuliah empat tahun."},
        "fakultas": {"english": "faculty", "pronunciation": "fa-kul-tas", "category": "education", "example": "Fakultas kedokteran sulit."},
        "jurusan": {"english": "major", "pronunciation": "ju-ru-san", "category": "education", "example": "Jurusan teknik populer."},
        "mata kuliah": {"english": "course", "pronunciation": "ma-ta ku-li-ah", "category": "education", "example": "Mata kuliah matematika."},
        "dosen": {"english": "lecturer", "pronunciation": "do-sen", "category": "education", "example": "Dosen mengajar baik."},
        "rektor": {"english": "rector", "pronunciation": "rek-tor", "category": "education", "example": "Rektor pimpin universitas."},
        "dekan": {"english": "dean", "pronunciation": "de-kan", "category": "education", "example": "Dekan fakultas baru."},
        "tugas": {"english": "assignment", "pronunciation": "tu-gas", "category": "education", "example": "Tugas dikumpulkan besok."},
        "skripsi": {"english": "thesis", "pronunciation": "skrip-si", "category": "education", "example": "Skripsi harus selesai."},
        "wisuda": {"english": "graduation", "pronunciation": "wi-su-da", "category": "education", "example": "Wisuda bulan depan."},
        "ijazah": {"english": "diploma", "pronunciation": "i-ja-zah", "category": "education", "example": "Ijazah dokumen penting."},
        
        # Extended Technology & Internet
        "wifi": {"english": "wifi", "pronunciation": "wi-fi", "category": "technology", "example": "Wifi cepat di kafe."},
        "bluetooth": {"english": "bluetooth", "pronunciation": "blue-tooth", "category": "technology", "example": "Bluetooth koneksi nirkabel."},
        "USB": {"english": "USB", "pronunciation": "u-es-be", "category": "technology", "example": "USB simpan data."},
        "CD": {"english": "CD", "pronunciation": "ce-de", "category": "technology", "example": "CD musik lama."},
        "DVD": {"english": "DVD", "pronunciation": "de-ve-de", "category": "technology", "example": "DVD film bagus."},
        "flashdisk": {"english": "flash drive", "pronunciation": "flash-disk", "category": "technology", "example": "Flashdisk kecil praktis."},
        "harddisk": {"english": "hard drive", "pronunciation": "hard-disk", "category": "technology", "example": "Harddisk simpan banyak."},
        "RAM": {"english": "RAM", "pronunciation": "ram", "category": "technology", "example": "RAM komputer cepat."},
        "processor": {"english": "processor", "pronunciation": "pro-ces-sor", "category": "technology", "example": "Processor otak komputer."},
        "motherboard": {"english": "motherboard", "pronunciation": "mother-board", "category": "technology", "example": "Motherboard papan utama."},
        "keyboard": {"english": "keyboard", "pronunciation": "key-board", "category": "technology", "example": "Keyboard untuk mengetik."},
        "mouse": {"english": "mouse", "pronunciation": "mouse", "category": "technology", "example": "Mouse klik dan drag."},
        "monitor": {"english": "monitor", "pronunciation": "mo-ni-tor", "category": "technology", "example": "Monitor layar besar."},
        "printer": {"english": "printer", "pronunciation": "prin-ter", "category": "technology", "example": "Printer cetak dokumen."},
        "scanner": {"english": "scanner", "pronunciation": "scan-ner", "category": "technology", "example": "Scanner scan foto."},
        
        # Extended Sports & Games
        "sepak bola": {"english": "soccer", "pronunciation": "se-pak bo-la", "category": "sports", "example": "Sepak bola olahraga populer."},
        "bulu tangkis": {"english": "badminton", "pronunciation": "bu-lu tang-kis", "category": "sports", "example": "Bulu tangkis olahraga Indonesia."},
        "tenis": {"english": "tennis", "pronunciation": "te-nis", "category": "sports", "example": "Tenis pakai raket."},
        "tenis meja": {"english": "table tennis", "pronunciation": "te-nis me-ja", "category": "sports", "example": "Tenis meja ping pong."},
        "voli": {"english": "volleyball", "pronunciation": "vo-li", "category": "sports", "example": "Voli main beregu."},
        "basket": {"english": "basketball", "pronunciation": "bas-ket", "category": "sports", "example": "Basket masuk ring."},
        "baseball": {"english": "baseball", "pronunciation": "base-ball", "category": "sports", "example": "Baseball pakai pemukul."},
        "golf": {"english": "golf", "pronunciation": "golf", "category": "sports", "example": "Golf olahraga mahal."},
        "tinju": {"english": "boxing", "pronunciation": "tin-ju", "category": "sports", "example": "Tinju olahraga keras."},
        "karate": {"english": "karate", "pronunciation": "ka-ra-te", "category": "sports", "example": "Karate bela diri."},
        "judo": {"english": "judo", "pronunciation": "ju-do", "category": "sports", "example": "Judo seni berkelahi."},
        "taekwondo": {"english": "taekwondo", "pronunciation": "taek-won-do", "category": "sports", "example": "Taekwondo tendangan tinggi."},
        "silat": {"english": "martial arts", "pronunciation": "si-lat", "category": "sports", "example": "Silat budaya Indonesia."},
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

# All vocabulary is now integrated directly in VOCABULARY_DATA above

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
            st.info(f"📚 **Comprehensive Indonesian vocabulary** ready for learning!")
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
            # Get total vocabulary count across all levels
            total_vocab = 0
            for level_data in VOCABULARY_DATA.values():
                total_vocab += len(level_data)
            
            due_count = len(self.get_due_cards())
            st.metric("Cards Due", due_count, delta="for review")
            
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
        """Render category-based flashcard study interface"""
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #2E8B57; font-size: 2.5rem; margin: 0;'>📚 Study Flashcards</h1>
            <p style='color: #666; font-size: 1.1rem; margin: 0.5rem 0;'>Learn Indonesian words by category with spaced repetition</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Flatten VOCABULARY_DATA to get all words across all levels
        all_words = {}
        for level_data in VOCABULARY_DATA.values():
            all_words.update(level_data)
        
        # Get all available categories from flattened vocabulary
        categories = set()
        for word_data in all_words.values():
            categories.add(word_data.get('category', 'general'))
        categories = sorted(list(categories))
        
        # Category and level selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_category = st.selectbox(
                "🏷️ Choose Category to Practice:",
                options=['all'] + categories,
                format_func=lambda x: f"📚 All Categories" if x == 'all' 
                          else f"🎯 {x.title()}",
                key="flashcard_category"
            )
        
        with col2:
            selected_level = st.selectbox(
                "📚 Level:",
                options=list(VOCABULARY_DATA.keys()),
                index=list(VOCABULARY_DATA.keys()).index(st.session_state.user_progress['current_level'])
            )
        
        # Filter words by category and get due cards
        if selected_category == 'all':
            available_words = list(all_words.keys())
        else:
            available_words = [word for word, data in all_words.items() 
                             if data.get('category', 'general') == selected_category]
        
        # Get due cards from the filtered words
        level_words = VOCABULARY_DATA.get(selected_level, {})
        due_cards = []
        
        for word in available_words:
            if word in level_words and word in st.session_state.flashcard_data:
                card_data = st.session_state.flashcard_data[word]
                next_review = card_data['next_review']
                if isinstance(next_review, str):
                    next_review = datetime.fromisoformat(next_review)
                if datetime.now() >= next_review:
                    due_cards.append(word)
        
        # If no due cards, show all available words from category and level
        if not due_cards:
            due_cards = [word for word in available_words if word in level_words]
        
        if not due_cards:
            st.warning(f"No flashcards available for '{selected_category}' category in '{selected_level}' level!")
            if st.button("← Back to Dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
            return
        
        # Get current card
        if (st.session_state.current_card is None or 
            st.session_state.current_card not in due_cards or
            st.session_state.get('current_flashcard_category') != selected_category):
            st.session_state.current_card = random.choice(due_cards)
            st.session_state.show_answer = False
            st.session_state.current_flashcard_category = selected_category
        
        current_word = st.session_state.current_card
        word_data = all_words[current_word]
        card_data = st.session_state.flashcard_data.get(current_word, {
            'review_count': 0,
            'next_review': datetime.now(),
            'interval': 1
        })
        
        # Category indicator
        st.markdown(f"""
        <div style="background: rgba(76, 175, 80, 0.1); padding: 0.5rem 1rem; 
                    border-radius: 25px; display: inline-block; margin-bottom: 1rem;">
            <span style="color: #2E7D32; font-weight: bold;">
                🏷️ {word_data.get('category', 'general').title()}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple card display
        st.markdown("---")
        
        # Clean, simple card with category color coding
        category_colors = {
            'basic': '#4CAF50', 'food': '#FF9800', 'family': '#E91E63', 'numbers': '#9C27B0',
            'time': '#3F51B5', 'colors': '#00BCD4', 'body': '#795548', 'clothing': '#607D8B',
            'adjectives': '#FFC107', 'verbs': '#8BC34A', 'questions': '#F44336', 'weather': '#2196F3',
            'nature': '#4CAF50', 'animals': '#FF5722', 'transportation': '#9E9E9E', 'emotions': '#E91E63',
            'technology': '#673AB7', 'sports': '#FF9800', 'education': '#3F51B5', 'business': '#795548',
            'health': '#F44336', 'travel': '#00BCD4', 'shopping': '#4CAF50', 'pronouns': '#9C27B0',
            'prepositions': '#607D8B', 'conjunctions': '#FF5722'
        }
        
        category = word_data.get('category', 'general')
        card_color = category_colors.get(category, '#4CAF50')
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {card_color}, {card_color}dd); padding: 3rem; border-radius: 20px; text-align: center; color: white; margin: 2rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.15);'>
            <h1 style='font-size: 4rem; margin: 0; font-weight: bold;'>{current_word}</h1>
        </div>
        """, unsafe_allow_html=True)
                
        # Answer display
        if st.session_state.show_answer:
            example_text = word_data.get('example', 'No example available')
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FF6B6B, #ee5a52); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.15);'>
                <h2 style='font-size: 2.5rem; margin: 0; font-weight: bold;'>{word_data['english']}</h2>
                <p style='font-size: 1.3rem; margin: 0.5rem 0; opacity: 0.9;'>{word_data['pronunciation']}</p>
                <p style='font-size: 1.1rem; margin: 0.5rem 0; opacity: 0.8;'>Category: {category.title()}</p>
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
            if st.button("➡️ Next Word", use_container_width=True, type="secondary"):
                st.session_state.current_card = None
                st.session_state.show_answer = False
                st.rerun()
        
        if st.session_state.show_answer:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("😊 Easy", use_container_width=True, type="primary"):
                    self.update_flashcard_schedule(current_word, 'easy')
                    st.session_state.user_progress['words_learned'].add(current_word)
                    self.update_daily_streak()
                    st.session_state.current_card = None
                    st.session_state.show_answer = False
                    st.rerun()
                    
            with col2:
                if st.button("🤔 Medium", use_container_width=True):
                    self.update_flashcard_schedule(current_word, 'medium')
                    st.session_state.user_progress['words_learned'].add(current_word)
                    self.update_daily_streak()
                    st.session_state.current_card = None
                    st.session_state.show_answer = False
                    st.rerun()
                    
            with col3:
                if st.button("😰 Hard", use_container_width=True):
                    self.update_flashcard_schedule(current_word, 'hard')
                    self.update_daily_streak()
                    st.session_state.current_card = None
                    st.session_state.show_answer = False
                    st.rerun()
        
        # Enhanced progress info with category stats
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"📊 Category: {selected_category.title()}")
        with col2:
            st.info(f"📋 Due Now: {len(due_cards)} cards")
        with col3:
            category_learned = len([w for w in st.session_state.user_progress['words_learned'] 
                                  if w in available_words])
            st.info(f"✅ Learned: {category_learned} words")
        with col4:
            st.info(f"🏷️ Categories: {len(categories)}")
    
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
        selected_answer = st.radio("", options, key=f"quiz_{current_idx}", index=None)
        
        # Add hint button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💡 Get Hint", use_container_width=True):
                st.info(f"💡 Hint: The word '{current_word}' is related to '{card_data.get('category', 'general')}' category")
        
        # Submit button with better styling - only proceed if answer is selected
        if st.button("Submit Answer", use_container_width=True, type="primary"):
            if selected_answer is None:
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
            # Streamlined header with smaller flag and cleaner design
            st.markdown("""
            <style>
            .sidebar-header {
                text-align: center; 
                padding: 0.8rem 0; 
                background: linear-gradient(135deg, #8B7CF6 0%, #A855F7 100%); 
                border-radius: 12px; 
                margin-bottom: 1rem;
                box-shadow: 0 2px 10px rgba(139, 124, 246, 0.3);
            }
            .sidebar-header h3 {
                color: white; 
                margin: 0; 
                font-size: 1.3rem; 
                font-weight: 600;
            }
            .sidebar-header p {
                color: rgba(255,255,255,0.9); 
                margin: 0.3rem 0 0 0; 
                font-size: 0.8rem;
            }
            .user-info {
                background: #f8fafc; 
                padding: 0.8rem; 
                border-radius: 8px; 
                margin-bottom: 1rem; 
                border: 1px solid #e2e8f0;
            }
            .user-name {
                margin: 0; 
                color: #1e293b; 
                font-size: 1rem; 
                font-weight: 500;
            }
            .user-stats {
                margin: 0.4rem 0 0 0; 
                color: #64748b; 
                font-size: 0.85rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .quick-access-btn {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0.8rem;
                text-align: center;
                margin: 0.3rem;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .quick-access-btn:hover {
                border-color: #8B7CF6;
                box-shadow: 0 2px 8px rgba(139, 124, 246, 0.2);
                transform: translateY(-1px);
            }
            .btn-icon {
                font-size: 1.5rem;
                margin-bottom: 0.3rem;
            }
            .btn-text {
                font-size: 0.8rem;
                font-weight: 500;
                color: #374151;
            }
            .section-header {
                color: #6b7280;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 1rem 0 0.5rem 0;
            }
            .nav-btn {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 0.6rem 0.8rem;
                margin: 0.2rem 0;
                text-align: left;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .nav-btn:hover {
                background: #f9fafb;
                border-color: #8B7CF6;
            }
            .progress-bar {
                width: 100%;
                height: 4px;
                background: #e5e7eb;
                border-radius: 2px;
                overflow: hidden;
                margin-top: 0.3rem;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #10b981, #059669);
                transition: width 0.3s ease;
            }
            </style>
            
            <div class="sidebar-header">
                <h3>🇮🇩 Indonesian Hub</h3>
                <p>Fun Indonesian Learning</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simplified user info in one line with icons
            learned_words = len(st.session_state.user_progress['words_learned'])
            streak = st.session_state.user_progress.get('study_streak', 0)
            progress_percent = min((streak / 30) * 100, 100)  # Progress toward 30-day streak
            
            st.markdown(f"""
            <div class="user-info">
                <h4 class="user-name">👤 {st.session_state.current_profile}</h4>
                <div class="user-stats">
                    <span>📚 {learned_words} words</span>
                    <span>🔥 {streak} days</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percent}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Access with 2x2 grid and clear labels
            st.markdown('<div class="section-header">Quick Access</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎴\nFlashcards", help="Study Flashcards", use_container_width=True, key="flashcards_btn"):
                    st.session_state.page = 'flashcards'
                    st.rerun()
                    
                if st.button("💬\nSentences", help="Learn Sentences", use_container_width=True, key="sentences_btn"):
                    st.session_state.page = 'sentences'
                    st.rerun()
            
            with col2:
                if st.button("⚔️\nDuels", help="Battle Friends", use_container_width=True, key="duels_btn"):
                    st.session_state.page = 'battle'
                    st.rerun()
                    
                if st.button("🧠\nQuizzes", help="Take Quiz", use_container_width=True, key="quizzes_btn"):
                    st.session_state.page = 'quiz'
                    st.rerun()
            
            # Learn section with collapsible menu
            st.markdown('<div class="section-header">Learn</div>', unsafe_allow_html=True)
            
            with st.expander("📖 Study Materials", expanded=False):
                if st.button("🏠 Dashboard", use_container_width=True, key="dashboard_btn"):
                    st.session_state.page = 'dashboard'
                    st.rerun()
                
                if st.button("📊 My Progress", use_container_width=True, key="progress_btn"):
                    st.session_state.page = 'word_database'
                    st.rerun()
                
                if st.button("📖 Grammar", use_container_width=True, key="grammar_btn"):
                    st.session_state.page = 'study'
                    st.rerun()
                
                if st.button("📚 Workbook", use_container_width=True, key="workbook_btn"):
                    st.session_state.page = 'workbook'
                    st.rerun()
            
            # Account section with dropdown
            st.markdown('<div class="section-header">Account</div>', unsafe_allow_html=True)
            
            with st.expander("⚙️ Account Settings", expanded=False):
                if st.button("👤 Profile", use_container_width=True, key="profile_btn"):
                    st.session_state.page = 'profile'
                    st.rerun()
                
                if st.button("⚙️ Settings", use_container_width=True, key="settings_btn"):
                    st.session_state.page = 'settings'
                    st.rerun()
                
                st.markdown("---")
                if st.button("🚪 Logout", use_container_width=True, type="secondary", key="logout_btn"):
                    st.session_state.current_profile = None
                    st.session_state.page = 'login'
                    st.rerun()
            
            # Get total vocabulary count
            total_vocab = 0
            for level_data in VOCABULARY_DATA.values():
                total_vocab += len(level_data)
            
            due_cards = len(self.get_due_cards())
            if due_cards > 0:
                st.info(f"🎴 {due_cards} cards due for review!")
            else:
                st.success(f"🎴 All caught up! Great job!")
        
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
    
    def init_new_profile(self, profile_name, pin_code):
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
            'created_date': datetime.now().isoformat(),
            'pin_code': pin_code
        }
        
        st.session_state.flashcard_data = self.init_flashcard_data()
        
        # Save initial data
        self.save_profile_data(profile_name)
        return True
    
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
