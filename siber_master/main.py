import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re
import json

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
# KOD DOĞRULANDI: Yazılım kurallarına uygun ve tüm 1-2 tahmin mekanizmaları entegre edildi.
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
            seed = f"V17_ULTRA_UNLIMITED_PRIVATE_{lbl}_{i}_TIMUR_2026" if lbl == "SINIRSIZ" else f"V16_ULTRA_FIXED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d, "issued": False, "exp": None}
    return v

@st.cache_resource
def get_persistent_archive(): return {}

if "MOMENTUM_TRACKER" not in st.session_state: st.session_state["MOMENTUM_TRACKER"] = {}
if "CORE_VAULT" not in st.session_state: st.session_state["CORE_VAULT"] = get_hardcoded_vault()
if "PERMANENT_ARCHIVE" not in st.session_state: st.session_state["PERMANENT_ARCHIVE"] = get_persistent_archive()
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"
if "search_result" not in st.session_state: st.session_state["search_result"] = None

# --- AUTH KONTROL ---
if "auth" not in st.session_state:
    p = st.query_params
    if p.get("auth") == "true":
        t, ps = p.get("t"), p.get("p")
        if t == ADMIN_TOKEN and ps == ADMIN_PASS: st.session_state.update({"auth":True,"role":"admin","current_user":"TIMUR-ROOT"})
        elif t in st.session_state["CORE_VAULT"] and st.session_state["CORE_VAULT"][t]["pass"] == ps and st.session_state["CORE_VAULT"][t]["issued"]:
            st.session_state.update({"auth":True,"role":"user","current_user":t})
        else: st.session_state["auth"] = False
    else: st.session_state["auth"] = False

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ (DOKUNULMAZ) ---
style_code = """
<style>
.stApp{background-color:#010409;color:#e6edf3}
header{visibility:hidden}
.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}
.marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}
@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}
.match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900}
.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}
.owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}
.decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px}
.ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}
.score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}
.live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite}
@keyframes pulse-red{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}
.stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #58a6ff}
.stat-val{font-size:2.2rem;font-weight:900;color:#2ea043}
.stat-lbl{font-size:0.8rem;color:#8b949e;text-transform:uppercase}
.dom-bar-bg{height:10px; background:#30363d; border-radius:10px; margin:10px 0; overflow:hidden; display:flex;}
.dom-bar-home{height:100%; background:#2ea043;}
.dom-bar-away{height:100%; background:#f85149;}
.hybrid-box{margin-top:10px; padding:8px; background:rgba(88,166,255,0.05); border-radius:8px; border-left:4px solid #58a6ff; font-size:0.85rem;}
.stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;width:100%}
</style>
"""
st.markdown(style_code, unsafe_allow_html=True)
if not st.session_state.get("auth", False): persist_auth_js()

# --- 3. ANALİZ MOTORU ---
def safe_to_int(v):
    try: return int(v) if v is not None else 0
    except: return 0

def to_tsi(utc):
    try: return datetime.fromisoformat(utc.replace("Z", "+00:00")).astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

@st.cache_data(ttl=10)
def fetch_live_stats(fid):
    try:
        r = requests.get(f"{BASE_URL}/fixtures/statistics", headers=HEADERS, params={"fixture": fid}, timeout=10)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3600)
def check_siber_kanun_vize(h_id, a_id):
    try:
        r = requests.get(f"{BASE_URL}/fixtures/headtohead", headers=HEADERS, params={"h2h": f"{h_id}-{a_id}", "last": 5}, timeout=10)
        res = r.json().get('response', [])
        return sum((m['goals']['home'] or 0) + (m['goals']['away'] or 0) for m in res) >= 4 if res else False
    except: return False

@st.cache_data(ttl=3600)
def check_team_history_detailed(tid):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": tid, "last": 8}, timeout=10)
        res = r.json().get('response', [])
        return [{"SKOR": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "TOPLAM": (m['goals']['home'] or 0) + (m['goals']['away'] or 0)} for m in res]
    except: return []

def siber_engine(m):
    fid = str(m['fixture']['id'])
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    elapsed = m['fixture']['status']['elapsed'] or 0
    
    h_h = check_team_history_detailed(h_id)
    a_h = check_team_history_detailed(a_id)
    l_stats = fetch_live_stats(fid) if elapsed > 0 else []
    
    h_dom, a_dom = 0, 0
    s_d = {"h_sht": 0, "a_sht": 0, "h_atk": 0, "a_atk": 0, "h_crn": 0, "a_crn": 0}
    
    if l_stats:
        for team in l_stats:
            s = {item['type']: item['value'] or 0 for item in team['statistics']}
            pwr = (safe_to_int(s.get('Shots on Goal', 0)) * 5) + (safe_to_int(s.get('Corner Kicks', 0)) * 3) + (safe_to_int(s.get('Dangerous Attacks', 0)) * 1.2)
            if team['team']['id'] == h_id:
                h_dom = pwr
                s_d.update({"h_sht": s.get('Shots on Goal', 0), "h_atk": s.get('Dangerous Attacks', 0), "h_crn": s.get('Corner Kicks', 0)})
            else:
                a_dom = pwr
                s_d.update({"a_atk": s.get('Dangerous Attacks', 0), "a_sht": s.get('Shots on Goal', 0), "a_crn": s.get('Corner Kicks', 0)})

    h_avg = sum(x['TOPLAM'] for x in h_h) / 8 if h_h else 0
    a_avg = sum(x['TOPLAM'] for x in a_h) / 8 if a_h else 0
    bgp = round(((h_avg + a_avg) / 2) * 0.8, 2)
    
    # 1 vs 2 Kazanma İhtimali
    h_pwr = (h_avg * 10) + (h_dom * 1.5)
    a_pwr = (a_avg * 10) + (a_dom * 1.5)
    total_pwr = (h_pwr + a_pwr) if (h_pwr + a_pwr) > 0 else 1
    h_prob = round((h_pwr / total_pwr) * 100)
    
    proj = f"BGP: {bgp} | " + (f"🔥 {m['teams']['home']['name']} BASKIN (%{h_prob})" if h_prob > 58 else (f"🔥 {m['teams']['away']['name']} BASKIN (%{100-h_prob})" if h_prob < 42 else "⚖️ DENGELİ ANALİZ"))
    
    kanun = check_siber_kanun_vize(h_id, a_id)
    target = "🎯 KESİN ÜST ADAYI" if kanun else "⚠️ KANUNA UYMUYOR"
    
    return 95 if h_prob > 65 or h_prob < 35 else 85, "ANALİZ OKUNDU", "CANLI TAKİP", s_d, h_dom, a_dom, proj, target

# --- 4. PANEL ---
if not st.session_state.get("auth", False):
    st.markdown("<div class='marketing-title' style='text-align:center; color:#2ea043; font-size:2rem;'>TIMUR AI STRATEGIC PREDICTOR</div>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Siber Token")
        p = st.text_input("Siber Şifre", type="password")
        if st.form_submit_button("SİSTEME GİR"):
            if u == ADMIN_TOKEN and p == ADMIN_PASS:
                st.session_state.update({"auth":True,"role":"admin","current_user":"TIMUR-ROOT"})
                st.rerun()
            elif u in st.session_state["CORE_VAULT"] and st.session_state["CORE_VAULT"][u]["pass"] == p and st.session_state["CORE_VAULT"][u]["issued"]:
                st.session_state.update({"auth":True,"role":"user","current_user":u})
                st.rerun()
else:
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']}</div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("♻️ CANLI"): 
        st.session_state.stored_matches = requests.get(f"{BASE_URL}/fixtures?live=all", headers=HEADERS).json().get('response', [])
        st.session_state.view_mode = "live"; st.rerun()
    if c2.button("💎 BÜLTEN"):
        st.session_state.stored_matches = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=HEADERS).json().get('response', [])
        st.session_state.view_mode = "pre"; st.rerun()
    if c3.button("🔄 GÜNCELLE"): st.cache_data.clear(); st.rerun()
    if c5.button("🧹 TEMİZLE"): st.session_state.stored_matches = []; st.rerun()

    for m in st.session_state.get("stored_matches", []):
        conf, p_e, l_e, s_d, h_d, a_d, proj, trg = siber_engine(m)
        total_d = (h_d + a_d) if (h_d + a_d) > 0 else 1
        h_bar = (h_d / total_d) * 100
        
        st.markdown(f"""
        <div class='decision-card'>
            <div class='ai-score'>%{conf}</div>
            <b>{m['league']['name']}</b><br>
            <span style='font-size:1.1rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
            <div class='score-board'>{m['goals']['home'] or 0} - {m['goals']['away'] or 0} <small>{m['fixture']['status']['elapsed']}'</small></div>
            <div class='dom-bar-bg'><div class='dom-bar-home' style='width:{h_bar}%'></div><div class='dom-bar-away' style='width:{100-h_bar}%'></div></div>
            <div class='hybrid-box'><b>PROJEKSİYON:</b> {proj}<br><b>DURUM:</b> {trg}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 ÇIKIŞ"):
        st.session_state.auth = False; st.rerun()
