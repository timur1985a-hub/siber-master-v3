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

if "MOMENTUM_TRACKER" not in st.session_state:
    st.session_state["MOMENTUM_TRACKER"] = {}

if "CORE_VAULT" not in st.session_state:
    st.session_state["CORE_VAULT"] = get_hardcoded_vault()

if "PERMANENT_ARCHIVE" not in st.session_state:
    st.session_state["PERMANENT_ARCHIVE"] = get_persistent_archive()

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
if "search_result" not in st.session_state: st.session_state["search_result"] = None

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}"
    ".marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}"
    ".match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-family:'Courier New',monospace;font-size:1rem}"
    "@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}"
    ".marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}"
    ".marketing-subtitle{text-align:center;color:#f85149;font-size:1.1rem;font-weight:700;margin-bottom:15px}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important;transition:all 0.1s ease-in-out!important;}"
    ".stButton>button:active{transform:scale(0.95)!important; background-color:#2ea043!important; color:#fff!important; box-shadow:0 0 15px rgba(46,160,67,0.4)!important;}"
    ".stButton>button:hover{border-color:#58a6ff!important; color:#58a6ff!important;}"
    ".pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}"
    ".pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}"
    ".pkg-price{color:#f1e05a;font-weight:800;font-size:0.9rem;margin-top:5px}"
    ".wa-small{display:block;width:100%;max-width:300px;margin:10px auto 20px auto;background:#238636;color:#fff!important;text-align:center;padding:12px;border-radius:8px;font-weight:700;text-decoration:none;border:1px solid #2ea043;transition:transform 0.1s;}"
    ".wa-small:active{transform:scale(0.95);}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite;margin-bottom:5px}"
    ".live-min-badge{background:rgba(241,224,90,0.1);color:#f1e05a;border:1px solid #f1e05a;padding:2px 8px;border-radius:4px;font-weight:bold;margin-left:10px;font-family:monospace}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #58a6ff;box-shadow:0 10px 20px rgba(0,0,0,0.4)}"
    ".stat-val{font-size:2.2rem;font-weight:900;color:#2ea043;line-height:1}"
    ".stat-lbl{font-size:0.8rem;color:#8b949e;text-transform:uppercase;font-weight:bold;margin-top:8px;letter-spacing:1px}"
    ".dom-container{background:rgba(46,160,67,0.05); border:1px solid #30363d; padding:12px; border-radius:8px; margin-top:10px;}"
    ".dom-bar-bg{height:8px; background:#30363d; border-radius:10px; margin:10px 0; overflow:hidden; display:flex;}"
    ".dom-bar-home{height:100%; background:#2ea043; transition:width 0.5s;}"
    ".dom-bar-away{height:100%; background:#f85149; transition:width 0.5s;}"
    ".search-box-sbr{border:1px solid #30363d; background:#0d1117; border-radius:8px; padding:10px; margin-bottom:20px; border-left:4px solid #58a6ff;}"
    ".siber-assistant-card{background:rgba(13,17,23,0.95); border:1px solid #2ea043; border-radius:15px; padding:15px; margin-top:20px; border-left:5px solid #2ea043; position:relative; overflow:hidden;}"
    ".siber-assistant-header{color:#2ea043; font-weight:800; font-size:1.1rem; display:flex; align-items:center; gap:8px; margin-bottom:10px; border-bottom:1px solid #30363d; padding-bottom:8px;}"
    ".siber-assistant-body{color:#8b949e; font-size:0.9rem; line-height:1.4;}"
    ".siber-assistant-highlight{color:#fff; font-weight:bold;}"
    ".siber-asistan-btn{background:#2ea043!important; color:#fff!important; width:100%; margin-top:10px; border-radius:8px!important; border:none!important; font-weight:800!important; transition:transform 0.1s!important;}"
    ".siber-asistan-btn:active{transform:scale(0.96)!important; opacity:0.8!important;}"
    ".iy-alarm{background:#f85149; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; animation:pulse-red 1s infinite; margin-left:10px;}"
    ".momentum-boost{color:#58a6ff; font-weight:bold; font-size:0.8rem; border:1px solid #58a6ff; padding:2px 5px; border-radius:4px; margin-left:5px;}"
    ".hybrid-target{background:#238636; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; margin-left:5px;}"
    ".hybrid-target-25{background:#f85149; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; margin-left:5px;}"
    ".hybrid-box{margin-top:10px; padding:8px; background:rgba(88,166,255,0.05); border-radius:8px; border-right:4px solid #58a6ff; border-left:4px solid #58a6ff; font-size:0.85rem;}"
    ".hybrid-label{color:#8b949e; font-size:0.7rem; text-transform:uppercase; font-weight:bold; display:block;}"
    ".hybrid-val{color:#fff; font-weight:800;}"
    "@keyframes pulse-red{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)
if not st.session_state["auth"]: persist_auth_js()

# --- 3. SİBER ANALİZ MOTORU ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        url = f"{BASE_URL}/fixtures?live=all" if live else f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def hybrid_search_engine(query):
    query = query.lower().strip()
    if not query: return []
    # 1. Aşama: Canlı Maçları Tara
    r_live = requests.get(f"{BASE_URL}/fixtures?live=all", headers=HEADERS, timeout=10)
    live_list = r_live.json().get('response', []) if r_live.status_code == 200 else []
    found = [m for m in live_list if query in m['teams']['home']['name'].lower() or query in m['teams']['away']['name'].lower()]
    
    # 2. Aşama: Canlıda yoksa bugünün tüm maçlarını tara
    if not found:
        today = datetime.now().strftime("%Y-%m-%d")
        r_today = requests.get(f"{BASE_URL}/fixtures?date={today}", headers=HEADERS, timeout=10)
        today_list = r_today.json().get('response', []) if r_today.status_code == 200 else []
        found = [m for m in today_list if query in m['teams']['home']['name'].lower() or query in m['teams']['away']['name'].lower()]
    
    return found

@st.cache_data(ttl=10)
def fetch_live_stats(fid):
    try:
        r = requests.get(f"{BASE_URL}/fixtures/statistics", headers=HEADERS, params={"fixture": fid}, timeout=10)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3600)
def check_team_history_detailed(team_id):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": team_id, "last": 8}, timeout=10)
        res = r.json().get('response', [])
        return [{"SKOR": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "TOPLAM": (m['goals']['home'] or 0) + (m['goals']['away'] or 0), "İY_GOL": (m['score']['halftime']['home'] or 0) + (m['score']['halftime']['away'] or 0)} for m in res]
    except: return []

def check_success(emir, gh, ga):
    total = gh + ga
    if "İLK YARI 0.5 ÜST" in emir: return total > 0 
    if "2.5 ÜST" in emir: return total > 2
    if "1.5 ÜST" in emir: return total > 1
    if "0.5 ÜST" in emir: return total > 0
    return False

def siber_engine(m):
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total = gh + ga
    fid = str(m['fixture']['id'])
    elapsed = m['fixture']['status']['elapsed'] or 0
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
    
    h_history = check_team_history_detailed(h_id)
    a_history = check_team_history_detailed(a_id)
    l_stats = fetch_live_stats(fid) if elapsed > 0 else []

    h_dom, a_dom = 0, 0
    stats_data = {"h_sht": 0, "a_sht": 0, "h_atk": 0, "a_atk": 0, "h_crn": 0, "a_crn": 0}
    
    if l_stats:
        for team in l_stats:
            s = {item['type']: item['value'] or 0 for item in team['statistics']}
            is_home = team['team']['id'] == h_id
            score = (safe_to_int(s.get('Shots on Goal', 0)) * 6) + (safe_to_int(s.get('Corner Kicks', 0)) * 3) + (safe_to_int(s.get('Dangerous Attacks', 0)) * 1.5)
            if is_home:
                h_dom = score
                stats_data.update({"h_sht": s.get('Shots on Goal', 0), "h_atk": s.get('Dangerous Attacks', 0), "h_crn": s.get('Corner Kicks', 0)})
            else:
                a_dom = score
                stats_data.update({"a_atk": s.get('Dangerous Attacks', 0), "a_sht": s.get('Shots on Goal', 0), "a_crn": s.get('Corner Kicks', 0)})

    current_total_atk = safe_to_int(stats_data['h_atk']) + safe_to_int(stats_data['a_atk'])
    momentum_boost = False
    if fid in st.session_state["MOMENTUM_TRACKER"]:
        old_data = st.session_state["MOMENTUM_TRACKER"][fid]
        atk_diff = current_total_atk - old_data['atk']
        time_diff = elapsed - old_data['min']
        if time_diff > 0 and (atk_diff / time_diff) > 2.5: momentum_boost = True
    
    st.session_state["MOMENTUM_TRACKER"][fid] = {'atk': current_total_atk, 'min': elapsed}

    h_past_wins = sum(1 for x in h_history if int(x['SKOR'].split('-')[0]) > int(x['SKOR'].split('-')[1]))
    a_past_wins = sum(1 for x in a_history if int(x['SKOR'].split('-')[1]) > int(x['SKOR'].split('-')[0]))
    h_power = (h_past_wins * 15) + (h_dom * 0.9)
    a_power = (a_past_wins * 15) + (a_dom * 0.9)
    sum_pow = (h_power + a_power) if (h_power + a_power) > 0 else 1
    h_prob = round((h_power / sum_pow) * 100)
    
    h_proj = f"🔥 {h_name} BASKIN (%{h_prob})" if h_prob > 60 else (f"🔥 {a_name} BASKIN (%{100-h_prob})" if h_prob < 40 else "⚖️ DENGE")

    h_iy_hits = sum(1 for x in h_history if x['İY_GOL'] > 0)
    a_iy_hits = sum(1 for x in a_history if x['İY_GOL'] > 0)
    h_25_hits = sum(1 for x in h_history if x['TOPLAM'] > 2)
    a_25_hits = sum(1 for x in a_history if x['TOPLAM'] > 2)

    iy_alarm_active = (0 < elapsed < 40 and total == 0 and (h_iy_hits + a_iy_hits) >= 11)
    strat_15_target = (h_25_hits + a_25_hits) >= 10
    
    strat_25_target = False
    if (h_25_hits + a_25_hits) >= 12: 
        if elapsed > 0:
            if total == 2 and elapsed < 78: strat_25_target = True
            elif total < 2 and (h_dom + a_dom) > 45: strat_25_target = True
        else:
            strat_25_target = True

    conf = 85
    pre_emir, live_emir = "1.5 ÜST", "BEKLEMEDE"
    if elapsed == 0:
        pre_emir = "İLK YARI 0.5 ÜST" if (h_iy_hits + a_iy_hits) >= 11 else "1.5 ÜST"
        conf = 95 if pre_emir == "İLK YARI 0.5 ÜST" else 89
    else:
        if elapsed < 42 and total == 0:
            live_emir, conf = ("İLK YARI 0.5 ÜST", 97) if (momentum_boost or iy_alarm_active) else ("0.5 Ü
