import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import json

# --- 1. MASTER SEO & DOUBLE ANALYTICS (PRENSİP: GİZLİ ENJEKSİYON) ---
st.set_page_config(
    page_title="Yapay Zeka Maç Tahmin | Siber Radar V250",
    page_icon="🎯",
    layout="wide"
)

# Çift Etiket Entegrasyonu (G-9KHTP6QZY8 & GT-MJSXTWTN)
st.markdown(f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9KHTP6QZY8"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=GT-MJSXTWTN"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-9KHTP6QZY8');
      gtag('config', 'GT-MJSXTWTN');
    </script>
    
    <style>
        .siber-ghost-layer {{ 
            position: absolute; top: -1000px; left: -1000px; 
            height: 0; width: 0; overflow: hidden;
        }}
    </style>
    <div class="siber-ghost-layer">
        <p>Verification IDs: G-9KHTP6QZY8, GT-MJSXTWTN</p>
        <meta name="google-site-verification" content="H1Ify4fYD3oQjHKjrcgFvUBOgndELK-wVkbSB0FrDJk" />
        <meta name="google-site-verification" content="8ffdf1f7bdb7adf3" />
    </div>
""", unsafe_allow_html=True)

# --- 2. SİBER HAFIZA VE LİSANS MOTORU (SABİT ÇEKİRDEK) ---
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
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

# --- 3. DEĞİŞMEZ TASARIM (KURALLAR: MİLİM OYNAMADI) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .hype-title { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 900; margin: 10px 0; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { 
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; 
        width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043;
    }
    .pkg-box b { color: #58a6ff; display: block; font-size: 0.9rem; }
    .wa-small {
        display: block; width: 300px; margin: 0 auto 15px auto;
        background: #238636; color: white !important; text-align: center; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 0.85rem; text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None, "active_key": None})

# --- 4. GİRİŞ VE MASTER SEKMELERİ (DOKUNULMAZ) ---
if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t1, t2 = st.tabs(["🔑 GİRİŞ", "👨‍💻 MASTER"])
        with t1:
            u_in = st.text_input("Anahtar:", type="password", key="login")
            if st.button("SİSTEMİ AÇ"):
                if u_in in VAULT:
                    if u_in not in st.session_state["lic_db"]: st.session_state["lic_db"][u_in] = datetime.now() + timedelta(days=VAULT[u_in]["days"])
                    if datetime.now() > st.session_state["lic_db"][u_in]: st.error("SÜRE DOLDU!")
                    else: st.session_state.update({"auth": True, "role": "user", "active_key": u_in}); st.rerun()
        with t2:
            a_t = st.text_input("Token:", type="password", key="at")
            a_p = st.text_input("Şifre:", type="password", key="ap")
            if st.button("ADMİN GİRİŞİ"):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin"}); st.rerun()
else:
    # --- 5. ANA PANEL ---
    st.markdown("<h1 style='text-align:center;'>İSPAT KANALLARI</h1>", unsafe_allow_html=True)
    st.info("🎯 Çift Katmanlı Google Etiketleri (G-9KHTP6QZY8 & GT-MJSXTWTN) Gizli Modda Aktif.")
