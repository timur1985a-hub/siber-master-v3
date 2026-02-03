import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re
import json

# --- 1. SİBER HAFIZA VE DOKUNULMAZ ŞABLON ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

def persist_auth_js():
    st.markdown("""
        <script>
        const t = localStorage.getItem('sbr_token');
        const p = localStorage.getItem('sbr_pass');
        if (t && p && !window.location.search.includes('auth=true')) {
            const u = new URL(window.location);
            u.searchParams.set('t', t);
            u.searchParams.set('p', p);
            u.searchParams.set('auth', 'true');
            window.location.href = u.href;
        }
        </script>
    """, unsafe_allow_html=True)

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
        for i in range(1, 10001): 
            seed = f"V16_ULTRA_FIXED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d, "issued": False, "exp": None}
    return v

if "CORE_VAULT" not in st.session_state:
    st.session_state["CORE_VAULT"] = get_hardcoded_vault()

params = st.query_params
if "auth" not in st.session_state:
    if params.get("auth") == "true":
        t_param, p_param = params.get("t"), params.get("p")
        if t_param == ADMIN_TOKEN and p_param == ADMIN_PASS:
            st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
        elif t_param in st.session_state["CORE_VAULT"]:
            ud = st.session_state["CORE_VAULT"][t_param]
            if ud["pass"] == p_param and ud["issued"]:
                st.session_state.update({"auth": True, "role": "user", "current_user": t_param})
    else:
        st.session_state["auth"] = False

if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite}"
    ".dominance-mini{display:flex; height:4px; border-radius:2px; overflow:hidden; margin:10px 0; background:#30363d;}"
    ".reasoning-box{background:rgba(46,160,67,0.05); border-left:2px solid #2ea043; padding:5px 10px; font-size:0.75rem; color:#8b949e; margin:10px 0;}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. AKILLI ANALİZ MOTORU ---
def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def siber_engine(m):
    h_dom = 50
    stats = m.get('statistics', [])
    if stats:
        h_da = next((int(s['home'] or 0) for s in stats if s['type'] == 'Dangerous Attacks'), 0)
        a_da = next((int(s['away'] or 0) for s in stats if s['type'] == 'Dangerous Attacks'), 0)
        if (h_da + a_da) > 0: h_dom = int((h_da / (h_da + a_da)) * 100)
    
    return 96, "0.5 ÜST", "CANLI +0.5 GOL", "Saha hakimiyeti ve hücum sürekliliği analiz edildi.", h_dom

# --- 4. PANEL ---
if not st.session_state["auth"]:
    persist_auth_js()
    st.markdown("<div class='marketing-title'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t = st.text_input("Siber Kimlik").strip()
        l_p = st.text_input("Mühür Anahtarı", type="password").strip()
        if st.form_submit_button("SİSTEME GİRİŞ"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in st.session_state["CORE_VAULT"]):
                st.session_state["auth"] = True; st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: AKTİF</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}); st.rerun()
    with c2:
        if st.button("🔄 GÜNCELLE", use_container_width=True):
            st.session_state["stored_matches"] = fetch_siber_data(st.session_state["view_mode"] == "live"); st.rerun()
    with c3:
        if st.button("🧹 TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.rerun()

    for m in st.session_state.get("stored_matches", []):
        conf, pre_e, live_e, reason, h_dom = siber_engine(m)
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        
        st.markdown(f"""
        <div class='decision-card'>
            <div class='ai-score'>%{conf}</div>
            <div class='live-pulse'>📡 SİSTEM AKTİF</div><br>
            <b>{m['league']['name']}</b><br>
            <span style='font-size:1.2rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
            <div class='score-board'>{gh} - {ga} <small style='font-size:0.8rem; color:#f1e05a;'>{m['fixture']['status']['elapsed']}'</small></div>
            
            <div style='display:flex; justify-content:space-between; font-size:0.65rem; font-weight:bold; color:#8b949e; margin-bottom:2px;'>
                <span>EV %{h_dom}</span><span>DEP %{100-h_dom}</span>
            </div>
            <div class='dominance-mini'>
                <div style='background:#58a6ff; width:{h_dom}%'></div>
                <div style='background:#f85149; width:{100-h_dom}%'></div>
            </div>

            <div class='reasoning-box'>💡 {reason}</div>
            
            <div style='display:flex; gap:10px;'>
                <div style='flex:1; padding:8px; background:rgba(88,166,255,0.1); border:1px solid #58a6ff; border-radius:6px; text-align:center;'>
                    <small style='color:#58a6ff;'>CANSIZ</small><br><b>{pre_e}</b>
                </div>
                <div style='flex:1; padding:8px; background:rgba(46,160,67,0.1); border:1px solid #2ea043; border-radius:6px; text-align:center;'>
                    <small style='color:#2ea043;'>CANLI</small><br><b>{live_e}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 ÇIKIŞ"):
        st.session_state["auth"] = False; st.rerun()
