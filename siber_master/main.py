import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= PROFESYONEL KOYU TEMA (HİÇ BEYAZ YOK) =================
def apply_ultra_dark_theme():
    st.markdown("""
        <style>
        /* Ana Arka Plan: Koyu Gece Mavisi */
        .stApp {
            background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
            color: #f1f5f9;
        }
        
        /* Sekmeler (Tabs): Beyazlığı Yok Et */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent;
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px 10px 0 0;
            color: #94a3b8 !important;
            padding: 10px 20px;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(56, 189, 248, 0.2) !important;
            color: #38bdf8 !important;
            border-bottom: 2px solid #38bdf8 !important;
        }

        /* Giriş Kutuları: Beyaz Yazı ve Koyu Arka Plan */
        .stTextInput input {
            background-color: #1e293b !important;
            color: #38bdf8 !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }
        .stTextInput label {
            color: #94a3b8 !important;
            font-weight: bold;
        }

        /* Kartlar (Glassmorphism) */
        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        }

        /* Butonlar: Neon Mavi */
        div.stButton > button {
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            color: white !important;
            border: none;
            border-radius: 12px;
            padding: 15px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6);
        }
        </style>
    """, unsafe_allow_html=True)

# ================= SİBER AYARLAR & LİSANS MOTORU (SABİT) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= ARAYÜZ KURULUM =================
st.set_page_config(page_title="Siber Master V2900", layout="wide")
apply_ultra_dark_theme()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8; margin-bottom:0;'>🛡️ SİBER MASTER PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>V2900 Elite Muhakeme Sistemi</p>", unsafe_allow_html=True)
    
    # VIP Paket Kartları
    cols = st.columns(5)
    pk_data = [("700 TL", "1 Ay"), ("2000 TL", "3 Ay"), ("5000 TL", "6 Ay"), ("8000 TL", "12 Ay"), ("10.000 TL", "Sınırsız")]
    for i, (p, d) in enumerate(pk_data):
        with cols[i]:
            st.markdown(f"<div class='glass-card' style='text-align:center; padding:15px;'><b style='color:#94a3b8;'>{d}</b><br><span style='color:#38bdf8; font-size:1.2rem; font-weight:bold;'>{p}</span></div>", unsafe_allow_html=True)

    # Giriş Paneli (Cam Kart İçinde)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 LİSANS GİRİŞİ", "👨‍💻 YÖNETİCİ GİRİŞİ"])
    
    with t1:
        u_lic = st.text_input("Anahtarınızı Buraya Girin:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZ MOTORUNU AÇ"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Geçersiz Lisans Anahtarı!")
            
    with t2:
        st.markdown("<p style='color:#94a3b8; font-size:0.8rem;'>Yönetici erişimi için token ve şifre gereklidir.</p>", unsafe_allow_html=True)
        a_t = st.text_input("Admin Token:", type="password", key="admin_t")
        a_p = st.text_input("Admin Şifre:", type="password", key="admin_p")
        if st.button("ADMİN PANELİNE BAĞLAN"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()
            else: st.error("🛑 Yetkisiz Erişim!")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ================= CANLI PANEL (FULL PRO) =================
    with st.sidebar:
        st.markdown("<h3 style='color:#38bdf8;'>⚙️ KOMUTA</h3>", unsafe_allow_html=True)
        trust_score = st.slider("Güven Eşiği (%)", 50, 95, 85)
        
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small style='color:#94a3b8;'>Süre:</small><br><b style='color:#4ade80;'>{rem.days} GÜN</b></div>", unsafe_allow_html=True)
        
        if st.session_state["role"] == "admin":
            st.divider()
            p_sel = st.selectbox("Paket Seç:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == p_sel]
            st.text_area("Satışa Hazır Kodlar:", value="\n".join(keys), height=200)
            
        if st.button("🔴 ÇIKIŞ YAP"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color: #38bdf8;'>🏆 CANLI ANALİZ VE MUHAKEME</h2>", unsafe_allow_html=True)
    

    # Dinamik Analiz Kartı
    st.markdown(f"""
        <div class='glass-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span style='color: #64748b;'>78' Dakika | Elite Analiz</span>
                <span style='color: #4ade80; font-weight:bold;'>%{trust_score} GÜVEN</span>
            </div>
            <div style='text-align:center; margin: 20px 0;'>
                <h2 style='color:white; margin:0;'>LIVERPOOL 2 - 2 REAL MADRID</h2>
                <p style='color:#38bdf8; margin-top:10px;'><b>AI MUHAKEME:</b> Baskı %88 seviyesine çıktı. Real Madrid kontra atak kovalıyor!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
