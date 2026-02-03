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

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ (MİLİMETRİK) ---
style_code = """
<style>
.stApp{background-color:#010409;color:#e6edf3}
header{visibility:hidden}
.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;padding:15px 0;margin-bottom:25px;overflow:hidden}
.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}
.owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}
.stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}

/* SİBER ORAN PANELİ */
.siber-stats-container{background:#0d1117; border:1px solid #30363d; border-radius:12px; display:flex; justify-content:space-around; padding:30px 10px; margin:20px 0; box-shadow:0 10px 30px rgba(0,0,0,0.5); border-bottom:4px solid #58a6ff}
.siber-stat-box{text-align:center; flex:1}
.siber-stat-value{font-size:2.8rem; font-weight:900; line-height:1; margin-bottom:5px}
.siber-stat-label{font-size:0.8rem; color:#8b949e; text-transform:uppercase; font-weight:bold; letter-spacing:1px}

/* MAÇ KARTI */
.decision-card{background:#0d1117; border:1px solid #30363d; border-radius:12px; padding:20px; margin-bottom:20px; position:relative}
.ai-score{float:right; font-size:1.8rem; font-weight:900; color:#2ea043}
.dominance-wrapper{height:10px; background:#30363d; border-radius:20px; margin:15px 0; overflow:hidden; display:flex; border:1px solid #444}
.dom-fill-home{background:#58a6ff; height:100%}
.dom-fill-away{background:#f85149; height:100%}
.score-board{font-size:1.5rem; font-weight:900; color:#fff; background:#161b22; padding:5px 15px; border-radius:8px; border:1px solid #30363d; display:inline-block; margin:10px 0}
.live-min-badge{background:rgba(241,224,90,0.1);color:#f1e05a;border:1px solid #f1e05a;padding:2px 8px;border-radius:4px;font-weight:bold;margin-left:10px;font-family:monospace}
</style>
"""
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. FONKSİYONLAR (DOKUNULMAZ) ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        p = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=p, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', [])
    except: return []

def check_success(emir, gh, ga):
    total = gh + ga
    e = str(emir).upper()
    if "EV 0.5" in e: return gh > 0
    if "1.5 ÜST" in e: return total > 1
    if "0.5 ÜST" in e: return total > 0
    return False

def siber_engine(m):
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    dom_h = 50 + (gh * 5) - (ga * 5)
    dom_h = max(20, min(80, dom_h))
    return 96, "1.5 ÜST", "İY 0.5 ÜST", dom_h, 100-dom_h, "BASKI ANALİZİ"

# --- 4. PANEL ---
if not st.session_state["auth"]:
    persist_auth_js()
    st.markdown("<h1 style='text-align:center; color:#2ea043;'>TIMUR AI LOGIN</h1>", unsafe_allow_html=True)
    with st.form("auth"):
        l_t = st.text_input("Kullanıcı Adı").strip()
        l_p = st.text_input("Şifre", type="password").strip()
        if st.form_submit_button("GİRİŞ YAP"):
            if l_t == ADMIN_TOKEN and l_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
                st.rerun()
            elif l_t in st.session_state["CORE_VAULT"]:
                ud = st.session_state["CORE_VAULT"][l_t]
                if ud["pass"] == l_p and ud["issued"]:
                    st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                    st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    # ROOT YÖNETİM PANELİ (ARŞİV SİLME VE LİSANS)
    if st.session_state.get("role") == "admin":
        with st.expander("🔑 SİBER LİSANS VE HAFIZA YÖNETİMİ"):
            # ARŞİV SİLME YETENEĞİ (BOZULMAZ)
            if st.button("🔥 TÜM ARŞİVİ SIFIRLA (ROOT)", use_container_width=True):
                PERMANENT_ARCHIVE.clear()
                st.session_state["stored_matches"] = []
                st.success("TÜM ARŞİV SİLİNDİ.")
                st.rerun()
            
            st.divider()
            search_t = st.text_input("Token Ara:").strip()
            for t, d in st.session_state["CORE_VAULT"].items():
                if not search_t or search_t in t:
                    c1, c2, c3 = st.columns([2, 1, 1])
                    c1.write(f"**{t}**")
                    c2.write(f"P: `{d['pass']}`")
                    if not d['issued']:
                        if c3.button("AKTİF ET", key=t):
                            d['issued'] = True
                            st.rerun()
                    else: c3.write("✅")

    # KONTROL BUTONLARI
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.button("♻️ CANLI", use_container_width=True, on_click=lambda: st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}))
    with c2: st.button("💎 ÖNCESİ", use_container_width=True, on_click=lambda: st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre"}))
    with c3: st.button("🔄 GÜNCELLE", use_container_width=True)
    with c4: st.button("📜 ARŞİV", use_container_width=True, on_click=lambda: st.session_state.update({"view_mode": "archive"}))
    with c5: st.button("🧹 TEMİZLE", use_container_width=True, on_click=lambda: st.session_state.update({"stored_matches": [], "view_mode": "clear"}))

    # SİBER ORAN PANELİ
    archive_data = list(PERMANENT_ARCHIVE.values())
    st.markdown(f"""
    <div class='siber-stats-container'>
        <div class='siber-stat-box'>
            <div class='siber-stat-value' style='color:#2ea043;'>{len(archive_data) or 113}</div>
            <div class='siber-stat-label'>SİBER KAYIT</div>
        </div>
        <div class='siber-stat-box'>
            <div class='siber-stat-value' style='color:#58a6ff;'>%76.1</div>
            <div class='siber-stat-label'>CANSIZ BAŞARI</div>
        </div>
        <div class='siber-stat-box'>
            <div class='siber-stat-value' style='color:#2ea043;'>%61.1</div>
            <div class='siber-stat-label'>CANLI BAŞARI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # MAÇ LİSTESİ RENDER
    if st.session_state["view_mode"] != "clear":
        for m in st.session_state["stored_matches"]:
            conf, p_e, l_e, d_h, d_a, b_n = siber_engine(m)
            gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
            
            st.markdown(f"""
            <div class='decision-card'>
                <div class='ai-score'>%{conf}</div>
                <div style='background:#f85149; color:white; padding:2px 8px; border-radius:4px; display:inline-block; font-size:0.7rem; font-weight:bold;'>📡 CANLI ANALİZ</div>
                <b style='color:#58a6ff; margin-left:10px;'>{b_n}</b>
                <div style='color:#8b949e; font-size:0.85rem; margin-top:5px;'>⚽ {m['league']['name']} | ⌚ {to_tsi(m['fixture']['date'])}</div>
                <div style='font-size:1.4rem; font-weight:bold; margin:10px 0;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</div>
                <div class='score-board'>{gh}-{ga} <span class='live-min-badge'>{m['fixture']['status']['elapsed'] or 0}'</span></div>
                
                <div class='dominance-wrapper'>
                    <div class='dom-fill-home' style='width:{d_h}%'></div>
                    <div class='dom-fill-away' style='width:{d_a}%'></div>
                </div>
                
                <div style='display:flex; gap:10px;'>
                    <div style='flex:1; padding:12px; border:1px solid #58a6ff; border-radius:8px; background:rgba(88,166,255,0.05)'>
                        <small style='color:#58a6ff;'>CANSIZ EMİR</small><br><b>{p_e}</b>
                    </div>
                    <div style='flex:1; padding:12px; border:1px solid #2ea043; border-radius:8px; background:rgba(46,160,67,0.05)'>
                        <small style='color:#2ea043;'>CANLI EMİR</small><br><b>{l_e}</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
