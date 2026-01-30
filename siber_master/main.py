import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC CORE", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

if "lic_db" not in st.session_state: st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            k = f"SBR-{lbl[:3]}-{hashlib.md5(f'V34_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            v[k] = {"label": lbl, "days": d}
    return v
VAULT = get_vault()

# --- 2. DEĞİŞMEZ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .welcome-title { text-align: center; color: #2ea043; font-size: 2.2rem; font-weight: 900; margin-bottom: 5px; }
    .owner-subtitle { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 25px; font-style: italic; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #238636, #2ea043); }
    .scan-box { background: #0d1117; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
    .status-text { font-family: 'Courier New', Courier, monospace; color: #58a6ff; font-size: 0.85rem; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043; }
    .card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #2ea043; }
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None})

# --- 3. GİRİŞ ÖNCESİ (SABİT ŞABLON) ---
if not st.session_state["auth"]:
    st.markdown("<div class='welcome-title'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown("<div class='owner-subtitle'>Bu yazılımın sahibi Timur'dur.</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div><div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div><div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div><div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div><div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' style='display:block; width:100%; max-width:300px; margin:0 auto 15px; background:#238636; color:white; text-align:center; padding:10px; border-radius:8px; font-weight:bold; text-decoration:none;'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t1, t2 = st.tabs(["🔑 GİRİŞ", "👨‍💻 MASTER"])
        with t1:
            u_in = st.text_input("Anahtar:", type="password", key="u_login")
            if st.button("SİSTEMİ AÇ", use_container_width=True):
                if u_in in VAULT: st.session_state.update({"auth": True, "role": "user"}); st.rerun()
        with t2:
            a_t = st.text_input("Token:", type="password", key="a_token")
            a_p = st.text_input("Şifre:", type="password", key="a_pass")
            if st.button("ADMİN GİRİŞİ", use_container_width=True):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS: st.session_state.update({"auth": True, "role": "admin"}); st.rerun()

else:
    # --- 4. GİRİŞ SONRASI (GÜNCELLEME VE TEMİZLEME MOTORU) ---
    st.markdown("<h2 style='text-align:center; color:#2ea043;'>🎯 ANALİZ MERKEZİ</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Tüm geçici dosyalar temizlendi.")
            time.sleep(1)
            st.rerun()
    with col_b:
        # GÜNCELLE BUTONU ARTIK VERİLERİ SIFIRLAYIP YENİDEN ÇEKMEYE HAZIRLAR
        if st.button("♻️ VERİLERİ GÜNCELLE", use_container_width=True):
            st.cache_data.clear() # Mevcut API verilerini siler
            st.info("Veri havuzu sıfırlandı, yeni tarama için hazır.")
            time.sleep(1)
            st.rerun()

    st.divider()

    # --- 5. GÖRSEL TARAMA MOTORU ---
    if st.button("🚀 KUSURSUZ DÜNYA TARAMASINI BAŞLAT", use_container_width=True):
        scan_placeholder = st.empty()
        with scan_placeholder.container():
            st.markdown("<div class='scan-box'>", unsafe_allow_html=True)
            status_msg = st.empty()
            progress_bar = st.progress(0)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # API'den taze veri çekimi (Cache temizlendiği için taze gelir)
            r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
            fixtures = r.json().get('response', [])
            
            total_matches = len(fixtures)
            if total_matches > 0:
                for i, match in enumerate(fixtures):
                    percent = int(((i + 1) / total_matches) * 100)
                    progress_bar.progress(percent)
                    league = match['league']['name']
                    teams = f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}"
                    status_msg.markdown(f"<div class='status-text'>📡 <b>LİG:</b> {league}<br>⚽ <b>MAÇ:</b> {teams}<br>📊 <b>DURUM:</b> {i+1}/{total_matches} (%{percent})</div>", unsafe_allow_html=True)
                    time.sleep(0.02) 
                status_msg.success(f"✅ Güncel Tarama Tamamlandı! {total_matches} maç taze olarak işlendi.")
            else:
                st.warning("Tarama yapılacak taze veri bulunamadı.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()
