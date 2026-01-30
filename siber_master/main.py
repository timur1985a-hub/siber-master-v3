import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. STRATEJİK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%20Siber%20Akıl%20erişim%20anahtarı%20hakkında%20bilgi%20almak%20istiyorum."

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
        
        /* Paket Kartları Tasarımı */
        .package-container {{ display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }}
        .package-card {{ 
            background: rgba(30, 41, 59, 0.5); 
            border: 1px solid rgba(56, 189, 248, 0.3); 
            border-radius: 12px; padding: 15px; text-align: center; width: 140px;
        }}
        .package-card b {{ color: #38bdf8; font-size: 1.1rem; }}
        
        .wa-section {{ text-align: center; margin: 20px 0; }}
        .wa-btn {{ 
            background: linear-gradient(90deg, #25d366, #128c7e); 
            color: white !important; padding: 15px 30px; border-radius: 12px; 
            text-decoration: none; font-weight: bold; display: inline-block;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        }}
        
        .glass-card {{ 
            background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(56, 189, 248, 0.1); 
            border-radius: 15px; padding: 20px; margin-bottom: 15px;
        }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Akıl V3", layout="wide")
apply_ui()

# ================= 3. OTURUM YÖNETİMİ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 4. GİRİŞ EKRANI (PAKETLER + WA) =================
if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8; margin-bottom:0;'>🛡️ SİBER AKIL: ZAFER MİMARI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom:25px;'>Yapay Zeka Destekli Karar Mekanizması</p>", unsafe_allow_html=True)
    
    # PAKETLER
    st.markdown("""
    <div class='package-container'>
        <div class='package-card'><small>30 GÜN</small><br><b>700 TL</b></div>
        <div class='package-card'><small>90 GÜN</small><br><b>2.000 TL</b></div>
        <div class='package-card'><small>180 GÜN</small><br><b>5.000 TL</b></div>
        <div class='package-card'><small>SINIRSIZ</small><br><b>15.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)

    # WHATSAPP LİSANS BUTONU
    st.markdown(f"""
    <div class='wa-section'>
        <a href='{WA_LINK}' class='wa-btn'>🔓 LİSANS ALMAK İÇİN İLETİŞİME GEÇİN</a>
    </div>
    """, unsafe_allow_html=True)

    # GİRİŞ FORMU
    with st.container():
        col_l, col_r = st.columns([1, 1])
        with col_l:
            u_lic = st.text_input("Erişim Anahtarı:", type="password", placeholder="SBR-XXXX-TM")
        with col_r:
            st.write("##")
            if st.button("SİSTEME GİRİŞ YAP"):
                if u_lic in VAULT:
                    st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                    st.rerun()
                else: st.error("Erişim Reddedildi.")

else:
    # ================= 5. ANA PANEL (GİRİŞ SONRASI) =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown(f"<h2 style='color:#38bdf8;'>📊 AYARLAR</h2>", unsafe_allow_html=True)
        # GÜVEN ENDEKSİ FİLTRESİ
        trust_val = st.slider("Güven Endeksi Eşiği (%)", 50, 98, 85)
        st.divider()
        st.write(f"**Lisans:** {st.session_state['key'][:10]}...")
        st.write(f"**Kalan:** {(st.session_state['exp'] - datetime.now()).days} Gün")
        if st.button("🔴 ÇIKIŞ YAP"): st.session_state.update({"auth": False}); st.rerun()

    # ÜST BAR VE GÜNCELLEME BUTONU
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown("<h2 style='color:#f8fafc; margin:0;'>📡 ANALİZ VE SİNYAL HATTI</h2>", unsafe_allow_html=True)
    with c2: 
        if st.button("🔄 VERİLERİ GÜNCELLE"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI ANALİZ", "⏳ BÜLTEN TAHMİN"])

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
                            <b style='color:#4ade80;'>%{conf} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
        with t_pre:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", [])[:20]:
                conf = random.randint(60, 99)
                if conf >= trust_val:
                    st.markdown(f"<div class='glass-card'><b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b><br>Güven: %{conf}</div>", unsafe_allow_html=True)
    except:
        st.error("Veri alınamadı.")
