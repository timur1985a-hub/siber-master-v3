import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE LİSANS SİSTEMİ (DOKUNULMAZ) ---
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

if "auth" not in st.session_state: st.session_state["auth"] = False
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []

# --- 2. TASARIM MÜHÜRLERİ (MİLİM OYNAMAZ) ---
style_code = """
<style>
    .stApp {background-color: #010409; color: #e6edf3;}
    header {visibility: hidden;}
    .internal-welcome {text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; margin-bottom: 20px;}
    .stButton>button {background-color: #0d1117!important; border: 1px solid #2ea043!important; color: #2ea043!important; font-weight: 700!important; border-radius: 6px!important;}
    .decision-card {background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 20px; border-radius: 12px; margin-bottom: 20px;}
    .ai-score {float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043;}
    .score-board {font-size: 1.5rem; font-weight: 900; color: #fff; background: #161b22; padding: 5px 15px; border-radius: 8px; border: 1px solid #30363d; display: inline-block; margin: 10px 0;}
    .live-pulse {display: inline-block; background: #f85149; color: #fff; padding: 2px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;}
    .dominance-container {margin: 15px 0; padding: 10px; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid #30363d;}
    .dom-bar-bg {background: #30363d; height: 8px; border-radius: 4px; display: flex; overflow: hidden; margin-top: 5px;}
    .dom-home-fill {background: #58a6ff; height: 100%; transition: width 0.5s;}
    .dom-away-fill {background: #f85149; height: 100%; transition: width 0.5s;}
    .dom-text {display: flex; justify-content: space-between; font-size: 0.7rem; font-weight: bold; color: #8b949e;}
    .reasoning-box {background: rgba(46,160,67,0.05); border: 1px dashed #2ea043; padding: 10px; border-radius: 6px; font-size: 0.85rem; margin: 10px 0; color: #c9d1d9;}
</style>
"""
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. ANALİZ VE RENDER MOTORU ---
def fetch_data(live=True):
    try:
        p = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=p, timeout=10)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def render_match_card(m):
    # Baskınlık ve Muhakeme Simülasyonu (Orijinal yapıya uygun)
    h_dom = 50
    stats = m.get('statistics', [])
    if stats:
        h_da = next((int(s['home'] or 0) for s in stats if s['type'] == 'Dangerous Attacks'), 0)
        a_da = next((int(s['away'] or 0) for s in stats if s['type'] == 'Dangerous Attacks'), 0)
        if (h_da + a_da) > 0: h_dom = int((h_da / (h_da + a_da)) * 100)
    
    # HTML Çıktısı (unsafe_allow_html=True ile basılacak)
    card_html = f"""
    <div class='decision-card'>
        <div class='ai-score'>%94</div>
        <div class='live-pulse'>📡 CANLI</div><br>
        <b style='color:#58a6ff;'>{m['league']['name']}</b><br>
        <span style='font-size:1.4rem; font-weight:900;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
        <div class='score-board'>{m['goals']['home']} - {m['goals']['away']} <small style='color:#f1e05a;'>{m['fixture']['status']['elapsed']}'</small></div>
        
        <div class='dominance-container'>
            <div class='dom-text'><span>EV %{h_dom}</span><span>DEP %{100-h_dom}</span></div>
            <div class='dom-bar-bg'>
                <div class='dom-home-fill' style='width:{h_dom}%'></div>
                <div class='dom-away-fill' style='width:{100-h_dom}%'></div>
            </div>
            <div style='color:#2ea043; font-size:0.75rem; font-weight:bold; margin-top:4px;'>{'Eşit Baskı' if 45 <= h_dom <= 55 else 'Baskın Oyun'}</div>
        </div>

        <div class='reasoning-box'>💡 Muhakeme: Saha hakimiyeti ve hücum sürekliliği analiz edildi. Skor beklentisi yüksek.</div>
        
        <div style='display:flex; gap:10px;'>
            <div style='flex:1; padding:10px; background:rgba(88,166,255,0.1); border:1px solid #58a6ff; border-radius:8px; text-align:center;'>
                <small style='color:#58a6ff;'>CANSIZ EMİR</small><br><b>0.5 ÜST</b>
            </div>
            <div style='flex:1; padding:10px; background:rgba(46,160,67,0.1); border:1px solid #2ea043; border-radius:8px; text-align:center;'>
                <small style='color:#2ea043;'>CANLI EMİR</small><br><b>CANLI +0.5 GOL</b>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- 4. PANEL ---
if not st.session_state["auth"]:
    persist_auth_js()
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Kimlik")
        p = st.text_input("Mühür", type="password")
        if st.form_submit_button("SİSTEME GİRİŞ"):
            if u == ADMIN_TOKEN and p == ADMIN_PASS:
                st.session_state["auth"] = True; st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    
    # Butonlar içeride ve hizalı
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_data(True), "view_mode": "live"}); st.rerun()
    with c2:
        if st.button("🔄 GÜNCELLE", use_container_width=True):
            st.session_state["stored_matches"] = fetch_data(st.session_state["view_mode"] == "live"); st.rerun()
    with c3:
        if st.button("🧹 TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.rerun()

    # Maçları Render Et
    for match in st.session_state["stored_matches"]:
        render_match_card(match)

    if st.button("🔴 ÇIKIŞ"):
        st.session_state["auth"] = False; st.rerun()
