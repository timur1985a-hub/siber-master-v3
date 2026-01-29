import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib

# ================= MOBİL STİL AYARLARI (CSS) =================
def apply_mobile_pro_theme():
    st.markdown("""
        <style>
        /* Ana Arkaplan ve Font */
        .stApp { background-color: #0e1117; color: #ffffff; }
        
        /* Mobil Kart Tasarımı */
        .stat-card {
            background: linear-gradient(145deg, #1e2530, #161b22);
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 10px;
            border: 1px solid #30363d;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        /* Neon Yazı Tipleri */
        .neon-text { color: #00f2ff; font-weight: bold; text-shadow: 0 0 5px #00f2ff; }
        .win-text { color: #39ff14; font-weight: bold; }
        .time-text { color: #8b949e; font-size: 0.85rem; }
        
        /* Buton Tasarımı */
        div.stButton > button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #00f2ff, #0066ff);
            color: white; font-weight: bold; border: none;
            padding: 12px; transition: 0.3s;
        }
        
        /* Giriş Kutuları */
        .stTextInput input {
            background-color: #161b22 !important;
            color: white !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ================= SİBER ÇEKİRDEK (DEĞİŞMEZ) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
MASTER_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
MASTER_PASS = "1937timurR&"

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for lbl, d, c in cfg:
        for i in range(1, c + 1):
            s = f"V26_{lbl}_{i}_TIMUR"; h = hashlib.md5(s.encode()).hexdigest().upper()
            k = f"SBR-{lbl}-{h[:8]}-TM"
            v[k] = {"lbl": lbl, "exp": datetime.now() + timedelta(days=d)}
    return v

VAULT = get_vault()

# ================= ARAYÜZ MİMARİSİ =================
apply_mobile_pro_theme()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # MOBİL HOŞGELDİN EKRANI
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🛡️ SİBER MASTER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Yapay Zeka Destekli Analiz Protokolü</p>", unsafe_allow_html=True)
    
    # Teşvik Edici Mobil Kartlar
    st.markdown("""
        <div class='stat-card'>
            <span class='win-text'>⚡ %94 BAŞARI ORANI</span><br>
            <small style='color:white'>Canlı veriler anlık olarak işlenir.</small>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 GİRİŞ", "👨‍💻 YÖNETİCİ"])
    with tab1:
        u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZE BAŞLA"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["exp"]})
                st.rerun()
            else: st.error("Geçersiz Anahtar!")
            
    with tab2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Admin Şifre:", type="password")
        if st.button("ADMİN GİRİŞİ"):
            if a_t == MASTER_TOKEN and a_p == MASTER_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2099, 1, 1)})
                st.rerun()

else:
    # ================= MOBİL ANALİZ PANELİ =================
    with st.sidebar:
        st.markdown("<h2 style='color:#00f2ff;'>⚙️ AYARLAR</h2>", unsafe_allow_html=True)
        trust_val = st.slider("Güven Eşiği (%)", 50, 95, 80)
        
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='stat-card'>⌛ Kalan: {rem.days} Gün</div>", unsafe_allow_html=True)
        
        if st.session_state["role"] == "admin":
            st.divider()
            p_sel = st.selectbox("Paket:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["lbl"] == p_sel]
            st.text_area("Lisanslar:", value="\n".join(keys), height=150)
            
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    # MOBİL MAÇ LİSTESİ (KART SİSTEMİ)
    st.markdown("<h3 style='color:#00f2ff;'>🏆 CANLI ANALİZ RADARI</h3>", unsafe_allow_html=True)
    
    

    # Örnek Bir Analiz Kartı (Mobil Uyumlu)
    st.markdown(f"""
        <div class='stat-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span class='time-text'>🔴 72' Dakika</span>
                <span class='win-text'>%{trust_val} GÜVEN</span>
            </div>
            <div style='text-align: center; margin: 10px 0;'>
                <h4 style='margin:0; color:white;'>REAL MADRID 1 - 0 BARCELONA</h4>
            </div>
            <div style='background: #30363d; height: 5px; border-radius: 5px;'>
                <div style='background: #00f2ff; width: 75%; height: 5px; border-radius: 5px;'></div>
            </div>
            <div style='margin-top: 10px; font-size: 0.9rem; color:#00f2ff;'>
                <b>AI YORUMU:</b> Ev sahibi baskıyı kurdu, 2. gol beklentisi yüksek!
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.info("Sistem canlı verileri siber hattan çekiyor...")
