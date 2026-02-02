import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

@st.cache_resource
def get_hardcoded_vault():
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d, "issued": False, "exp": None}
    return v

def siber_normalize(text):
    if not text: return ""
    text = str(text).lower()
    text = text.replace('ı', 'i').replace('ç', 'c').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o')
    return re.sub(r'[^a-z0-9]', '', text)

if "CORE_VAULT" not in st.session_state:
    st.session_state["CORE_VAULT"] = get_hardcoded_vault()

if "PERMANENT_ARCHIVE" not in st.session_state:
    st.session_state["PERMANENT_ARCHIVE"] = {}

if "auth" not in st.session_state: st.session_state["auth"] = False
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ (MİLİMETRİK) ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800;margin-top:10px}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".license-card{background:#161b22;border:1px solid #30363d;padding:12px;border-radius:8px;margin-bottom:10px;border-left:4px solid #f1e05a}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".tsi-time{color:#f1e05a!important;font-family:'Courier New',monospace;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px;border:1px solid rgba(241,224,90,0.2)}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #f85149;box-shadow: 0 4px 15px rgba(0,0,0,0.5)}"
    ".stat-val{font-size:2rem;font-weight:900;color:#2ea043}"
    ".stat-lbl{font-size:0.75rem;color:#8b949e;text-transform:uppercase;font-weight:bold;letter-spacing:1px}"
    ".search-box-style{background:#0d1117; border:1px solid #2ea043; border-radius:8px; padding:5px; margin-bottom:15px;}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. SİBER ANALİZ MOTORU ---
def check_success(emir, score_str):
    try:
        gh, ga = map(int, score_str.split('-'))
        total = gh + ga
        if "2.5 ÜST" in emir: return total > 2
        if "1.5 ÜST" in emir: return total > 1
        if "0.5 ÜST" in emir: return total > 0
        if "KG VAR" in emir: return gh > 0 and ga > 0
        if "1X" in emir: return gh >= ga
        if "X2" in emir: return ga >= gh
        return False
    except: return False

def advanced_decision_engine(m):
    league = m['league']['name'].upper()
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total, elapsed = gh + ga, m['fixture']['status']['elapsed'] or 0
    is_high = any(x in league for x in ["BUNDES", "EREDI", "ELITE", "AUSTRIA", "ICELAND", "U19", "U21"])
    pre_emir, conf = ("1.5 ÜST", 92) if is_high else ("0.5 ÜST", 90)
    if elapsed > 0:
        if elapsed < 35: live_emir = "İY 0.5 ÜST" if total == 0 else "1.5 ÜST"
        elif 35 <= elapsed < 70: live_emir = "0.5 ÜST" if total == 0 else "KG VAR"
        else: live_emir = "0.5 ÜST (SİBER)"
    else: live_emir = "0.5 ÜST"
    return conf, pre_emir, live_emir

def fetch_siber_data(live=True):
    try:
        url = f"{BASE_URL}/fixtures?live=all" if live else f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

# --- 4. PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='internal-welcome'>TIMUR AI - STRATEGIC ACCESS</div>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t = st.text_input("Token:", type="password").strip()
        l_p = st.text_input("Pass:", type="password").strip()
        if st.form_submit_button("SİSTEME GİR"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in st.session_state["CORE_VAULT"] and st.session_state["CORE_VAULT"][l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    # Navigasyon (Tam Liste)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: 
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True): 
            st.session_state["stored_matches"] = fetch_siber_data(True)
            st.session_state["view_mode"] = "live"
            st.rerun()
    with c2: 
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True): 
            st.session_state["stored_matches"] = fetch_siber_data(False)
            st.session_state["view_mode"] = "pre"
            st.rerun()
    with c3: 
        if st.button("🔄 GÜNCELLE", use_container_width=True): 
            st.session_state["stored_matches"] = fetch_siber_data(st.session_state["view_mode"] == "live")
            st.rerun()
    with c4: 
        if st.button("📜 SİBER ARŞİV", use_container_width=True): st.session_state["view_mode"] = "archive"; st.rerun()
    with c5: 
        if st.session_state["role"] == "admin":
            if st.button("🔑 LİSANS DAĞIT", use_container_width=True): st.session_state["view_mode"] = "admin_vault"; st.rerun()
        else:
            if st.button("🧹 TEMİZLE", use_container_width=True): 
                st.session_state["stored_matches"] = []
                st.session_state["view_mode"] = "clear"
                st.rerun()

    # Arama Çubuğu
    st.markdown("<div class='search-box-style'>", unsafe_allow_html=True)
    search_input = st.text_input("🔍 TAKIM VEYA LİG ARA:", placeholder="Fenerbahçe, Madrid...").strip()
    st.markdown("</div>", unsafe_allow_html=True)

    # Arşiv İşleme
    for m in st.session_state.get("stored_matches", []):
        fid = str(m['fixture']['id'])
        conf, p_e, l_e = advanced_decision_engine(m)
        st.session_state["PERMANENT_ARCHIVE"][fid] = {
            "fid": fid, "conf": conf, "league": m['league']['name'], "home": m['teams']['home']['name'], 
            "away": m['teams']['away']['name'], "date": to_tsi(m['fixture']['date']), 
            "pre_emir": p_e, "live_emir": l_e, "score": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", 
            "status": m['fixture']['status']['short']
        }

    # Filtreleme
    if st.session_state["view_mode"] == "archive":
        display_list = list(st.session_state["PERMANENT_ARCHIVE"].values())
    else:
        current_ids = [str(m['fixture']['id']) for m in st.session_state.get("stored_matches", [])]
        display_list = [v for k, v in st.session_state["PERMANENT_ARCHIVE"].items() if k in current_ids]

    if search_input:
        nq = siber_normalize(search_input)
        display_list = [x for x in display_list if nq in siber_normalize(x['home']) or nq in siber_normalize(x['away']) or nq in siber_normalize(x['league'])]

    # Başarı Paneli
    finished = [d for d in st.session_state["PERMANENT_ARCHIVE"].values() if d['status'] in ['FT', 'AET', 'PEN']]
    if finished and st.session_state["view_mode"] != "clear":
        p_ok = sum(1 for d in finished if check_success(d['pre_emir'], d['score']))
        l_ok = sum(1 for d in finished if check_success(d['live_emir'], d['score']))
        st.markdown(f"<div class='stats-panel'><div><div class='stat-val'>{len(finished)}</div><div class='stat-lbl'>Siber Kayıt</div></div><div><div class='stat-val' style='color:#58a6ff;'>%{ (p_ok/len(finished))*100:.1f}</div><div class='stat-lbl'>Cansız Başarı</div></div><div><div class='stat-val' style='color:#2ea043;'>%{ (l_ok/len(finished))*100:.1f}</div><div class='stat-lbl'>Canlı Başarı</div></div></div>", unsafe_allow_html=True)

    # --- LİSANS SİSTEMİ (MİLİMETRİK GERİ YÜKLENDİ) ---
    if st.session_state["view_mode"] == "admin_vault" and st.session_state["role"] == "admin":
        st.markdown("### 🗄️ LİSANS DAĞITIM SİSTEMİ")
        now = datetime.now(pytz.timezone("Europe/Istanbul"))
        tabs = st.tabs(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
        for i, pkg in enumerate(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"]):
            with tabs[i]:
                pkg_lics = {k: v for k, v in st.session_state["CORE_VAULT"].items() if v["label"] == pkg}
                for t, info in pkg_lics.items():
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        exp_txt = f"⌛ KALAN: {(info['exp'] - now).days} GÜN" if info["issued"] else "⚪ BEKLEMEDE"
                        st.markdown(f"<div class='license-card'><b>{t}</b> | Pass: {info['pass']}<br><small>{exp_txt}</small></div>", unsafe_allow_html=True)
                    with col_b:
                        if not info["issued"]:
                            if st.button("DAĞIT", key=f"d_{t}"):
                                st.session_state["CORE_VAULT"][t].update({"issued": True, "exp": now + timedelta(days=info["days"])})
                                st.rerun()
    elif st.session_state["view_mode"] != "clear":
        for arc in display_list:
            is_fin = arc['status'] in ['FT', 'AET', 'PEN']
            win_p = "✅" if check_success(arc['pre_emir'], arc['score']) else ("❌" if is_fin else "")
            win_l = "✅" if check_success(arc['live_emir'], arc['score']) else ("❌" if is_fin else "")
            st.markdown(f"<div class='decision-card'><div class='ai-score'>%{arc['conf']}</div><b style='color:#58a6ff;'>⚽ {arc['league']}</b> | <span class='tsi-time'>⌚ {arc['date']}</span><br><span style='font-size:1.2rem; font-weight:bold;'>{arc['home']} vs {arc['away']}</span><br><div class='score-board'>{arc['score']}</div><div style='display:flex; gap:10px;'><div style='flex:1; background:rgba(88,166,255,0.05); padding:8px; border-radius:6px; border:1px solid #30363d;'><small>CANSIZ</small><br><b>{arc['pre_emir']}</b> {win_p}</div><div style='flex:1; background:rgba(46,160,67,0.05); padding:8px; border-radius:6px; border:1px solid #2ea043;'><small>CANLI</small><br><b>{arc['live_emir']}</b> {win_l}</div></div></div>", unsafe_allow_html=True)

    # Güvenli Çıkış
    if st.button("🔴 GÜVENLİ ÇIKIŞ", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()
