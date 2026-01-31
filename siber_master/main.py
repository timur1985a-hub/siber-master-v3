import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE KESİN GİRİŞ PROTOKOLÜ (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"

# Mühürlü Admin Bilgileri
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_hardcoded_vault():
    """V16 Şifre Politikası: Değişmez lisans üretim merkezi."""
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

if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---"
    })

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        box-shadow: 0px 0px 15px rgba(248, 81, 73, 0.2); padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace;
        box-shadow: inset 0px 0px 5px rgba(248, 81, 73, 0.3); font-size: 1rem;
    }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043; }
    .wa-small { display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto; background: #238636; color: white !important; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .tsi-time { color: #f1e05a; font-family: monospace; font-weight: bold; border: 1px solid rgba(241, 224, 90, 0.4); padding: 2px 4px; border-radius: 4px; }
    .live-minute { color: #f1e05a; font-family: monospace; font-weight: 900; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }
    .live-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink 1s infinite; }
    .stat-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: #8b949e; margin-top: 5px; font-family: monospace; }
    .stat-val { color: #58a6ff; font-weight: bold; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR VE VERİ MOTORU ---
def to_tsi(utc_str):
    try:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S+00:00")
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "00:00"

@st.cache_data(ttl=60)
def fetch_data_from_api():
    try:
        now_utc = datetime.utcnow()
        today = now_utc.strftime("%Y-%m-%d")
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": today, "timezone": "UTC"}, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            all_data = r.json().get('response', [])
            filtered = []
            for m in all_data:
                status = m['fixture']['status']['short']
                m_date_utc = datetime.strptime(m['fixture']['date'], "%Y-%m-%dT%H:%M:%S+00:00")
                if status in ['FT', 'AET', 'PEN', 'ABD', 'CANCL', 'PST']: continue
                if status in ['1H', '2H', 'HT', 'LIVE'] and (now_utc - m_date_utc).total_seconds() > 9000: continue
                filtered.append(m)
            return filtered
        return []
    except: return []

# ---
