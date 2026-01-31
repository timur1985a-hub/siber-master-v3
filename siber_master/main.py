import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz
import random

# --- 1. SİBER HAFIZA VE BAŞLATMA (KESİN ÖNCELİKLİ) ---
st.set_page_config(page_title="TIMUR AI - DIAGNOSTIC", layout="wide")

# Session State Değişkenlerini "Garantili" Başlatma
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "stored_matches" not in st.session_state:
    st.session_state["stored_matches"] = []
if "diag_log" not in st.session_state:
    st.session_state["diag_log"] = "Sistem Başlatıldı. Beklemede..."

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_hardcoded_vault():
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            seed = f"V16_FIXED_SEED_{lbl}_{i}"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

# --- 2. DEĞİŞMEZ TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .diag-box { background: #0d1117; border: 1px solid #f85149; padding: 10px; color: #f85149; font-family: monospace; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 3. TEŞHİS FONKSİYONU ---
def run_diagnostic_fetch():
    log = [f"[{datetime.now().strftime('%H:%M:%S')}] İstek Gönderiliyor..."]
    try:
        curr_date = datetime.now().strftime("%Y-%m-%d")
        r = requests.get(
            f"{BASE_URL}/fixtures", 
            headers=HEADERS, 
            params={"date": curr_date, "random": random.randint(1, 9999)}, 
            timeout=10
        )
        log.append(f"HTTP: {r.status_code}")
        if r.status_code == 200:
            data = r.json().get('response', [])
            log.append(f"Ham Veri: {len(data)} maç.")
            active = [m for m in data if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
            log.append(f"Aktif Veri: {len(active)} maç.")
            st.session_state["stored_matches"] = active
            log.append("Hafıza güncellendi.")
        else:
            log.append(f"Hata: {r.text[:100]}")
    except Exception as e:
        log.append(f"Hata: {str(e)}")
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 4. AKIŞ KONTROLÜ ---
if not st.session_state.get("auth"):
    st.title("TİMUR AI - LOGIN")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Token", type="password")
        l_p = st.text_input("Şifre", type="password")
        if st.button("SİSTEME GİR"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state["auth"] = True
                st.session_state["role"] = "admin" if l_t == ADMIN_TOKEN else "user"
                st.session_state["current_user"] = l_t
                st.rerun()
            else: st.error("Giriş Reddedildi.")
else:
    st.subheader("🛡️ TİMUR AI SİSTEM TERMİNALİ")
    
    # Teşhis Alanı - Hata Almaması İçin .get() Kullanıldı
    with st.expander("🛠️ SİSTEM LOGLARI", expanded=True):
        st.code(st.session_state.get("diag_log", "Log Bekleniyor..."))
        if st.button("VERİ BAĞLANTISINI ZORLA"):
            run_diagnostic_fetch()
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 HAFIZAYI SİL"):
            st.session_state["stored_matches"] = []
            st.session_state["diag_log"] = "Temizlendi."
            st.rerun()
    with col2:
        if st.button("♻️ GÜNCELLE"):
            run_diagnostic_fetch()
            st.rerun()

    st.divider()

    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches[:15]):
            st.markdown(f"""
                <div class='decision-card'>
                    <b>{m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | Dakika: {m['fixture']['status']['elapsed']}'</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Hafızada maç yok. 'GÜNCELLE' butonuna basın.")

    if st.button("EXIT"):
        st.session_state.clear()
        st.rerun()
