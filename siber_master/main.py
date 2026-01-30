import streamlit as st
import requests
from datetime import datetime, timedelta
import hashlib

# --- 0. VERSİYON KONTROL ---
VERSION = "2.5.3-MOBILE-FIX" 

st.set_page_config(page_title="SIBER RADAR V250", layout="wide")

# Google Doğrulama (Görünmez)
st.markdown("""<div style="display:none;"><meta name="google-site-verification" content="8ffdf1f7bdb7adf3" /></div>""", unsafe_allow_html=True)

# --- 1. SİBER HAFIZA VE LİSANS ---
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

if "lic_db" not in st.session_state: st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            k = f"SBR-{lbl[:3]}-{hashlib.md5(f'V34_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            v[k] = {"label": lbl, "days": d}
    return v
VAULT = get_vault()

# --- 2. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .hype-title { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 900; margin: 10px 0; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { 
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; 
        width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043;
    }
    .wa-small {
        display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto;
        background: #238636; color: white !important; text-align: center; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 0.85rem; text-decoration: none;
    }
    .card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 6px solid #238636; }
    </style>
""", unsafe_allow_html=True)

# --- 3. GİRİŞ VE ANA KONTROL PANELİ (ORTA BÖLÜM) ---
if not st.session_state.get("auth"):
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    # BUTONLARI BURAYA (MOBİLDE HERKESİN GÖRECEĞİ YERE) ALDIM
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ SİL", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    with col_b:
        if st.button("♻️ GÜNCELLE", use_container_width=True):
            st.rerun()

    st.divider()
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_in = st.text_input("Anahtar:", type="password")
        if st.button("SİSTEMİ AÇ", use_container_width=True):
            if u_in in VAULT or u_in == ADMIN_PASS:
                st.session_state["auth"] = True
                st.rerun()
else:
    # Uygulama İçeriği (Giriş Yapılınca Burası Görünür)
    st.markdown("<h1 style='text-align:center;'>🎯 SİBER RADAR V250</h1>", unsafe_allow_html=True)
    if st.button("🔴 ÇIKIŞ YAP"):
        st.session_state.clear()
        st.rerun()
