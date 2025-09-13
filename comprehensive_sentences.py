"""
Comprehensive Indonesian Sentence Database
High-quality sentences for effective Indonesian learning
"""

SENTENCE_DATABASE = {
    # BEGINNER LEVEL - Essential Daily Life
    "beginner": {
        "greetings": [
            {
                "indonesian": "Halo, nama saya [Your Name]. Senang bertemu dengan Anda.",
                "english": "Hello, my name is [Your Name]. Nice to meet you.",
                "pronunciation": "HAH-lo, NAH-mah sah-YAH [Your Name]. Seh-NAHNG ber-teh-MOO deh-NGAN Ahn-DAH",
                "category": "Greetings",
                "grammar_focus": "Self-introduction, formal greeting",
                "key_words": ["nama", "senang", "bertemu"],
                "difficulty": 1
            },
            {
                "indonesian": "Apa kabar? Saya baik-baik saja, terima kasih.",
                "english": "How are you? I'm fine, thank you.",
                "pronunciation": "AH-pah KAH-bar? SAH-yah BAH-ik BAH-ik SAH-jah, teh-REE-mah KAH-seeh",
                "category": "Greetings",
                "grammar_focus": "Question formation, polite response",
                "key_words": ["apa kabar", "baik-baik saja", "terima kasih"],
                "difficulty": 1
            },
            {
                "indonesian": "Selamat pagi! Bagaimana hari Anda?",
                "english": "Good morning! How is your day?",
                "pronunciation": "Seh-LAH-mat PAH-gee! Bah-GAI-mah-nah HAH-ree Ahn-DAH?",
                "category": "Greetings",
                "grammar_focus": "Time-specific greeting, question about day",
                "key_words": ["selamat pagi", "bagaimana", "hari"],
                "difficulty": 1
            }
        ],
        
        "daily_activities": [
            {
                "indonesian": "Saya bangun pagi-pagi sekali setiap hari.",
                "english": "I wake up very early every day.",
                "pronunciation": "SAH-yah BAHN-goon PAH-gee PAH-gee seh-KAH-lee seh-TIAP HAH-ree",
                "category": "Daily Activities",
                "grammar_focus": "Daily routine, time expressions",
                "key_words": ["bangun", "pagi-pagi", "setiap hari"],
                "difficulty": 1
            },
            {
                "indonesian": "Setelah sarapan, saya pergi ke kantor dengan bus.",
                "english": "After breakfast, I go to the office by bus.",
                "pronunciation": "Seh-TEH-lah sah-RAH-pan, SAH-yah PER-gee keh KAN-tor deh-NGAN boos",
                "category": "Daily Activities",
                "grammar_focus": "Sequence of actions, transportation",
                "key_words": ["setelah", "sarapan", "pergi", "kantor", "bus"],
                "difficulty": 2
            },
            {
                "indonesian": "Saya suka minum kopi di pagi hari sambil membaca koran.",
                "english": "I like to drink coffee in the morning while reading the newspaper.",
                "pronunciation": "SAH-yah SOO-kah MEE-noom KOH-pee dee PAH-gee HAH-ree SAHM-beel meh-MBAH-chah KOR-an",
                "category": "Daily Activities",
                "grammar_focus": "Preferences, simultaneous actions",
                "key_words": ["suka", "minum", "kopi", "sambil", "membaca"],
                "difficulty": 2
            }
        ],
        
        "family_relationships": [
            {
                "indonesian": "Saya punya dua saudara laki-laki dan satu saudara perempuan.",
                "english": "I have two brothers and one sister.",
                "pronunciation": "SAH-yah POON-yah DOO-ah sah-oo-DAH-rah LAH-kee LAH-kee dan SAH-too sah-oo-DAH-rah peh-REHM-poo-an",
                "category": "Family",
                "grammar_focus": "Possession, family members, numbers",
                "key_words": ["punya", "saudara", "laki-laki", "perempuan"],
                "difficulty": 2
            },
            {
                "indonesian": "Orang tua saya tinggal di desa yang tenang.",
                "english": "My parents live in a quiet village.",
                "pronunciation": "OR-ang TOO-ah SAH-yah TING-gal dee DEH-sah yang teh-NAHNG",
                "category": "Family",
                "grammar_focus": "Family terms, location, adjectives",
                "key_words": ["orang tua", "tinggal", "desa", "tenang"],
                "difficulty": 2
            }
        ],
        
        "shopping_food": [
            {
                "indonesian": "Saya pergi ke pasar untuk membeli sayuran segar.",
                "english": "I go to the market to buy fresh vegetables.",
                "pronunciation": "SAH-yah PER-gee keh PAH-sar oon-TOOK meh-MBEH-lee sah-YOO-rah-an seh-GAR",
                "category": "Shopping",
                "grammar_focus": "Purpose with 'untuk', shopping vocabulary",
                "key_words": ["pasar", "untuk", "membeli", "sayuran", "segar"],
                "difficulty": 2
            },
            {
                "indonesian": "Berapa harga nasi gudeg ini?",
                "english": "How much does this nasi gudeg cost?",
                "pronunciation": "Beh-RAH-pah HAR-gah NAH-see GOO-deg EE-nee?",
                "category": "Shopping",
                "grammar_focus": "Asking for prices, Indonesian food",
                "key_words": ["berapa", "harga", "nasi gudeg"],
                "difficulty": 2
            },
            {
                "indonesian": "Tolong bungkus makanan ini untuk dibawa pulang.",
                "english": "Please wrap this food to take home.",
                "pronunciation": "TOH-long BOONG-koos mah-KAHN-an EE-nee oon-TOOK dee-BAH-wah POO-lahng",
                "category": "Shopping",
                "grammar_focus": "Polite requests, takeaway food",
                "key_words": ["tolong", "bungkus", "makanan", "dibawa pulang"],
                "difficulty": 2
            },
            {
                "indonesian": "Apakah ada diskon untuk pembelian dalam jumlah besar?",
                "english": "Is there a discount for bulk purchases?",
                "pronunciation": "Ah-PAH-kah AH-dah DEES-kon oon-TOOK peh-MBEH-lee-an DAH-lam JOOM-lah BAH-sar?",
                "category": "Shopping",
                "grammar_focus": "Asking about discounts, business vocabulary",
                "key_words": ["diskon", "pembelian", "jumlah besar"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya ingin membeli baju batik yang bagus untuk acara resmi.",
                "english": "I want to buy a nice batik shirt for a formal event.",
                "pronunciation": "SAH-yah ING-gin meh-MBEH-lee BAH-joo BAH-teek yang BAH-goos oon-TOOK AH-chah-rah rehs-MEE",
                "category": "Shopping",
                "grammar_focus": "Describing clothing, cultural items",
                "key_words": ["baju batik", "bagus", "acara resmi"],
                "difficulty": 3
            },
            {
                "indonesian": "Bisakah saya mencoba sepatu ini?",
                "english": "Can I try on these shoes?",
                "pronunciation": "BEE-sah-kah SAH-yah mehn-CHOH-bah seh-PAH-too EE-nee?",
                "category": "Shopping",
                "grammar_focus": "Asking permission, trying on clothes",
                "key_words": ["bisakah", "mencoba", "sepatu"],
                "difficulty": 2
            },
            {
                "indonesian": "Harga ini terlalu mahal, ada yang lebih murah?",
                "english": "This price is too expensive, is there something cheaper?",
                "pronunciation": "HAR-gah EE-nee ter-LAH-loo mah-HAL, AH-dah yang LEH-beh MOO-rah?",
                "category": "Shopping",
                "grammar_focus": "Negotiating prices, comparisons",
                "key_words": ["terlalu mahal", "lebih murah"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya akan membayar dengan kartu kredit.",
                "english": "I will pay with a credit card.",
                "pronunciation": "SAH-yah AH-kan meh-MBAH-yar deh-NGAN KAR-too KREH-deet",
                "category": "Shopping",
                "grammar_focus": "Payment methods, future tense",
                "key_words": ["membayar", "kartu kredit"],
                "difficulty": 2
            }
        ],
        
        "weather_environment": [
            {
                "indonesian": "Hari ini cuacanya sangat panas dan terik.",
                "english": "Today the weather is very hot and scorching.",
                "pronunciation": "HAH-ree EE-nee choo-AH-chah-nyah sahng-GAT PAH-nas dan teh-REEK",
                "category": "Weather",
                "grammar_focus": "Weather descriptions, adjectives",
                "key_words": ["cuaca", "panas", "terik"],
                "difficulty": 2
            },
            {
                "indonesian": "Hujan deras turun sepanjang malam.",
                "english": "Heavy rain fell all night long.",
                "pronunciation": "HOO-jan DEH-ras TOO-roon seh-PAHN-jahng MAH-lam",
                "category": "Weather",
                "grammar_focus": "Past tense, weather events",
                "key_words": ["hujan deras", "turun", "sepanjang malam"],
                "difficulty": 2
            },
            {
                "indonesian": "Saya suka berjalan-jalan di pantai saat matahari terbenam.",
                "english": "I like walking on the beach when the sun sets.",
                "pronunciation": "SAH-yah SOO-kah ber-JAH-lan JAH-lan dee PAN-tah-ee SAH-at mah-tah-HAH-ree ter-beh-NAM",
                "category": "Weather",
                "grammar_focus": "Preferences, time expressions",
                "key_words": ["berjalan-jalan", "pantai", "matahari terbenam"],
                "difficulty": 3
            },
            {
                "indonesian": "Angin kencang bertiup dari laut.",
                "english": "Strong wind is blowing from the sea.",
                "pronunciation": "AHN-gin ken-CHAHNG ber-TEE-oop DAH-ree LAH-oot",
                "category": "Weather",
                "grammar_focus": "Present continuous, direction",
                "key_words": ["angin kencang", "bertiup", "dari laut"],
                "difficulty": 2
            }
        ],
        
        "health_medical": [
            {
                "indonesian": "Saya merasa tidak enak badan hari ini.",
                "english": "I don't feel well today.",
                "pronunciation": "SAH-yah meh-RAH-sah tee-DAK eh-NAK BAH-dan HAH-ree EE-nee",
                "category": "Health",
                "grammar_focus": "Expressing illness, feelings",
                "key_words": ["merasa", "tidak enak badan"],
                "difficulty": 2
            },
            {
                "indonesian": "Kepala saya pusing dan demam tinggi.",
                "english": "My head is dizzy and I have a high fever.",
                "pronunciation": "keh-PAH-lah SAH-yah POO-sing dan deh-MAM TING-gee",
                "category": "Health",
                "grammar_focus": "Body parts, symptoms",
                "key_words": ["kepala", "pusing", "demam tinggi"],
                "difficulty": 2
            },
            {
                "indonesian": "Saya perlu pergi ke dokter untuk pemeriksaan.",
                "english": "I need to go to the doctor for a check-up.",
                "pronunciation": "SAH-yah peh-LOO PER-gee keh DOK-ter oon-TOOK peh-meh-REEK-sah-an",
                "category": "Health",
                "grammar_focus": "Necessity, medical appointments",
                "key_words": ["perlu", "dokter", "pemeriksaan"],
                "difficulty": 3
            },
            {
                "indonesian": "Apakah ada obat untuk sakit kepala?",
                "english": "Is there medicine for a headache?",
                "pronunciation": "Ah-PAH-kah AH-dah OH-bat oon-TOOK SAH-keet keh-PAH-lah?",
                "category": "Health",
                "grammar_focus": "Asking for medicine, medical help",
                "key_words": ["obat", "sakit kepala"],
                "difficulty": 2
            }
        ],
        
        "emotions_feelings": [
            {
                "indonesian": "Saya sangat senang bisa bertemu dengan Anda.",
                "english": "I am very happy to meet you.",
                "pronunciation": "SAH-yah sahng-GAT seh-NAHNG BEE-sah ber-teh-MOO deh-NGAN Ahn-DAH",
                "category": "Emotions",
                "grammar_focus": "Expressing happiness, meeting people",
                "key_words": ["senang", "bertemu"],
                "difficulty": 2
            },
            {
                "indonesian": "Saya merasa sedih karena kehilangan teman baik.",
                "english": "I feel sad because I lost a good friend.",
                "pronunciation": "SAH-yah meh-RAH-sah seh-DEEH kah-REH-nah keh-hee-LAHN-gan teh-MAN BAH-eek",
                "category": "Emotions",
                "grammar_focus": "Expressing sadness, cause and effect",
                "key_words": ["sedih", "kehilangan", "teman baik"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya bangga dengan prestasi anak saya di sekolah.",
                "english": "I am proud of my child's achievement at school.",
                "pronunciation": "SAH-yah BAHN-gah deh-NGAN preh-STAH-see AH-nak SAH-yah dee seh-KOH-lah",
                "category": "Emotions",
                "grammar_focus": "Expressing pride, family relationships",
                "key_words": ["bangga", "prestasi", "anak"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya takut naik pesawat terbang.",
                "english": "I am afraid of flying in an airplane.",
                "pronunciation": "SAH-yah TAH-koot NAH-eek peh-SAH-wat ter-BAHNG",
                "category": "Emotions",
                "grammar_focus": "Expressing fear, transportation",
                "key_words": ["takut", "naik", "pesawat terbang"],
                "difficulty": 2
            }
        ]
    },
    
    # INTERMEDIATE LEVEL - Practical Situations
    "intermediate": {
        "travel_directions": [
            {
                "indonesian": "Permisi, di mana letak stasiun kereta terdekat?",
                "english": "Excuse me, where is the nearest train station?",
                "pronunciation": "Per-MEE-see, dee MAH-nah leh-TAK stah-SEE-oon keh-REH-tah ter-DEH-kat?",
                "category": "Travel",
                "grammar_focus": "Asking for directions, location questions",
                "key_words": ["permisi", "di mana", "letak", "stasiun", "terdekat"],
                "difficulty": 3
            },
            {
                "indonesian": "Bagaimana cara menuju ke bandara dari hotel ini?",
                "english": "How do I get to the airport from this hotel?",
                "pronunciation": "Bah-GAI-mah-nah CHAH-rah meh-NOO-joo keh ban-DAH-rah dee-REE ho-TEL EE-nee?",
                "category": "Travel",
                "grammar_focus": "Asking for directions, transportation",
                "key_words": ["bagaimana cara", "menuju", "bandara", "dari"],
                "difficulty": 3
            },
            {
                "indonesian": "Apakah ada bus yang pergi ke pusat kota?",
                "english": "Is there a bus that goes to the city center?",
                "pronunciation": "Ah-PAH-kah AH-dah boos yang per-GEE keh POO-sat KOH-tah?",
                "category": "Travel",
                "grammar_focus": "Existence questions, relative clauses",
                "key_words": ["apakah ada", "yang", "pusat kota"],
                "difficulty": 3
            }
        ],
        
        "restaurant_dining": [
            {
                "indonesian": "Saya ingin memesan nasi gudeg dan es teh manis.",
                "english": "I would like to order nasi gudeg and sweet iced tea.",
                "pronunciation": "SAH-yah ING-gin meh-MEH-san NAH-see GOO-deg dan es teh MAH-nees",
                "category": "Dining",
                "grammar_focus": "Ordering food, preferences",
                "key_words": ["ingin", "memesan", "es teh manis"],
                "difficulty": 3
            },
            {
                "indonesian": "Apakah makanan ini pedas? Saya tidak bisa makan makanan yang terlalu pedas.",
                "english": "Is this food spicy? I can't eat food that's too spicy.",
                "pronunciation": "Ah-PAH-kah mah-KAHN-an EE-nee peh-DAS? SAH-yah tee-DAK BEE-sah MAH-kan mah-KAHN-an yang ter-LAH-loo peh-DAS",
                "category": "Dining",
                "grammar_focus": "Asking about food, expressing inability",
                "key_words": ["pedas", "tidak bisa", "terlalu"],
                "difficulty": 3
            }
        ],
        
        "work_business": [
            {
                "indonesian": "Saya bekerja sebagai guru bahasa Inggris di sekolah menengah.",
                "english": "I work as an English teacher at a high school.",
                "pronunciation": "SAH-yah beh-KER-jah seh-BAH-gai GOO-roo bah-HAH-sah ING-grees dee seh-KOH-lah meh-NEH-gah",
                "category": "Work",
                "grammar_focus": "Profession, workplace description",
                "key_words": ["bekerja", "sebagai", "guru", "sekolah menengah"],
                "difficulty": 3
            },
            {
                "indonesian": "Rapat akan dimulai pukul sembilan pagi besok.",
                "english": "The meeting will start at nine o'clock tomorrow morning.",
                "pronunciation": "RAH-pat AH-kan dee-moo-LAH-ee POO-kool seh-MBEH-lan PAH-gee beh-SOK",
                "category": "Work",
                "grammar_focus": "Future tense, time expressions",
                "key_words": ["rapat", "akan", "dimulai", "pukul", "besok"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya perlu menyelesaikan laporan ini sebelum tengah malam.",
                "english": "I need to finish this report before midnight.",
                "pronunciation": "SAH-yah peh-LOO meh-nyah-leh-SAH-ee-kan lah-POR-an EE-nee seh-BEH-lum teh-NGAH MAH-lam",
                "category": "Work",
                "grammar_focus": "Necessity, deadlines, time expressions",
                "key_words": ["menyelesaikan", "laporan", "sebelum", "tengah malam"],
                "difficulty": 3
            },
            {
                "indonesian": "Bisakah kita mengadakan rapat darurat untuk membahas masalah ini?",
                "english": "Can we hold an emergency meeting to discuss this issue?",
                "pronunciation": "BEE-sah-kah KEE-tah mehng-AH-dah-kan RAH-pat dah-ROO-rat oon-TOOK meh-BAH-has mah-SAH-lah EE-nee?",
                "category": "Work",
                "grammar_focus": "Asking for meetings, business communication",
                "key_words": ["mengadakan", "rapat darurat", "membahas", "masalah"],
                "difficulty": 4
            },
            {
                "indonesian": "Saya akan mengirim email konfirmasi kepada semua peserta.",
                "english": "I will send a confirmation email to all participants.",
                "pronunciation": "SAH-yah AH-kan mehng-GEE-reem EE-mayl kon-feer-MAH-see keh-PAH-dah seh-MOO-ah peh-SER-tah",
                "category": "Work",
                "grammar_focus": "Future tense, business communication",
                "key_words": ["mengirim", "email", "konfirmasi", "peserta"],
                "difficulty": 3
            }
        ],
        
        "technology_modern": [
            {
                "indonesian": "Saya menggunakan aplikasi ini untuk belajar bahasa Indonesia.",
                "english": "I use this application to learn Indonesian language.",
                "pronunciation": "SAH-yah mehng-GOO-nah-kan ah-plee-KAH-see EE-nee oon-TOOK beh-LAH-jar bah-HAH-sah In-do-NEH-see-ah",
                "category": "Technology",
                "grammar_focus": "Technology vocabulary, purpose with 'untuk'",
                "key_words": ["menggunakan", "aplikasi", "belajar"],
                "difficulty": 3
            },
            {
                "indonesian": "Internet di sini sangat lambat dan tidak stabil.",
                "english": "The internet here is very slow and unstable.",
                "pronunciation": "In-ter-NET dee SEE-nee sahng-GAT LAM-bat dan tee-DAK stah-BEEL",
                "category": "Technology",
                "grammar_focus": "Describing technology problems",
                "key_words": ["internet", "lambat", "tidak stabil"],
                "difficulty": 3
            },
            {
                "indonesian": "Bisakah Anda membantu saya mengatur password baru?",
                "english": "Can you help me set up a new password?",
                "pronunciation": "BEE-sah-kah Ahn-DAH meh-MBAN-too SAH-yah mehng-AH-toor PAHSS-werd BAH-roo?",
                "category": "Technology",
                "grammar_focus": "Asking for help, technology support",
                "key_words": ["mengatur", "password", "baru"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya akan mengunduh file presentasi dari cloud storage.",
                "english": "I will download the presentation file from cloud storage.",
                "pronunciation": "SAH-yah AH-kan mehng-OON-doh FEE-leh preh-sen-TAH-see DAH-ree KLOUD STOR-ahj",
                "category": "Technology",
                "grammar_focus": "Technology actions, cloud computing",
                "key_words": ["mengunduh", "file", "presentasi", "cloud storage"],
                "difficulty": 4
            }
        ],
        
        "education_learning": [
            {
                "indonesian": "Saya sedang mempersiapkan diri untuk ujian akhir semester.",
                "english": "I am preparing myself for the final semester exam.",
                "pronunciation": "SAH-yah seh-DAHNG meh-per-see-AH-pan DEE-ree oon-TOOK oo-JEE-an AH-kheer seh-MEHS-ter",
                "category": "Education",
                "grammar_focus": "Present continuous, academic preparation",
                "key_words": ["mempersiapkan", "ujian", "akhir semester"],
                "difficulty": 3
            },
            {
                "indonesian": "Guru memberikan tugas kelompok untuk proyek sains.",
                "english": "The teacher assigned group work for the science project.",
                "pronunciation": "GOO-roo meh-MBER-ee-kan TOO-gahs keh-LOMP-ok oon-TOOK PROH-yek SAH-eens",
                "category": "Education",
                "grammar_focus": "Academic assignments, group work",
                "key_words": ["guru", "memberikan", "tugas kelompok", "proyek sains"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya harus membaca lima buku sebelum ujian minggu depan.",
                "english": "I have to read five books before next week's exam.",
                "pronunciation": "SAH-yah hah-ROOS meh-MBAH-chah LEE-mah BOO-koo seh-BEH-lum oo-JEE-an MING-goo deh-PAN",
                "category": "Education",
                "grammar_focus": "Obligation, academic requirements",
                "key_words": ["harus", "membaca", "sebelum", "minggu depan"],
                "difficulty": 3
            }
        ]
    },
    
    # ADVANCED LEVEL - Complex Communication
    "advanced": {
        "cultural_topics": [
            {
                "indonesian": "Indonesia memiliki keanekaragaman budaya yang sangat kaya dan unik.",
                "english": "Indonesia has a very rich and unique cultural diversity.",
                "pronunciation": "In-do-NEH-see-ah meh-MEE-lee-ee keh-ah-neh-kah-rah-GAH-man boo-DAH-yah yang sahng-GAT KAH-yah dan OO-neek",
                "category": "Culture",
                "grammar_focus": "Complex adjectives, cultural concepts",
                "key_words": ["keanekaragaman", "budaya", "kaya", "unik"],
                "difficulty": 4
            },
            {
                "indonesian": "Tradisi gotong royong masih sangat kuat di masyarakat Indonesia.",
                "english": "The tradition of mutual cooperation is still very strong in Indonesian society.",
                "pronunciation": "Trah-DEE-see goh-TONG ROY-ong MAH-shee sahng-GAT KOO-at dee mah-sya-RAH-kat In-do-NEH-see-ah",
                "category": "Culture",
                "grammar_focus": "Cultural concepts, social values",
                "key_words": ["tradisi", "gotong royong", "masyarakat"],
                "difficulty": 4
            }
        ],
        
        "abstract_concepts": [
            {
                "indonesian": "Pendidikan adalah kunci untuk masa depan yang lebih baik.",
                "english": "Education is the key to a better future.",
                "pronunciation": "Pen-dee-DEE-kan ah-DAH-lah KOON-chee oon-TOOK MAH-sah dee-PAN yang LEH-beh BAH-ik",
                "category": "Abstract",
                "grammar_focus": "Abstract concepts, metaphors",
                "key_words": ["pendidikan", "kunci", "masa depan", "lebih baik"],
                "difficulty": 4
            },
            {
                "indonesian": "Teknologi telah mengubah cara kita berkomunikasi dengan orang lain.",
                "english": "Technology has changed the way we communicate with others.",
                "pronunciation": "Tek-NOH-lo-gee teh-LAH mehng-OO-bah CHAH-rah KEE-tah ber-ko-moo-NEE-ka-see deh-NGAN OR-ang LAH-in",
                "category": "Technology",
                "grammar_focus": "Past perfect, technology impact",
                "key_words": ["teknologi", "mengubah", "berkomunikasi"],
                "difficulty": 4
            }
        ]
    },
    
    # CONVERSATIONAL PATTERNS
    "conversational": {
        "expressing_opinions": [
            {
                "indonesian": "Menurut saya, belajar bahasa Indonesia tidak terlalu sulit.",
                "english": "In my opinion, learning Indonesian is not too difficult.",
                "pronunciation": "Meh-NOO-root SAH-yah, beh-LAH-jar bah-HAH-sah In-do-NEH-see-ah tee-DAK ter-LAH-loo soo-LEET",
                "category": "Opinions",
                "grammar_focus": "Expressing opinions, difficulty levels",
                "key_words": ["menurut saya", "belajar", "tidak terlalu sulit"],
                "difficulty": 3
            },
            {
                "indonesian": "Saya setuju dengan pendapat Anda tentang pentingnya pendidikan.",
                "english": "I agree with your opinion about the importance of education.",
                "pronunciation": "SAH-yah seh-TOO-joo deh-NGAN pen-DAH-pat Ahn-DAH ten-TANG pen-TING-ah-nya pen-dee-DEE-kan",
                "category": "Opinions",
                "grammar_focus": "Agreement, importance expressions",
                "key_words": ["setuju", "pendapat", "pentingnya"],
                "difficulty": 3
            }
        ],
        
        "making_requests": [
            {
                "indonesian": "Bolehkah saya meminta bantuan Anda untuk menjelaskan ini?",
                "english": "May I ask for your help to explain this?",
                "pronunciation": "BOH-leh-kah SAH-yah meh-MIN-tah bahn-TOO-an Ahn-DAH oon-TOOK meh-nyah-LAS-kan EE-nee?",
                "category": "Requests",
                "grammar_focus": "Polite requests, asking for help",
                "key_words": ["bolehkah", "meminta bantuan", "menjelaskan"],
                "difficulty": 3
            },
            {
                "indonesian": "Apakah Anda bisa membantu saya mengerjakan tugas ini?",
                "english": "Could you help me with this assignment?",
                "pronunciation": "Ah-PAH-kah Ahn-DAH BEE-sah meh-MBAN-too SAH-yah meh-nger-JAH-kan TOO-gahs EE-nee?",
                "category": "Requests",
                "grammar_focus": "Ability questions, academic help",
                "key_words": ["bisa membantu", "mengerjakan", "tugas"],
                "difficulty": 3
            }
        ]
    }
}

# Additional sentence patterns for workbook exercises
SENTENCE_PATTERNS = {
    "basic_patterns": [
        {
            "pattern": "Saya [verb] [object]",
            "example": "Saya minum kopi",
            "translation": "I drink coffee",
            "grammar_focus": "Subject + Verb + Object",
            "difficulty": 1
        },
        {
            "pattern": "Saya [adjective]",
            "example": "Saya lapar",
            "translation": "I am hungry",
            "grammar_focus": "Subject + Adjective (no copula)",
            "difficulty": 1
        },
        {
            "pattern": "Saya [location] [verb]",
            "example": "Saya di rumah makan",
            "translation": "I am at home eating",
            "grammar_focus": "Location + Action",
            "difficulty": 2
        }
    ],
    
    "question_patterns": [
        {
            "pattern": "Apa [subject] [verb]?",
            "example": "Apa Anda makan?",
            "translation": "What are you eating?",
            "grammar_focus": "What questions",
            "difficulty": 2
        },
        {
            "pattern": "Di mana [subject] [verb]?",
            "example": "Di mana Anda tinggal?",
            "translation": "Where do you live?",
            "grammar_focus": "Where questions",
            "difficulty": 2
        },
        {
            "pattern": "Kapan [subject] [verb]?",
            "example": "Kapan Anda pergi?",
            "translation": "When are you going?",
            "grammar_focus": "When questions",
            "difficulty": 2
        }
    ]
}

# Grammar focus areas for workbook
GRAMMAR_AREAS = {
    "basic_grammar": [
        "Subject + Verb + Object",
        "Adjectives without copula",
        "Basic question formation",
        "Time expressions",
        "Location prepositions"
    ],
    "intermediate_grammar": [
        "Past tense (sudah/telah)",
        "Future tense (akan)",
        "Modal verbs (bisa, harus, boleh)",
        "Relative clauses (yang)",
        "Passive voice (di- prefix)"
    ],
    "advanced_grammar": [
        "Complex sentence structures",
        "Conditional sentences (jika/kalau)",
        "Subjunctive mood",
        "Formal vs informal register",
        "Cultural context in language"
    ]
}
