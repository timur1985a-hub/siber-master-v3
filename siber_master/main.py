import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from datetime import datetime
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

# CANLI DESTEK ENJEKSİYONU (Tawk.to)
def inject_tawk():
    # Bu senin sitene özel canlı destek kodudur
    tawk_script = """
    <script type="text/javascript">
    var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
    (function(){
    var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
    s1.async=true;
    s1.src='https://embed.tawk.to/679ce6813bd1a41921669ef0/1ijseeg0h';
    s1.charset='UTF-8';
    s1.setAttribute('crossorigin','*');
    s0.parentNode.insertBefore(s1,s0);
    })();
    </script>
    """
    components.html(tawk_script, height=0)

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 20px; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .support-badge { background: rgba(46, 160, 67, 0.1); border: 1px solid #2ea043; color: #2ea043; padding: 5px 15px; border-radius: 50px; font-size: 0.8rem; font-weight: bold; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .stTextInput>div>div>input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #2ea043 !important; }
    </style>
""", unsafe_allow_html=True)

# Canlı Desteği Başlat
inject_tawk()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "current_user": None})

# --- 4. GİRİŞ EKRANI ---
if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center;'><span class='support-badge'>🟢 SİBER UZMAN ÇEVRİMİÇİ - SORU SORABİLİRSİNİZ</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🔑 SİBER TERMİNAL GİRİŞİ</h3>", unsafe_allow_html=True)
        l_t = st.text_input("Giriş Tokeni:", type="password", key="l_token").strip()
        l_p = st.text_input("Şifre:", type="password", key="l_pass").strip()
        if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
            if l_t == ADMIN_TOKEN and l_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()
            else: st.error("❌ Geçersiz Giriş!")
else:
    # --- 5. PANEL ---
    st.markdown(f"<h2 style='text-align:center; color:#2ea043;'>HOŞ GELDİN MASTER TIMUR</h2>", unsafe_allow_html=True)
    st.info("💡 Sağ alttaki panelden gelen ziyaretçileri anlık takip edebilir ve onlarla konuşabilirsin.")
    
    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()
