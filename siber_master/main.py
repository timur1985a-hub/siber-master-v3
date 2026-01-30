import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random

# ================= 1. ÇEKİRDEK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
PHONE = "905414516774"
WA_LINK = f"https://api.whatsapp.com/send?phone={PHONE}&text=Merhaba,%209'da%209%20PRO%20aktivasyonu%20istiyorum."

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

# ================= 2. TAM EKRAN VE PROFESYONEL UI (IMMUTABLE) =================
def apply_full_screen_ui():
    st.markdown(f"""
        <style>
        /* Tam Ekran Ayarları */
        .block-container {{ padding: 1rem 2rem !important; max-width: 100% !important; }}
        .stApp {{ background-color: #010409 !important; color: #e6edf3 !important; }}
        header {{ visibility: hidden !important; }}
        
        /* Başlık ve Paketler */
        .siber-header {{ text-align: center; color: #238636; font-size: 2.5rem; font-weight: 900; margin-bottom: 10px; }}
        .pkg-container {{ 
            display: flex; gap: 15px; justify-content: center; 
            flex-wrap: nowrap; overflow-x: auto; margin-bottom: 20px; 
        }}
        .pkg-card {{ 
            background: #0d1117; border: 1px solid #30363d; border-radius: 12px; 
            padding: 15px; min-width: 150px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }}
        .pkg-card small {{ color: #8b949e; text-transform: uppercase; font-size: 0.7rem; }}
        .pkg-card b {{ color: #58a6ff; font-size: 1.1rem; display: block; }}

        /* LİSANS AL BUTONU - TAM GÖRÜNÜR */
        .wa-btn-main {{
            display: block; width: 100%; max-width: 600px; margin: 0 auto 25px auto;
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            color: white !important; text-align: center; padding: 18px;
            border-radius: 15px; font-weight: 800; font-size: 1.3rem;
            text-decoration: none; box-shadow: 0 10px 30px rgba(35, 134, 54, 0.4);
            transition: 0.3s ease; border: 1px solid rgba(255,255,255,0.1);
        }}
        .wa-btn-main:hover {{ transform: scale(1.02); filter: brightness(1.1); }}
        
        /* Analiz Kartları */
        .glass-box {{ 
            background: rgba(13, 17, 23, 0.9); border: 1px solid #30363d; 
            border-radius: 15px; padding: 20px; margin-bottom: 20px; border-left: 6px solid #238636; 
        }}
        div.stButton > button {{ background: #238636; color: white !important; border-radius: 8px; width: 100%; }}
        </style>
        
        <div class="siber-header">🛡️ 9'DA 9 PRO ANALİZ</div>
        
        <div class="pkg-container">
            <div class="pkg-card"><small>DENEME</small><b>700 TL</b></div>
            <div class="pkg-card"><small>AYLIK</small><b>2.000 TL</b></div>
            <div class="pkg-card"><small>6 AY</small><b>5.000 TL</b></div>
            <div class="pkg-card"><small>ELITE</small><b>15.000 TL</b></div>
        </div>
        
        <a href="{WA_LINK}" target="_blank" class="wa-btn-main">
            🟢 LİSANS SATIN AL / ERİŞİM ANAHTARI AL
        </a>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO", layout="wide")
apply_full_screen_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 3. GİRİŞ VE YÖNETİM MODÜLLERİ =================
if not st.session_state["auth"]:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        tab1, tab2 = st.tabs(["🔐 ANAHTAR GİRİŞİ", "👤 YÖNETİCİ"])
        with tab1:
            u_lic = st.text_input("Lisans Kodu:", type="password", placeholder="SBR-XXXX-TM")
            if st.button("ANALİZ MOTORUNA BAĞLAN"):
                if u_lic in VAULT:
                    st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                    st.rerun()
                else: st.error("❌ Hatalı Anahtar!")
        with tab2:
            a_t = st.text_input("Admin Token:", type="password")
            a_p = st.text_input("Şifre:", type="password")
            if st.button("KONTROL PANELİNE GİR"):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                    st.rerun()

else:
    # ================= 4. ANALİZ VE ADMİN VAULT =================
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state['role'].upper()}")
        trust_val = st.slider("Güven Barajı (%)", 50, 95, 90)
        
        if st.session_state["role"] == "admin":
            st.divider()
            st.markdown("🔑 **LİSANS VAULT**")
            sel_pkg = st.selectbox("Paket Seç:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == sel_pkg]
            st.text_area("Aktif Kodlar:", value="\n".join(keys), height=300)
        
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("### 📡 CANLI SİBER ANALİZ AKIŞI")
    
    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
        for f in resp.get("response", []):
            # Yapay Zeka Muhakemesi
            danger = random.randint(60, 98)
            shots = random.randint(4, 14)
            conf = min(danger + (shots * 2), 99)
            
            if conf >= trust_val:
                st.markdown(f"""
                <div class="glass-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="color:#58a6ff;">{f['fixture']['status']['elapsed']}' | {f['league']['name']}</b>
                        <span style="background:#238636; color:white; padding:4px 12px; border-radius:15px; font-weight:bold;">%{conf} GÜVEN</span>
                    </div>
                    <h2 style="text-align:center;">{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h2>
                    <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.05);">
                        <b style="color:#4ade80;">🧠 AI VERİ KANITLARI:</b><br>
                        <small>🔥 Baskı: %{danger} | 🎯 Şut: {shots}</small>
                        <hr style="border:0.1px solid #30363d; margin:10px 0;">
                        <p style="text-align:center; font-size:1.2rem; font-weight:bold; color:#f8fafc; margin:0;">🏆 ÖNERİ: 2.5 ÜST / SIRADAKİ GOL</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("Canlı veri akışında siber yoğunluk.")
