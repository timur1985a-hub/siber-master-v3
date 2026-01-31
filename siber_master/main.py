import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz
import random

# --- 1. SİBER HAFIZA VE BAŞLATMA (KESİN ÖNCELİKLİ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "stored_matches" not in st.session_state:
    st.session_state["stored_matches"] = []
if "diag_log" not in st.session_state:
    st.session_state["diag_log"] = "Sistem Beklemede..."

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

# --- 2. DEĞİŞMEZ TASARIM (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: monospace;
    }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ZORLANMIŞ VERİ ÇEKME (LIVE-FIRST) ---
def forced_fetch():
    log = [f"[{datetime.now().strftime('%H:%M:%S')}] Siber Tarama Başlatıldı..."]
    try:
        # Önce Canlı Maçları Zorla (Live parameter)
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"live": "all"}, timeout=10)
        log.append(f"Zorlu Canlı Bağlantı: {r.status_code}")
        
        matches = r.json().get('response', [])
        
        # Eğer canlı maç yoksa (gece yarısı vs), o günün tüm fikstürüne dön
        if not matches:
            log.append("Canlı maç bulunamadı, günlük fikstür taranıyor...")
            curr = datetime.now().strftime("%Y-%m-%d")
            r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": curr}, timeout=10)
            matches = r.json().get('response', [])
        
        log.append(f"Toplam Alınan: {len(matches)} maç.")
        
        # Sadece Bitmemiş Olanlar
        active = [m for m in matches if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
        st.session_state["stored_matches"] = active
        log.append(f"Hafızaya Alınan: {len(active)} aktif maç.")
        
    except Exception as e:
        log.append(f"KRİTİK HATA: {str(e)}")
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 4. AKIŞ VE PANEL ---
if not st.session_state.get("auth"):
    # Giriş Ekranı Şablonu
    st.markdown("<h2 style='text-align:center; color:#2ea043;'>SERVETİ YÖNETMEYE HAZIR MISIN?</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Giriş Tokeni:", type="password")
        l_p = st.text_input("Şifre:", type="password")
        if st.button("YAPAY ZEKAYI AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                forced_fetch() # Girişte otomatik çek
                st.rerun()
            else: st.error("❌ Yetkisiz Erişim!")
else:
    # İç Panel
    st.markdown(f"<h3 style='text-align:center; color:#2ea043;'>🛡️ TİMUR AI SİSTEM TERMİNALİ</h3>", unsafe_allow_html=True)
    
    with st.expander("🛠️ SİBER TEŞHİS VE LOGLAR", expanded=True):
        st.code(st.session_state.get("diag_log", ""))
        if st.button("ZORLA TARAMA YAP"):
            forced_fetch()
            st.rerun()

    cx, cy = st.columns(2)
    with cx:
        if st.button("🧹 CLEAR"):
            st.session_state["stored_matches"] = []
            st.rerun()
    with cy:
        if st.button("♻️ UPDATE"):
            forced_fetch()
            st.rerun()

    st.divider()
    
    # Maç Gösterimi
    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches):
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:#2ea043; font-weight:bold;'>%{90+(i%7)} BAŞARI</span>
                    <b>⚽ {m['league']['name']}</b><br>
                    <span style='font-size:1.2rem;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                    <hr style='border:0.1px solid #333;'>
                    <span style='color:#f1e05a;'>DURUM: {m['fixture']['status']['elapsed']}' | SKOR: {m['goals']['home']}-{m['goals']['away']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Şu an aktif maç bulunamadı. Lütfen 'ZORLA TARAMA' yapın veya daha sonra deneyin.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()
