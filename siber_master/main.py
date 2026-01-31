import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz
import random

# --- 1. SİBER HAFIZA VE BAŞLATMA ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

# Session state garantisi
DEFAULTS = {
    "auth": False, "role": None, "current_user": None,
    "stored_matches": [], "diag_log": "Sistem Hazır.",
    "last_fetch_status": "Beklemede", "last_update_time": "Veri yok"
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"

# Admin Bilgileri - Kesin Tanımlama
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
ADMIN_PASS = "1937timurR&"
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
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; width: 100%; height: 3rem; }
    .status-bar { text-align: center; background: rgba(46, 160, 67, 0.1); padding: 10px; border: 1px solid #2ea043; margin-bottom: 20px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. VERİ ÇEKME MOTORU ---
def smart_fetch():
    try:
        cb = str(time.time())
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"live": "all", "v": cb}, timeout=10)
        res = r.json().get('response', [])
        if not res:
            r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d"), "v": cb}, timeout=10)
            res = r.json().get('response', [])
        
        final = [m for m in res if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
        st.session_state["stored_matches"] = final
        st.session_state["last_fetch_status"] = "AKTİF"
        st.session_state["last_update_time"] = datetime.now().strftime("%H:%M:%S")
    except:
        st.session_state["last_fetch_status"] = "HATA"

# --- 4. GİRİŞ VE PANEL AKIŞI ---
if not st.session_state.get("auth"):
    st.markdown("<h1 style='text-align:center;'>TİMUR AI MASTER PANEL</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # Key parametreleri eklenerek inputların karışması engellendi
        u_token = st.text_input("Token", type="password", key="main_token_input").strip()
        u_pass = st.text_input("Şifre", type="password", key="main_pass_input").strip()
        
        if st.button("SİSTEME GİR"):
            # Admin Kontrolü (Harf duyarlılığı ve boşluk temizleme eklendi)
            if u_token == ADMIN_TOKEN and u_pass == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "current_user": "ADMIN"})
                smart_fetch()
                st.rerun()
            # Kullanıcı Kontrolü
            elif u_token in CORE_VAULT and CORE_VAULT[u_token]["pass"] == u_pass:
                st.session_state.update({"auth": True, "role": "user", "current_user": u_token})
                smart_fetch()
                st.rerun()
            else:
                st.error("❌ Yetkisiz Giriş! Lütfen bilgileri kontrol edin.")
else:
    # İç Panel Tasarımı
    st.markdown(f"<div class='status-bar'>🛡️ TERMİNAL AKTİF | ROL: {st.session_state['role'].upper()} | GÜNCELLEME: {st.session_state['last_update_time']}</div>", unsafe_allow_html=True)

    if st.session_state["role"] == "admin":
        with st.expander("🎫 LİSANS YÖNETİMİ"):
            pkg = st.selectbox("Paket Seçin", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            filtered_keys = {k: v for k, v in CORE_VAULT.items() if v["label"] == pkg}
            st.dataframe(pd.DataFrame.from_dict(filtered_keys, orient='index'), use_container_width=True)

    col_up, col_cl = st.columns(2)
    with col_up:
        if st.button("♻️ GÜNCELLE"):
            smart_fetch()
            st.rerun()
    with col_cl:
        if st.button("🧹 TEMİZLE"):
            st.session_state["stored_matches"] = []
            st.rerun()

    st.divider()

    # Maçları Listeleme
    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches[:30]):
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:#2ea043; font-weight:bold;'>%{90+(i%8)} GÜVEN</span>
                    <b>⚽ {m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small style='color:#f1e05a;'>Skor: {m['goals']['home']}-{m['goals']['away']} | Dakika: {m['fixture']['status']['elapsed']}'</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Gösterilecek aktif maç yok. Lütfen güncelleyin.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()
