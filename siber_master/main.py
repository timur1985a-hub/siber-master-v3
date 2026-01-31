import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE SABİT VERİTABANI ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# ÇEREZLERİ AŞAN SİSTEM: Tokenlar artık hesaplanmıyor, doğrudan kodun içinde kayıtlı.
# Sadece örnek olması için aşağıya mühürlüyorum. 
# NOT: Buradaki liste 'GLOBAL_VAULT' olarak sistemin kalbidir.
@st.cache_resource
def get_immutable_vault():
    vault = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            # Buradaki salt (V10_FINAL) asla değişmemeli!
            token = f"SBR-{lbl}-{hashlib.md5(f'V10_FINAL_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f'P_FINAL_{lbl}_{i}'.encode()).hexdigest().upper()[:6]
            vault[token] = {"pass": pas, "label": lbl, "days": d}
    return vault

# Uygulama yaşadığı sürece bu liste asla değişmez.
GLOBAL_VAULT = get_immutable_vault()

# Aktivasyonları sunucu bazlı sakla (Session State yerine kalıcı DB önerilir ama şimdilik en sağlamı bu)
if "permanent_acts" not in st.session_state:
    st.session_state["permanent_acts"] = {}

# --- 2. TASARIM VE NEON CSS (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 20px;}
    .pkg-row { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; width: 18%; text-align: center; border-top: 3px solid #2ea043; }
    .wa-small { display: block; width: 100%; max-width: 350px; margin: 0 auto 20px auto; background: #238636; color: white !important; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 20px; border-radius: 12px; margin-bottom: 15px; }
    .ai-score { float: right; font-size: 1.6rem; font-weight: 900; color: #2ea043; }
    .live-minute { color: #f85149; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# --- 3. GİRİŞ KONTROL ---
if "auth" not in st.session_state: 
    st.session_state.update({"auth": False, "role": None, "user": None})

if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'>1 AYLIK<br><b>700 TL</b></div>
        <div class='pkg-box'>3 AYLIK<br><b>2.000 TL</b></div>
        <div class='pkg-box'>6 AYLIK<br><b>5.000 TL</b></div>
        <div class='pkg-box'>12 AYLIK<br><b>9.000 TL</b></div>
        <div class='pkg-box'>SINIRSIZ<br><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<h3 style='text-align:center;'>🔑 SİBER GİRİŞ</h3>", unsafe_allow_html=True)
            u_tok = st.text_input("Token:", key="t_input").strip()
            u_pas = st.text_input("Şifre:", type="password", key="p_input").strip()
            
            if st.button("SİSTEMİ AKTİF ET", use_container_width=True):
                # MASTER ADMIN GİRİŞİ
                if u_tok == ADMIN_TOKEN and u_pas == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin"})
                    st.rerun()
                
                # TOKEN KONTROLÜ
                elif u_tok in GLOBAL_VAULT:
                    if GLOBAL_VAULT[u_tok]["pass"] == u_pas:
                        now = datetime.now()
                        if u_tok not in st.session_state["permanent_acts"]:
                            st.session_state["permanent_acts"][u_tok] = now + timedelta(days=GLOBAL_VAULT[u_tok]["days"])
                        
                        if now > st.session_state["permanent_acts"][u_tok]:
                            st.error("❌ Lisans Süresi Dolmuş!")
                        else:
                            st.session_state.update({"auth": True, "role": "user", "user": u_tok})
                            st.rerun()
                    else:
                        st.error("❌ Hatalı Şifre!")
                else:
                    st.error("❌ Token Tanınamadı!")
else:
    # --- 4. PANEL EKRANLARI ---
    if st.session_state["role"] == "admin":
        st.success("SBR-MASTER PANEL AKTİF")
        pkg = st.selectbox("Paket Listele:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
        filtered = {k: v for k, v in GLOBAL_VAULT.items() if v["label"] == pkg}
        st.dataframe(pd.DataFrame.from_dict(filtered, orient='index'))
    else:
        st.info(f"Kullanıcı: {st.session_state['user']} | Lisans Aktif")
        if st.button("🚀 ANALİZİ BAŞLAT"):
            st.write("Veriler Nesine üzerinden taranıyor...")

    if st.button("ÇIKIŞ YAP"):
        st.session_state.clear()
        st.rerun()
