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

def safe_int(val):
    if val is None: return 0
    try:
        clean_val = re.sub(r'[^0-9]', '', str(val))
        return int(clean_val) if clean_val else 0
    except: return 0

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

if "MOMENTUM_TRACKER" not in st.session_state: st.session_state["MOMENTUM_TRACKER"] = {}
if "CORE_VAULT" not in st.session_state: st.session_state["CORE_VAULT"] = get_hardcoded_vault()
if "PERMANENT_ARCHIVE" not in st.session_state: st.session_state["PERMANENT_ARCHIVE"] = get_persistent_archive()

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

if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"

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
    ".momentum-boost{color:#58a6ff; font-weight:bold; font-size:0.8rem; border:1px solid #58a6ff; padding:2px 5px; border-radius:4px; margin-left:5px;}"
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
    pool = st.session_state.get("stored_matches", [])
    found = [m for m in pool if query in m['teams']['home']['name'].lower() or query in m['teams']['away']['name'].lower()]
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
        return [{"SKOR": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "İY": f"{m['score']['halftime']['home'] or 0}-{m['score']['halftime']['away'] or 0}", "TOPLAM": (m['goals']['home'] or 0) + (m['goals']['away'] or 0), "İY_GOL": (m['score']['halftime']['home'] or 0) + (m['score']['halftime']['away'] or 0)} for m in res]
    except: return []

def check_success(emir, gh, ga):
    total = gh + ga
    if "1.5 ÜST" in emir: return total > 1
    if "0.5 ÜST" in emir: return total > 0
    if "İLK YARI 0.5" in emir: return total > 0
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
    live_data_found = False

    if l_stats:
        live_data_found = True
        for team in l_stats:
            s = {item['type']: item['value'] or 0 for item in team['statistics']}
            is_home = team['team']['id'] == h_id
            score = (safe_int(s.get('Shots on Goal', 0)) * 5) + (safe_int(s.get('Corner Kicks', 0)) * 3) + (safe_int(s.get('Dangerous Attacks', 0)) * 1.2)
            if is_home:
                h_dom = score
                stats_data.update({"h_sht": s.get('Shots on Goal', 0), "h_atk": s.get('Dangerous Attacks', 0), "h_crn": s.get('Corner Kicks', 0)})
            else:
                a_dom = score
                stats_data.update({"a_atk": s.get('Dangerous Attacks', 0), "a_sht": s.get('Shots on Goal', 0), "a_crn": s.get('Corner Kicks', 0)})

    current_total_atk = safe_int(stats_data.get('h_atk', 0)) + safe_int(stats_data.get('a_atk', 0))
    momentum_boost = False
    if live_data_found:
        if fid in st.session_state["MOMENTUM_TRACKER"]:
            old_data = st.session_state["MOMENTUM_TRACKER"][fid]
            if elapsed > old_data['min'] and (current_total_atk - old_data['atk']) / (elapsed - old_data['min']) > 2.2: momentum_boost = True
        st.session_state["MOMENTUM_TRACKER"][fid] = {'atk': current_total_atk, 'min': elapsed}

    # --- HİBRİT SİBER PROJEKSİYON ---
    h_25_ust_count = sum(1 for x in h_history if x['TOPLAM'] > 2)
    a_25_ust_count = sum(1 for x in a_history if x['TOPLAM'] > 2)
    h_iy_hits = sum(1 for x in h_history if x['İY_GOL'] > 0)
    a_iy_hits = sum(1 for x in a_history if x['İY_GOL'] > 0)
    avg_total = sum(x['TOPLAM'] for x in h_history + a_history) / (len(h_history + a_history) or 1)
    
    h_prob = round(((h_25_ust_count / 8) * 100))
    a_prob = round(((a_25_ust_count / 8) * 100))
    h_proj = f"📊 HİBRİT GOL GÜCÜ: %{round((h_prob+a_prob)/2)}"

    conf = 85
    pre_emir = "ANALİZ DIŞI"
    live_emir = "BEKLEMEDE"
    iy_alarm_active = False

    # Stratejik 2.5 ÜST -> 1.5 ÜST Döngüsü
    if avg_total > 2.7 or (h_25_ust_count + a_25_ust_count) >= 10:
        pre_emir = "1.5 ÜST (STRATEJİK)"
        conf = 96
    elif avg_total > 2.2:
        pre_emir = "1.5 ÜST (MAKUL)"
        conf = 88

    # --- HİBRİT ALARM (CANLI VERİ OLSADA OLMASADA) ---
    if 0 < elapsed < 80:
        if total == 0:
            # Hem geçmişi İY golcü hem de dakika 25+ ise veya yüksek atak varsa
            if (h_iy_hits + a_iy_hits) >= 11 or (elapsed > 25 and (h_iy_hits + a_iy_hits) >= 8) or momentum_boost:
                live_emir, conf, iy_alarm_active = "İLK YARI 0.5 ÜST", 98 if momentum_boost else 95, True
            else: live_emir, conf = "0.5 ÜST", 91
        elif total == 1:
            if (h_25_ust_count + a_25_ust_count) >= 9 or (elapsed > 60 and live_data_found and current_total_atk/elapsed > 1.8):
                live_emir, conf = "1.5 ÜST (HİBRİT ALARM)", 97
            else: live_emir, conf = "1.5 ÜST", 92

    return conf, pre_emir, live_emir, h_history, a_history, stats_data, h_dom, a_dom, iy_alarm_active, momentum_boost, h_proj

# --- 4. PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>Siber Hafıza ve Canlı Momentumun Hibrit Gücü</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(True)[:10]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>PAKET</small><br><b>1-AY</b><div class='pkg-price'>700 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>3-AY</b><div class='pkg-price'>2.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>6-AY</b><div class='pkg-price'>5.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>12-AY</b><div class='pkg-price'>9.000 TL</div></div><div class='pkg-box'><small>KAMPANYA</small><br><b>SINIRSIZ</b><div class='pkg-price'>20.000 TL</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>💬 BİZE ULAŞIN (WHATSAPP)</a>", unsafe_allow_html=True)
    
    with st.form("auth_f"):
        l_t = st.text_input("Kullanıcı Adınız", placeholder="SBR-XXXX-XXXX-TM", key="username").strip()
        l_p = st.text_input("Siber Şifreniz", type="password", key="password").strip()
        if st.form_submit_button("AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS):
                st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
                st.query_params.update({"auth": "true", "t": l_t, "p": l_p})
                st.markdown(f"<script>localStorage.setItem('sbr_token', '{l_t}'); localStorage.setItem('sbr_pass', '{l_p}');</script>", unsafe_allow_html=True)
                st.rerun()
            elif l_t in st.session_state["CORE_VAULT"]:
                ud = st.session_state["CORE_VAULT"][l_t]
                if ud["pass"] == l_p and ud["issued"]:
                    st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                    st.query_params.update({"auth": "true", "t": l_t, "p": l_p})
                    st.markdown(f"<script>localStorage.setItem('sbr_token', '{l_t}'); localStorage.setItem('sbr_pass', '{l_p}');</script>", unsafe_allow_html=True)
                    st.rerun()
                else: st.error("❌ HATALI GİRİŞ")
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    if st.session_state.get("role") == "admin":
        with st.expander("🔑 SİBER LİSANS YÖNETİMİ"):
            t_tabs = st.tabs(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            for i, pkg in enumerate(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"]):
                with t_tabs[i]:
                    subset = {k: v for k, v in st.session_state["CORE_VAULT"].items() if v["label"] == pkg}
                    for tk in list(subset.keys())[:10]:
                        v = subset[tk]
                        c1_l, c2_l = st.columns([3, 1])
                        c1_l.markdown(f"**{tk}** | P: {v['pass']} | {'✅' if v['issued'] else '⚪'}")
                        if not v["issued"] and c2_l.button("DAĞIT", key=f"d_{tk}"):
                            st.session_state["CORE_VAULT"][tk].update({"issued": True, "exp": datetime.now() + timedelta(days=v["days"])})
                            st.rerun()

    st.markdown("<div class='search-box-sbr'>", unsafe_allow_html=True)
    s_col1, s_col2 = st.columns([4,1])
    query = s_col1.text_input("🔍 Siber Arama...", placeholder="Takım veya Maç Yazın", label_visibility="collapsed")
    if s_col2.button("ARA", use_container_width=True):
        if query:
            with st.spinner("Siber Arama Yapılıyor..."):
                found_matches = hybrid_search_engine(query)
                if found_matches:
                    st.session_state["search_result"] = found_matches
                    st.session_state["view_mode"] = "search"
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live", "search_result": None}); st.rerun()
    with c2:
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre", "search_result": None}); st.rerun()
    with c3:
        if st.button("🔄 GÜNCELLE", use_container_width=True):
            st.cache_data.clear()
            st.session_state["stored_matches"] = fetch_siber_data(st.session_state["view_mode"] == "live")
            st.rerun()
    with c4:
        if st.button("📜 SİBER ARŞİV", use_container_width=True):
            st.session_state["view_mode"] = "archive"; st.rerun()
    with c5:
        if st.button("🧹 EKRANI TEMİZLE", use_container_width=True):
            st.session_state.update({"stored_matches": [], "view_mode": "clear", "search_result": None}); st.rerun()

    display_list = []
    current_matches = []
    if st.session_state["view_mode"] == "search" and st.session_state["search_result"]:
        current_matches = st.session_state["search_result"]
    elif st.session_state["view_mode"] in ["live", "pre"]:
        current_matches = st.session_state["stored_matches"]
    elif st.session_state["view_mode"] == "archive":
        display_list = list(st.session_state["PERMANENT_ARCHIVE"].values())

    if current_matches:
        for m in current_matches:
            fid = str(m['fixture']['id'])
            conf, p_emir, l_emir, h_h, a_h, s_d, h_d, a_d, iy_alarm, m_boost, h_proj = siber_engine(m)
            if p_emir != "ANALİZ DIŞI":
                st.session_state["PERMANENT_ARCHIVE"][fid] = {
                    "fid": fid, "conf": conf, "league": m['league']['name'], 
                    "home": m['teams']['home']['name'], "away": m['teams']['away']['name'], 
                    "date": to_tsi(m['fixture']['date']), "pre_emir": p_emir, 
                    "live_emir": l_emir, "score": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", 
                    "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0, 
                    "h_h": h_h, "a_h": a_h, "stats": s_d, "h_d": h_d, "a_d": a_d, "iy_alarm": iy_alarm, "m_boost": m_boost, "h_proj": h_proj
                }
                display_list.append(st.session_state["PERMANENT_ARCHIVE"][fid])

    for arc in display_list:
        is_live_card = arc['status'] not in ['FT', 'AET', 'PEN', 'NS', 'TBD']
        card_color = "#2ea043" if arc['conf'] >= 94 else "#f1e05a"
        win_status = "✅" if check_success(arc['pre_emir'], *map(int, arc['score'].split('-'))) else ""
        alarm_html = "<span class='iy-alarm'>🚨 HİBRİT IY ALARMI</span>" if arc.get('iy_alarm') else ""
        boost_html = "<span class='momentum-boost'>⚡ MOMENTUM GÜCÜ</span>" if arc.get('m_boost') else ""
        hybrid_html = f"<div class='hybrid-box'><span class='hybrid-label'>📍 STRATEJİK PROJEKSİYON (2.5 -> 1.5 ÜST):</span><span class='hybrid-val'>{arc.get('h_proj', 'ANALİZ EDİLİYOR')}</span></div>"
        
        st.markdown(f"<div class='decision-card' style='border-left:6px solid {card_color};'><div class='ai-score' style='color:{card_color};'>%{arc['conf']}</div><div class='live-pulse' style='display:{'inline-block' if is_live_card else 'none'}'>📡 CANLI</div>{alarm_html}{boost_html}<br><b style='color:#58a6ff;'>{arc['league']}</b> | {arc['date']}<br><span style='font-size:1.2rem; font-weight:bold;'>{arc['home']} vs {arc['away']}</span><br><div class='score-board'>{arc['score']} <span class='live-min-badge'>{arc['min']}'</span></div><div style='display:flex; gap:10px;'><div style='flex:1; background:rgba(88,166,255,0.1); padding:5px; border-radius:5px;'><small>PROJEKSİYON HEDEFİ</small><br><b>{arc['pre_emir']}</b> {win_status}</div><div style='flex:1; background:rgba(46,160,67,0.1); padding:5px; border-radius:5px;'><small>CANLI HİBRİT KARAR</small><br><b>{arc['live_emir']}</b></div></div>{hybrid_html}</div>", unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.query_params.clear()
        st.markdown("<script>localStorage.removeItem('sbr_token'); localStorage.removeItem('sbr_pass');</script>", unsafe_allow_html=True)
        st.session_state["auth"] = False
        st.rerun()
