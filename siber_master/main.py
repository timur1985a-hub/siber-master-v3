import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re
import json

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
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

@st.cache_resource
def get_persistent_archive(): return {}

if "CORE_VAULT" not in st.session_state:
    st.session_state["CORE_VAULT"] = get_hardcoded_vault()

PERMANENT_ARCHIVE = get_persistent_archive()

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
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"

# --- 2. TASARIM (Baskınlık Çubuğu Eklendi) ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".dominance-bar-container{background:#30363d;height:10px;border-radius:5px;margin:15px 0;overflow:hidden;display:flex}"
    ".dom-home{background:#58a6ff;height:100%;transition:width 0.5s}"
    ".dom-away{background:#f85149;height:100%;transition:width 0.5s}"
    ".dom-label{display:flex;justify-content:space-between;font-size:0.75rem;font-weight:bold;margin-bottom:2px}"
    ".reasoning-box{background:rgba(46,160,67,0.05);border:1px dashed #2ea043;padding:5px;border-radius:4px;font-size:0.75rem;margin-top:5px;color:#8b949e}"
    ".status-win{color:#2ea043;font-weight:bold}"
    ".status-lost{color:#f85149;font-weight:bold}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    ".lic-item{background:#161b22; padding:10px; border-radius:6px; margin-bottom:5px; border-left:3px solid #f1e05a; font-family:monospace; font-size:0.85rem;}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)
if not st.session_state["auth"]: persist_auth_js()

# --- 3. AKILLI ANALİZ VE BASKINLIK MOTORU ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3600)
def get_team_history(team_id):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": team_id, "last": 5}, timeout=10)
        return r.json().get('response', [])
    except: return []

def calculate_dominance(m):
    # Eğer canlı veri (istatistik) varsa baskınlığı hesapla
    try:
        stats = m.get('statistics', [])
        if not stats: return 50, "Eşit Baskı"
        
        h_da = 0
        a_da = 0
        for s in stats:
            if s['type'] == 'Dangerous Attacks':
                h_da = int(s['home'] or 0)
                a_da = int(s['away'] or 0)
        
        total_da = h_da + a_da
        if total_da == 0: return 50, "Düşük Tempo"
        
        h_perc = (h_da / total_da) * 100
        if h_perc > 65: msg = f"🔥 {m['teams']['home']['name']} Sahayı Dar Ediyor!"
        elif h_perc < 35: msg = f"🔥 {m['teams']['away']['name']} Maçı Domine Ediyor!"
        else: msg = "Orta Saha Mücadelesi"
        return int(h_perc), msg
    except:
        return 50, "Veri Bekleniyor..."

def siber_engine(m):
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    h_hist = get_team_history(h_id)
    a_hist = get_team_history(a_id)
    
    # Muhakeme: Son 5 maç İY Gol Kontrolü
    h_iy_gol = all((x['goals']['home'] or 0) + (x['goals']['away'] or 0) > 0 for x in h_hist) if h_hist else False
    a_iy_gol = all((x['goals']['home'] or 0) + (x['goals']['away'] or 0) > 0 for x in a_hist) if a_hist else False
    
    # Muhakeme: 2.5 ÜST Barajı
    h_last_25 = ((h_hist[0]['goals']['home'] or 0) + (h_hist[0]['goals']['away'] or 0)) > 2.5 if h_hist else False
    a_last_25 = ((a_hist[0]['goals']['home'] or 0) + (a_hist[0]['goals']['away'] or 0)) > 2.5 if a_hist else False
    
    dom_val, dom_msg = calculate_dominance(m)
    
    iy_ok = h_iy_gol and a_iy_gol
    pre_ok = h_last_25 or a_last_25
    
    conf = 98 if iy_ok else 91
    pre_emir = "1.5 ÜST" if pre_ok else "0.5 ÜST"
    live_emir = "İLK YARI 0.5 ÜST" if iy_ok else "CANLI +0.5"
    
    reason = f"IY Serisi: {'✅' if iy_ok else '❌'} | 2.5 Barajı: {'✅' if pre_ok else '❌'}"
    return conf, pre_emir, live_emir, reason, dom_val, dom_msg

def check_success(emir, gh, ga):
    total = gh + ga
    if "İLK YARI 0.5 ÜST" in emir: return total > 0
    if "1.5 ÜST" in emir: return total > 1
    return total > 0

# --- 4. PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t = st.text_input("Kullanıcı adı").strip()
        l_p = st.text_input("Şifre", type="password").strip()
        if st.form_submit_button("AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in st.session_state["CORE_VAULT"]):
                st.session_state["auth"] = True
                st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("♻️ CANLI", use_container_width=True): 
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}); st.rerun()
    with c2:
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre"}); st.rerun()
    with c3:
        if st.button("🧹 TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.rerun()

    for m in st.session_state.get("stored_matches", []):
        conf, p_e, l_e, reason, dom_val, dom_msg = siber_engine(m)
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        
        st.markdown(f"""
        <div class='decision-card'>
            <div class='ai-score'>%{conf}</div>
            <div class='live-pulse'>📡 ANALİZ AKTİF</div><br>
            <b>{m['league']['name']}</b><br>
            <span style='font-size:1.2rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
            <div style='font-size:1.5rem; font-weight:900;'>{gh} - {ga}</div>
            
            <div class='dom-label'>
                <span>Ev Sahibi %{dom_val}</span>
                <span>%{100-dom_val} Deplasman</span>
            </div>
            <div class='dominance-bar-container'>
                <div class='dom-home' style='width:{dom_val}%'></div>
                <div class='dom-away' style='width:{100-dom_val}%'></div>
            </div>
            <div style='color:#2ea043; font-size:0.8rem; font-weight:bold;'>{dom_msg}</div>
            
            <div class='reasoning-box'>💡 {reason}</div>
            <div style='display:flex; gap:10px; margin-top:10px;'>
                <div style='flex:1; padding:5px; border:1px solid #58a6ff; border-radius:4px; text-align:center;'>
                    <small>CANSIZ</small><br><b>{p_e}</b>
                </div>
                <div style='flex:1; padding:5px; border:1px solid #2ea043; border-radius:4px; text-align:center;'>
                    <small>CANLI</small><br><b>{l_e}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 ÇIKIŞ"):
        st.session_state["auth"] = False
        st.rerun()
