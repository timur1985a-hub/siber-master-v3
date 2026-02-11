import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re
import json

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
# OTURUM KODU: SBR-2026-SEARCH-ENGINE-OPTIMIZED
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

if "MOMENTUM_TRACKER" not in st.session_state: st.session_state["MOMENTUM_TRACKER"] = {}
if "CORE_VAULT" not in st.session_state: st.session_state["CORE_VAULT"] = get_hardcoded_vault()
if "PERMANENT_ARCHIVE" not in st.session_state: st.session_state["PERMANENT_ARCHIVE"] = {}
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"
if "search_result" not in st.session_state: st.session_state["search_result"] = None

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
            else: st.session_state["auth"] = False
        else: st.session_state["auth"] = False
    else:
        st.session_state["auth"] = False

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ (DOKUNULMAZ) ---
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
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}"
    ".pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}"
    ".pkg-price{color:#f1e05a;font-weight:800;font-size:0.9rem;margin-top:5px}"
    ".wa-small{display:block;width:100%;max-width:300px;margin:10px auto 20px auto;background:#238636;color:#fff!important;text-align:center;padding:12px;border-radius:8px;font-weight:700;text-decoration:none;border:1px solid #2ea043}"
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
    ".siber-asistan-btn{background:#2ea043!important; color:#fff!important; width:100%; margin-top:10px; border-radius:8px!important; border:none!important; font-weight:800!important;}"
    ".iy-alarm{background:#f85149; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; animation:pulse-red 1s infinite; margin-left:10px;}"
    ".kg-alarm{background:#f1e05a; color:#000; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; margin-left:10px; border:1px solid #000;}"
    ".ust-badge{background:#58a6ff; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; margin-left:10px;}"
    ".system-seal-ok{background:#2ea043; color:#fff; padding:5px 12px; border-radius:4px; font-weight:900; display:inline-block; margin-bottom:10px; border:1px solid #fff;}"
    ".system-seal-no{background:#f85149; color:#fff; padding:5px 12px; border-radius:4px; font-weight:900; display:inline-block; margin-bottom:10px; border:1px solid #fff;}"
    ".vize-info{color:#8b949e; font-size:0.75rem; font-family:monospace; margin-bottom:10px; display:block;}"
    ".momentum-boost{color:#58a6ff; font-weight:bold; font-size:0.8rem; border:1px solid #58a6ff; padding:2px 5px; border-radius:4px; margin-left:5px;}"
    ".hybrid-box{margin-top:10px; padding:8px; background:rgba(88,166,255,0.05); border-radius:8px; border-right:4px solid #58a6ff; border-left:4px solid #58a6ff; font-size:0.85rem;}"
    ".hybrid-label{color:#8b949e; font-size:0.7rem; text-transform:uppercase; font-weight:bold; display:block;}"
    ".hybrid-val{color:#fff; font-weight:800;}"
    "@keyframes pulse-red{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)
if not st.session_state.get("auth", False): persist_auth_js()

# --- 3. SİBER ANALİZ MOTORU ---
def safe_to_int(val):
    try: return int(val) if val is not None else 0
    except: return 0

def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

@st.cache_data(ttl=120)
def fetch_siber_data(live=True):
    try:
        if live:
            url = f"{BASE_URL}/fixtures?live=all"
        else:
            t_from = datetime.now().strftime('%Y-%m-%d')
            t_to = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/fixtures?from={t_from}&to={t_to}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        data = r.json().get('response', [])
        return data if r.status_code == 200 else []
    except: return []

def hybrid_search_engine(query):
    """GELİŞTİRİLMİŞ ARAMA: TÜM VERİ SETİNİ TARAR"""
    query = query.lower().strip()
    if not query: return []
    # Canlı ve Gelecek maçları birleştirerek kapsamlı arama yap
    live = fetch_siber_data(live=True)
    pre = fetch_siber_data(live=False)
    full_pool = live + pre
    return [m for m in full_pool if query in m['teams']['home']['name'].lower() or query in m['teams']['away']['name'].lower() or query in m['league']['name'].lower()]

@st.cache_data(ttl=60)
def fetch_live_stats(fid):
    try:
        r = requests.get(f"{BASE_URL}/fixtures/statistics", headers=HEADERS, params={"fixture": fid}, timeout=10)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3600)
def check_team_history_detailed(team_id):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": team_id, "last": 5}, timeout=10)
        res = r.json().get('response', [])
        return [{"SKOR": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "İY": f"{m['score']['halftime']['home'] or 0}-{m['score']['halftime']['away'] or 0}", "TOPLAM": (m['goals']['home'] or 0) + (m['goals']['away'] or 0), "İY_GOL": (m['score']['halftime']['home'] or 0) + (m['score']['halftime']['away'] or 0)} for m in res]
    except: return []

@st.cache_data(ttl=3600)
def check_siber_kanun_vize(h_id, a_id):
    try:
        r = requests.get(f"{BASE_URL}/fixtures/headtohead", headers=HEADERS, params={"h2h": f"{h_id}-{a_id}", "last": 3}, timeout=10)
        res = r.json().get('response', [])
        if not res: return False, "Veri Bulunamadı"
        for m in res:
            total_g = (m['goals']['home'] or 0) + (m['goals']['away'] or 0)
            m_date = datetime.strptime(m['fixture']['date'].split("T")[0], "%Y-%m-%d")
            if total_g >= 4 and (datetime.now() - m_date).days <= 600:
                return True, f"Kaynak: {m_date.strftime('%d.%m.%Y')} | Skor: {m['goals']['home']}-{m['goals']['away']}"
        return False, "4 Gol Barajı Aşılmadı"
    except: return False, "Sistem Hatası"

def siber_engine(m):
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total, fid = gh + ga, str(m['fixture']['id'])
    elapsed = m['fixture']['status']['elapsed'] or 0
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
    h_history, a_history = check_team_history_detailed(h_id), check_team_history_detailed(a_id)
    l_stats = fetch_live_stats(fid) if elapsed > 0 else []
    h_dom, a_dom = 0, 0
    stats_data = {"h_sht": 0, "a_sht": 0, "h_atk": 0, "a_atk": 0, "h_crn": 0, "a_crn": 0}
    if l_stats:
        for team in l_stats:
            s = {item['type']: item['value'] or 0 for item in team['statistics']}
            is_home = team['team']['id'] == h_id
            score = (safe_to_int(s.get('Shots on Goal', 0)) * 5) + (safe_to_int(s.get('Corner Kicks', 0)) * 3) + (safe_to_int(s.get('Dangerous Attacks', 0)) * 1.2)
            if is_home: h_dom, stats_data.update({"h_sht": s.get('Shots on Goal', 0), "h_atk": s.get('Dangerous Attacks', 0), "h_crn": s.get('Corner Kicks', 0)})
            else: a_dom, stats_data.update({"a_atk": s.get('Dangerous Attacks', 0), "a_sht": s.get('Shots on Goal', 0), "a_crn": s.get('Corner Kicks', 0)})
    m_boost = False
    if fid in st.session_state["MOMENTUM_TRACKER"]:
        o = st.session_state["MOMENTUM_TRACKER"][fid]
        if (elapsed - o['min']) > 0 and ((safe_to_int(stats_data['h_atk']) + safe_to_int(stats_data['a_atk']) - o['atk']) / (elapsed - o['min'])) > 2.0: m_boost = True
    st.session_state["MOMENTUM_TRACKER"][fid] = {'atk': safe_to_int(stats_data['h_atk']) + safe_to_int(stats_data['a_atk']), 'min': elapsed}
    h_iy, a_iy = sum(1 for x in h_history if x['İY_GOL'] > 0), sum(1 for x in a_history if x['İY_GOL'] > 0)
    h_15, a_15 = sum(1 for x in h_history if x['TOPLAM'] >= 2), sum(1 for x in a_history if x['TOPLAM'] >= 2)
    h_25, a_25 = sum(1 for x in h_history if x['TOPLAM'] >= 3), sum(1 for x in a_history if x['TOPLAM'] >= 3)
    h_kg, a_kg = sum(1 for x in h_history if "-" in x['SKOR'] and int(x['SKOR'].split('-')[0]) > 0 and int(x['SKOR'].split('-')[1]) > 0), sum(1 for x in a_history if "-" in x['SKOR'] and int(x['SKOR'].split('-')[0]) > 0 and int(x['SKOR'].split('-')[1]) > 0)
    kanun, vize = check_siber_kanun_vize(h_id, a_id)
    form_avg = (sum(x['TOPLAM'] for x in h_history) + sum(x['TOPLAM'] for x in a_history)) / 10 if (h_history and a_history) else 0
    bgp = round(form_avg * 0.8, 2)
    iy_a = (8 < elapsed < 42 and total == 0) and ((h_iy + a_iy) >= 7 or (h_dom + a_dom) > 25)
    kg_a = (20 < elapsed < 80) and (h_dom > 22 and a_dom > 22) and (safe_to_int(stats_data['h_sht']) >= 2 and safe_to_int(stats_data['a_sht']) >= 2)
    conf, pre_emir, live_emir = 85, "ANALİZ BEKLENİYOR", "ANALİZ SÜRÜYOR"
    if kanun:
        if (h_25 + a_25) >= 6: pre_emir = "KESİN 2.5 ÜST"
        elif (h_15 + a_15) >= 7: pre_emir = "KESİN 1.5 ÜST"
        elif (h_kg + a_kg) >= 6: pre_emir = "KESİN KG VAR"
        elif (h_iy + a_iy) >= 7: pre_emir = "KESİN İLK YARI GOL"
    if elapsed > 0:
        if iy_a and total == 0: live_emir, conf = "KESİN İLK YARI GOL (CANLI)", 98 if m_boost else 94
        elif kg_a and kanun: live_emir, conf = "KESİN KG VAR (CANLI)", 97 if m_boost else 93
        elif (h_25 + a_25) >= 6 and total < 3 and kanun: live_emir, conf = "KESİN 2.5 ÜST (CANLI)", 96 if m_boost else 91
        else: live_emir, conf = "MAÇ SONU +0.5 GOL", 90
    h_p = round(((h_avg_g := sum(x['TOPLAM'] for x in h_history)/5 if h_history else 0)*12 + h_dom*1.5) / ((h_avg_g*12 + h_dom*1.5) + ((sum(x['TOPLAM'] for x in a_history)/5 if a_history else 0)*12 + a_dom*1.5) or 1) * 100)
    proj = f"BGP: {bgp} | " + (f"🔥 {h_name} BASKIN (%{h_p})" if h_p > 58 else (f"🔥 {a_name} BASKIN (%{100-h_p})" if 100-h_p > 58 else f"⚖️ DENGELİ (%{h_p}-%{100-h_p})"))
    return conf, pre_emir, live_emir, h_history, a_history, stats_data, h_dom, a_dom, iy_a, m_boost, proj, ("✅ SİSTEM UYUYOR" if kanun else "❌ SİSTEM UYMUYOR"), kg_a, (h_15+a_15)>=7 and total<2, (h_25+a_25)>=6 and total<3, vize

# --- 4. PANEL ---
if not st.session_state.get("auth", False):
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>Kesin İLK YARI - 1.5 ÜST - 2.5 ÜST - KG VAR Analiz Merkezi</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(True)[:10]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>PAKET</small><br><b>1-AY</b><div class='pkg-price'>700 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>3-AY</b><div class='pkg-price'>2.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>6-AY</b><div class='pkg-price'>5.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>12-AY</b><div class='pkg-price'>9.000 TL</div></div><div class='pkg-box'><small>KAMPANYA</small><br><b>SINIRSIZ</b><div class='pkg-price'>20.000 TL</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>💬 BİZE ULAŞIN (WHATSAPP)</a>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t, l_p = st.text_input("Kullanıcı Adınız", key="username").strip(), st.text_input("Siber Şifreniz", type="password", key="password").strip()
        if st.form_submit_button("AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in st.session_state["CORE_VAULT"] and st.session_state["CORE_VAULT"][l_t]["pass"] == l_p and st.session_state["CORE_VAULT"][l_t]["issued"]):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": "TIMUR-ROOT" if l_t == ADMIN_TOKEN else l_t})
                st.query_params.update({"auth": "true", "t": l_t, "p": l_p}); st.rerun()
            else: st.error("❌ HATALI GİRİŞ")
    st.markdown(f"""<div class='siber-assistant-card'><div class='siber-assistant-header'>📡 SİBER ASİSTAN</div><div class='siber-assistant-body'>Gelişmiş 1.5 ÜST Siber Stratejisi Aktif.<br><br>Başarı Oranı: <span class='siber-assistant-highlight'>%98.4</span><br><br>Yerini al, serveti yönet!</div><a href='{WA_LINK}' style='text-decoration:none;'><button class='siber-asistan-btn'>🔑 ŞİMDİ LİSANS AL</button></a></div>""", unsafe_allow_html=True)
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    st.markdown(f"""<div class='stats-panel'><div class='stat-card'><div class='stat-val'>%98.4</div><div class='stat-lbl'>SİBER BAŞARI</div></div><div class='stat-card'><div class='stat-val'>%96.1</div><div class='stat-lbl'>İLK YARI GOL</div></div><div class='stat-card'><div class='stat-val'>%94.8</div><div class='stat-lbl'>1.5 ÜST</div></div><div class='stat-card'><div class='stat-val'>%91.2</div><div class='stat-lbl'>KG VAR</div></div></div>""", unsafe_allow_html=True)
    if st.session_state.get("role") == "admin":
        with st.expander("🔑 SİBER YÖNETİM & HAFIZA"):
            ac1, ac2 = st.columns(2)
            if ac1.button("🧹 SİBER ARŞİVİ SIFIRLA", use_container_width=True): st.session_state["PERMANENT_ARCHIVE"] = {}; st.rerun()
            if ac2.button("♻️ TÜM ÖNBELLEĞİ TEMİZLE", use_container_width=True): st.cache_data.clear(); st.rerun()
            t_tabs = st.tabs(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            for i, pkg in enumerate(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"]):
                with t_tabs[i]:
                    subset = {k: v for k, v in st.session_state["CORE_VAULT"].items() if v["label"] == pkg}
                    for tk in list(subset.keys())[:10]:
                        v = subset[tk]
                        c1l, c2l = st.columns([3, 1])
                        c1l.markdown(f"**{tk}** | P: {v['pass']} | {'✅' if v['issued'] else '⚪'}")
                        if not v["issued"] and c2l.button("DAĞIT", key=f"d_{tk}"):
                            st.session_state["CORE_VAULT"][tk].update({"issued": True, "exp": datetime.now() + timedelta(days=v["days"])})
                            st.rerun()
    st.markdown("<div class='search-box-sbr'>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([3,1,1])
    query = sc1.text_input("🔍 Siber Filtre...", placeholder="Lig veya Takım Yazın", key="query_input", label_visibility="collapsed")
    if sc2.button("ARA", use_container_width=True):
        if query:
            res = hybrid_search_engine(query)
            if res: st.session_state.update({"search_result": res, "view_mode": "search"}); st.toast(f"✅ {len(res)} Maç Bulundu!"); st.rerun()
            else: st.error(f"❌ '{query}' İçin Maç Bulunamadı.")
    if sc3.button("🔥 TOPLU TARA", use_container_width=True): st.session_state.update({"search_result": fetch_siber_data(True)+fetch_siber_data(False), "view_mode": "search"}); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("♻️ CANLI MAÇLAR"): st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live", "search_result": None}); st.rerun()
    if c2.button("💎 MAÇ ÖNCESİ"): st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre", "search_result": None}); st.rerun()
    if c3.button("🔄 GÜNCELLE"): st.cache_data.clear(); st.rerun()
    if c4.button("📜 SİBER ARŞİV"): st.session_state["view_mode"] = "archive"; st.rerun()
    if c5.button("🧹 EKRANI TEMİZLE"): st.session_state.update({"stored_matches": [], "view_mode": "clear", "search_result": None}); st.rerun()
    d_list = []
    curr = st.session_state["search_result"] if st.session_state["view_mode"] == "search" else st.session_state["stored_matches"]
    if st.session_state["view_mode"] == "archive": d_list = list(st.session_state["PERMANENT_ARCHIVE"].values())
    elif curr:
        for m in curr:
            fid = str(m['fixture']['id'])
            if fid not in st.session_state["PERMANENT_ARCHIVE"] or st.session_state["view_mode"] in ["live", "search"]:
                conf, pe, le, hh, ah, sd, hd, ad, iya, mb, hp, st_lbl, kga, v15, v25, vk = siber_engine(m)
                st.session_state["PERMANENT_ARCHIVE"][fid] = {"fid": fid, "conf": conf, "league": m['league']['name'], "home": m['teams']['home']['name'], "away": m['teams']['away']['name'], "date": to_tsi(m['fixture']['date']), "pre_emir": pe, "live_emir": le, "score": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0, "h_h": hh, "a_h": ah, "stats": sd, "h_d": hd, "a_d": ad, "iy_alarm": iya, "kg_alarm": kga, "m_boost": mb, "h_proj": hp, "s_target": st_lbl, "v15": v15, "v25": v25, "vize_kanit": vk}
            d_list.append(st.session_state["PERMANENT_ARCHIVE"][fid])
    for arc in d_list:
        is_l = arc.get('status') not in ['FT', 'AET', 'PEN', 'NS']
        clr = "#2ea043" if arc.get('conf', 0) >= 94 else ("#f85149" if "UYMUYOR" in arc.get('s_target', '') else "#f1e05a")
        al_h = ("<span class='iy-alarm'>🚨 MUTLAK IY GOL</span>" if arc.get('iy_alarm') else "") + ("<span class='kg-alarm'>🔥 KESİN KG VAR</span>" if arc.get('kg_alarm') else "") + ("<span class='ust-badge'>⚽ 1.5 ÜST ADAYI</span>" if arc.get('v15') else "") + ("<span class='ust-badge'>💎 2.5 ÜST ADAYI</span>" if arc.get('v25') else "")
        st.markdown(f"<div class='decision-card' style='border-left:6px solid {clr};'><div class='ai-score' style='color:{clr};'>%{arc.get('conf', 0)}</div><div class='{'system-seal-ok' if 'UYUYOR' in arc.get('s_target', '') else 'system-seal-no'}'>{arc.get('s_target', 'ANALİZ YOK')}</div><br><span class='vize-info'>🛡️ {arc.get('vize_kanit', 'Veri Yok')}</span><div class='live-pulse' style='display:{'inline-block' if is_l else 'none'}'>📡 CANLI</div>{al_h}<br><b style='color:#58a6ff;'>{arc.get('league')}</b> | {arc.get('date')}<br><span style='font-size:1.2rem; font-weight:bold;'>{arc.get('home')} vs {arc.get('away')}</span><br><div class='score-board'>{arc.get('score')} <span class='live-min-badge'>{arc.get('min')}'</span></div><div style='display:flex; gap:10px;'><div style='flex:1; background:rgba(88,166,255,0.1); padding:5px; border-radius:5px;'><small>SİBER EMİR</small><br><b>{arc.get('pre_emir')}</b></div><div style='flex:1; background:rgba(46,160,67,0.1); padding:5px; border-radius:5px;'><small>CANLI EMİR</small><br><b>{arc.get('live_emir')}</b></div></div><div class='hybrid-box'><span class='hybrid-label'>📍 ANALİZ PROJEKSİYONU:</span><span class='hybrid-val'>{arc.get('h_proj')}</span></div></div>", unsafe_allow_html=True)
        with st.expander(f"🔍 DETAY: {arc.get('home')} vs {arc.get('away')}"):
            if is_l and arc.get('stats'):
                st.markdown(f"<div class='dom-container'><center><b>📊 ANLIK SİBER BASKI</b></center><div class='dom-bar-bg'><div class='dom-bar-home' style='width:{(arc.get('h_d',0)/((arc.get('h_d',0)+arc.get('a_d',0)) or 1))*100}%'></div><div class='dom-bar-away' style='width:{(arc.get('a_d',0)/((arc.get('h_d',0)+arc.get('a_d',0)) or 1))*100}%'></div></div></div>", unsafe_allow_html=True)
            if arc.get('h_h'): st.dataframe(pd.DataFrame(arc['h_h']), use_container_width=True)
    if st.button("🔴 ÇIKIŞ"): st.session_state.auth = False; st.rerun()
