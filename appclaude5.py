# # =====================================================================================
# # ArogyaBridge - "Bridge to Healthcare"
# # SIH 2026 | PS ID: SIH26133
# # Streamlit Prototype (MVP v3)
# #
# # Run:
# #     pip install -r requirements.txt
# #     streamlit run app.py
# #
# # Optional:
# #     export GROQ_API_KEY=...
# #     export ASHA_PIN=1111
# #     export DOCTOR_PIN=2222
# #     export ADMIN_PIN=3333
# # =====================================================================================

# import os
# import re
# import sqlite3
# import json
# import uuid
# import random
# import hashlib
# import secrets
# from collections import Counter
# from datetime import date, datetime, timedelta

# import pandas as pd
# import streamlit as st


# # =============================================================================
# # CONFIG
# # =============================================================================

# DB_PATH = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)),
#     "arogyabridge.db",
# )

# GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
# GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

# DEMO_PINS = {
#     "asha": os.environ.get("ASHA_PIN", "1111"),
#     "doctor": os.environ.get("DOCTOR_PIN", "2222"),
#     "admin": os.environ.get("ADMIN_PIN", "3333"),
# }

# OUTBREAK_CLUSTER_THRESHOLD = 3
# OUTBREAK_LOOKBACK_DAYS = 30

# FACILITIES = [
#     "Sub-Centre Wagholi",
#     "PHC Ranjangaon",
#     "District Hospital Pune",
# ]

# APPOINTMENT_SLOTS = [
#     "09:00-10:00",
#     "10:00-11:00",
#     "11:00-12:00",
#     "14:00-15:00",
#     "15:00-16:00",
# ]

# DIAGNOSTIC_TESTS = [
#     "CBC",
#     "Hb",
#     "Blood Sugar (F)",
#     "Blood Sugar (PP)",
#     "Malaria RDT",
#     "Dengue NS1",
#     "X-Ray Chest",
#     "Urine Analysis",
# ]

# PRIORITY_COLORS = {
#     "RED": "#e53935",
#     "YELLOW": "#fbc02d",
#     "GREEN": "#43a047",
# }

# PRIORITY_ORDER = {
#     "RED": 0,
#     "YELLOW": 1,
#     "GREEN": 2,
# }

# STATUS_COLORS = {
#     "PENDING": "#fb8c00",
#     "ACKNOWLEDGED": "#1e88e5",
#     "COMPLETED": "#43a047",
# }

# STATUS_ORDER = {
#     "PENDING": 0,
#     "ACKNOWLEDGED": 1,
#     "COMPLETED": 2,
# }


# st.set_page_config(
#     page_title="ArogyaBridge | SIH26133",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st.markdown(
#     """
#     <style>
#     :root {
#         --ab-teal: #12806B;
#         --ab-teal-dark: #0B5347;
#         --ab-terracotta: #D97A46;
#         --ab-mustard: #E0AC4E;
#     }

#     /* Headings — same warm teal on both light and dark backgrounds */
#     h1, h2, h3 {
#         color: var(--ab-teal) !important;
#         font-family: Georgia, 'Times New Roman', serif;
#     }

#     /* Buttons — brand teal, readable text on both themes */
#     div.stButton > button:first-child {
#         background-color: var(--ab-teal);
#         color: #ffffff !important;
#         border-radius: 8px;
#         border: none;
#         padding: 0.5em 1.3em;
#         font-weight: 600;
#     }
#     div.stButton > button:first-child:hover {
#         background-color: var(--ab-teal-dark);
#         color: #ffffff !important;
#     }
#     div.stButton > button:first-child p { color: #ffffff !important; }

#     /* Metric numbers — terracotta accent, visible either way */
#     div[data-testid="stMetricValue"] { color: var(--ab-terracotta) !important; }

#     /* Expanders / dividers — subtle border only, no fixed bg color */
#     div[data-testid="stExpander"] {
#         border: 1px solid var(--ab-mustard);
#         border-radius: 10px;
#     }
#     .stAlert { border-radius: 10px; }

#     /* Sidebar accent border only — background left to the active theme */
#     section[data-testid="stSidebar"] {
#         border-right: 3px solid var(--ab-teal);
#     }

#     /* Tabs — brand-colored underline for the active tab */
#     button[data-baseweb="tab"][aria-selected="true"] {
#         color: var(--ab-teal) !important;
#         border-bottom-color: var(--ab-teal) !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # =============================================================================
# # TRANSLATIONS
# # =============================================================================

# T = {
#     "en": {
#         "app_title": "ArogyaBridge — Bridge to Healthcare",
#         "role": "Select your role",
#         "asha": "ASHA / ANM Worker",
#         "doctor": "Doctor / Facility Dashboard",
#         "admin": "District Admin Dashboard",
#         "medicine": "Medicine Stock Checker",
#         "patient_portal": "Patient Portal",
#         "register_patient": "Register New Patient",
#         "name": "Full Name",
#         "age": "Age",
#         "gender": "Gender",
#         "village": "Village / Ward",
#         "phone": "Phone Number",
#         "language": "Preferred Language",
#         "register_btn": "Register Patient (Generate ABHA-linked ID)",
#         "symptoms": "Describe symptoms",
#         "run_triage": "Run AI Triage",
#         "priority": "Priority",
#         "refer_btn": "Refer to Facility",
#         "select_facility": "Refer to which facility?",
#         "queue": "Live Patient Queue",
#         "no_referrals": "No referrals in queue yet.",
#         "prescription": "Prescription",
#         "save_prescription": "Save Prescription & Complete Referral",
#         "teleconsult": "Start Teleconsultation (WebRTC)",
#         "login": "Login",
#         "register_tab": "Register",
#         "login_btn": "Login",
#         "confirm_password": "Confirm Password",
#         "password": "Password",
#         "invalid_login": "Invalid phone number or password.",
#         "welcome_back": "Welcome back",
#         "my_health_record": "My Health Record",
#         "my_triage_history": "My Symptom / Triage History",
#         "my_referrals": "My Referrals & Prescriptions",
#         "book_appointment": "Book Appointment",
#         "sos": "Emergency SOS",
#         "logout": "Logout",
#         "no_records_yet": "No records yet.",
#         "create_login": "Create app login",
#         "phone_login_hint": "Use your registered phone number to log in.",
#         "acknowledge_btn": "✅ Acknowledge Patient Arrival",
#         "awaiting_arrival": "Awaiting patient arrival at this facility.",
#         "acknowledged_on": "Arrival acknowledged on",
#         "acknowledged_by": "Acknowledged by",
#         "doctor_name_label": "Your name (Doctor / Facility Staff)",
#         "offline_mode": "Simulate Offline Mode (ASHA)",
#         "pending_sync": "Pending Sync Queue",
#         "sync_now": "➡ Sync Now",
#         "synced_msg": "Synced {n} record(s) to the central server.",
#         "saved_offline": "Saved locally (offline) — will sync when connectivity returns.",
#         "status_pending": "PENDING (awaiting arrival)",
#         "status_ack": "ACKNOWLEDGED (patient arrived)",
#         "status_completed": "COMPLETED",
#         "referral_funnel": "Referral Funnel (Closed-Loop Tracking)",
#         "vitals_section": "Vitals (optional, improves triage accuracy)",
#         "temp_label": "Temperature (°F)",
#         "spo2_label": "SpO2 (%)",
#         "pulse_label": "Pulse (bpm)",
#         "bp_sys_label": "BP Systolic",
#         "bp_dia_label": "BP Diastolic",
#         "vitals_hint": "Leave a field at 0 if not measured.",
#         "trigger_sos": "🚨 Trigger Emergency SOS for this Patient",
#         "sos_logged": "🚨 Emergency SOS logged — visible on the District Admin Dashboard.",
#         "resolve": "Mark Resolved",
#         "active_alerts": "🚨 Active Emergency Alerts",
#         "no_active_alerts": "No active emergency alerts.",
#         "outbreak": "📈 Village Outbreak Signals",
#         "no_outbreak": "No outbreak clusters detected in the selected window.",
#         "turnaround": "Referral Turnaround Time (Closed-Loop Efficiency)",
#         "download_csv": "⬇ Download CSV",
#         "download_prescription": "Download Prescription",
#         "pin_unlock": "Unlock",
#         "pin_label": "Enter PIN",
#         "pin_wrong": "Incorrect PIN — please try again.",
#         "pin_hint": "Demo access control",
#         "search_patient": "Search by patient name",
#     },
#     "hi": {
#         "app_title": "ArogyaBridge — स्वास्थ्य सेवा का पुल",
#         "role": "अपनी भूमिका चुनें",
#         "asha": "आशा / एएनएम कार्यकर्ता",
#         "doctor": "डॉक्टर / सुविधा डैशबोर्ड",
#         "admin": "जिला प्रशासन डैशबोर्ड",
#         "medicine": "दवा स्टॉक जांच",
#         "patient_portal": "रोगी पोर्टल",
#         "register_patient": "नया रोगी पंजीकृत करें",
#         "name": "पूरा नाम",
#         "age": "आयु",
#         "gender": "लिंग",
#         "village": "गांव / वार्ड",
#         "phone": "फ़ोन नंबर",
#         "language": "पसंदीदा भाषा",
#         "register_btn": "रोगी पंजीकृत करें (ABHA ID बनाएं)",
#         "symptoms": "लक्षण बताएं",
#         "run_triage": "AI ट्राएज चलाएं",
#         "priority": "प्राथमिकता",
#         "refer_btn": "सुविधा के लिए रेफर करें",
#         "select_facility": "किस सुविधा के लिए रेफर करें?",
#         "queue": "लाइव रोगी कतार",
#         "no_referrals": "कतार में अभी कोई रेफरल नहीं।",
#         "prescription": "नुस्खा",
#         "save_prescription": "नुस्खा सहेजें और रेफरल पूरा करें",
#         "login": "लॉगिन",
#         "register_tab": "पंजीकरण",
#         "login_btn": "लॉगिन करें",
#         "confirm_password": "पासवर्ड की पुष्टि करें",
#         "password": "पासवर्ड",
#         "invalid_login": "फ़ोन नंबर या पासवर्ड गलत है।",
#         "welcome_back": "वापसी पर स्वागत है",
#         "my_health_record": "मेरा स्वास्थ्य रिकॉर्ड",
#         "my_triage_history": "मेरा लक्षण / ट्राएज इतिहास",
#         "my_referrals": "मेरे रेफरल और नुस्खे",
#         "book_appointment": "अपॉइंटमेंट बुक करें",
#         "sos": "आपातकालीन SOS",
#         "logout": "लॉगआउट",
#         "no_records_yet": "अभी तक कोई रिकॉर्ड नहीं।",
#         "create_login": "ऐप लॉगिन बनाएं",
#         "phone_login_hint": "लॉगिन करने के लिए अपना पंजीकृत फ़ोन नंबर उपयोग करें।",
#     },
#     "mr": {
#         "app_title": "ArogyaBridge — आरोग्यसेवेचा पूल",
#         "role": "तुमची भूमिका निवडा",
#         "asha": "आशा / एएनएम कार्यकर्ता",
#         "doctor": "डॉक्टर / सुविधा डॅशबोर्ड",
#         "admin": "जिल्हा प्रशासन डॅशबोर्ड",
#         "medicine": "औषध साठा तपासणी",
#         "patient_portal": "रुग्ण पोर्टल",
#         "register_patient": "नवीन रुग्ण नोंदणी",
#         "name": "पूर्ण नाव",
#         "age": "वय",
#         "gender": "लिंग",
#         "village": "गाव / वॉर्ड",
#         "phone": "फोन नंबर",
#         "language": "पसंतीची भाषा",
#         "register_btn": "रुग्ण नोंदणी करा (ABHA ID तयार करा)",
#         "symptoms": "लक्षणे सांगा",
#         "run_triage": "AI ट्रायेज चालवा",
#         "priority": "प्राधान्य",
#         "refer_btn": "सुविधेकडे संदर्भित करा",
#         "select_facility": "कोणत्या सुविधेकडे संदर्भित करायचे?",
#         "queue": "थेट रुग्ण रांग",
#         "no_referrals": "रांगेत अद्याप कोणतेही संदर्भ नाहीत.",
#         "prescription": "प्रिस्क्रिप्शन",
#         "save_prescription": "प्रिस्क्रिप्शन जतन करा आणि संदर्भ पूर्ण करा",
#         "login": "लॉगिन",
#         "register_tab": "नोंदणी",
#         "login_btn": "लॉगिन करा",
#         "confirm_password": "पासवर्डची पुष्टी करा",
#         "password": "पासवर्ड",
#         "invalid_login": "फोन नंबर किंवा पासवर्ड चुकीचा आहे.",
#         "welcome_back": "पुन्हा स्वागत आहे",
#         "my_health_record": "माझा आरोग्य रेकॉर्ड",
#         "my_triage_history": "माझा लक्षण / ट्रायेज इतिहास",
#         "my_referrals": "माझे संदर्भ आणि प्रिस्क्रिप्शन",
#         "book_appointment": "अपॉइंटमेंट बुक करा",
#         "sos": "आपत्कालीन SOS",
#         "logout": "लॉगआउट",
#                 "no_records_yet": "अद्याप कोणतेही रेकॉर्ड नाही.",
#         "create_login": "अॅप लॉगिन तयार करा",
#         "phone_login_hint": "लॉगिनसाठी नोंदणीकृत फोन नंबर वापरा.",
#     },
#     "ta": {
#         "app_title": "ArogyaBridge — சுகாதார சேவைக்கான பாலம்",
#         "role": "உங்கள் பாத்திரத்தைத் தேர்ந்தெடுக்கவும்",
#         "asha": "ஆஷா / ஏஎன்எம் பணியாளர்",
#         "doctor": "மருத்துவர் / மையம் டாஷ்போர்டு",
#         "admin": "மாவட்ட நிர்வாக டாஷ்போர்டு",
#         "medicine": "மருந்து கையிருப்பு சரிபார்ப்பு",
#         "patient_portal": "நோயாளர் போர்ட்டல்",
#         "register_patient": "புதிய நோயாளியைப் பதிவு செய்யவும்",
#         "name": "முழுப் பெயர்", "age": "வயது", "gender": "பாலினம்",
#         "village": "கிராமம் / வார்டு", "phone": "தொலைபேசி எண்",
#         "language": "விருப்பமான மொழி",
#         "symptoms": "அறிகுறிகளை விவரிக்கவும்",
#         "run_triage": "AI ட்ரையேஜ் இயக்கவும்", "priority": "முன்னுரிமை",
#         "queue": "நேரடி நோயாளர் வரிசை", "sos": "அவசர SOS",
#     },
#     "te": {
#         "app_title": "ArogyaBridge — ఆరోగ్య సేవకు వంతెన",
#         "role": "మీ పాత్రను ఎంచుకోండి",
#         "asha": "ఆశా / ఏఎన్ఎం కార్యకర్త",
#         "doctor": "డాక్టర్ / సదుపాయ డాష్‌బోర్డ్",
#         "admin": "జిల్లా అడ్మిన్ డాష్‌బోర్డ్",
#         "medicine": "మందుల నిల్వ తనిఖీ",
#         "patient_portal": "రోగి పోర్టల్",
#         "register_patient": "కొత్త రోగిని నమోదు చేయండి",
#         "name": "పూర్తి పేరు", "age": "వయస్సు", "gender": "లింగం",
#         "village": "గ్రామం / వార్డు", "phone": "ఫోన్ నంబర్",
#         "language": "ఇష్టమైన భాష",
#         "symptoms": "లక్షణాలను వివరించండి",
#         "run_triage": "AI ట్రయాజ్ నడపండి", "priority": "ప్రాధాన్యత",
#         "queue": "ప్రత్యక్ష రోగుల క్యూ", "sos": "అత్యవసర SOS",
#     },
#     "bn": {
#         "app_title": "ArogyaBridge — স্বাস্থ্যসেবার সেতু",
#         "role": "আপনার ভূমিকা নির্বাচন করুন",
#         "asha": "আশা / এএনএম কর্মী",
#         "doctor": "ডাক্তার / সুবিধা ড্যাশবোর্ড",
#         "admin": "জেলা প্রশাসন ড্যাশবোর্ড",
#         "medicine": "ওষুধ স্টক পরীক্ষা",
#         "patient_portal": "রোগী পোর্টাল",
#         "register_patient": "নতুন রোগী নিবন্ধন করুন",
#         "name": "পুরো নাম", "age": "বয়স", "gender": "লিঙ্গ",
#         "village": "গ্রাম / ওয়ার্ড", "phone": "ফোন নম্বর",
#         "language": "পছন্দের ভাষা",
#         "symptoms": "লক্ষণ বর্ণনা করুন",
#         "run_triage": "AI ট্রায়াজ চালান", "priority": "অগ্রাধিকার",
#         "queue": "লাইভ রোগীর সারি", "sos": "জরুরি SOS",
#     },
# }


# def tr(key: str) -> str:
#     lang = st.session_state.get("ui_lang", "en")
#     return T.get(lang, T["en"]).get(key, T["en"].get(key, key))


# # =============================================================================
# # DATABASE
# # =============================================================================

# def get_conn():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     conn = get_conn()
#     cur = conn.cursor()

#     cur.executescript(
#         """
#         CREATE TABLE IF NOT EXISTS patients (
#             abha_id TEXT PRIMARY KEY,
#             name TEXT NOT NULL,
#             age INTEGER,
#             gender TEXT,
#             village TEXT,
#             phone TEXT,
#             language TEXT,
#             created_at TEXT,
#             password_hash TEXT,
#             salt TEXT,
#             created_by TEXT
#         );

#         CREATE TABLE IF NOT EXISTS triage (
#             id TEXT PRIMARY KEY,
#             abha_id TEXT NOT NULL,
#             symptoms_text TEXT,
#             priority TEXT,
#             rationale TEXT,
#             created_by TEXT,
#             created_at TEXT
#         );

#         CREATE TABLE IF NOT EXISTS referrals (
#             id TEXT PRIMARY KEY,
#             abha_id TEXT NOT NULL,
#             triage_id TEXT NOT NULL,
#             facility TEXT,
#             status TEXT,
#             prescription TEXT,
#             doctor_notes TEXT,
#             created_at TEXT,
#             acknowledged_at TEXT,
#             acknowledged_by TEXT,
#             completed_at TEXT
#         );

#         CREATE TABLE IF NOT EXISTS medicine_stock (
#             id TEXT PRIMARY KEY,
#             facility TEXT,
#             medicine_name TEXT,
#             quantity INTEGER,
#             unit TEXT,
#             last_updated TEXT
#         );

#         CREATE TABLE IF NOT EXISTS emergency_alerts (
#             id TEXT PRIMARY KEY,
#             abha_id TEXT,
#             patient_name TEXT,
#             village TEXT,
#             triggered_by TEXT,
#             status TEXT,
#             created_at TEXT,
#             resolved_at TEXT
#         );

#         CREATE TABLE IF NOT EXISTS appointments (
#             id TEXT PRIMARY KEY,
#             abha_id TEXT,
#             facility TEXT,
#             appointment_date TEXT,
#             slot TEXT,
#             reason TEXT,
#             status TEXT,
#             created_at TEXT
#         );

#         CREATE TABLE IF NOT EXISTS diagnostics (
#             id TEXT PRIMARY KEY,
#             abha_id TEXT,
#             referral_id TEXT,
#             facility TEXT,
#             test_name TEXT,
#             status TEXT,
#             ordered_at TEXT,
#             result_notes TEXT
#         );

#         CREATE TABLE IF NOT EXISTS notifications (
#             id TEXT PRIMARY KEY,
#             role TEXT,
#             message TEXT,
#             is_read INTEGER DEFAULT 0,
#             created_at TEXT
#         );
#         """
#     )

#     # -------------------------------------------------------------------------
#     # Safe migrations
#     # -------------------------------------------------------------------------

#     patient_columns = {
#         row[1]
#         for row in cur.execute("PRAGMA table_info(patients)").fetchall()
#     }

#     if "password_hash" not in patient_columns:
#         cur.execute("ALTER TABLE patients ADD COLUMN password_hash TEXT")

#     if "salt" not in patient_columns:
#         cur.execute("ALTER TABLE patients ADD COLUMN salt TEXT")

#     if "created_by" not in patient_columns:
#         cur.execute("ALTER TABLE patients ADD COLUMN created_by TEXT")

#     referral_columns = {
#         row[1]
#         for row in cur.execute("PRAGMA table_info(referrals)").fetchall()
#     }

#     if "acknowledged_at" not in referral_columns:
#         cur.execute("ALTER TABLE referrals ADD COLUMN acknowledged_at TEXT")

#     if "acknowledged_by" not in referral_columns:
#         cur.execute("ALTER TABLE referrals ADD COLUMN acknowledged_by TEXT")

#     if "completed_at" not in referral_columns:
#         cur.execute("ALTER TABLE referrals ADD COLUMN completed_at TEXT")

#     # -------------------------------------------------------------------------
#     # Seed medicine inventory
#     # -------------------------------------------------------------------------

#     medicine_count = cur.execute(
#         "SELECT COUNT(*) FROM medicine_stock"
#     ).fetchone()[0]

#     if medicine_count == 0:
#         medicines = [
#             ("Paracetamol 500mg", "tablets", 40),
#             ("ORS Sachets", "sachets", 5),
#             ("Iron Folic Acid", "tablets", 120),
#             ("Amoxicillin 250mg", "capsules", 8),
#             ("Insulin (Regular)", "vials", 15),
#             ("ASHA Kit - BP Monitor", "units", 3),
#             ("Antenatal Vitamin D", "tablets", 60),
#         ]

#         now = datetime.now().isoformat()

#         for facility in FACILITIES:
#             for medicine, unit, quantity in medicines:
#                 quantity = max(0, quantity + random.randint(-5, 10))

#                 cur.execute(
#                     """
#                     INSERT INTO medicine_stock
#                     (id, facility, medicine_name, quantity, unit, last_updated)
#                     VALUES (?, ?, ?, ?, ?, ?)
#                     """,
#                     (
#                         str(uuid.uuid4()),
#                         facility,
#                         medicine,
#                         quantity,
#                         unit,
#                         now,
#                     ),
#                 )

#     conn.commit()
#     conn.close()


# def df(query, params=()):
#     conn = get_conn()
#     try:
#         return pd.read_sql_query(query, conn, params=params)
#     finally:
#         conn.close()


# # =============================================================================
# # PASSWORD HELPERS
# # =============================================================================

# def hash_password(password: str, salt: str | None = None):
#     if salt is None:
#         salt = secrets.token_hex(16)

#     password_hash = hashlib.pbkdf2_hmac(
#         "sha256",
#         password.encode("utf-8"),
#         salt.encode("utf-8"),
#         100_000,
#     ).hex()

#     return password_hash, salt


# def verify_password(password: str, salt: str, stored_hash: str) -> bool:
#     if not salt or not stored_hash:
#         return False

#     test_hash, _ = hash_password(password, salt)

#     return secrets.compare_digest(
#         test_hash,
#         stored_hash,
#     )
# def _get_cipher():
#     """Returns a Fernet cipher if `cryptography` is installed, else None
#     (fields fall back to plain text — fine for a hackathon demo, but a real
#     deployment should `pip install cryptography`)."""
#     try:
#         from cryptography.fernet import Fernet
#         key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".demo_key")
#         if os.path.exists(key_path):
#             key = open(key_path, "rb").read()
#         else:
#             key = Fernet.generate_key()
#             with open(key_path, "wb") as f:
#                 f.write(key)
#         return Fernet(key)
#     except Exception:
#         return None


# def encrypt_field(value: str) -> str:
#     cipher = _get_cipher()
#     if cipher and value:
#         return "ENC::" + cipher.encrypt(value.encode()).decode()
#     return value or ""


# def decrypt_field(value: str) -> str:
#     if value and str(value).startswith("ENC::"):
#         cipher = _get_cipher()
#         if cipher:
#             try:
#                 return cipher.decrypt(value[5:].encode()).decode()
#             except Exception:
#                 return "(decryption error)"
#     return value or ""


# # =============================================================================
# # ID / UI HELPERS
# # =============================================================================

# def gen_abha_id():
#     return "ABHA-" + uuid.uuid4().hex[:8].upper()


# def priority_badge(priority: str):
#     color = PRIORITY_COLORS.get(priority, "#777")

#     return (
#         f"<span style='background:{color};"
#         "color:white;padding:4px 10px;border-radius:14px;"
#         "font-weight:700;font-size:0.85em'>"
#         f"{priority}</span>"
#     )
# def render_triage_legend():
#     st.markdown(
#         """
#         <div style="display:flex; gap:10px; margin:6px 0 18px 0; flex-wrap:wrap;">
#             <span style="background:#e53935;color:#fff;padding:5px 14px;border-radius:14px;font-weight:700;font-size:0.85em;">🔴 RED — Emergency, refer immediately</span>
#             <span style="background:#fbc02d;color:#2B2621;padding:5px 14px;border-radius:14px;font-weight:700;font-size:0.85em;">🟡 YELLOW — Facility follow-up needed</span>
#             <span style="background:#43a047;color:#fff;padding:5px 14px;border-radius:14px;font-weight:700;font-size:0.85em;">🟢 GREEN — Routine care, ASHA can manage</span>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# def status_badge(status: str):
#     color = STATUS_COLORS.get(status, "#777")

#     return (
#         f"<span style='background:{color};"
#         "color:white;padding:4px 10px;border-radius:14px;"
#         "font-weight:700;font-size:0.85em'>"
#         f"{status}</span>"
#     )


# def maybe_render_qr(data: str, caption: str = ""):
#     try:
#         import io
#         import qrcode

#         image = qrcode.make(data)
#         buffer = io.BytesIO()
#         image.save(buffer, format="PNG")

#         st.image(
#             buffer.getvalue(),
#             caption=caption,
#             width=160,
#         )
#     except ImportError:
#         st.caption("Install `qrcode` to display QR codes.")


# # =============================================================================
# # NOTIFICATIONS
# # =============================================================================

# def notify(role: str, message: str):
#     conn = get_conn()

#     conn.execute(
#         """
#         INSERT INTO notifications
#         (id, role, message, is_read, created_at)
#         VALUES (?, ?, ?, 0, ?)
#         """,
#         (
#             str(uuid.uuid4()),
#             role,
#             message,
#             datetime.now().isoformat(),
#         ),
#     )

#     conn.commit()
#     conn.close()


# def unread_count(role: str):
#     result = df(
#         """
#         SELECT COUNT(*) AS n
#         FROM notifications
#         WHERE role = ? AND is_read = 0
#         """,
#         (role,),
#     )

#     return int(result.iloc[0]["n"])


# def mark_all_read(role: str):
#     conn = get_conn()

#     conn.execute(
#         """
#         UPDATE notifications
#         SET is_read = 1
#         WHERE role = ? AND is_read = 0
#         """,
#         (role,),
#     )

#     conn.commit()
#     conn.close()


# # =============================================================================
# # AI TRIAGE
# # =============================================================================

# RED_FLAGS = [
#     "chest pain",
#     "severe bleeding",
#     "unconscious",
#     "seizure",
#     "not breathing",
#     "difficulty breathing",
#     "breathlessness",
#     "convulsion",
#     "high fever infant",
#     "severe abdominal pain",
#     "stroke",
#     "paralysis",
#     "blue lips",
#     "सीने में दर्द",
#     "बेहोश",
#     "दौरा",
#     "सांस लेने में तकलीफ",
#     "सांस लेने में परेशानी",
#     "तेज़ बुखार शिशु",
#     "अत्यधिक रक्तस्राव",
#     "लकवा",
# ]

# YELLOW_FLAGS = [
#     "fever",
#     "vomiting",
#     "diarrhea",
#     "dehydration",
#     "moderate pain",
#     "pregnancy bleeding",
#     "high blood pressure",
#     "persistent cough",
#     "बुखार",
#     "उल्टी",
#     "दस्त",
#     "डिहाइड्रेशन",
#     "गर्भावस्था रक्तस्राव",
#     "उच्च रक्तचाप",
#     "लगातार खांसी",
# ]


# def rule_based_triage(symptoms_text: str):
#     text = symptoms_text.lower().strip()

#     for flag in RED_FLAGS:
#         if flag.lower() in text:
#             return (
#                 "RED",
#                 f"Red-flag symptom detected: '{flag}'. Immediate escalation is recommended.",
#             )

#     for flag in YELLOW_FLAGS:
#         if flag.lower() in text:
#             return (
#                 "YELLOW",
#                 f"Moderate-risk symptom detected: '{flag}'. Facility follow-up is recommended.",
#             )

#     return (
#         "GREEN",
#         "No high-risk keywords detected. Routine care advised.",
#     )


# def worse_priority(a: str, b: str):
#     return a if PRIORITY_ORDER[a] <= PRIORITY_ORDER[b] else b


# def vitals_risk(
#     temp_f=0.0,
#     spo2=0,
#     pulse=0,
#     bp_sys=0,
#     bp_dia=0,
# ):
#     priority = "GREEN"
#     reasons = []

#     if spo2 and spo2 < 90:
#         priority = "RED"
#         reasons.append(f"Critically low SpO2 ({spo2}%)")

#     elif spo2 and spo2 < 94:
#         priority = worse_priority(priority, "YELLOW")
#         reasons.append(f"Borderline SpO2 ({spo2}%)")

#     if temp_f and temp_f >= 104:
#         priority = "RED"
#         reasons.append(f"High temperature ({temp_f}°F)")

#     elif temp_f and temp_f >= 100.4:
#         priority = worse_priority(priority, "YELLOW")
#         reasons.append(f"Fever ({temp_f}°F)")

#     if bp_sys and (bp_sys >= 180 or bp_sys <= 90):
#         priority = "RED"
#         reasons.append(
#             f"Critical BP ({bp_sys}/{bp_dia or '?'} mmHg)"
#         )

#     elif bp_sys and bp_sys >= 140:
#         priority = worse_priority(priority, "YELLOW")
#         reasons.append(
#             f"Elevated BP ({bp_sys}/{bp_dia or '?'} mmHg)"
#         )

#     if pulse and (pulse >= 130 or pulse <= 45):
#         priority = "RED"
#         reasons.append(f"Abnormal pulse ({pulse} bpm)")

#     return priority, reasons


# def groq_triage(symptoms_text: str):
#     if not GROQ_API_KEY:
#         return None

#     try:
#         from groq import Groq

#         client = Groq(api_key=GROQ_API_KEY)

#         prompt = f"""
# You are a clinical triage assistant supporting a rural Indian ASHA worker.

# Classify symptoms into exactly one of:
# RED, YELLOW, GREEN

# RED = emergency / immediate escalation
# YELLOW = needs facility assessment soon
# GREEN = routine care

# Symptoms may be in Hindi or English.

# Return ONLY:
# PRIORITY|one sentence rationale

# Symptoms:
# {symptoms_text}
# """

#         response = client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt,
#                 }
#             ],
#             max_tokens=100,
#             temperature=0.2,
#         )

#         output = response.choices[0].message.content.strip()

#         if "|" not in output:
#             return None

#         priority, rationale = output.split("|", 1)

#         priority = priority.strip().upper()
#         rationale = rationale.strip()

#         if priority not in PRIORITY_ORDER:
#             return None

#         return priority, rationale

#     except Exception:
#         return None


# def run_triage(symptoms_text: str, vitals: dict | None = None):
#     ai_result = groq_triage(symptoms_text)

#     if ai_result:
#         symptom_priority, symptom_rationale = ai_result
#     else:
#         symptom_priority, symptom_rationale = rule_based_triage(
#             symptoms_text
#         )

#     if not vitals:
#         return symptom_priority, symptom_rationale

#     vital_priority, vital_reasons = vitals_risk(**vitals)

#     final_priority = worse_priority(
#         symptom_priority,
#         vital_priority,
#     )

#     rationale = symptom_rationale

#     if vital_reasons:
#         rationale += " | Vitals flags: " + "; ".join(vital_reasons)

#     return final_priority, rationale


# # =============================================================================
# # PATIENT TIMELINE
# # =============================================================================

# def get_patient_timeline(abha_id: str):
#     events = []

#     def add_event(dt, kind, color, detail):
#         if dt:
#             events.append(
#                 {
#                     "date": dt,
#                     "kind": kind,
#                     "color": color,
#                     "detail": detail,
#                 }
#             )

#     # Registration
#     registration = df(
#         """
#         SELECT created_at
#         FROM patients
#         WHERE abha_id = ?
#         """,
#         (abha_id,),
#     )

#     if not registration.empty:
#         add_event(
#             registration.iloc[0]["created_at"],
#             "REGISTERED",
#             "#1e88e5",
#             "Patient registered — ABHA-linked ID issued",
#         )

#     # Triage
#     # Triage
#     triages = df(
#         """
#         SELECT symptoms_text, priority, rationale, created_at, created_by
#         FROM triage
#         WHERE abha_id = ?
#         ORDER BY created_at
#         """,
#         (abha_id,),
#     )

#     for _, row in triages.iterrows():
#         detail = f"{row['symptoms_text']} (by {row['created_by']})"
#         if row.get("rationale"):
#             detail += f" — AI note: {row['rationale']}"
#         add_event(
#             row["created_at"],
#             f"TRIAGE: {row['priority']}",
#             PRIORITY_COLORS.get(row["priority"], "#777"),
#             detail,
#         )

#     # SOS
#     alerts = df(
#         """
#         SELECT created_at, triggered_by, status
#         FROM emergency_alerts
#         WHERE abha_id = ?
#         ORDER BY created_at
#         """,
#         (abha_id,),
#     )

#     for _, row in alerts.iterrows():
#         add_event(
#             row["created_at"],
#             f"SOS ALERT ({row['status']})",
#             "#e53935",
#             f"Triggered by {row['triggered_by']}",
#         )

#     # Referrals
#     referrals = df(
#         """
#         SELECT
#             created_at,
#             acknowledged_at,
#             completed_at,
#             facility,
#             status,
#             prescription
#         FROM referrals
#         WHERE abha_id = ?
#         ORDER BY created_at
#         """,
#         (abha_id,),
#     )

#     for _, row in referrals.iterrows():
#         add_event(
#             row["created_at"],
#             f"REFERRAL → {row['facility']}",
#             "#fb8c00",
#             f"Referral created — {row['status']}",
#         )

#         if row["acknowledged_at"]:
#             add_event(
#                 row["acknowledged_at"],
#                 "ARRIVAL ACKNOWLEDGED",
#                 "#1e88e5",
#                 f"Patient arrived at {row['facility']}",
#             )

#         if row["completed_at"]:
#             detail = "Prescription issued"

#             if row["prescription"]:
#                 detail += f" — {row['prescription']}"

#             add_event(
#                 row["completed_at"],
#                 "REFERRAL COMPLETED",
#                 "#43a047",
#                 detail,
#             )

#     # Diagnostics
#     diagnostics = df(
#         """
#         SELECT ordered_at, test_name, status
#         FROM diagnostics
#         WHERE abha_id = ?
#         ORDER BY ordered_at
#         """,
#         (abha_id,),
#     )

#     for _, row in diagnostics.iterrows():
#         add_event(
#             row["ordered_at"],
#             f"DIAGNOSTIC: {row['test_name']}",
#             "#8e24aa",
#             f"Status: {row['status']}",
#         )

#     events.sort(
#         key=lambda x: x["date"],
#         reverse=True,
#     )

#     return events


# # =============================================================================
# # SYMPTOM TRENDS
# # =============================================================================

# def symptom_trends(top_n=10):
#     stopwords = {
#         "the",
#         "and",
#         "with",
#         "from",
#         "that",
#         "this",
#         "have",
#         "has",
#         "had",
#         "been",
#         "very",
#         "mild",
#         "moderate",
#         "severe",
#         "days",
#         "day",
#         "since",
#         "after",
#         "before",
#         "also",
#         "today",
#         "there",
#         "feeling",
#         "feels",
#         "gets",
#         "getting",
#     }

#     texts = df(
#         """
#         SELECT symptoms_text
#         FROM triage
#         ORDER BY created_at DESC
#         LIMIT 300
#         """
#     )

#     counts = Counter()

#     if texts.empty:
#         return []

#     for text in texts["symptoms_text"].dropna():
#         words = re.findall(
#             r"[a-zA-Z']+",
#             str(text).lower(),
#         )

#         for word in words:
#             if len(word) > 3 and word not in stopwords:
#                 counts[word] += 1

#     return counts.most_common(top_n)


# # =============================================================================
# # DEMO DATA
# # =============================================================================

# def seed_demo_data():
#     conn = get_conn()
#     cur = conn.cursor()

#     existing = cur.execute(
#         "SELECT COUNT(*) FROM patients"
#     ).fetchone()[0]

#     if existing > 0:
#         conn.close()
#         return False

#     now = datetime.now()

#     def ago(**kwargs):
#         return (
#             now - timedelta(**kwargs)
#         ).isoformat()

#     asha_names = [
#         "ASHA Kavita",
#         "ASHA Shraddha",
#         "ANM Priya",
#     ]

#     people = [
#         (
#             "Sunita Pawar",
#             34,
#             "Female",
#             "Wagholi",
#             "9876501234",
#             "Marathi",
#         ),
#         (
#             "Rahul Jadhav",
#             45,
#             "Male",
#             "Ranjangaon",
#             "9876505678",
#             "Hindi",
#         ),
#         (
#             "Geeta Patil",
#             27,
#             "Female",
#             "Wagholi",
#             "9876509012",
#             "Marathi",
#         ),
#         (
#             "Imran Sheik",
#             60,
#             "Male",
#             "Shirval",
#             "9876503456",
#             "Urdu",
#         ),
#         (
#             "Meena Mandale",
#             52,
#             "Female",
#             "Lalgaon",
#             "9876507890",
#             "Marathi",
#         ),
#         (
#             "Vikram Solu",
#             8,
#             "Male",
#             "Shirval",
#             "9876502345",
#             "Hindi",
#         ),
#         (
#             "Aarti Kuwar",
#             22,
#             "Female",
#             "Chaki",
#             "9876508901",
#             "Hindi",
#         ),
#     ]

#     abha_map = {}

#     for i, person in enumerate(people):
#         name, age, gender, village, phone, language = person

#         abha_id = gen_abha_id()
#         abha_map[i] = abha_id

#         cur.execute(
#             """
#             INSERT INTO patients
#             (
#                 abha_id,
#                 name,
#                 age,
#                 gender,
#                 village,
#                 phone,
#                 language,
#                 created_at,
#                 password_hash,
#                 salt,
#                 created_by
#             )
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 abha_id,
#                 name,
#                 age,
#                 gender,
#                 village,
#                 phone,
#                 language,
#                 ago(hours=30 - i * 3),
#                 None,
#                 None,
#                 asha_names[i % len(asha_names)],
#             ),
#         )

#     # -------------------------------------------------------------------------
#     # Triage + referrals
#     # -------------------------------------------------------------------------

#     triage_rows = [
#         (
#             0,
#             "High fever for 3 days with cough and body ache",
#             "YELLOW",
#             "Fever detected. Needs facility follow-up.",
#             "PHC Ranjangaon",
#             "ACKNOWLEDGED",
#             3,
#             2,
#             None,
#             "Dr. Neha (PHC)",
#         ),
#         (
#             1,
#             "Breathlessness and chest pain since morning",
#             "RED",
#             "Breathlessness and chest pain require immediate escalation.",
#             "District Hospital Pune",
#             "COMPLETED",
#             26,
#             24,
#             22,
#             "Dr. Anil (DH)",
#         ),
#         (
#             2,
#             "Vomiting and diarrhea, feels dehydrated",
#             "YELLOW",
#             "Vomiting and diarrhea with dehydration risk.",
#             "PHC Ranjangaon",
#             "COMPLETED",
#             20,
#             19,
#             18,
#             "Dr. Neha (PHC)",
#         ),
#         (
#             4,
#             "Frequent urination, fatigue and dizziness",
#             "YELLOW",
#             "Needs Hb and diabetes evaluation.",
#             "Sub-Centre Wagholi",
#             "COMPLETED",
#             15,
#             14,
#             13,
#             "Dr. Kavita (SCW)",
#         ),
#         (
#             5,
#             "Mild fever and headache, no other complaints",
#             "GREEN",
#             "No high-risk symptoms detected.",
#             None,
#             None,
#             12,
#             None,
#             None,
#             None,
#         ),
#         (
#             3,
#             "Unconscious for a few minutes after a seizure",
#             "RED",
#             "Unconsciousness and seizure require emergency escalation.",
#             "District Hospital Pune",
#             "PENDING",
#             1,
#             None,
#             None,
#             None,
#         ),
#         (
#             6,
#             "Skin rashes and itching after changing feed",
#             "GREEN",
#             "No high-risk symptoms detected.",
#             None,
#             None,
#             6,
#             None,
#             None,
#             None,
#         ),
#     ]

#     for (
#         index,
#         symptoms,
#         priority,
#         rationale,
#         facility,
#         status,
#         created_hours,
#         ack_hours,
#         completed_hours,
#         doctor,
#     ) in triage_rows:

#         triage_id = str(uuid.uuid4())

#         cur.execute(
#             """
#             INSERT INTO triage
#             (
#                 id,
#                 abha_id,
#                 symptoms_text,
#                 priority,
#                 rationale,
#                 created_by,
#                 created_at
#             )
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 triage_id,
#                 abha_map[index],
#                 symptoms,
#                 priority,
#                 rationale,
#                 asha_names[index % len(asha_names)],
#                 ago(hours=created_hours),
#             ),
#         )

#         if facility and status:

#             referral_id = str(uuid.uuid4())

#             acknowledged_at = None
#             acknowledged_by = None
#             completed_at = None
#             prescription = ""
#             notes = ""

#             if ack_hours is not None:
#                 acknowledged_at = ago(hours=ack_hours)
#                 acknowledged_by = doctor or "Duty Doctor"

#             if completed_hours is not None:
#                 completed_at = ago(hours=completed_hours)

#                 prescriptions = {
#                     1: (
#                         "Amoxicillin 500mg BD x 5d\n"
#                         "Paracetamol 650mg SOS\n"
#                         "Salbutamol inhalation twice daily"
#                     ),
#                     2: (
#                         "ORS sachet as needed\n"
#                         "Domperidone 10mg TID x 3d\n"
#                         "Clear liquid diet"
#                     ),
#                     4: (
#                         "Hb test advised\n"
#                         "Iron + Folic Acid OD x 30d\n"
#                         "Diet counselling"
#                     ),
#                 }

#                 notes_map = {
#                     1: "Severe pneumonia suspected; admitted for observation.",
#                     2: "Acute gastroenteritis with mild dehydration.",
#                     4: "Suspected anemia; Hb follow-up scheduled.",
#                 }

#                 prescription = prescriptions.get(
#                     index,
#                     "Review after 3 days.",
#                 )

#                 notes = notes_map.get(index, "")

#             cur.execute(
#                 """
#                 INSERT INTO referrals
#                 (
#                     id,
#                     abha_id,
#                     triage_id,
#                     facility,
#                     status,
#                     prescription,
#                     doctor_notes,
#                     created_at,
#                     acknowledged_at,
#                     acknowledged_by,
#                     completed_at
#                 )
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 (
#                     referral_id,
#                     abha_map[index],
#                     triage_id,
#                     facility,
#                     status,
#                     prescription,
#                     notes,
#                     ago(hours=created_hours),
#                     acknowledged_at,
#                     acknowledged_by,
#                     completed_at,
#                 ),
#             )

#     # -------------------------------------------------------------------------
#     # SOS
#     # -------------------------------------------------------------------------

#     cur.execute(
#         """
#         INSERT INTO emergency_alerts
#         (
#             id,
#             abha_id,
#             patient_name,
#             village,
#             triggered_by,
#             status,
#             created_at,
#             resolved_at
#         )
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             str(uuid.uuid4()),
#             abha_map[3],
#             "Imran Sheik",
#             "Shirval",
#             "ASHA Kavita (RED triage)",
#             "ACTIVE",
#             ago(hours=1),
#             None,
#         ),
#     )

#     # -------------------------------------------------------------------------
#     # Appointments
#     # -------------------------------------------------------------------------

#     cur.execute(
#         """
#         INSERT INTO appointments
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             str(uuid.uuid4()),
#             abha_map[1],
#             "District Hospital Pune",
#             (date.today() + timedelta(days=1)).isoformat(),
#             "10:00-11:00",
#             "Fever follow-up",
#             "REQUESTED",
#             ago(hours=2),
#         ),
#     )

#     cur.execute(
#         """
#         INSERT INTO appointments
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             str(uuid.uuid4()),
#             abha_map[0],
#             "PHC Ranjangaon",
#             (date.today() + timedelta(days=2)).isoformat(),
#             "11:00-12:00",
#             "Ante-natal check-up",
#             "CONFIRMED",
#             ago(hours=8),
#         ),
#     )

#     # -------------------------------------------------------------------------
#     # Diagnostics
#     # -------------------------------------------------------------------------

#     diagnostic_examples = [
#         (
#             abha_map[1],
#             "District Hospital Pune",
#             "CBC",
#             "COMPLETED",
#         ),
#         (
#             abha_map[4],
#             "Sub-Centre Wagholi",
#             "Hb",
#             "ORDERED",
#         ),
#     ]

#     for patient_id, facility, test_name, status in diagnostic_examples:
#         referral = cur.execute(
#             """
#             SELECT id
#             FROM referrals
#             WHERE abha_id = ?
#             ORDER BY created_at DESC
#             LIMIT 1
#             """,
#             (patient_id,),
#         ).fetchone()

#         referral_id = referral["id"] if referral else None

#         cur.execute(
#             """
#             INSERT INTO diagnostics
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 str(uuid.uuid4()),
#                 patient_id,
#                 referral_id,
#                 facility,
#                 test_name,
#                 status,
#                 ago(hours=3),
#                 "Normal" if status == "COMPLETED" else None,
#             ),
#         )

#     # -------------------------------------------------------------------------
#     # Notifications
#     # -------------------------------------------------------------------------

#     notifications = [
#         (
#             "admin",
#             "🚨 Active SOS: Imran Sheik from Shirval.",
#         ),
#         (
#             "doctor",
#             "📅 New appointment request received.",
#         ),
#         (
#             "asha",
#             "💊 Referral completed and prescription issued.",
#         ),
#         (
#             "admin",
#             "📊 Diagnostics load updated.",
#         ),
#     ]

#     for role, message in notifications:
#         cur.execute(
#             """
#             INSERT INTO notifications
#             VALUES (?, ?, ?, 0, ?)
#             """,
#             (
#                 str(uuid.uuid4()),
#                 role,
#                 message,
#                 ago(hours=random.randint(1, 5)),
#             ),
#         )

#     conn.commit()
#     conn.close()

#     return True


# # =============================================================================
# # OFFLINE QUEUE
# # =============================================================================

# def queue_offline_record(record_type, values):
#     st.session_state.offline_queue.append(
#         {
#             "type": record_type,
#             "values": values,
#         }
#     )


# def get_offline_patient_options():
#     options = {}

#     for item in st.session_state.offline_queue:
#         if item["type"] != "patient":
#             continue

#         values = item["values"]

#         abha_id = values[0]
#         name = values[1]

#         options[
#             f"{name} ({abha_id}) [offline]"
#         ] = abha_id

#     return options


# def sync_offline_queue():
#     if not st.session_state.offline_queue:
#         return 0

#     conn = get_conn()
#     cur = conn.cursor()

#     synced = 0

#     for item in st.session_state.offline_queue:

#         record_type = item["type"]
#         values = item["values"]

#         if record_type == "patient":
#             offline_phone = values[5]
#             offline_created_at = values[7]

#             existing = cur.execute(
#                 "SELECT abha_id, created_at FROM patients WHERE phone = ? AND phone != ''",
#                 (offline_phone,),
#             ).fetchone()

#             if existing:
#                 # Smart timestamp-based conflict resolution: only overwrite
#                 # the existing record if the offline copy is actually newer
#                 # — protects against a stale offline queue clobbering a
#                 # record someone already updated on the server in the
#                 # meantime.
#                 try:
#                     is_newer = offline_created_at > existing["created_at"]
#                 except Exception:
#                     is_newer = False

#                 if is_newer:
#                     cur.execute(
#                         """
#                         UPDATE patients
#                         SET name=?, age=?, gender=?, village=?, language=?,
#                             created_at=?, created_by=?
#                         WHERE phone=?
#                         """,
#                         (
#                             values[1], values[2], values[3], values[4], values[6],
#                             offline_created_at, values[10], offline_phone,
#                         ),
#                     )
#             else:
#                 cur.execute(
#                     """
#                     INSERT OR IGNORE INTO patients
#                     (abha_id, name, age, gender, village, phone, language,
#                      created_at, password_hash, salt, created_by)
#                     VALUES (?,?,?,?,?,?,?,?,?,?,?)
#                     """,
#                     values,
#                 )

#             synced += 1

#         elif record_type == "triage":
#             cur.execute(
#                 """
#                 INSERT OR IGNORE INTO triage
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 values,
#             )

#             synced += 1

#         elif record_type == "referral":
#             cur.execute(
#                 """
#                 INSERT OR IGNORE INTO referrals
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 values,
#             )

#             synced += 1

#     conn.commit()
#     conn.close()

#     st.session_state.offline_queue = []

#     return synced


# # =============================================================================
# # PIN AUTH
# # =============================================================================

# def require_pin(role_key: str, role_label: str):
#     session_key = f"auth_{role_key}"

#     if st.session_state.get(session_key):
#         return True

#     st.info(
#         f"{tr('pin_hint')} for **{role_label}**. "
#         f"Demo PIN: **{DEMO_PINS[role_key]}**"
#     )

#     pin = st.text_input(
#         tr("pin_label"),
#         type="password",
#         key=f"pin_input_{role_key}",
#     )

#     if st.button(
#         tr("pin_unlock"),
#         key=f"pin_button_{role_key}",
#         type="primary",
#     ):
#         if secrets.compare_digest(
#             pin,
#             DEMO_PINS[role_key],
#         ):
#             st.session_state[session_key] = True
#             st.rerun()
#         else:
#             st.error(tr("pin_wrong"))

#     return False


# # =============================================================================
# # PRESCRIPTION
# # =============================================================================

# def build_prescription_text(
#     patient_name,
#     abha_id,
#     facility,
#     priority,
#     symptoms_text,
#     prescription,
#     doctor_notes,
#     doctor_name,
#     completed_at,
# ):
#     return "\n".join(
#         [
#             "=" * 50,
#             "       ArogyaBridge — Prescription Summary",
#             "=" * 50,
#             f"Patient Name : {patient_name}",
#             f"ABHA ID      : {abha_id}",
#             f"Facility     : {facility}",
#             f"Triage       : {priority}",
#             f"Symptoms     : {symptoms_text}",
#             "-" * 50,
#             "Prescription:",
#             prescription or "(none recorded)",
#             "-" * 50,
#             f"Doctor Notes : {doctor_notes or '(none)'}",
#             f"Attending Dr : {doctor_name or '(not recorded)'}",
#             f"Completed On : {completed_at or '(not recorded)'}",
#             "=" * 50,
#             "Generated by ArogyaBridge (SIH26133).",
#             "Demo prototype — not a legal medical document.",
#         ]
#     )

# def build_abdm_export(abha_id: str) -> str:
#     """Lightweight FHIR-inspired JSON export of a patient's record —
#     illustrates ABDM-ready structured interoperability. Not a certified
#     FHIR resource, but demonstrates the data-portability story for judges."""
#     patient = df("SELECT * FROM patients WHERE abha_id=?", (abha_id,))
#     if patient.empty:
#         return json.dumps({"error": "patient not found"})
#     p = patient.iloc[0]

#     triage = df("SELECT * FROM triage WHERE abha_id=? ORDER BY created_at", (abha_id,))
#     referrals = df("SELECT * FROM referrals WHERE abha_id=? ORDER BY created_at", (abha_id,))

#     bundle = {
#         "resourceType": "Bundle",
#         "type": "collection",
#         "meta": {"profile": "ArogyaBridge-ABDM-lite-v1"},
#         "entry": [{
#             "resourceType": "Patient",
#             "identifier": [{"system": "ABDM/ABHA", "value": p["abha_id"]}],
#             "name": p["name"], "gender": p["gender"], "age": int(p["age"]),
#             "address": {"village": p["village"]}, "language": p["language"],
#         }],
#     }
#     for _, t in triage.iterrows():
#         bundle["entry"].append({
#             "resourceType": "Observation", "category": "triage",
#             "priority": t["priority"], "symptoms": t["symptoms_text"],
#             "rationale": t["rationale"], "recordedBy": t["created_by"],
#             "effectiveDateTime": t["created_at"],
#         })
#     for _, r in referrals.iterrows():
#         bundle["entry"].append({
#             "resourceType": "ServiceRequest/Encounter",
#             "facility": r["facility"], "status": r["status"],
#             "prescription": decrypt_field(r["prescription"]),
#             "notes": decrypt_field(r["doctor_notes"]),
#             "createdAt": r["created_at"], "acknowledgedAt": r["acknowledged_at"],
#             "completedAt": r["completed_at"],
#         })
#     return json.dumps(bundle, indent=2, default=str)
# # =============================================================================
# # INITIALIZE SESSION
# # =============================================================================

# init_db()

# if "ui_lang" not in st.session_state:
#     st.session_state.ui_lang = "en"

# if "offline_mode" not in st.session_state:
#     st.session_state.offline_mode = False

# if "offline_queue" not in st.session_state:
#     st.session_state.offline_queue = []

# if "patient_logged_in" not in st.session_state:
#     st.session_state.patient_logged_in = False

# if "patient_abha_id" not in st.session_state:
#     st.session_state.patient_abha_id = None


# # =============================================================================
# # SIDEBAR
# # =============================================================================

# with st.sidebar:

#     st.markdown("# 🏥 ArogyaBridge")

#     language_labels = {
#         "en": "English",
#         "hi": "हिंदी (Hindi)",
#         "mr": "मराठी (Marathi)",
#         "ta": "தமிழ் (Tamil)",
#         "te": "తెలుగు (Telugu)",
#         "bn": "বাংলা (Bengali)",
#     }

#     current_language_label = language_labels.get(
#         st.session_state.ui_lang,
#         "English",
#     )

#     selected_language = st.selectbox(
#         "Language / भाषा",
#         list(language_labels.values()),
#         index=list(language_labels.values()).index(
#             current_language_label
#         ),
#     )

#     st.session_state.ui_lang = next(
#         code
#         for code, label in language_labels.items()
#         if label == selected_language
#     )

#     if "simple_mode" not in st.session_state:
#         st.session_state.simple_mode = False
#     if "selected_page" not in st.session_state:
#         st.session_state.selected_page = None

#     st.session_state.simple_mode = st.checkbox(
#         "🔤 Simple Icon Mode (low-literacy friendly)",
#         value=st.session_state.simple_mode,
#         help="Switches role selection to large icon buttons with minimal "
#              "text — for ASHA workers and patients with limited reading ability.",
#     )

#     role_options = [
#         (tr("patient_portal"), "🧑‍🤝‍🧑"),
#         (tr("asha"), "🚴"),
#         (tr("doctor"), "🩺"),
#         (tr("admin"), "🏛️"),
#         (tr("medicine"), "💊"),
#     ]

#     if st.session_state.simple_mode:
#         st.caption("👉 Tap an icon to continue")
#         icon_cols = st.columns(len(role_options))
#         for col, (label, icon) in zip(icon_cols, role_options):
#             if col.button(icon, key=f"icon_role_{label}", use_container_width=True):
#                 st.session_state.selected_page = label
#         if st.session_state.selected_page not in [r[0] for r in role_options]:
#             st.session_state.selected_page = role_options[0][0]
#         st.success(f"Selected: {st.session_state.selected_page}")
#         page = st.session_state.selected_page
#     else:
#         page = st.radio(
#             tr("role"),
#             [r[0] for r in role_options],
#         )
#         st.session_state.selected_page = page

#     st.divider()

#     # -------------------------------------------------------------------------
#     # Demo seed
#     # -------------------------------------------------------------------------

#     patient_count = int(
#         df(
#             "SELECT COUNT(*) AS n FROM patients"
#         ).iloc[0]["n"]
#     )

#     if patient_count == 0:

#         st.warning("Start the demo with sample data?")

#         if st.button(
#             "🌱 Load Demo Data",
#             type="primary",
#             use_container_width=True,
#         ):
#             if seed_demo_data():
#                 st.success(
#                     "Demo data loaded successfully."
#                 )

#             st.rerun()

#         st.divider()

#     # -------------------------------------------------------------------------
#     # AI status
#     # -------------------------------------------------------------------------

#     if GROQ_API_KEY:
#         st.caption(
#             "🤖 AI mode: Groq Llama 3.1 (live)"
#         )
#     else:
#         st.caption(
#             "🤖 AI mode: Rule-based + vitals fallback"
#         )

#     st.divider()

#     # -------------------------------------------------------------------------
#     # Offline mode
#     # -------------------------------------------------------------------------

#     st.markdown("### 📡 Offline-First Demo")

#     st.session_state.offline_mode = st.checkbox(
#         tr("offline_mode"),
#         value=st.session_state.offline_mode,
#         help=(
#             "When enabled, ASHA records are stored in the "
#             "session until Sync Now is pressed."
#         ),
#     )

#     queue_length = len(
#         st.session_state.offline_queue
#     )

#     if queue_length:
#         st.warning(
#             f"📥 {tr('pending_sync')}: "
#             f"**{queue_length}**"
#         )

#         if st.button(
#             tr("sync_now"),
#             type="primary",
#             use_container_width=True,
#         ):
#             synced = sync_offline_queue()

#             st.success(
#                 tr("synced_msg").format(n=synced)
#             )

#             st.rerun()

#     elif st.session_state.offline_mode:
#         st.caption(
#             "No records queued yet."
#         )

#     # -------------------------------------------------------------------------
#     # Notifications
#     # -------------------------------------------------------------------------

#     role_map = {
#         tr("asha"): "asha",
#         tr("doctor"): "doctor",
#         tr("admin"): "admin",
#         tr("medicine"): "admin",
#     }

#     current_role = role_map.get(page)

#     if current_role:

#         st.divider()

#         unread = unread_count(current_role)

#         st.markdown(
#             f"### 🔔 Notifications ({unread})"
#         )

#         notifications = df(
#             """
#             SELECT message, created_at
#             FROM notifications
#             WHERE role = ?
#             ORDER BY created_at DESC
#             LIMIT 5
#             """,
#             (current_role,),
#         )

#         if notifications.empty:
#             st.caption(
#                 "No notifications yet."
#             )
#         else:
#             for _, row in notifications.iterrows():
#                 st.markdown(
#                     f"• {row['message']}"
#                 )

#                 st.caption(
#                     str(row["created_at"])[:16]
#                 )

#             if unread:
#                 if st.button(
#                     "Mark all as read",
#                     use_container_width=True,
#                 ):
#                     mark_all_read(current_role)
#                     st.rerun()

#     # -------------------------------------------------------------------------
#     # Active SOS
#     # -------------------------------------------------------------------------

#     active_alert_count = int(
#         df(
#             """
#             SELECT COUNT(*) AS n
#             FROM emergency_alerts
#             WHERE status = 'ACTIVE'
#             """
#         ).iloc[0]["n"]
#     )

#     if active_alert_count:
#         st.divider()

#         st.error(
#             f"🚨 {active_alert_count} active emergency alert(s)"
#         )


# # =============================================================================
# # MAIN TITLE
# # =============================================================================

# st.title(tr("app_title"))


# # =============================================================================
# # PATIENT PORTAL
# # =============================================================================

# if page == tr("patient_portal"):

#     if not st.session_state.patient_logged_in:

#         login_tab, register_tab = st.tabs(
#             [
#                 "🔐 " + tr("login"),
#                 "📝 " + tr("register_tab"),
#             ]
#         )

#         # ---------------------------------------------------------------------
#         # LOGIN
#         # ---------------------------------------------------------------------

#         with login_tab:

#             st.caption(
#                 tr("phone_login_hint")
#             )

#             login_phone = st.text_input(
#                 tr("phone"),
#                 key="login_phone",
#             )

#             login_password = st.text_input(
#                 tr("password"),
#                 type="password",
#                 key="login_password",
#             )

#             if st.button(
#                 tr("login_btn"),
#                 type="primary",
#                 key="patient_login_button",
#             ):

#                 match = df(
#                     """
#                     SELECT
#                         abha_id,
#                         name,
#                         password_hash,
#                         salt
#                     FROM patients
#                     WHERE phone = ?
#                     AND password_hash IS NOT NULL
#                     LIMIT 1
#                     """,
#                     (login_phone,),
#                 )

#                 valid = (
#                     not match.empty
#                     and verify_password(
#                         login_password,
#                         match.iloc[0]["salt"],
#                         match.iloc[0]["password_hash"],
#                     )
#                 )

#                 if not valid:
#                     st.error(
#                         tr("invalid_login")
#                     )

#                 else:
#                     st.session_state.patient_logged_in = True
#                     st.session_state.patient_abha_id = (
#                         match.iloc[0]["abha_id"]
#                     )
#                     st.session_state.patient_name = (
#                         match.iloc[0]["name"]
#                     )

#                     st.rerun()

#         # ---------------------------------------------------------------------
#         # PATIENT REGISTRATION
#         # ---------------------------------------------------------------------

#         with register_tab:

#             st.caption(
#                 tr("create_login")
#             )

#             with st.form(
#                 "patient_self_register_form"
#             ):

#                 c1, c2 = st.columns(2)

#                 r_name = c1.text_input(
#                     tr("name")
#                 )

#                 r_age = c2.number_input(
#                     tr("age"),
#                     min_value=0,
#                     max_value=120,
#                     value=30,
#                 )

#                 r_gender = c1.selectbox(
#                     tr("gender"),
#                     [
#                         "Female",
#                         "Male",
#                         "Other",
#                     ],
#                 )

#                 r_village = c2.text_input(
#                     tr("village")
#                 )

#                 r_phone = c1.text_input(
#                     tr("phone")
#                 )

#                 r_language = c2.selectbox(
#                     tr("language"),
#                     [
#                         "Marathi",
#                         "Hindi",
#                         "Tamil",
#                         "Telugu",
#                         "Bengali",
#                         "English",
#                     ],
#                 )

#                 r_password = c1.text_input(
#                     tr("password"),
#                     type="password",
#                 )

#                 r_confirm = c2.text_input(
#                     tr("confirm_password"),
#                     type="password",
#                 )

#                 submitted = st.form_submit_button(
#                     tr("register_btn"),
#                     type="primary",
#                 )

#                 if submitted:

#                     existing = df(
#                         """
#                         SELECT abha_id
#                         FROM patients
#                         WHERE phone = ?
#                         """,
#                         (r_phone,),
#                     )

#                     if not r_name.strip():
#                         st.error(
#                             "Name is required."
#                         )

#                     elif not r_phone.strip():
#                         st.error(
#                             "Phone number is required."
#                         )

#                     elif not r_password:
#                         st.error(
#                             "Password is required."
#                         )

#                     elif r_password != r_confirm:
#                         st.error(
#                             "Passwords do not match."
#                         )

#                     elif not existing.empty:
#                         st.error(
#                             "An account with this phone number already exists."
#                         )

#                     else:

#                         password_hash, salt = hash_password(
#                             r_password
#                         )

#                         new_abha_id = gen_abha_id()

#                         conn = get_conn()

#                         conn.execute(
#                             """
#                             INSERT INTO patients
#                             (
#                                 abha_id,
#                                 name,
#                                 age,
#                                 gender,
#                                 village,
#                                 phone,
#                                 language,
#                                 created_at,
#                                 password_hash,
#                                 salt,
#                                 created_by
#                             )
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                             """,
#                             (
#                                 new_abha_id,
#                                 r_name.strip(),
#                                 r_age,
#                                 r_gender,
#                                 r_village.strip(),
#                                 r_phone.strip(),
#                                 r_language,
#                                 datetime.now().isoformat(),
#                                 password_hash,
#                                 salt,
#                                 "Patient (self)",
#                             ),
#                         )

#                         conn.commit()
#                         conn.close()

#                         st.success(
#                             f"✅ Account created! "
#                             f"Your ABHA-linked ID is "
#                             f"**{new_abha_id}**."
#                         )

#                         maybe_render_qr(
#                             new_abha_id,
#                             "Your ABHA-linked ID",
#                         )
                        

#     # -------------------------------------------------------------------------
#     # LOGGED-IN PATIENT
#     # -------------------------------------------------------------------------

#     else:

#         abha_id = (
#             st.session_state.patient_abha_id
#         )

#         profile = df(
#             """
#             SELECT *
#             FROM patients
#             WHERE abha_id = ?
#             """,
#             (abha_id,),
#         )

#         if profile.empty:
#             st.session_state.patient_logged_in = False
#             st.session_state.patient_abha_id = None
#             st.error("Patient record not found.")
#             st.stop()

#         patient = profile.iloc[0]

#         col_a, col_b = st.columns(
#             [5, 1]
#         )

#         col_a.subheader(
#             f"👋 {tr('welcome_back')}, "
#             f"{patient['name']}"
#         )

#         if col_b.button(
#             tr("logout")
#         ):
#             st.session_state.patient_logged_in = False
#             st.session_state.patient_abha_id = None
#             st.rerun()

#         st.divider()

#         c1, c2, c3 = st.columns(3)

#         c1.metric(
#             "ABHA ID",
#             patient["abha_id"],
#         )

#         c2.metric(
#             tr("age"),
#             int(patient["age"]),
#         )

#         c3.metric(
#             tr("village"),
#             patient["village"] or "—",
#         )

#         maybe_render_qr(patient["abha_id"], "ABHA-linked ID")
#         st.download_button(
#             "⬇️ Download ABDM-Ready Health Record (JSON)",
#             data=build_abdm_export(patient["abha_id"]),
#             file_name=f"abdm_record_{patient['abha_id']}.json",
#             mime="application/json",
#         )

#         # ---------------------------------------------------------------------
#         # Appointment + SOS
#         # ---------------------------------------------------------------------

#         b1, b2 = st.columns(2)

#         with b1:

#             with st.expander(
#                 "📅 " + tr("book_appointment")
#             ):

#                 with st.form(
#                     "appointment_form"
#                 ):

#                     facility = st.selectbox(
#                         "Facility",
#                         FACILITIES,
#                     )

#                     appointment_date = st.date_input(
#                         "Preferred date",
#                         min_value=date.today(),
#                     )

#                     slot = st.selectbox(
#                         "Slot",
#                         APPOINTMENT_SLOTS,
#                     )

#                     reason = st.text_input(
#                         "Reason"
#                     )

#                     submitted = st.form_submit_button(
#                         "Request Appointment",
#                         type="primary",
#                     )

#                     if submitted:

#                         conn = get_conn()

#                         conn.execute(
#                             """
#                             INSERT INTO appointments
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#                             """,
#                             (
#                                 str(uuid.uuid4()),
#                                 patient["abha_id"],
#                                 facility,
#                                 appointment_date.isoformat(),
#                                 slot,
#                                 reason.strip(),
#                                 "REQUESTED",
#                                 datetime.now().isoformat(),
#                             ),
#                         )

#                         conn.commit()
#                         conn.close()

#                         notify(
#                             "doctor",
#                             f"📅 New appointment request from "
#                             f"{patient['name']} at {facility} "
#                             f"on {appointment_date} ({slot})",
#                         )

#                         st.success(
#                             "Appointment requested."
#                         )

#         with b2:

#             st.markdown("### 🚨 Emergency")

#             if st.button(
#                 "🚨 " + tr("sos"),
#                 type="primary",
#                 use_container_width=True,
#             ):

#                 conn = get_conn()

#                 conn.execute(
#                     """
#                     INSERT INTO emergency_alerts
#                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#                     """,
#                     (
#                         str(uuid.uuid4()),
#                         patient["abha_id"],
#                         patient["name"],
#                         patient["village"],
#                         "Patient Portal (self-reported)",
#                         "ACTIVE",
#                         datetime.now().isoformat(),
#                         None,
#                     ),
#                 )

#                 conn.commit()
#                 conn.close()

#                 notify(
#                     "admin",
#                     f"🚨 Self-reported SOS: "
#                     f"{patient['name']} "
#                     f"({patient['village']})",
#                 )

#                 st.error(
#                     tr("sos_logged")
#                 )

#         # ---------------------------------------------------------------------
#         # Appointments
#         # ---------------------------------------------------------------------

#         appointments = df(
#             """
#             SELECT
#                 appointment_date,
#                 slot,
#                 reason,
#                 status
#             FROM appointments
#             WHERE abha_id = ?
#             ORDER BY appointment_date DESC
#             """,
#             (abha_id,),
#         )

#         if not appointments.empty:

#             st.divider()
#             st.subheader(
#                 "📅 My Appointments"
#             )

#             st.dataframe(
#                 appointments,
#                 use_container_width=True,
#                 hide_index=True,
#             )

#         # ---------------------------------------------------------------------
#         # Health Record
#         # ---------------------------------------------------------------------

#         st.divider()

#         st.subheader(
#             "📋 " + tr("my_health_record")
#         )

#         journey_tab, triage_tab, referral_tab, diagnostic_tab = st.tabs(
#             [
#                 "🗺 Full Journey",
#                 "🩺 " + tr("my_triage_history"),
#                 "📨 " + tr("my_referrals"),
#                 "🧪 Diagnostics",
#             ]
#         )

#         # Journey
#         with journey_tab:

#             events = get_patient_timeline(
#                 abha_id
#             )

#             if not events:
#                 st.info(
#                     tr("no_records_yet")
#                 )

#             else:

#                 for event in events:

#                     st.markdown(
#                         f"""
#                         <div style="
#                             border-left:4px solid {event['color']};
#                             padding-left:12px;
#                             margin:12px 0;
#                         ">
#                             <strong>{event['kind']}</strong>
#                             — {event['detail']}
#                             <br>
#                             <small style="color:#888">
#                                 {event['date']}
#                             </small>
#                         </div>
#                         """,
#                         unsafe_allow_html=True,
#                     )

#         # Triage
#         with triage_tab:
#             render_triage_legend()
#             triage_history = df(
#                 """
#                 SELECT
#                     symptoms_text,
#                     priority,
#                     rationale,
#                     created_by,
#                     created_at
#                 FROM triage
#                 WHERE abha_id = ?
#                 ORDER BY created_at DESC
#                 """,
#                 (abha_id,),
#             )

#             if triage_history.empty:
#                 st.info(
#                     tr("no_records_yet")
#                 )
#             else:
#                 st.dataframe(
#                     triage_history,
#                     use_container_width=True,
#                     hide_index=True,
#                 )

#         # Referrals
#         with referral_tab:

#             referral_history = df(
#                 """
#                 SELECT
#                     r.facility,
#                     r.status,
#                     r.prescription,
#                     r.doctor_notes,
#                     r.created_at,
#                     r.acknowledged_at,
#                     r.acknowledged_by,
#                     r.completed_at,
#                     t.priority,
#                     t.symptoms_text
#                 FROM referrals r
#                 JOIN triage t
#                     ON t.id = r.triage_id
#                 WHERE r.abha_id = ?
#                 ORDER BY r.created_at DESC
#                 """,
#                 (abha_id,),
#             )

#             if referral_history.empty:
#                 st.info(
#                     tr("no_records_yet")
#                 )

#             else:

#                 st.dataframe(
#                     referral_history[
#                         [
#                             "facility",
#                             "status",
#                             "prescription",
#                             "doctor_notes",
#                             "created_at",
#                             "acknowledged_at",
#                             "completed_at",
#                         ]
#                     ],
#                     use_container_width=True,
#                     hide_index=True,
#                 )

#                 completed_rows = referral_history[
#                     referral_history["status"]
#                     == "COMPLETED"
#                 ]

#                 if not completed_rows.empty:

#                     st.caption(
#                         "📄 Download completed prescriptions:"
#                     )

#                     for i, row in completed_rows.iterrows():

#                         prescription_text = build_prescription_text(
#                             patient["name"],
#                             patient["abha_id"],
#                             row["facility"],
#                             row["priority"],
#                             row["symptoms_text"],
#                             decrypt_field(row["prescription"]),
#                             decrypt_field(row["doctor_notes"]),
#                             row["acknowledged_by"],
#                             row["completed_at"],
#                         )

#                         st.download_button(
#                             f"⬇️ {row['facility']} — "
#                             f"{row['completed_at']}",
#                             data=prescription_text,
#                             file_name=(
#                                 f"prescription_"
#                                 f"{abha_id}_{i}.txt"
#                             ),
#                             key=f"patient_prescription_{i}",
#                         )
                        

#         # Diagnostics
#         with diagnostic_tab:

#             diagnostics = df(
#                 """
#                 SELECT
#                     test_name,
#                     facility,
#                     status,
#                     ordered_at,
#                     result_notes
#                 FROM diagnostics
#                 WHERE abha_id = ?
#                 ORDER BY ordered_at DESC
#                 """,
#                 (abha_id,),
#             )

#             if diagnostics.empty:
#                 st.info(
#                     "No diagnostics ordered yet."
#                 )
#             else:
#                 st.dataframe(
#                     diagnostics,
#                     use_container_width=True,
#                     hide_index=True,
#                 )


# # =============================================================================
# # ASHA / ANM
# # =============================================================================

# elif page == tr("asha"):

#     if not require_pin(
#         "asha",
#         tr("asha"),
#     ):
#         st.stop()

#     with st.expander("📖 New here? 60-second guide — no training required"):
#         st.markdown(
#             "1. **Type the patient's name & symptoms** — no medical jargon needed.\n"
#             "2. **Tap 'Run AI Triage'** — the app tells you RED, YELLOW or GREEN.\n"
#             "3. **RED or YELLOW?** Just tap 'Refer to Facility' — the app handles the rest.\n"
#             "4. **No signal?** Turn on Offline Mode in the sidebar — nothing is lost; "
#             "it syncs automatically the moment you're back online.\n\n"
#             "Works on any basic Android smartphone your ASHA kit already has — "
#             "**no new hardware required**."
#         )

#     if st.session_state.offline_mode:
#         st.info(
#             "📡 Offline mode is ON. "
#             "New ASHA records will remain locally queued "
#             "until synchronization."
#         )

#     register_tab, triage_tab = st.tabs(
#         [
#             "📝 " + tr("register_patient"),
#             "🤖 " + tr("run_triage") + " & Referral",
#         ]
#     )

#     # -------------------------------------------------------------------------
#     # Registration
#     # -------------------------------------------------------------------------

#     with register_tab:

#         with st.form("asha_register_form"):

#             c1, c2 = st.columns(2)

#             name = c1.text_input(
#                 tr("name")
#             )

#             age = c2.number_input(
#                 tr("age"),
#                 min_value=0,
#                 max_value=120,
#                 value=30,
#             )

#             gender = c1.selectbox(
#                 tr("gender"),
#                 [
#                     "Female",
#                     "Male",
#                     "Other",
#                 ],
#             )

#             village = c2.text_input(
#                 tr("village")
#             )

#             phone = c1.text_input(
#                 tr("phone")
#             )

#             patient_language = c2.selectbox(
#                 tr("language"),
#                 [
#                     "Marathi",
#                     "Hindi",
#                     "Tamil",
#                     "Telugu",
#                     "Bengali",
#                     "English",
#                 ],
#             )

#             worker_name = c1.text_input(
#                 "Your name (ASHA/ANM)",
#                 value="ASHA Worker",
#             )

#             setup_login = st.checkbox(
#                 tr("create_login")
#             )

#             asha_password = ""

#             if setup_login:
#                 asha_password = st.text_input(
#                     tr("password"),
#                     type="password",
#                 )

#             submitted = st.form_submit_button(
#                 tr("register_btn"),
#                 type="primary",
#             )

#             if submitted:

#                 if not name.strip():
#                     st.error(
#                         "Name is required."
#                     )

#                 elif setup_login and not asha_password:
#                     st.error(
#                         "Enter a password or disable app login."
#                     )

#                 else:

#                     abha_id = gen_abha_id()

#                     if setup_login:
#                         password_hash, salt = hash_password(
#                             asha_password
#                         )
#                     else:
#                         password_hash, salt = None, None

#                     values = (
#                         abha_id,
#                         name.strip(),
#                         age,
#                         gender,
#                         village.strip(),
#                         phone.strip(),
#                         patient_language,
#                         datetime.now().isoformat(),
#                         password_hash,
#                         salt,
#                         worker_name.strip(),
#                     )

#                     if st.session_state.offline_mode:

#                         queue_offline_record(
#                             "patient",
#                             values,
#                         )

#                         st.info(
#                             f"💾 {tr('saved_offline')} "
#                             f"ABHA ID: **{abha_id}**"
#                         )

#                     else:

#                         conn = get_conn()

#                         conn.execute(
#                             """
#                             INSERT INTO patients
#                             (
#                                 abha_id,
#                                 name,
#                                 age,
#                                 gender,
#                                 village,
#                                 phone,
#                                 language,
#                                 created_at,
#                                 password_hash,
#                                 salt,
#                                 created_by
#                             )
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                             """,
#                             values,
#                         )

#                         conn.commit()
#                         conn.close()

#                         st.success(
#                             f"✅ Patient registered! "
#                             f"ABHA ID: **{abha_id}**"
#                         )

#                         maybe_render_qr(
#                             abha_id,
#                             "Patient ABHA-linked ID",
#                         )

#                     if setup_login:
#                         st.info(
#                             "Patient can now use the Patient Portal "
#                             "with their registered phone and password."
#                         )

#         st.divider()

#         st.subheader(
#             "Registered Patients"
#         )

#         patients = df(
#             """
#             SELECT
#                 abha_id,
#                 name,
#                 age,
#                 gender,
#                 village,
#                 phone,
#                 language,
#                 created_by,
#                 created_at
#             FROM patients
#             ORDER BY created_at DESC
#             """
#         )

#         st.dataframe(
#             patients,
#             use_container_width=True,
#             hide_index=True,
#         )

#     # -------------------------------------------------------------------------
#     # Triage
#     # -------------------------------------------------------------------------

#     with triage_tab:

#         patients = df(
#             """
#             SELECT abha_id, name
#             FROM patients
#             ORDER BY created_at DESC
#             """
#         )

#         options = {}

#         for _, row in patients.iterrows():
#             options[
#                 f"{row['name']} ({row['abha_id']})"
#             ] = row["abha_id"]

#         options.update(
#             get_offline_patient_options()
#         )

#         if not options:

#             st.info(
#                 "Register a patient first."
#             )

#         else:

#             selected = st.selectbox(
#                 "Select Patient",
#                 list(options.keys()),
#             )

#             abha_id = options[selected]

#             with st.expander(
#                 "🗺 Recent patient journey"
#             ):

#                 events = get_patient_timeline(
#                     abha_id
#                 )[:5]

#                 if not events:
#                     st.caption(
#                         "No synced history yet."
#                     )

#                 else:

#                     for event in events:
#                         st.markdown(
#                             f"• **{event['kind']}** — "
#                             f"{event['detail']}"
#                         )
#             render_triage_legend()
#             symptoms = st.text_area(
#                 tr("symptoms"),
#                 placeholder=(
#                     "Example: High fever for 3 days "
#                     "with breathlessness / "
#                     "बुखार और सांस लेने में तकलीफ"
#                 ),
#                 height=120,
#             )

#             with st.expander(
#                 "🩺 " + tr("vitals_section")
#             ):

#                 st.caption(
#                     tr("vitals_hint")
#                 )

#                 v1, v2, v3, v4, v5 = st.columns(5)

#                 temp_f = v1.number_input(
#                     tr("temp_label"),
#                     min_value=0.0,
#                     max_value=112.0,
#                     value=0.0,
#                     step=0.1,
#                 )

#                 spo2 = v2.number_input(
#                     tr("spo2_label"),
#                     min_value=0,
#                     max_value=100,
#                     value=0,
#                     step=1,
#                 )

#                 pulse = v3.number_input(
#                     tr("pulse_label"),
#                     min_value=0,
#                     max_value=220,
#                     value=0,
#                     step=1,
#                 )

#                 bp_sys = v4.number_input(
#                     tr("bp_sys_label"),
#                     min_value=0,
#                     max_value=260,
#                     value=0,
#                     step=1,
#                 )

#                 bp_dia = v5.number_input(
#                     tr("bp_dia_label"),
#                     min_value=0,
#                     max_value=200,
#                     value=0,
#                     step=1,
#                 )

#             worker_name = st.text_input(
#                 "ASHA/ANM name",
#                 value="ASHA Worker",
#                 key="triage_worker_name",
#             )

#             if st.button(
#                 "🤖 " + tr("run_triage"),
#                 type="primary",
#             ):

#                 if not symptoms.strip():

#                     st.warning(
#                         "Please enter symptoms."
#                     )

#                 else:

#                     vitals = {
#                         "temp_f": temp_f,
#                         "spo2": spo2,
#                         "pulse": pulse,
#                         "bp_sys": bp_sys,
#                         "bp_dia": bp_dia,
#                     }

#                     with st.spinner(
#                         "Running triage..."
#                     ):
#                         priority, rationale = run_triage(
#                             symptoms,
#                             vitals,
#                         )

#                     triage_id = str(uuid.uuid4())

#                     triage_values = (
#                         triage_id,
#                         abha_id,
#                         symptoms.strip(),
#                         priority,
#                         rationale,
#                         worker_name.strip(),
#                         datetime.now().isoformat(),
#                     )

#                     if st.session_state.offline_mode:

#                         queue_offline_record(
#                             "triage",
#                             triage_values,
#                         )

#                         st.info(
#                             f"💾 {tr('saved_offline')}"
#                         )

#                     else:

#                         conn = get_conn()

#                         conn.execute(
#                             """
#                             INSERT INTO triage
#                             VALUES (?, ?, ?, ?, ?, ?, ?)
#                             """,
#                             triage_values,
#                         )

#                         conn.commit()
#                         conn.close()

#                     st.session_state.last_triage_id = triage_id
#                     st.session_state.last_triage_priority = priority
#                     st.session_state.last_triage_abha_id = abha_id

#                     st.markdown(
#                         f"### {tr('priority')}: "
#                         f"{priority_badge(priority)}",
#                         unsafe_allow_html=True,
#                     )

#                     st.write(rationale)

#             last_triage_id = st.session_state.get(
#                 "last_triage_id"
#             )

#             if last_triage_id:

#                 priority = st.session_state.get(
#                     "last_triage_priority",
#                     "GREEN",
#                 )

#                 triage_abha_id = st.session_state.get(
#                     "last_triage_abha_id",
#                     abha_id,
#                 )

#                 if priority in (
#                     "RED",
#                     "YELLOW",
#                 ):

#                     st.warning(
#                         "This patient needs facility follow-up."
#                     )

#                     # ---------------------------------------------------------
#                     # SOS
#                     # ---------------------------------------------------------

#                     if priority == "RED":

#                         if st.button(
#                             tr("trigger_sos"),
#                             type="primary",
#                         ):

#                             patient_lookup = df(
#                                 """
#                                 SELECT name, village
#                                 FROM patients
#                                 WHERE abha_id = ?
#                                 """,
#                                 (triage_abha_id,),
#                             )

#                             if not patient_lookup.empty:

#                                 patient_name = (
#                                     patient_lookup.iloc[0]["name"]
#                                 )

#                                 patient_village = (
#                                     patient_lookup.iloc[0]["village"]
#                                 )

#                             else:

#                                 patient_name = selected.split(
#                                     " ("
#                                 )[0]

#                                 patient_village = (
#                                     "Unknown"
#                                 )

#                             conn = get_conn()

#                             conn.execute(
#                                 """
#                                 INSERT INTO emergency_alerts
#                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#                                 """,
#                                 (
#                                     str(uuid.uuid4()),
#                                     triage_abha_id,
#                                     patient_name,
#                                     patient_village,
#                                     f"ASHA: {worker_name}",
#                                     "ACTIVE",
#                                     datetime.now().isoformat(),
#                                     None,
#                                 ),
#                             )

#                             conn.commit()
#                             conn.close()

#                             notify(
#                                 "admin",
#                                 f"🚨 SOS: {patient_name} "
#                                 f"({patient_village}) — "
#                                 f"escalated by {worker_name}",
#                             )

#                             st.error(
#                                 tr("sos_logged")
#                             )

#                     # ---------------------------------------------------------
#                     # Referral
#                     # ---------------------------------------------------------

#                     facility = st.selectbox(
#                         tr("select_facility"),
#                         FACILITIES,
#                         key="asha_referral_facility",
#                     )

#                     if st.button(
#                         "📨 " + tr("refer_btn"),
#                         type="primary",
#                     ):

#                         referral_id = str(
#                             uuid.uuid4()
#                         )

#                         referral_values = (
#                             referral_id,
#                             triage_abha_id,
#                             last_triage_id,
#                             facility,
#                             "PENDING",
#                             "",
#                             "",
#                             datetime.now().isoformat(),
#                             None,
#                             None,
#                             None,
#                         )

#                         if st.session_state.offline_mode:

#                             queue_offline_record(
#                                 "referral",
#                                 referral_values,
#                             )

#                             st.info(
#                                 f"💾 {tr('saved_offline')} "
#                                 f"Referral queued for "
#                                 f"{facility}."
#                             )

#                         else:

#                             conn = get_conn()

#                             conn.execute(
#                                 """
#                                 INSERT INTO referrals
#                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                                 """,
#                                 referral_values,
#                             )

#                             conn.commit()
#                             conn.close()

#                             notify(
#                                 "doctor",
#                                 f"📨 New referral for "
#                                 f"{facility}."
#                             )

#                             st.success(
#                                 f"Referral sent to {facility}. "
#                                 "Status: PENDING."
#                             )

#                         st.session_state.pop(
#                             "last_triage_id",
#                             None,
#                         )

#                 else:

#                     st.info(
#                         "GREEN priority — routine care. "
#                         "No referral required."
#                     )


# # =============================================================================
# # DOCTOR / FACILITY DASHBOARD
# # =============================================================================

# elif page == tr("doctor"):

#     if not require_pin(
#         "doctor",
#         tr("doctor"),
#     ):
#         st.stop()

#     facility = st.selectbox(
#         "Facility",
#         FACILITIES,
#     )

#     doctor_name = st.text_input(
#         tr("doctor_name_label"),
#         value="Duty Doctor",
#     )

#     name_filter = st.text_input(
#         "🔎 " + tr("search_patient")
#     )

#     queue = df(
#         """
#         SELECT
#             r.id AS ref_id,
#             p.abha_id,
#             p.name,
#             p.age,
#             p.gender,
#             p.village,
#             t.symptoms_text,
#             t.priority,
#             t.rationale,
#             t.created_by,
#             r.status,
#             r.created_at,
#             r.acknowledged_at,
#             r.acknowledged_by
#         FROM referrals r
#         JOIN patients p
#             ON p.abha_id = r.abha_id
#         JOIN triage t
#             ON t.id = r.triage_id
#         WHERE r.facility = ?
#         AND r.status != 'COMPLETED'
#         """,
#         (facility,),
#     )

#     if (
#         name_filter.strip()
#         and not queue.empty
#     ):
#         queue = queue[
#             queue["name"].str.contains(
#                 name_filter,
#                 case=False,
#                 na=False,
#             )
#         ]

#     st.subheader(
#         f"📋 {tr('queue')} — {facility}"
#     )
#     render_triage_legend()
#     st.caption(
#         "🌐 This dashboard works remotely from any internet-connected device — "
#         "no facility-specific hardware required."
#     )

#     if queue.empty:

#         st.info(
#             tr("no_referrals")
#         )

#     else:

#         queue["priority_sort"] = queue[
#             "priority"
#         ].map(PRIORITY_ORDER)

#         queue["status_sort"] = queue[
#             "status"
#         ].map(STATUS_ORDER)

#         queue = queue.sort_values(
#             [
#                 "status_sort",
#                 "priority_sort",
#             ]
#         )

#         for _, row in queue.iterrows():

#             with st.expander(
#                 f"{row['name']} · "
#                 f"{row['age']}y · "
#                 f"{row['priority']} · "
#                 f"{row['status']}",
#                 expanded=(
#                     row["status"]
#                     == "PENDING"
#                 ),
#             ):

#                 st.markdown(
#                     f"{priority_badge(row['priority'])} "
#                     f"&nbsp; "
#                     f"{status_badge(row['status'])}",
#                     unsafe_allow_html=True,
#                 )

#                 st.write(
#                     f"**ABHA ID:** {row['abha_id']}  "
#                     f"| **Village:** {row['village']}"
#                 )

#                 st.write(
#                     f"**Symptoms:** "
#                     f"{row['symptoms_text']}"
#                 )

#                 st.caption(
#                     f"AI rationale: "
#                     f"{row['rationale']}"
#                 )

#                 st.caption(
#                     f"Referred on: "
#                     f"{row['created_at']}"
#                 )

#                 # -------------------------------------------------------------
#                 # Acknowledge
#                 # -------------------------------------------------------------

#                 if row["status"] == "PENDING":

#                     st.warning(
#                         "🚦 " + tr("awaiting_arrival")
#                     )

#                     if st.button(
#                         tr("acknowledge_btn"),
#                         key=f"ack_{row['ref_id']}",
#                         type="primary",
#                     ):

#                         now = datetime.now().isoformat()

#                         conn = get_conn()

#                         conn.execute(
#                             """
#                             UPDATE referrals
#                             SET
#                                 status = 'ACKNOWLEDGED',
#                                 acknowledged_at = ?,
#                                 acknowledged_by = ?
#                             WHERE id = ?
#                             """,
#                             (
#                                 now,
#                                 doctor_name,
#                                 row["ref_id"],
#                             ),
#                         )

#                         conn.commit()
#                         conn.close()

#                         notify(
#                             "asha",
#                             f"✅ {row['name']} arrived at "
#                             f"{facility}.",
#                         )

#                         notify(
#                             "admin",
#                             f"✅ Arrival acknowledged: "
#                             f"{row['name']} at {facility}.",
#                         )

#                         st.success(
#                             "Patient arrival acknowledged."
#                         )

#                         st.rerun()

#                 # -------------------------------------------------------------
#                 # Acknowledged workflow
#                 # -------------------------------------------------------------

#                 elif row["status"] == "ACKNOWLEDGED":

#                     st.success(
#                         f"✅ {tr('acknowledged_on')} "
#                         f"{row['acknowledged_at']} "
#                         f"({tr('acknowledged_by')}: "
#                         f"{row['acknowledged_by']})"
#                     )

#                     tc1, tc2 = st.columns(2)

#                     with tc1:

#                         if st.button(
#                             "📹 " + tr("teleconsult"),
#                             key=f"tc_{row['ref_id']}",
#                         ):
#                             st.info(
#                                 "Teleconsultation room placeholder. "
#                                 "Integrate Daily.co/WebRTC here."
#                             )

#                     with tc2:

#                         st.write(
#                             "Referral status: "
#                             f"`{row['status']}`"
#                         )

#                     # ---------------------------------------------------------
#                     # Diagnostics
#                     # ---------------------------------------------------------

#                     st.markdown(
#                         "### 🧪 Diagnostics"
#                     )

#                     tests = st.multiselect(
#                         "Order diagnostics",
#                         DIAGNOSTIC_TESTS,
#                         key=f"diag_{row['ref_id']}",
#                     )

#                     if st.button(
#                         "🏥 Order Selected Tests",
#                         key=f"order_diag_{row['ref_id']}",
#                     ):

#                         if not tests:

#                             st.warning(
#                                 "Select at least one test."
#                             )

#                         else:

#                             conn = get_conn()

#                             for test in tests:

#                                 conn.execute(
#                                     """
#                                     INSERT INTO diagnostics
#                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#                                     """,
#                                     (
#                                         str(uuid.uuid4()),
#                                         row["abha_id"],
#                                         row["ref_id"],
#                                         facility,
#                                         test,
#                                         "ORDERED",
#                                         datetime.now().isoformat(),
#                                         None,
#                                     ),
#                                 )

#                             conn.commit()
#                             conn.close()

#                             notify(
#                                 "asha",
#                                 f"🧪 {len(tests)} diagnostic "
#                                 f"test(s) ordered for "
#                                 f"{row['name']}.",
#                             )

#                             st.success(
#                                 f"{len(tests)} test(s) ordered."
#                             )

#                     # ---------------------------------------------------------
#                     # Prescription
#                     # ---------------------------------------------------------

#                     prescription = st.text_area(
#                         tr("prescription"),
#                         key=f"prescription_{row['ref_id']}",
#                         height=150,
#                     )

#                     notes = st.text_area(
#                         "Doctor notes",
#                         key=f"notes_{row['ref_id']}",
#                     )

#                     if st.button(
#                         tr("save_prescription"),
#                         key=f"complete_{row['ref_id']}",
#                         type="primary",
#                     ):

#                         completed_at = (
#                             datetime.now().isoformat()
#                         )

#                         conn = get_conn()

#                         conn.execute(
#                             """
#                             UPDATE referrals
#                             SET
#                                 status = 'COMPLETED',
#                                 prescription = ?,
#                                 doctor_notes = ?,
#                                 completed_at = ?
#                             WHERE id = ?
#                             """,
#                             (
#                                 encrypt_field(prescription),
#                                 encrypt_field(notes),
#                                 completed_at,
#                                 row["ref_id"],
#                             ),
#                         )

#                         conn.commit()
#                         conn.close()

#                         notify(
#                             "asha",
#                             f"💊 Prescription issued for "
#                             f"{row['name']} — referral completed.",
#                         )

#                         notify(
#                             "admin",
#                             f"💊 Referral completed: "
#                             f"{row['name']} at {facility}.",
#                         )

#                         st.success(
#                             "Referral completed and prescription saved."
#                         )

#                         prescription_text = build_prescription_text(
#                             row["name"],
#                             row["abha_id"],
#                             facility,
#                             row["priority"],
#                             row["symptoms_text"],
#                             prescription,
#                             notes,
#                             doctor_name,
#                             completed_at,
#                         )

#                         st.download_button(
#                             tr("download_prescription"),
#                             data=prescription_text,
#                             file_name=(
#                                 f"prescription_"
#                                 f"{row['abha_id']}.txt"
#                             ),
#                             key=f"download_{row['ref_id']}",
#                         )

#     # -------------------------------------------------------------------------
#     # Completed referrals
#     # -------------------------------------------------------------------------

#     st.divider()

#     st.subheader(
#         "Completed Referrals (History)"
#     )

#     history = df(
#         """
#         SELECT
#             p.name,
#             t.priority,
#             r.acknowledged_at,
#             r.prescription,
#             r.completed_at
#         FROM referrals r
#         JOIN patients p
#             ON p.abha_id = r.abha_id
#         JOIN triage t
#             ON t.id = r.triage_id
#         WHERE r.facility = ?
#         AND r.status = 'COMPLETED'
#         ORDER BY r.completed_at DESC
#         """,
#         (facility,),
#     )

#     st.dataframe(
#         history,
#         use_container_width=True,
#         hide_index=True,
#     )

#     # -------------------------------------------------------------------------
#     # Appointments
#     # -------------------------------------------------------------------------

#     st.divider()

#     st.subheader(
#         "📅 Facility Appointments"
#     )

#     appointments = df(
#         """
#         SELECT
#             a.id,
#             a.abha_id,
#             p.name,
#             a.appointment_date,
#             a.slot,
#             a.reason,
#             a.status
#         FROM appointments a
#         JOIN patients p
#             ON p.abha_id = a.abha_id
#         WHERE a.facility = ?
#         ORDER BY a.appointment_date, a.slot
#         """,
#         (facility,),
#     )

#     if appointments.empty:

#         st.info(
#             "No appointments for this facility."
#         )

#     else:

#         for _, appointment in appointments.iterrows():

#             c1, c2, c3 = st.columns(
#                 [5, 1, 1]
#             )

#             c1.write(
#                 f"**{appointment['name']}** — "
#                 f"{appointment['appointment_date']} "
#                 f"{appointment['slot']} — "
#                 f"{appointment['reason']} "
#                 f"({appointment['status']})"
#             )

#             if appointment["status"] == "REQUESTED":

#                 if c2.button(
#                     "Confirm",
#                     key=f"confirm_{appointment['id']}",
#                 ):

#                     conn = get_conn()

#                     conn.execute(
#                         """
#                         UPDATE appointments
#                         SET status = 'CONFIRMED'
#                         WHERE id = ?
#                         """,
#                         (appointment["id"],),
#                     )

#                     conn.commit()
#                     conn.close()

#                     notify(
#                         "asha",
#                         f"📅 Appointment confirmed for "
#                         f"{appointment['name']} at {facility}.",
#                     )

#                     st.rerun()

#                 if c3.button(
#                     "Decline",
#                     key=f"decline_{appointment['id']}",
#                 ):

#                     conn = get_conn()

#                     conn.execute(
#                         """
#                         UPDATE appointments
#                         SET status = 'DECLINED'
#                         WHERE id = ?
#                         """,
#                         (appointment["id"],),
#                     )

#                     conn.commit()
#                     conn.close()

#                     st.rerun()

#             elif appointment["status"] == "CONFIRMED":

#                 if c2.button(
#                     "Mark Done",
#                     key=f"done_{appointment['id']}",
#                 ):

#                     conn = get_conn()

#                     conn.execute(
#                         """
#                         UPDATE appointments
#                         SET status = 'DONE'
#                         WHERE id = ?
#                         """,
#                         (appointment["id"],),
#                     )

#                     conn.commit()
#                     conn.close()

#                     st.rerun()

#             else:

#                 c2.write(
#                     appointment["status"]
#                 )


# # =============================================================================
# # DISTRICT ADMIN
# # =============================================================================

# elif page == tr("admin"):

#     if not require_pin("admin", tr("admin")):
#         st.stop()

#     total_patients = int(df("SELECT COUNT(*) AS n FROM patients").iloc[0]["n"])
#     total_triage = int(df("SELECT COUNT(*) AS n FROM triage").iloc[0]["n"])
#     total_referrals = int(df("SELECT COUNT(*) AS n FROM referrals").iloc[0]["n"])
#     completed_referrals = int(
#         df("SELECT COUNT(*) AS n FROM referrals WHERE status = 'COMPLETED'").iloc[0]["n"]
#     )
#     completion_rate = (completed_referrals / total_referrals * 100) if total_referrals else 0
#     active_alert_count = int(
#         df("SELECT COUNT(*) AS n FROM emergency_alerts WHERE status='ACTIVE'").iloc[0]["n"]
#     )

#     tab_overview, tab_emergency, tab_referrals, tab_outbreak, tab_ops, tab_impact = st.tabs(
#         [
#             "📊 Overview",
#             f"🚨 Emergency ({active_alert_count})",
#             "🔗 Referrals & Facilities",
#             "📈 Outbreak & Trends",
#             "🧪 Operations",
#             "🌍 Impact & Compliance",
#         ]
#     )

#     # =========================================================================
#     # TAB 1 — OVERVIEW
#     # =========================================================================
#     with tab_overview:

#         c1, c2, c3, c4 = st.columns(4)
#         c1.metric("Registered Patients", total_patients)
#         c2.metric("Triage Runs", total_triage)
#         c3.metric("Referrals", total_referrals)
#         c4.metric("Completion Rate", f"{completion_rate:.0f}%")

#         if active_alert_count:
#             st.error(f"🚨 {active_alert_count} active emergency alert(s) — see the Emergency tab.")

#         st.divider()
#         st.subheader("🏆 ASHA / ANM Performance Leaderboard")

#         registrations = df(
#             "SELECT created_by, COUNT(*) AS patients FROM patients "
#             "WHERE created_by IS NOT NULL GROUP BY created_by"
#         )
#         triages = df("SELECT created_by, COUNT(*) AS triages FROM triage GROUP BY created_by")
#         referrals_by_asha = df(
#             "SELECT t.created_by, COUNT(DISTINCT r.id) AS referrals FROM referrals r "
#             "JOIN triage t ON t.id = r.triage_id GROUP BY t.created_by"
#         )

#         worker_names = set()
#         for tbl in (registrations, triages, referrals_by_asha):
#             if not tbl.empty:
#                 worker_names.update(tbl["created_by"].dropna())

#         if worker_names:
#             performance = pd.DataFrame({"created_by": sorted(worker_names)})
#             performance = performance.merge(registrations, on="created_by", how="left")
#             performance = performance.merge(triages, on="created_by", how="left")
#             performance = performance.merge(referrals_by_asha, on="created_by", how="left")
#             performance = performance.fillna(0)
#             performance["total_touches"] = (
#                 performance["patients"] + performance["triages"] + performance["referrals"]
#             )
#             performance = performance.sort_values("patients", ascending=False)

#             st.dataframe(performance, use_container_width=True, hide_index=True)
#             st.bar_chart(performance.set_index("created_by")[["total_touches"]])
#         else:
#             st.info("No ASHA activity recorded yet.")

#     # =========================================================================
#     # TAB 2 — EMERGENCY
#     # =========================================================================
#     with tab_emergency:

#         st.subheader(tr("active_alerts"))

#         active_alerts = df(
#             "SELECT id, patient_name, village, triggered_by, created_at "
#             "FROM emergency_alerts WHERE status='ACTIVE' ORDER BY created_at DESC"
#         )

#         if active_alerts.empty:
#             st.success(tr("no_active_alerts"))
#         else:
#             for _, alert in active_alerts.iterrows():
#                 c1, c2 = st.columns([6, 1])
#                 c1.error(
#                     f"🚨 **{alert['patient_name']}** ({alert['village']}) — "
#                     f"reported by *{alert['triggered_by']}* at {alert['created_at']}"
#                 )
#                 if c2.button(tr("resolve"), key=f"resolve_{alert['id']}"):
#                     conn = get_conn()
#                     conn.execute(
#                         "UPDATE emergency_alerts SET status='RESOLVED', resolved_at=? WHERE id=?",
#                         (datetime.now().isoformat(), alert["id"]),
#                     )
#                     conn.commit()
#                     conn.close()
#                     notify("asha", f"✅ SOS for {alert['patient_name']} was resolved by admin.")
#                     st.rerun()

#         st.divider()
#         st.subheader("🗂️ Resolved Alert History")
#         resolved = df(
#             "SELECT patient_name, village, triggered_by, created_at, resolved_at "
#             "FROM emergency_alerts WHERE status='RESOLVED' ORDER BY resolved_at DESC LIMIT 20"
#         )
#         if resolved.empty:
#             st.caption("No resolved alerts yet.")
#         else:
#             st.dataframe(resolved, use_container_width=True, hide_index=True)

#     # =========================================================================
#     # TAB 3 — REFERRALS & FACILITIES
#     # =========================================================================
#     with tab_referrals:

#         st.subheader("🔗 " + tr("referral_funnel"))
#         render_triage_legend()

#         pending = int(df("SELECT COUNT(*) AS n FROM referrals WHERE status='PENDING'").iloc[0]["n"])
#         acknowledged = int(
#             df("SELECT COUNT(*) AS n FROM referrals WHERE status='ACKNOWLEDGED'").iloc[0]["n"]
#         )
#         completed = completed_referrals

#         f1, f2, f3 = st.columns(3)
#         f1.metric(tr("status_pending"), pending)
#         f2.metric(tr("status_ack"), acknowledged)
#         f3.metric(tr("status_completed"), completed)

#         funnel = pd.DataFrame(
#             {"Status": ["PENDING", "ACKNOWLEDGED", "COMPLETED"], "Count": [pending, acknowledged, completed]}
#         )
#         st.bar_chart(funnel.set_index("Status"))
#         st.caption(
#             "Closed-loop referral tracking shows the patient journey from referral "
#             "creation through arrival acknowledgement to completion."
#         )

#         st.divider()
#         st.subheader(tr("turnaround"))

#         referral_times = df(
#             "SELECT facility, created_at, acknowledged_at, completed_at "
#             "FROM referrals WHERE status='COMPLETED'"
#         )
#         if referral_times.empty:
#             st.info("No completed referrals yet.")
#         else:
#             for column in ["created_at", "acknowledged_at", "completed_at"]:
#                 referral_times[column] = pd.to_datetime(referral_times[column], errors="coerce")
#             referral_times["hrs_to_ack"] = (
#                 referral_times["acknowledged_at"] - referral_times["created_at"]
#             ).dt.total_seconds() / 3600
#             referral_times["hrs_ack_to_completion"] = (
#                 referral_times["completed_at"] - referral_times["acknowledged_at"]
#             ).dt.total_seconds() / 3600

#             t1, t2 = st.columns(2)
#             t1.metric("Avg. time to acknowledgement", f"{referral_times['hrs_to_ack'].mean():.1f} hrs")
#             t2.metric(
#                 "Avg. arrival → completion", f"{referral_times['hrs_ack_to_completion'].mean():.1f} hrs"
#             )

#             by_facility = referral_times.groupby("facility")[
#                 ["hrs_to_ack", "hrs_ack_to_completion"]
#             ].mean()
#             st.bar_chart(by_facility)

#         st.divider()
#         st.subheader("🏥 Facility Comparison Board")

#         facility_data = df(
#             """
#             SELECT
#                 facility,
#                 COUNT(*) AS total,
#                 SUM(CASE WHEN status IN ('ACKNOWLEDGED','COMPLETED') THEN 1 ELSE 0 END) AS arrived,
#                 SUM(CASE WHEN status='COMPLETED' THEN 1 ELSE 0 END) AS completed,
#                 ROUND(AVG(CASE WHEN acknowledged_at IS NOT NULL
#                     THEN (JULIANDAY(acknowledged_at) - JULIANDAY(created_at)) * 24 END), 1) AS avg_hrs_to_ack
#             FROM referrals GROUP BY facility ORDER BY facility
#             """
#         )
#         if not facility_data.empty:
#             facility_data["arrival_rate"] = (facility_data["arrived"] / facility_data["total"] * 100).round(1)
#             facility_data["completion_rate"] = (facility_data["completed"] / facility_data["total"] * 100).round(1)

#             display_facility = facility_data.rename(
#                 columns={
#                     "facility": "Facility", "total": "Referrals", "arrived": "Arrived",
#                     "completed": "Completed", "avg_hrs_to_ack": "Avg hrs to acknowledge",
#                     "arrival_rate": "Arrival rate %", "completion_rate": "Completion rate %",
#                 }
#             )
#             st.dataframe(display_facility, use_container_width=True, hide_index=True)
#             st.bar_chart(facility_data.set_index("facility")[["arrival_rate", "completion_rate"]])
#         else:
#             st.info("No referral data yet.")

#         st.divider()
#         st.subheader("📅 All Facility Appointments")
#         all_appointments = df(
#             """
#             SELECT p.name, a.facility, a.appointment_date, a.slot, a.reason, a.status
#             FROM appointments a JOIN patients p ON p.abha_id = a.abha_id
#             ORDER BY a.appointment_date DESC
#             """
#         )
#         if all_appointments.empty:
#             st.caption("No appointments booked yet.")
#         else:
#             st.dataframe(all_appointments, use_container_width=True, hide_index=True)

#     # =========================================================================
#     # TAB 4 — OUTBREAK & TRENDS
#     # =========================================================================
#     with tab_outbreak:

#         st.subheader(tr("outbreak"))
#         render_triage_legend()

#         recent_triage = df(
#             "SELECT t.priority, t.created_at, p.village FROM triage t "
#             "JOIN patients p ON p.abha_id = t.abha_id"
#         )
#         if recent_triage.empty:
#             st.info(tr("no_outbreak"))
#         else:
#             recent_triage["created_at"] = pd.to_datetime(recent_triage["created_at"], errors="coerce")
#             cutoff = datetime.now() - timedelta(days=OUTBREAK_LOOKBACK_DAYS)
#             recent_triage = recent_triage[recent_triage["created_at"] >= cutoff]
#             risky = recent_triage[recent_triage["priority"].isin(["RED", "YELLOW"])]
#             clusters = (
#                 risky.groupby("village").size().reset_index(name="risk_case_count")
#                 .sort_values("risk_case_count", ascending=False)
#             )
#             clusters = clusters[clusters["risk_case_count"] >= OUTBREAK_CLUSTER_THRESHOLD]

#             if clusters.empty:
#                 st.success(tr("no_outbreak"))
#             else:
#                 for _, row in clusters.iterrows():
#                     st.warning(
#                         f"⚠️ **{row['village']}**: {row['risk_case_count']} RED/YELLOW cases "
#                         f"in the last {OUTBREAK_LOOKBACK_DAYS} days."
#                     )
#                 st.bar_chart(clusters.set_index("village"))

#         st.divider()
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Triage Priority Breakdown")
#             priority_data = df("SELECT priority, COUNT(*) AS count FROM triage GROUP BY priority")
#             if not priority_data.empty:
#                 st.bar_chart(priority_data.set_index("priority"))
#             else:
#                 st.info("No triage data yet.")
#         with col2:
#             st.subheader("Referrals by Facility")
#             referral_data = df("SELECT facility, COUNT(*) AS count FROM referrals GROUP BY facility")
#             if not referral_data.empty:
#                 st.bar_chart(referral_data.set_index("facility"))
#             else:
#                 st.info("No referral data yet.")

#         st.divider()
#         st.subheader("🤧 Symptom Trends")
#         trends = symptom_trends()
#         if not trends:
#             st.info("No triage text available.")
#         else:
#             trend_series = pd.Series(dict(trends)).sort_values(ascending=True)
#             st.bar_chart(trend_series)
#             st.caption("Frequent symptom keywords from recent triages. This is a screening signal, not a diagnosis.")

#         st.divider()
#         st.subheader("🩺 Recent Disease / Symptom Signals")
#         recent = df(
#             "SELECT symptoms_text, priority, created_at FROM triage ORDER BY created_at DESC LIMIT 15"
#         )
#         st.dataframe(recent, use_container_width=True, hide_index=True)

#     # =========================================================================
#     # TAB 5 — OPERATIONS (diagnostics + medicine stock + data export)
#     # =========================================================================
#     with tab_ops:

#         st.subheader("🧪 Diagnostics Load")
#         total_tests = int(df("SELECT COUNT(*) AS n FROM diagnostics").iloc[0]["n"])
#         pending_tests = int(
#             df("SELECT COUNT(*) AS n FROM diagnostics WHERE status='ORDERED'").iloc[0]["n"]
#         )
#         d1, d2 = st.columns(2)
#         d1.metric("Tests ordered", total_tests)
#         d2.metric("Awaiting reports", pending_tests)

#         diagnostic_recent = df(
#             """
#             SELECT p.name, d.facility, d.test_name, d.status, d.ordered_at
#             FROM diagnostics d JOIN patients p ON p.abha_id = d.abha_id
#             ORDER BY d.ordered_at DESC LIMIT 10
#             """
#         )
#         if not diagnostic_recent.empty:
#             st.dataframe(diagnostic_recent, use_container_width=True, hide_index=True)
#         else:
#             st.caption("No diagnostics ordered yet.")

#         st.divider()
#         st.subheader("💊 Low Medicine Stock Alerts")
#         low_stock = df(
#             "SELECT facility, medicine_name, quantity, unit FROM medicine_stock "
#             "WHERE quantity < 10 ORDER BY quantity ASC"
#         )
#         if low_stock.empty:
#             st.success("No low-stock alerts.")
#         else:
#             st.dataframe(low_stock, use_container_width=True, hide_index=True)

#         st.divider()
#         st.subheader("📤 Data Export")
#         export1, export2, export3 = st.columns(3)
#         all_patients = df("SELECT * FROM patients")
#         all_triage = df("SELECT * FROM triage")
#         all_referrals = df("SELECT * FROM referrals")

#         export1.download_button(
#             "⬇ Patients CSV", data=all_patients.to_csv(index=False),
#             file_name="patients_export.csv", mime="text/csv",
#         )
#         export2.download_button(
#             "⬇ Triage CSV", data=all_triage.to_csv(index=False),
#             file_name="triage_export.csv", mime="text/csv",
#         )
#         export3.download_button(
#             "⬇ Referrals CSV", data=all_referrals.to_csv(index=False),
#             file_name="referrals_export.csv", mime="text/csv",
#         )

#     # =========================================================================
#     # TAB 6 — IMPACT & COMPLIANCE
#     # =========================================================================
#     with tab_impact:

#         st.subheader("🌍 Social, Economic & Environmental Impact (Estimated)")
#         st.caption(
#             "Illustrative estimate based on configurable assumptions — "
#             "adjust the sliders to match real district data."
#         )

#         imp1, imp2, imp3 = st.columns(3)
#         avg_km_per_trip = imp1.slider("Avg. one-way distance avoided per case (km)", 1, 60, 15)
#         cost_per_km = imp2.slider("Assumed cost per km (₹)", 1, 30, 8)
#         co2_per_km = imp3.slider("CO₂ emitted per km avoided (kg)", 0.05, 0.50, 0.12, step=0.01)

#         green_triage_count = int(
#             df("SELECT COUNT(*) AS n FROM triage WHERE priority='GREEN'").iloc[0]["n"]
#         )
#         cases_with_avoided_travel = green_triage_count + completed_referrals
#         total_km_saved = cases_with_avoided_travel * avg_km_per_trip * 2
#         total_cost_saved = total_km_saved * cost_per_km
#         total_co2_saved = total_km_saved * co2_per_km

#         im1, im2, im3, im4 = st.columns(4)
#         im1.metric("Cases with avoided/optimized travel", cases_with_avoided_travel)
#         im2.metric("Estimated distance saved", f"{total_km_saved:,.0f} km")
#         im3.metric("Estimated cost saved", f"₹{total_cost_saved:,.0f}")
#         im4.metric("Estimated CO₂ avoided", f"{total_co2_saved:,.1f} kg")

#         st.caption(
#             "Social impact: routine (GREEN) cases are resolved by the ASHA worker without "
#             "any facility visit, and every completed referral reflects a patient who did not "
#             "fall through the referral gap."
#         )

#         st.divider()
#         st.subheader("🇮🇳 Feasibility, Interoperability & Rollout Strategy")
#         st.markdown(
#             "**Technical feasibility**\n"
#             "- ✅ Runs on low-end smartphones, offline-sync included\n"
#             "- ✅ ABDM-ready unique patient ID for nationwide interoperability\n"
#             "- ✅ Icon-driven, minimal-text UI (Simple Icon Mode in the sidebar) for low-literacy users\n"
#             "- ✅ Smart sync with timestamp-based conflict resolution\n\n"
#             "**Operational feasibility**\n"
#             "- ✅ No new hardware — works on the phone ASHA workers already carry\n"
#             "- ✅ Built-in 60-second guide removes the need for formal training\n"
#             "- ✅ Doctors get remote access to patient records & referrals from any device\n\n"
#             "**Data privacy & compliance**\n"
#             "- ✅ Encryption at rest for prescriptions & doctor notes "
#             f"({'active — cryptography installed' if _get_cipher() else 'inactive — run `pip install cryptography`'})\n"
#             "- ✅ Structured, ABDM-schema-inspired FHIR-lite JSON export\n"
#             "- 🔜 Full ABDM API integration — planned for production rollout\n\n"
#             "**Adoption strategy**\n"
#             "- 🔜 Pilot rollouts in 1–2 PHCs before district-wide scale-up\n"
#             "- 🔜 Awareness campaigns with local ASHA supervisors to reduce resistance to change"
#         )

# # =============================================================================
# # MEDICINE STOCK
# # =============================================================================

# elif page == tr("medicine"):

#     st.subheader(
#         "💊 " + tr("medicine")
#     )

#     facility = st.selectbox(
#         "Facility",
#         ["All"] + FACILITIES,
#     )

#     search = st.text_input(
#         "Search medicine name"
#     )

#     query = """
#         SELECT
#             facility,
#             medicine_name,
#             quantity,
#             unit,
#             last_updated
#         FROM medicine_stock
#         WHERE 1 = 1
#     """

#     params = []

#     if facility != "All":

#         query += """
#             AND facility = ?
#         """

#         params.append(facility)

#     if search.strip():

#         query += """
#             AND medicine_name LIKE ?
#         """

#         params.append(
#             f"%{search.strip()}%"
#         )

#     query += """
#         ORDER BY facility, medicine_name
#     """

#     stock = df(
#         query,
#         tuple(params),
#     )

#     if stock.empty:

#         st.info(
#             "No matching medicine records."
#         )

#     else:

#         def highlight_low(row):

#             if row["quantity"] < 10:
#                 return [
#                     "background-color:#ffccd2;color:#000"
#                     for _ in row
#                 ]

#             return [
#                 ""
#                 for _ in row
#             ]

#         styled_stock = stock.style.apply(
#             highlight_low,
#             axis=1,
#         )

#         st.dataframe(
#             styled_stock,
#             use_container_width=True,
#             hide_index=True,
#         )

#         st.caption(
#             "🔴 Highlighted rows indicate quantity below 10."
#         )

#         st.download_button(
#             tr("download_csv"),
#             data=stock.to_csv(
#                 index=False
#             ),
#             file_name="medicine_stock_export.csv",
#             mime="text/csv",
#         )

#     # -------------------------------------------------------------------------
#     # Inventory update
#     # -------------------------------------------------------------------------

#     st.divider()

#     st.subheader(
#         "🔄 Restock / Update Inventory"
#     )

#     update_tab, add_tab = st.tabs(
#         [
#             "Update Existing Stock",
#             "Add New Medicine",
#         ]
#     )

#     # Update
#     with update_tab:

#         all_medicines = df(
#             """
#             SELECT
#                 id,
#                 facility,
#                 medicine_name,
#                 quantity,
#                 unit
#             FROM medicine_stock
#             ORDER BY facility, medicine_name
#             """
#         )

#         if all_medicines.empty:

#             st.info(
#                 "No medicines in inventory."
#             )

#         else:

#             labels = {
#                 (
#                     f"{row['medicine_name']} — "
#                     f"{row['facility']} "
#                     f"(currently: "
#                     f"{row['quantity']} "
#                     f"{row['unit']})"
#                 ): row["id"]
#                 for _, row in all_medicines.iterrows()
#             }

#             selected_label = st.selectbox(
#                 "Select medicine",
#                 list(labels.keys()),
#             )

#             selected_id = labels[
#                 selected_label
#             ]

#             action = st.radio(
#                 "Action",
#                 [
#                     "Add stock (restock delivery)",
#                     "Remove stock (dispensed/damaged)",
#                     "Set exact quantity",
#                 ],
#             )

#             amount = st.number_input(
#                 "Amount",
#                 min_value=0,
#                 value=10,
#                 step=1,
#             )

#             if st.button(
#                 "Apply Update",
#                 type="primary",
#             ):

#                 conn = get_conn()

#                 result = conn.execute(
#                     """
#                     SELECT quantity
#                     FROM medicine_stock
#                     WHERE id = ?
#                     """,
#                     (selected_id,),
#                 ).fetchone()

#                 current_quantity = int(
#                     result[0]
#                 )

#                 if action.startswith("Add"):
#                     new_quantity = (
#                         current_quantity
#                         + amount
#                     )

#                 elif action.startswith("Remove"):
#                     new_quantity = max(
#                         0,
#                         current_quantity
#                         - amount,
#                     )

#                 else:
#                     new_quantity = amount

#                 conn.execute(
#                     """
#                     UPDATE medicine_stock
#                     SET
#                         quantity = ?,
#                         last_updated = ?
#                     WHERE id = ?
#                     """,
#                     (
#                         new_quantity,
#                         datetime.now().isoformat(),
#                         selected_id,
#                     ),
#                 )

#                 conn.commit()
#                 conn.close()

#                 st.success(
#                     f"Inventory updated. "
#                     f"New quantity: "
#                     f"{new_quantity}"
#                 )

#                 st.rerun()

#     # Add medicine
#     with add_tab:

#         with st.form(
#             "add_medicine_form"
#         ):

#             new_facility = st.selectbox(
#                 "Facility",
#                 FACILITIES,
#                 key="new_medicine_facility",
#             )

#             new_name = st.text_input(
#                 "Medicine name"
#             )

#             new_quantity = st.number_input(
#                 "Starting quantity",
#                 min_value=0,
#                 value=50,
#                 step=1,
#             )

#             new_unit = st.selectbox(
#                 "Unit",
#                 [
#                     "tablets",
#                     "capsules",
#                     "vials",
#                     "sachets",
#                     "units",
#                     "bottles",
#                 ],
#             )

#             submitted = st.form_submit_button(
#                 "➕ Add Medicine",
#                 type="primary",
#             )

#             if submitted:

#                 if not new_name.strip():

#                     st.error(
#                         "Medicine name is required."
#                     )

#                 else:

#                     conn = get_conn()

#                     conn.execute(
#                         """
#                         INSERT INTO medicine_stock
#                         VALUES (?, ?, ?, ?, ?, ?)
#                         """,
#                         (
#                             str(uuid.uuid4()),
#                             new_facility,
#                             new_name.strip(),
#                             new_quantity,
#                             new_unit,
#                             datetime.now().isoformat(),
#                         ),
#                     )

#                     conn.commit()
#                     conn.close()

#                     st.success(
#                         f"Added {new_name} "
#                         f"({new_quantity} {new_unit}) "
#                         f"to {new_facility}."
#                     )

#                     st.rerun()
