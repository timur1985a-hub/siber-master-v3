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

# URL'den Geri Yükleme ve Auth Kontrolü
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
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}"
    ".pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}"
    ".pkg-price{color:#f1e05a;font-weight:800;font-size:0.9rem;margin-top:5px}"
    ".wa-small{display:block;width:100%;max-width:300px;margin:10px auto 20px auto;background:#238636;color:#fff!important;text-align:center;padding:12px;border-radius:8px;font-weight:700;text-decoration:none;border:1px solid #2ea043}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".tsi-time{color:#f1e05a!important;font-family:'Courier New',monospace;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px;border:1px solid rgba(241,224,90,0.2)}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".status-win{color:#2ea043;font-weight:bold;border:1px solid #2ea043;padding:2px 5px;border-radius:4px;margin-left:5px}"
    ".status-lost{color:#f85149;font-weight:bold;border:1px solid #f85149;padding:2px 5px;border-radius:4px;margin-left:5px}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite;margin-bottom:5px}"
    ".live-min-badge{background:rgba(241,224,90,0.1);color:#f1e05a;border:1px solid #f1e05a;padding:2px 8px;border-radius:4px;font-weight:bold;margin-left:10px;font-family:monospace}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #58a6ff;box-shadow:0 10px 20px rgba(0,0,0,0.4)}"
    ".stat-val{font-size:2.2rem;font-weight:900;color:#2ea043;line-height:1}"
    ".stat-lbl{font-size:0.8rem;color:#8b949e;text-transform:uppercase;font-weight:bold;margin-top:8px;letter-spacing:1px}"
    ".archive-badge{display:inline-block;background:rgba(248,81,73,0.1);color:#f85149;border:1px solid #f85149;padding:2px 8px;border-radius:4px;font-size:0.75rem;margin-bottom:5px;font-weight:bold}"
    ".lic-item{background:#161b22; padding:10px; border-radius:6px; margin-bottom:5px; border-left:3px solid #f1e05a; font-family:monospace; font-size:0.85rem;}"
    ".dominance-container{margin:10px 0; padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; border:1px solid #30363d;}"
    ".dom-bar-bg{background:#30363d; height:8px; border-radius:4px; display:flex; overflow:hidden; margin-top:5px;}"
    ".dom-home-fill{background:#58a6ff; height:100%; transition: width 0.6s ease;}"
    ".dom-away-fill{background:#f85149; height:100%; transition: width 0.6s ease;}"
    ".dom-text{display:flex; justify-content:space-between; font-size:0.7rem; font-weight:bold; color:#8b949e;}"
    ".reasoning-box{background:rgba(46,160,67,0.05); border:1px dashed #2ea043; padding:8px; border-radius:6px; font-size:0.8rem; margin:10px 0; color:#c9d1d9;}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)
if not st.session_state["auth"]: persist_auth_js()

# --- 3. SİBER ANALİZ VE GEÇMİŞ FİLTRE MOTORU ---
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
def check_past_history(team_id, mode="iy_gol"):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": team_id, "last": 5}, timeout=10)
        fixtures = r.json().get('response', [])
        if len(fixtures) < 5: return False
        for f in fixtures:
            gh, ga = f['goals']['home'] or 0, f['goals']['away'] or 0
            if mode == "iy_gol":
                iyh, iya = f['score']['halftime']['home'] or 0, f['score']['halftime']['away'] or 0
                if (iyh + iya) == 0: return False
            elif mode == "2.5_ust":
                if (gh + ga) <= 2: return False
        return True
    except: return False

def check_success(emir, gh, ga):
    total = gh + ga
    if "İLK YARI 0.5 ÜST" in emir: return total > 0
    if "2.5 ÜST" in emir: return total > 2
    if "1.5 ÜST" in emir: return total > 1
    if "0.5 ÜST" in emir: return total > 0
    if "KG VAR" in emir: return gh > 0 and ga > 0
    if "+0.5 GOL" in emir: return total > 0
    return False

def siber_engine(m):
    # Hakimiyet Analizi
    h_dom, d_msg = 50, "Eşit Baskı"
    stats = m.get('statistics', [])
    if stats:
        h_da, a_da = 0, 0
        for s in stats:
            if s.get('type') == 'Dangerous Attacks':
                h_da = int(s.get('home') or 0)
                a_da = int(s.get('away') or 0)
        if (h_da + a_da) > 0:
            h_dom = int((h_da / (h_da + a_da)) * 100)
            if h_dom > 60: d_msg = "🔥 Ev Sahibi Domine Ediyor"
            elif h_dom < 40: d_msg = "🔥 Deplasman Domine Ediyor"
            else: d_msg = "⚖️ Dengeli Hakimiyet"

    # Karar Motoru
    elapsed = m['fixture']['status']['elapsed'] or 0
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    is_live = elapsed > 0
    
    # Filtreleme Kontrolü
    if is_live:
        if not (check_past_history(h_id, "iy_gol") and check_past_history(a_id, "iy_gol")):
            return None # Filtre dışı
        pre_emir, live_emir, conf = "0.5 ÜST", "İLK YARI 0.5 ÜST", 95
    else:
        if not (check_past_history(h_id, "2.5_ust") and check_past_history(a_id, "2.5_ust")):
            return None # Filtre dışı
        pre_emir, live_emir, conf = "2.5 ÜST", "MAÇ SONU 2.5 ÜST", 92

    return conf, pre_emir, live_emir, h_dom, d_msg

# --- 4. PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>Siber Analiz ve Yapay Zeka Stratejileri</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(True)[:10]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>PAKET</small><br><b>1-AY</b><div class='pkg-price'>700 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>3-AY</b><div class='pkg-price'>2.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>6-AY</b><div class='pkg-price'>5.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>12-AY</b><div class='pkg-price'>9.000 TL</div></div><div class='pkg-box'><small>KAMPANYA</small><br><b>SINIRSIZ</b><div class='pkg-price'>20.000 TL</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>💬 BİZE ULAŞIN (WHATSAPP)</a>", unsafe_allow_html=True)
    
    with st.form("auth_f"):
        l_t = st.text_input("Kullanıcı adı", key="username").strip()
        l_p = st.text_input("Şifre", type="password", key="password").strip()
        if st.form_submit_button("AKTİF ET"):
            now = datetime.now(pytz.timezone("Europe/Istanbul"))
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS):
                st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
                st.query_params.update({"auth": "true", "t": l_t, "p": l_p})
                st.markdown(f"<script>localStorage.setItem('sbr_token', '{l_t}'); localStorage.setItem('sbr_pass', '{l_p}');</script>", unsafe_allow_html=True)
                st.rerun()
            elif l_t in st.session_state["CORE_VAULT"]:
                ud = st.session_state["CORE_VAULT"][l_t]
                if ud["pass"] == l_p and ud["issued"] and (ud["exp"] is None or now < ud["exp"]):
                    st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                    st.query_params.update({"auth": "true", "t": l_t, "p": l_p})
                    st.markdown(f"<script>localStorage.setItem('sbr_token', '{l_t}'); localStorage.setItem('sbr_pass', '{l_p}');</script>", unsafe_allow_html=True)
                    st.rerun()
                else: st.error("❌ HATALI GİRİŞ VEYA GEÇERSİZ LİSANS")
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    if st.session_state.get("role") == "admin":
        with st.expander("🔑 SİBER LİSANS VE HAFIZA YÖNETİMİ"):
            t_tabs = st.tabs(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            for i, pkg in enumerate(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"]):
                with t_tabs[i]:
                    subset = {k: v for k, v in st.session_state["CORE_VAULT"].items() if v["label"] == pkg}
                    for tk in list(subset.keys())[:15]:
                        v = subset[tk]
                        c1, c2 = st.columns([3, 1])
                        c1.markdown(f"<div class='lic-item'><b>{tk}</b><br>Pass: {v['pass']} | {'✅ AKTİF' if v['issued'] else '⚪ BEKLEMEDE'}</div>", unsafe_allow_html=True)
                        if not v["issued"] and c2.button("DAĞIT", key=f"d_{tk}"):
                            st.session_state["CORE_VAULT"][tk].update({"issued": True, "exp": datetime.now(pytz.timezone("Europe/Istanbul")) + timedelta(days=v["days"])})
                            st.rerun()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}); st.rerun()
    with c2:
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre"}); st.rerun()
    with c3:
        if st.button("🔄 GÜNCELLE", use_container_width=True):
            if st.session_state["view_mode"] != "archive":
                st.session_state["stored_matches"] = fetch_siber_data(st.session_state["view_mode"] == "live")
            st.rerun()
    with c4:
        if st.button("📜 SİBER ARŞİV", use_container_width=True):
            st.session_state["view_mode"] = "archive"; st.rerun()
    with c5:
        if st.button("🧹 EKRANI TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.session_state["view_mode"] = "clear"; st.rerun()

    search_q = st.text_input("🔍 Siber Arama:", placeholder="Takım/Lig...").strip().lower()
    mode = st.session_state["view_mode"]
    display_list = []

    if mode in ["live", "pre"] and st.session_state["stored_matches"]:
        for m in st.session_state["stored_matches"]:
            analysis = siber_engine(m)
            if analysis is None: continue # Filtreye uymayanları atla
            
            fid = str(m['fixture']['id'])
            gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
            status, elapsed = m['fixture']['status']['short'], m['fixture']['status']['elapsed'] or 0
            conf, p_emir, l_emir, h_dom, d_msg = analysis
            
            if fid not in PERMANENT_ARCHIVE:
                PERMANENT_ARCHIVE[fid] = {"fid": fid, "conf": conf, "league": m['league']['name'], "home": m['teams']['home']['name'], "away": m['teams']['away']['name'], "date": to_tsi(m['fixture']['date']), "pre_emir": p_emir, "live_emir": l_emir, "score": f"{gh}-{ga}", "status": status, "min": elapsed, "h_dom": h_dom, "d_msg": d_msg}
            else:
                PERMANENT_ARCHIVE[fid].update({"score": f"{gh}-{ga}", "status": status, "min": elapsed, "h_dom": h_dom, "d_msg": d_msg})

    if mode == "archive": display_list = list(PERMANENT_ARCHIVE.values())
    elif mode != "clear":
        display_list = [v for k, v in PERMANENT_ARCHIVE.items() if any(m['fixture']['id'] == int(k) for m in st.session_state.get("stored_matches", []))]

    if search_q:
        display_list = [d for d in display_list if search_q in d['home'].lower() or search_q in d['away'].lower() or search_q in d['league'].lower()]

    for arc in display_list:
        gh_v, ga_v = map(int, arc['score'].split('-'))
        is_fin = arc['status'] in ['FT', 'AET', 'PEN']
        win_pre = f"<span class='status-win'>✅</span>" if check_success(arc['pre_emir'], gh_v, ga_v) else (f"<span class='status-lost'>❌</span>" if is_fin else "")
        win_live = f"<span class='status-win'>✅</span>" if check_success(arc['live_emir'], gh_v, ga_v) else (f"<span class='status-lost'>❌</span>" if is_fin else "")
        color = "#2ea043" if arc['conf'] >= 94 else "#f1e05a"
        is_live = arc['status'] not in ['TBD', 'NS', 'FT', 'AET', 'PEN', 'P', 'CANC', 'ABD', 'AWD', 'WO']
        live_tag = "<div class='live-pulse'>📡 CANLI SİSTEM AKTİF</div>" if is_live else "<div class='archive-badge'>🔒 SİBER MÜHÜR</div>"
        min_tag = f"<span class='live-min-badge'>{arc['min']}'</span>" if is_live else ""
        
        # Hakimiyet Barı ve Analiz Kutusu Entegrasyonu
        st.markdown(f"""
        <div class='decision-card' style='border-left:6px solid {color};'>
            <div class='ai-score' style='color:{color};'>%{arc['conf']}</div>
            {live_tag}<br>
            <b style='color:#58a6ff;'>⚽ {arc['league']}</b> | <span class='tsi-time'>⌚ {arc['date']}</span><br>
            <span style='font-size:1.3rem; font-weight:bold;'>{arc['home']} vs {arc['away']}</span><br>
            <div class='score-board'>{arc['score']} {min_tag}</div>
            
            <div class='dominance-container'>
                <div class='dom-text'><span>EV %{arc['h_dom']}</span><span>DEP %{100-arc['h_dom']}</span></div>
                <div class='dom-bar-bg'>
                    <div class='dom-home-fill' style='width:{arc['h_dom']}%'></div>
                    <div class='dom-away-fill' style='width:{100-arc['h_dom']}%'></div>
                </div>
                <div style='color:#2ea043; font-size:0.75rem; font-weight:bold; margin-top:4px;'>{arc['d_msg']}</div>
            </div>
            
            <div class='reasoning-box'>💡 Analiz: Son 5 Maç Filtresi Aktif | Gelişmiş Hakimiyet Sorgusu</div>

            <div style='display:flex; gap:10px; margin-top:10px;'>
                <div style='flex:1; padding:8px; background:rgba(88,166,255,0.1); border:1px solid #58a6ff; border-radius:6px;'><small style='color:#58a6ff;'>CANSIZ EMİR</small><br><b>{arc['pre_emir']}</b> {win_pre}</div>
                <div style='flex:1; padding:8px; background:rgba(46,160,67,0.1); border:1px solid #2ea043; border-radius:6px;'><small style='color:#2ea043;'>CANLI EMİR</small><br><b>{arc['live_emir']}</b> {win_live}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.query_params.clear()
        st.markdown("<script>localStorage.removeItem('sbr_token'); localStorage.removeItem('sbr_pass');</script>", unsafe_allow_html=True)
        st.session_state["auth"] = False
        st.rerun()
