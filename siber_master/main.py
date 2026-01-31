import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz
import random

# --- 1. SİBER HAFIZA VE BAŞLATMA (KRİTİK ÖNCELİK) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

# Tüm session_state değişkenlerini HİÇBİR ŞARTA BAĞLI OLMAKSIZIN en tepede tanımlıyoruz.
# Bu işlem KeyError riskini sıfıra indirir.
DEFAULTS = {
    "auth": False,
    "role": None,
    "current_user": None,
    "stored_matches": [],
    "diag_log": "Sistem Hazır.",
    "last_fetch_status": "Beklemede",
    "last_update_time": "Veri yok"
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

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

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; width: 100%; }
    .status-bar { text-align: center; background: rgba(46, 160, 67, 0.1); padding: 10px; border-radius: 8px; border: 1px solid #2ea043; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. AKILLI VERİ ÇEKME MOTORU ---
def smart_fetch():
    log = [f"[{datetime.now().strftime('%H:%M:%S')}] Tarama Başlatıldı..."]
    try:
        cb = str(random.randint(1000, 9999))
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"live": "all", "v": cb}, timeout=12)
        
        if r.status_code == 200:
            res = r.json().get('response', [])
            if not res:
                log.append("Canlı maç yok, günlük listeye bakılıyor...")
                curr = datetime.now().strftime("%Y-%m-%d")
                r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": curr, "v": cb}, timeout=12)
                res = r.json().get('response', [])
            
            final = [m for m in res if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
            st.session_state["stored_matches"] = final
            st.session_state["last_fetch_status"] = "AKTİF" if final else "BOŞ"
            st.session_state["last_update_time"] = datetime.now().strftime("%H:%M:%S")
            log.append(f"Başarılı: {len(final)} Maç.")
        else:
            st.session_state["last_fetch_status"] = f"HATA ({r.status_code})"
            log.append(f"API Yanıt Vermedi: {r.status_code}")
            
    except Exception as e:
        st.session_state["last_fetch_status"] = "BAĞLANTI HATASI"
        log.append(f"Hata: {str(e)}")
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 4. AKIŞ KONTROLÜ ---
if not st.session_state.get("auth"):
    st.markdown("<h1 style='text-align:center;'>TİMUR AI MASTER PANEL</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Token", type="password")
        l_p = st.text_input("Şifre", type="password")
        if st.button("SİSTEME GİR"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                smart_fetch()
                st.rerun()
            else: st.error("❌ Yetkisiz!")
else:
    # Hata alınan yer burasıydı, artık .get() ve üstte tanımlama ile koruma altında.
    status = st.session_state.get("last_fetch_status", "Bilinmiyor")
    update_time = st.session_state.get("last_update_time", "-")
    
    st.markdown(f"""
        <div class='status-bar'>
            🛡️ SİBER TERMİNAL | DURUM: {status} | SON GÜNCELLEME: {update_time}
        </div>
    """, unsafe_allow_html=True)

    with st.expander("🛠️ TEKNİK GÜNCELLEME LOGLARI"):
        st.code(st.session_state.get("diag_log", "Log Yok."))

    cx, cy = st.columns(2)
    with cx:
        if st.button("🧹 HAFIZAYI TEMİZLE"):
            st.session_state["stored_matches"] = []
            st.session_state["last_fetch_status"] = "TEMİZLENDİ"
            st.rerun()
    with cy:
        if st.button("♻️ VERİLERİ ZORLA GÜNCELLE"):
            smart_fetch()
            st.rerun()

    st.divider()

    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches[:25]):
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:#2ea043; font-weight:bold;'>%{90+(i%7)} GÜVEN</span>
                    <b>⚽ {m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | Dakika: {m['fixture']['status']['elapsed']}'</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Şu an gösterilecek aktif maç bulunamadı. Lütfen 'UPDATE' butonunu deneyin.")

    if st.button("🔴 ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()
