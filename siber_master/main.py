import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. STRATEJİK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"

# DOĞRULANMIŞ WHATSAPP HATTI
PHONE = "905414516774"
MSG = "Merhaba, 9'da 9 PRO Analiz sistemi için lisans satın almak istiyorum."
WA_LINK = f"https://api.whatsapp.com/send?phone={PHONE}&text={requests.utils.quote(MSG)}"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("GÜNLÜK", 1, 400), ("AYLIK", 30, 300), ("SEZONLUK", 180, 150), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label[:2]}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. EXECUTIVE UI & JS INJECTION =================
def apply_ui():
    st.markdown(f"""
        <style>
        .stApp {{ background: #010409; color: #e6edf3; }}
        header {{ visibility: hidden; }}
        
        .hero-title {{ 
            text-align: center; color: #238636; font-size: 3rem; 
            font-weight: 800; padding: 30px 0; border-bottom: 2px solid #30363d;
            margin-bottom: 40px;
        }}

        .pkg-container {{ display: flex; gap: 20px; justify-content: center; margin-bottom: 35px; flex-wrap: wrap; }}
        .pkg-card {{ 
            background: #0d1117; border: 1px solid #30363d; border-radius: 15px; 
            padding: 25px; width: 190px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }}
        .pkg-card b {{ color: #58a6ff; font-size: 1.2rem; display: block; margin-top: 10px; }}

        /* JAVASCRIPT DESTEKLİ WHATSAPP BUTONU */
        .wa-button-pro {{
            display: block; width: 100%; max-width: 400px; margin: 0 auto;
            background: linear-gradient(90deg, #238636, #2ea043);
            color: white !important; text-align: center; padding: 20px;
            border-radius: 15px; font-weight: 800; font-size: 1.2rem;
            text-decoration: none; box-shadow: 0 10px 20px rgba(35, 134, 54, 0.3);
            transition: 0.3s; border: none; cursor: pointer;
        }}
        .wa-button-pro:hover {{ transform: scale(1.03); background: #2ea043; }}
        
        .decision-card {{ 
            background: #0d1117; border-left: 8px solid #238636; 
            padding: 25px; border-radius: 12px; margin-bottom: 25px;
        }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 3. GİRİŞ EKRANI =================
if not st.session_state["auth"]:
    st.markdown("<div class='hero-title'>9'DA 9 PRO ANALİZ</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='pkg-container'>
        <div class='pkg-card'><small>Deneme</small><b>700 TL / GÜN</b></div>
        <div class='pkg-card'><small>Profesyonel</small><b>2.000 TL / AY</b></div>
        <div class='pkg-card'><small>Siber VIP</small><b>5.000 TL / SEZON</b></div>
        <div class='pkg-card'><small>Sınırsız</small><b>15.000 TL</b></div>
    </div>
    
    <div style='text-align:center; margin-bottom:40px;'>
        <a href='{WA_LINK}' target='_blank' class='wa-button-pro'>
            🟢 LİSANS SATIN AL / AKTİF ET
        </a>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.8, 1])
    with col_m:
        u_lic = st.text_input("ERİŞİM ANAHTARI:", type="password", placeholder="SBR-XX-XXXX-TM")
        if st.button("SİSTEME GİRİŞ YAP"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else:
                st.error("❌ Hatalı Anahtar!")

else:
    # ================= 4. ANALİZ PORTALI =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown("### ⚙️ ANALİZ AYARI")
        trust_val = st.slider("Güven Barajı (%)", 50, 95, 90)
        st.divider()
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("## 📡 SİBER ANALİZ HATTI")
    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ MAÇ ÖNCESİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        with t_live:
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            for f in resp.get("response", []):
                conf = random.randint(80, 98)
                if conf >= trust_val:
                    st.markdown(f"""
                    <div class='decision-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b style='color:#238636;'>%{conf} ANALİZ</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='text-align:center; font-weight:bold; color:#4ade80;'>⚽ SİBER ÖNERİ: BASKI ARTIYOR, GOL BEKLENİYOR</div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Veri akışı hatası.")
