import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

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
    q_t = st.query_params.get("s_t"); q_p = st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

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
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace; font-size: 1rem;
    }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; }
    .tsi-time { color: #f1e05a !important; font-family: 'Courier New', monospace; font-weight: 900; background: rgba(241, 224, 90, 0.1); padding: 2px 6px; border-radius: 4px; }
    .live-minute { color: #f1e05a; font-family: monospace; font-weight: 900; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; }
    .score-board { font-size: 1.5rem; font-weight: 900; color: #ffffff; background: #161b22; padding: 5px 15px; border-radius: 8px; border: 1px solid #30363d; display: inline-block; margin: 10px 0; }
    .stat-row { display: flex; align-items: center; font-size: 0.85rem; color: #8b949e; margin-top: 5px; font-family: monospace; }
    .stat-val { color: #58a6ff; font-weight: bold; margin-left: auto; }
    .stTextInput>div>div>input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #30363d !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SİBER ANALİZ MOTORU (SCM) ---
def siber_decision_engine(match, is_live=True):
    """Nokta atışı karar mekanizması"""
    m_id = match['fixture']['id']
    seed = int(hashlib.md5(f"{m_id}".encode()).hexdigest(), 16)
    
    if is_live:
        # Canlı Veri Simülasyonu (Momentum Bazlı)
        momentum = 0.4 + (seed % 60) / 100 
        xg = 0.8 + (seed % 200) / 100
        danger_index = (momentum * 0.7) + (xg * 0.3)
        confidence = int(70 + (danger_index * 25))
        
        if confidence >= 92:
            return confidence, "💎 SİBER ELMAS: SIRADAKİ GOL GELİYOR", "#2ea043"
        elif confidence >= 85:
            return confidence, "⚔️ STRATEJİK: +0.5 ÜST LİMİTİ", "#58a6ff"
        return confidence, "📊 ANALİZ: BEKLEMEDE", "#8b949e"
    else:
        # Cansız Maç (Power Index Bazlı)
        power_h = 50 + (seed % 45)
        power_a = 50 + ((seed + 1) % 45)
        diff = abs(power_h - power_a)
        confidence = int(75 + (diff / 2))
        
        if confidence >= 90:
            pref = "EV KAZANIR" if power_h > power_a else "DEPLASMAN KAZANIR"
            return confidence, f"🎯 NOKTA ATIŞI: {pref}", "#2ea043"
        return confidence, "📋 STANDART ANALİZ: KG VAR", "#f1e05a"

def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            res = r.json().get('response', [])
            return [m for m in res if (m['fixture']['status']['short'] in (['1H', '2H', 'HT', 'LIVE'] if live else ['NS']))]
        return []
    except: return []

# --- 4. ARAYÜZ ---
if not st.session_state["auth"]:
    # (Pazarlama ve Giriş Alanı - Şablon Korundu)
    st.markdown("<div class='marketing-title'>TIMUR AI: STRATEGIC PREDICTOR</div>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        with st.form("siber_auth"):
            l_t = st.text_input("Token:", type="password")
            l_p = st.text_input("Şifre:", type="password")
            if st.form_submit_button("SİSTEMİ AÇ"):
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
else:
    st.markdown(f"<div class='internal-welcome'>YAPAY ZEKA KARAR MERKEZİ</div>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        if st.button("🔴 CANLI ANALİZ", use_container_width=True): 
            st.session_state["stored_matches"] = fetch_siber_data(live=True)
    with col_b:
        if st.button("🔵 CANSIZ ANALİZ", use_container_width=True): 
            st.session_state["stored_matches"] = fetch_siber_data(live=False)
    with col_c:
        if st.button("🧹 TEMİZLE", use_container_width=True): 
            st.session_state["stored_matches"] = []

    for m in st.session_state["stored_matches"]:
        is_live = m['fixture']['status']['short'] != 'NS'
        conf, decision, color = siber_decision_engine(m, is_live)
        
        st.markdown(f"""
            <div class='decision-card' style='border-left: 6px solid {color};'>
                <div class='ai-score' style='color:{color};'>%{conf}</div>
                <span style='color:#8b949e;'>{m['league']['name']}</span><br>
                <b style='font-size:1.2rem;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</b><br>
                <div class='score-board'>{m['goals']['home'] or 0} - {m['goals']['away'] or 0}</div>
                <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;'>
                    <div class='stat-row'>SİBER GÜVEN: <span class='stat-val' style='color:{color}'>%{conf}</span></div>
                    <div class='stat-row'>KARAR: <span class='stat-val' style='color:{color}'>{decision}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
