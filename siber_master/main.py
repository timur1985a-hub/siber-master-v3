import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="SIBER RADAR V250", layout="wide")

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

# --- 2. DEĞİŞMEZ TASARIM (RENK UYUMU AKTİF) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    
    /* Global Buton Uyumu */
    .stButton>button {
        background-color: #0d1117 !important;
        border: 2px solid #2ea043 !important;
        color: #2ea043 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ea043 !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.4);
    }

    .hype-title { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 900; margin: 10px 0; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { 
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; 
        width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043;
    }
    .pkg-box b { color: #58a6ff; display: block; font-size: 0.9rem; }
    .wa-small {
        display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto;
        background: #238636; color: white !important; text-align: center; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 0.85rem; text-decoration: none;
    }
    .card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 6px solid #238636; }
    
    /* Yan Menü (Sidebar) Uyumu */
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- 3. GLOBAL YAN PANEL (HER AN ERİŞİLEBİLİR) ---
with st.sidebar:
    st.markdown("<h3 style='color:#2ea043; text-align:center;'>⚙️ KONTROL</h3>", unsafe_allow_html=True)
    if st.button("🧹 BELLEĞİ SİL", use_container_width=True, key="side_clear"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    if st.button("♻️ GÜNCELLE", use_container_width=True, key="side_refresh"):
        st.rerun()
    st.divider()
    if st.session_state.get("auth"):
        st.success(f"YETKİ: {st.session_state['role'].upper()}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state.clear()
            st.rerun()

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None, "active_key": None})

# --- 4. GİRİŞ PANELİ (SABİT ŞABLON) ---
if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t1, t2 = st.tabs(["🔑 GİRİŞ", "👨‍💻 MASTER"])
        with t1:
            u_in = st.text_input("Anahtar:", type="password", key="user_login")
            if st.button("SİSTEMİ AÇ", use_container_width=True):
                if u_in in VAULT:
                    st.session_state.update({"auth": True, "role": "user", "active_key": u_in}); st.rerun()
        with t2:
            a_t = st.text_input("Token:", type="password", key="admin_token")
            a_p = st.text_input("Şifre:", type="password", key="admin_pass")
            if st.button("ADMİN GİRİŞİ", use_container_width=True):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS: st.session_state.update({"auth": True, "role": "admin"}); st.rerun()
    
    # Ana Ekran Kurtarma Butonları (Renk Uyumlu)
    st.markdown("<br><p style='text-align:center; color:#58a6ff; font-size:0.8rem;'>Hata durumunda aşağıdaki butonları kullanın.</p>", unsafe_allow_html=True)
    col_x, col_y = st.columns(2)
    with col_x:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True, key="main_clear"):
            st.cache_data
