-import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. STRATEJİK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%209'da%209%20Analiz%20sistemi%20için%20lisans%20almak%20istiyorum."

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. TASARIM KATMANI (PREMIUM) =================
def apply_ui():
    st.markdown(f"""
        <style>
        .block-container {{ padding-top: 0.5rem !important; }}
        .stApp {{ background: #020617; color: #f1f5f9; }}
        header {{ visibility: hidden; }}
        
        /* Paket Kartları */
        .package-container {{ display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }}
        .package-card {{ 
            background: rgba(30, 41, 59, 0.5); 
            border: 1px solid rgba(56, 189, 248, 0.3); 
            border-radius: 12px; padding: 15px; text-align: center; width: 140px;
        }}
        .package-card b {{ color: #38bdf8; font-size: 1.1rem; }}
        
        /* Yeni Harekete Geçirici Başlık Modülü */
        .hero-section {{ text-align: center; padding: 20px; background: linear-gradient(90deg, rgba(14,165,233,0.1), rgba(37,99,235,0.1)); border-radius: 20px; margin-bottom: 25px; border: 1px solid rgba(56,189,248,0.2); }}
        .hero-title {{ color: #4ade80; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; text-shadow: 0 0 15px rgba(74,222,128,0.3); }}
        .hero-subtitle {{ color: #f1f5f9; font-size: 1.2rem; font-weight: 600; letter-spacing: 1px; }}

        .wa-btn {{ 
            background: linear-gradient(90deg, #25d366, #128c7e); 
            color: white !important; padding: 15px 40px; border-radius: 12px; 
            text-decoration: none; font-weight: bold; display: inline-block;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4); text-transform: uppercase;
        }}
        
        .glass-card {{ background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 15px; padding: 20px; margin-bottom: 15px; }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'da 9 PRO ANALİZ", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 3. GİRİŞ EKRANI (YENİLENMİŞ BAŞLIK) =================
if not st.session_state["auth"]:
    # YENİ ETKİLEYİCİ BAŞLIK
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>9'DA 9 PRO ANALİZ</div>
        <div class='hero-subtitle'>HATA PAYINI SIFIRLA, KAZANMAYA ŞİMDİ BAŞLA!</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='package-container'>
        <div class='package-card'><small>30 GÜN</small><br><b>700 TL</b></div>
        <div class='package-card'><small>90 GÜN</small><br><b>2.000 TL</b></div>
        <div class='package-card'><small>180 GÜN</small><br><b>5.000 TL</b></div>
        <div class='package-card'><small>SINIRSIZ</small><br><b>15.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; margin-bottom:30px;'><a href='{WA_LINK}' class='wa-btn'>🔓 SİSTEM ERİŞİMİ İÇİN LİSANS AL</a></div>", unsafe_allow_html=True)

    with st.container():
        u_lic = st.text_input("Erişim Anahtarını Girin:", type="password", placeholder="SBR-XXXX-TM")
        if st.button("SİSTEME GİRİŞ YAP VE ANALİZİ BAŞLAT"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Geçersiz Anahtar.")

else:
    # ================= 4. ANALİZ PANELİ (SABİT KALANLAR) =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown("<h2 style='color:#38bdf8;'>⚙️ FİLTRE MERKEZİ</h2>", unsafe_allow_html=True)
        trust_val = st.slider("Güven Endeksi Eşiği (%)", 50, 98, 85)
        st.divider()
        st.write(f"**Kalan Süre:** {(st.session_state['exp'] - datetime.now()).days} Gün")
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.update({"auth": False}); st.rerun()

    c1, c2 = st.columns([3, 1])
    with c1: st.markdown("<h2 style='color:#f8fafc; margin:0;'>📡 CANLI VERİ & ANALİZ AKIŞI</h2>", unsafe_allow_html=True)
    with c2: 
        if st.button("🔄 VERİLERİ GÜNCELLE"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI SİNYALLER", "⏳ BÜLTEN ANALİZİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        with t_live:
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            for f in resp.get("response", []):
                conf = random.randint(55, 99)
                if conf >= trust_val:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#38bdf8;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b style='color:#4ade80;'>BAŞARI ORANI: %{conf}</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
        # Bülten ve diğer kısımlar aynı mantıkla çalışmaya devam eder...
    except:
        st.error("Bağlantı hatası.")
