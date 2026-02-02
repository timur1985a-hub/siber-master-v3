import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - PRO STRATEGIC", layout="wide")

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
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
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
    q_t = st.query_params.get("s_t")
    q_p = st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM ---
style_code = """<style>.stApp{background-color:#010409;color:#e6edf3}header{visibility:hidden}.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;padding:15px 0;margin-bottom:25px;overflow:hidden}.marquee-text{display:inline-block;white-space:nowrap;padding-left:100%;animation:marquee 100s linear infinite}.match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900}.marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900}.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}.decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px}.ai-score{float:right;font-size:1.5rem;font-weight:900}.score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;display:inline-block;margin:10px 0}.pressure-bg{background:#30363d;height:8px;width:100%;border-radius:10px;margin-top:10px}.pressure-fill{height:8px;border-radius:10px;transition:width 0.5s}.unit-box{background:rgba(88,166,255,0.1);border:1px dashed #58a6ff;padding:5px;border-radius:6px;font-size:0.9rem;color:#58a6ff;margin-top:10px;text-align:center;font-weight:bold}.wa-small{display:block;width:100%;max-width:300px;margin:10px auto;background:#238636;color:#fff!important;text-align:center;padding:10px;border-radius:8px;font-weight:700;text-decoration:none}.pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}.pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}.live-minute{color:#f1e05a;border:1px solid #f1e05a;padding:2px 6px;border-radius:4px;font-family:monospace;font-weight:900}.tsi-time{color:#f1e05a;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px}</style>"""
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc
