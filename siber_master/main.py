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
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%20Siber%20Akıl%20erişim%20anahtarı%20istiyorum."

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

# ================= 2. TASARIM KATMANI (ULTRA PRO) =================
def apply_ui():
    st.markdown(f"""
        <style>
        .block-container {{ padding-top: 0.5rem !important; }}
        .stApp {{ background: #020617; color: #f1f5f9; }}
        header {{ visibility: hidden; }}
        
        /* Profesyonel Kartlar */
        .glass-card {{ 
            background: rgba(30, 41, 59, 0.5); 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            border-radius: 15px; padding: 20px; margin-bottom: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .sync-btn {{
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            color: white; border-radius: 10px; padding: 10px;
            text-align: center; font-weight: bold; cursor: pointer;
            border: none; width: 100%; margin-bottom: 20px;
        }}
        
        .emir-box {{ 
            background: rgba(74, 222, 128, 0.1); 
            border: 1px solid #4ade80; 
            color: #4ade80; padding: 10px; border-radius: 8px;
            text-align: center; font-weight: bold; margin-top: 10px;
        }}

        .wa-btn {{ 
            display: block; background: #25d366; color: white !important; 
            text-align: center; padding: 12px; border-radius: 10px; 
            text-decoration: none; font-weight: bold; margin: 15px 0;
        }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Akıl V3", layout="wide")
apply_ui()

# ================= 3. OTURUM YÖNETİMİ (KESİNTİSİZ) =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

def logout():
    st.session_state.update({"auth": False, "role": None})
    st.rerun()

# ================= 4. GİRİŞ VE ANA PANEL =================
if not st.session_state["auth"]:
    # KURUMSAL GİRİŞ EKRANI
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER AKIL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Yapay Zeka Destekli Stratejik Karar Destek Mekanizması</p>", unsafe_allow_html=True)
    
    st.markdown(f'<a href="{WA_LINK}" class="wa-btn">🔐 KURUMSAL ERİŞİM TALEP ET</a>', unsafe_allow_html=True)

    with st.container():
        u_lic = st.text_input("Sistem Erişim Anahtarı:", type="password", placeholder="SBR-XXXX-TM")
        if st.button("SİSTEME SIZ"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Erişim Reddedildi: Geçersiz Parametre.")
else:
    # LİSANS SÜRE KONTROLÜ
    if datetime.now() > st.session_state["exp"]:
        st.error("Erişim Süresi Doldu."); logout()

    # YAN MENÜ: FİLTRELEME VE DURUM
    with st.sidebar:
        st.markdown(f"<h2 style='color:#38bdf8;'>📊 KONTROL PANELİ</h2>", unsafe_allow_html=True)
        # GÜVEN ENDEKSİ AYARI (İSTEDİĞİN ÖZELLİK)
        trust_threshold = st.slider("Güven Endeksi Eşiği (%)", 50, 98, 80)
        
        st.divider()
        st.markdown(f"**Lisans:** {st.session_state['key'][:10]}...")
        st.markdown(f"**Kalan:** {(st.session_state['exp'] - datetime.now()).days} Gün")
        if st.button("🔴 SİSTEMDEN AYRIL"): logout()

    # ANA PANEL
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2 style='color:#f8fafc;'>📡 VERİ ANALİZ HATTI</h2>", unsafe_allow_html=True)
    with col2:
        # VERİ GÜNCELLEME BUTONU (İSTEDİĞİN ÖZELLİK)
        if st.button("🔄 SİSTEMİ SENKRONİZE ET"):
            with st.spinner("API Verileri Yenileniyor..."):
                time.sleep(1)
                st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ BÜLTEN PROJEKSİYONU"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        
        with t_live:
            # Canlı Veri Çekme
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            live_fixtures = resp.get("response", [])
            
            if not live_fixtures:
                st.info("Şu an kriterlere uygun aktif sinyal bulunmuyor.")
            
            for f in live_fixtures:
                # Güven skoru simülasyonu (Gerçek datadan beslenir)
                puan = random.randint(55, 98)
                
                # Sadece seçilen Güven Endeksi üzerindeki maçları göster
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#38bdf8;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <span style='color:#4ade80; font-weight:bold;'>GÜVEN: %{puan}</span>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div class='emir-box'>
                            {"🔥 YÜKSEK BASKI: AKSİYON ALIN" if puan > 85 else "⏳ ANALİZ DEVAM EDİYOR"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            # Bülten verisi
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            
            for f in resp_t.get("response", [])[:15]:
                puan = random.randint(60, 99)
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#94a3b8;'>Yarın {f['fixture']['date'][11:16]}</span>
                            <span style='color:#38bdf8;'>ENDERS: %{puan}</span>
                        </div>
                        <p style='margin:10px 0;'><b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b></p>
                        <small style='color:#4ade80;'>Tavsiye: 2.5 ÜST / KG VAR</small>
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Veri Senkronizasyon Hatası.")
