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

# --- 2. TASARIM SİSTEMİ (MİLİMETRİK SABİT) ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".dominance-container{margin:10px 0; padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; border:1px solid #30363d;}"
    ".dom-bar-bg{background:#30363d; height:8px; border-radius:4px; display:flex; overflow:hidden; margin-top:5px;}"
    ".dom-home-fill{background:#58a6ff; height:100%; transition: width 0.6s ease;}"
    ".dom-away-fill{background:#f85149; height:100%; transition: width 0.6s ease;}"
    ".dom-text{display:flex; justify-content:space-between; font-size:0.7rem; font-weight:bold; color:#8b949e;}"
    ".reasoning-box{background:rgba(46,160,67,0.05); border:1px dashed #2ea043; padding:8px; border-radius:6px; font-size:0.8rem; margin:10px 0; color:#c9d1d9;}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. ANALİZ VE GEÇMİŞ VERİ FİLTRE MOTORU ---
def check_past_performance(team_id, mode="iy_gol"):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": team_id, "last": 5}, timeout=10)
        res = r.json().get('response', [])
        if len(res) < 5: return False
        
        for m in res:
            gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
            if mode == "iy_gol":
                iy_h, iy_a = m['score']['halftime']['home'] or 0, m['score']['halftime']['away'] or 0
                if (iy_h + iy_a) == 0: return False
            elif mode == "25_ust":
                if (gh + ga) <= 2: return False
        return True
    except: return False

def siber_engine(m, mode="live"):
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    
    # Geçmiş Filtresi Uygula
    p_mode = "iy_gol" if mode == "live" else "25_ust"
    if not (check_past_performance(h_id, p_mode) and check_past_performance(a_id, p_mode)):
        return None # Filtreye takıldı

    # Hakimiyet Hesaplama
    h_dom, dom_msg = 50, "Eşit Baskı"
    stats = m.get('statistics', [])
    if stats:
        h_da, a_da = 0, 0
        for s in stats:
            if s.get('type') == 'Dangerous Attacks':
                h_da = int(s.get('home') or 0)
                a_da = int(s.get('away') or 0)
        if (h_da + a_da) > 0:
            h_dom = int((h_da / (h_da + a_da)) * 100)
            if h_dom > 65: dom_msg = "🔥 Ev Sahibi Yüksek Baskı"
            elif h_dom < 35: dom_msg = "🔥 Deplasman Yüksek Baskı"
            elif h_dom > 55: dom_msg = "📈 Ev Sahibi Üstün"
            elif h_dom < 45: dom_msg = "📈 Deplasman Üstün"

    reason = f"Analiz: Son 5 Maç Serisi + Hakimiyet"
    pre_emir = "2.5 ÜST" if mode == "pre" else "0.5 ÜST"
    live_emir = "CANLI GOL POTANSİYELİ" if mode == "live" else "SABİT EMİR"
    
    return 95, pre_emir, live_emir, h_dom, dom_msg, reason

# --- 4. PANEL ---
if "auth" not in st.session_state: st.session_state["auth"] = False

if not st.session_state["auth"]:
    with st.form("auth_f"):
        l_t = st.text_input("Kullanıcı Adı").strip()
        l_p = st.text_input("Şifre", type="password").strip()
        if st.form_submit_button("GİRİŞ"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in st.session_state["CORE_VAULT"]):
                st.session_state.update({"auth": True, "current_user": l_t})
                st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA STRATEJİK ANALİZ</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("♻️ CANLI ANALİZ", use_container_width=True):
            st.session_state["stored_matches"] = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"live": "all"}).json().get('response', [])
            st.session_state["view_mode"] = "live"; st.rerun()
    with c2:
        if st.button("🔄 GÜNCELLE", use_container_width=True): st.rerun()
    with c3:
        if st.button("🧹 TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.rerun()

    for m in st.session_state.get("stored_matches", []):
        res = siber_engine(m, st.session_state.get("view_mode", "live"))
        if res is None: continue # Filtreye uymayanı gösterme
        
        conf, pre_e, live_e, h_dom, d_msg, reason = res
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        
        st.markdown(f"""
        <div class='decision-card'>
            <div class='ai-score'>%{conf}</div>
            <div class='live-pulse'>📡 ANALİZ EDİLDİ</div><br>
            <b>{m['league']['name']}</b><br>
            <span style='font-size:1.2rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
            <div class='score-board'>{gh} - {ga} <small>{m['fixture']['status']['elapsed']}'</small></div>
            
            <div class='dominance-container'>
                <div class='dom-text'><span>EV %{h_dom} BASKI</span><span>DEP %{100-h_dom} BASKI</span></div>
                <div class='dom-bar-bg'>
                    <div class='dom-home-fill' style='width:{h_dom}%'></div>
                    <div class='dom-away-fill' style='width:{100-h_dom}%'></div>
                </div>
                <div style='color:#2ea043; font-size:0.75rem; font-weight:bold; margin-top:4px;'>{d_msg}</div>
            </div>

            <div class='reasoning-box'>💡 {reason}</div>
            
            <div style='display:flex; gap:10px;'>
                <div style='flex:1; padding:8px; background:rgba(88,166,255,0.1); border:1px solid #58a6ff; border-radius:6px; text-align:center;'>
                    <small style='color:#58a6ff;'>BAZ EMİR</small><br><b>{pre_e}</b>
                </div>
                <div style='flex:1; padding:8px; background:rgba(46,160,67,0.1); border:1px solid #2ea043; border-radius:6px; text-align:center;'>
                    <small style='color:#2ea043;'>CANLI EMİR</small><br><b>{live_e}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
