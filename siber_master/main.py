import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

def safe_int(val):
    if val is None: return 0
    try:
        clean_val = re.sub(r'[^0-9]', '', str(val))
        return int(clean_val) if clean_val else 0
    except: return 0

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

if "MOMENTUM_TRACKER" not in st.session_state: st.session_state["MOMENTUM_TRACKER"] = {}
if "auth" not in st.session_state: st.session_state["auth"] = False

# --- 2. TASARIM SİSTEMİ (MİLİMETRİK KORUMA) ---
style_code = """
<style>
    .stApp{background-color:#010409;color:#e6edf3}
    header{visibility:hidden}
    .decision-card{background:#0d1117;border:1px solid #30363d;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}
    .ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}
    .score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}
    .iy-alarm{background:#f85149; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; animation:pulse-red 1s infinite; margin-right:5px}
    .hybrid-target{background:#238636; color:#fff; padding:4px 8px; border-radius:4px; font-weight:900; font-size:0.85rem; margin-right:5px}
    .siber-table{width:100%; border-collapse:collapse; margin-top:10px; font-size:0.75rem; color:#8b949e}
    .siber-table th{text-align:left; border-bottom:1px solid #30363d; padding:5px; color:#58a6ff}
    .siber-table td{padding:5px; border-bottom:1px solid #161b22}
    .hybrid-box{margin-top:10px; padding:8px; background:rgba(88,166,255,0.05); border-radius:8px; border:1px solid #30363d; font-size:0.85rem}
    @keyframes pulse-red{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}
</style>
"""
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. HİBRİT ALARM VE ANALİZ MOTORU ---
@st.cache_data(ttl=3600)
def check_team_history_detailed(team_id):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"team": team_id, "last": 8}, timeout=10)
        res = r.json().get('response', [])
        return [{"SKOR": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "İY": f"{m['score']['halftime']['home'] or 0}-{m['score']['halftime']['away'] or 0}", "TOPLAM": (m['goals']['home'] or 0) + (m['goals']['away'] or 0), "İY_GOL": (m['score']['halftime']['home'] or 0) + (m['score']['halftime']['away'] or 0)} for m in res]
    except: return []

def siber_engine(m):
    fid = str(m['fixture']['id'])
    elapsed = m['fixture']['status']['elapsed'] or 0
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total = gh + ga
    
    h_h = check_team_history_detailed(m['teams']['home']['id'])
    a_h = check_team_history_detailed(m['teams']['away']['id'])
    
    # 1. ALARM: GEÇMİŞ İY MUKAYESESİ (İY 0.5 ÜST ALARMI)
    h_iy_hits = sum(1 for x in h_h if x['İY_GOL'] > 0)
    a_iy_hits = sum(1 for x in a_h if x['İY_GOL'] > 0)
    iy_alarm_active = False
    if total == 0 and 15 < elapsed < 40:
        if (h_iy_hits + a_iy_hits) >= 11: iy_alarm_active = True # %70+ İY gol oranı

    # 2. ALARM: STRATEJİK HEDEF (2.5 -> 1.5 ÜST MUKAYESESİ)
    h_25_hits = sum(1 for x in h_h if x['TOPLAM'] > 2)
    a_25_hits = sum(1 for x in a_h if x['TOPLAM'] > 2)
    strategic_target = False
    if (h_25_hits + a_25_hits) >= 10: strategic_target = True

    # PROJEKSİYON HESABI
    proj_val = round(((h_25_hits + a_25_hits + h_iy_hits + a_iy_hits) / 32) * 100)
    
    return h_h, a_h, iy_alarm_active, strategic_target, proj_val

# --- 4. PANEL ---
if not st.session_state["auth"]:
    with st.form("login"):
        u = st.text_input("Siber Kullanıcı").strip()
        p = st.text_input("Şifre", type="password").strip()
        if st.form_submit_button("SİSTEME GİR"):
            if u == ADMIN_TOKEN and p == ADMIN_PASS:
                st.session_state["auth"] = True
                st.rerun()
else:
    st.markdown("<h2 style='text-align:center; color:#2ea043;'>HİBRİT ANALİZ MERKEZİ</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 MAÇLARI VE ALARMLARI GÜNCELLE"):
        st.session_state["stored_matches"] = requests.get(f"{BASE_URL}/fixtures?live=all", headers=HEADERS).json().get('response', [])
        st.rerun()

    if "stored_matches" in st.session_state:
        for m in st.session_state["stored_matches"]:
            h_h, a_h, iy_alarm, strat_target, proj = siber_engine(m)
            
            card_border = "#2ea043" if proj > 80 else "#30363d"
            
            st.markdown(f"""
            <div class='decision-card' style='border-left: 6px solid {card_border}'>
                <div class='ai-score'>%{proj}</div>
                <small style='color:#8b949e'>{m['league']['name']}</small><br>
                <b>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</b><br>
                <div class='score-board'>{m['goals']['home'] or 0}-{m['goals']['away'] or 0} <small>{m['fixture']['status']['elapsed']}'</small></div><br>
                {'<span class="iy-alarm">🚨 GEÇMİŞ SKOR İY ALARMI</span>' if iy_alarm else ''}
                {'<span class="hybrid-target">🎯 STRATEJİK 1.5 ÜST HEDEFİ</span>' if strat_target else ''}
                <div class='hybrid-box'>📍 <b>HİBRİT PROJEKTÖR:</b> Bu eşleşme geçmiş skor mukayesesinde %{proj} güven puanı aldı.</div>
            """, unsafe_allow_html=True)
            
            with st.expander("📊 SİBER HAFIZA: GEÇMİŞ SKOR MUKAYESESİ"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"🏠 {m['teams']['home']['name']}")
                    table_h = "".join([f"<tr><td>{x['SKOR']}</td><td>{x['İY']}</td><td>{x['TOPLAM']}</td></tr>" for x in h_h])
                    st.markdown(f"<table class='siber-table'><tr><th>MS</th><th>İY</th><th>TOP</th></tr>{table_h}</table>", unsafe_allow_html=True)
                with col2:
                    st.write(f"🚀 {m['teams']['away']['name']}")
                    table_a = "".join([f"<tr><td>{x['SKOR']}</td><td>{x['İY']}</td><td>{x['TOPLAM']}</td></tr>" for x in a_h])
                    st.markdown(f"<table class='siber-table'><tr><th>MS</th><th>İY</th><th>TOP</th></tr>{table_a}</table>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state["auth"] = False
        st.rerun()
