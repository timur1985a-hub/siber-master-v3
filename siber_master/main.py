import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib

# ================= KORUNAN SİBER AYARLAR =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= MOBİL UYUMLU TASARIM (BEYAZSIZ & SIKIŞTIRILMIŞ) =================
def apply_mobile_optimized_ui():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        
        /* Karşılama Yazıları Kartı */
        .call-to-action {
            background: rgba(56, 189, 248, 0.1);
            border: 1px dashed #38bdf8;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Mobil Paket Kartları (Grid Yapısı) */
        .package-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr); /* Mobilde yan yana 2 tane */
            gap: 10px;
            margin-bottom: 20px;
        }
        .package-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
        }
        .package-card h4 { color: #94a3b8; margin: 0; font-size: 0.9rem; }
        .package-card h2 { color: #38bdf8; margin: 5px 0; font-size: 1.2rem; }

        .glass-card { background: rgba(15, 23, 42, 0.65); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 20px; padding: 20px; }
        .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 12px !important; }
        div.stButton > button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

# ================= ARAYÜZ KURULUM =================
st.set_page_config(page_title="Siber Master V3150", layout="wide")
apply_mobile_optimized_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # 1. TÜM KARŞILAMA YAZILARI (KORUNDU)
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER MASTER AI</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='call-to-action'>
            <h3 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜNE HOŞ GELDİNİZ</h3>
            <p style='color: #94a3b8; margin:10px 0 0 0;'>Sıradan bahisçiler tahmin eder, <b>Siber Master sahipleri veriyi yönetir.</b><br>
            Finansal özgürlüğün anahtarı elinizde.</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. PAKETLERİ MOBİLE SIĞDIRMA (GRID)
    st.markdown("<p style='text-align:center; color:#38bdf8; font-weight:bold;'>PRO ANALİZ PAKETLERİ</p>", unsafe_allow_html=True)
    
    # HTML ile 2'li ızgara yapısı (5. paket en alta tek sığar)
    st.markdown("""
        <div class='package-grid'>
            <div class='package-card'><h4>1 AY</h4><h2>700 TL</h2></div>
            <div class='package-card'><h4>3 AY</h4><h2>2000 TL</h2></div>
            <div class='package-card'><h4>6 AY</h4><h2>5000 TL</h2></div>
            <div class='package-card'><h4>12 AY</h4><h2>8000 TL</h2></div>
        </div>
        <div class='package-card' style='margin-bottom:20px;'><h4>SINIRSIZ</h4><h2 style='color:#4ade80;'>10.000 TL</h2></div>
    """, unsafe_allow_html=True)

    # 3. GİRİŞ ALANI
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 LİSANS GİRİŞİ", "👨‍💻 ADMİN"])
    with t1:
        u_lic = st.text_input("Anahtar:", placeholder="SBR-XXXX-TM")
        if st.button("SİSTEME GİRİŞ YAP"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Hatalı Anahtar!")
    with t2:
        a_t = st.text_input("Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("YÖNETİCİ GİRİŞİ"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # (Buradan sonrası V3100 ile aynıdır, muhakeme motoru çalışır)
    st.sidebar.markdown("<h3 class='neon-blue'>⚙️ GÜVEN ENDEKSİ</h3>", unsafe_allow_html=True)
    trust = st.sidebar.slider("Eşik %", 50, 98, 80)
    st.write(f"Siber Analiz Aktif. Güven Eşiği: %{trust}")
    if st.sidebar.button("ÇIKIŞ"): st.session_state.clear(); st.rerun()
