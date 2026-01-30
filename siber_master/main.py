import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random
import time

# ================= 1. AYARLAR VE API MÜHÜRLERİ =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
# Senin Shopier JWT Token'ın
SHOPIER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..." 

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 200), ("3-AY", 90, 200), ("6-AY", 180, 200), ("12-AY", 365, 200)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. GELİŞMİŞ TIKLANABİLİR UI =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu, header, footer, .stDeployButton {visibility: hidden; display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        
        /* Paket Kartı Tasarımı */
        .stButton > button {
            width: 100%;
            height: 120px;
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 15px !important;
            color: white !important;
            transition: all 0.3s ease !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        /* Üstüne Gelince Vurgu (Hover) */
        .stButton > button:hover {
            background: linear-gradient(145deg, rgba(14, 165, 233, 0.2), rgba(37, 99, 235, 0.2)) !important;
            border-color: #38bdf8 !important;
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }

        .success-box { background: rgba(74, 222, 128, 0.1); border: 1px solid #4ade80; padding: 15px; border-radius: 10px; text-align: center; color: #4ade80; }
        .ai-muhakeme { background: rgba(14, 165, 233, 0.1); border-left: 4px solid #38bdf8; padding: 10px; border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Muhakeme", layout="wide", initial_sidebar_state="collapsed")
apply_fixed_ui()

# ================= 3. GİRİŞ VE DİREKT ÖDEME MATRİSİ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "purchased_key": None})

if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding:20px;'><h1 style='color:#38bdf8;'>🛡️ SİBER MASTER</h1><p>Hemen bir paket seç ve terminale eriş.</p></div>", unsafe_allow_html=True)

    # PAKET MATRİSİ - HER BİRİ TIKLANABİLİR DEV BUTON
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💎 1 AY ERİŞİM\n\n700 TL", key="p1"):
            with st.spinner("Ödeme Sayfası Hazırlanıyor..."):
                time.sleep(1.5)
                st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "1-AY")
    
    with col2:
        if st.button("🚀 3 AY ERİŞİM\n\n2.000 TL", key="p2"):
            with st.spinner("Ödeme Sayfası Hazırlanıyor..."):
                time.sleep(1.5)
                st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "3-AY")

    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🔥 6 AY ERİŞİM\n\n5.000 TL", key="p3"):
            with st.spinner("Ödeme Sayfası Hazırlanıyor..."):
                time.sleep(1.5)
                st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "6-AY")
    
    with col4:
        if st.button("👑 SINIRSIZ ERİŞİM\n\n15.000 TL", key="p4"):
            with st.spinner("Ödeme Sayfası Hazırlanıyor..."):
                time.sleep(1.5)
                st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "SINIRSIZ")

    # BAŞARILI ÖDEME SONRASI EKRAN
    if st.session_state.purchased_key:
        st.markdown(f"""
            <div class='success-box'>
                ✅ ÖDEME BAŞARILI!<br>
                <span style='font-size:1.2rem;'>ANAHTARINIZ: <b>{st.session_state.purchased_key}</b></span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # LİSANS AKTİVASYON
    u_lic = st.text_input("Lisans Anahtarını Buraya Gir:", value=st.session_state.purchased_key if st.session_state.purchased_key else "")
    if st.button("🚀 TERMİNALİ ÇALIŞTIR", key="launch"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "key": u_lic})
            st.rerun()
        else:
            st.error("Geçersiz Anahtar.")

# ================= 4. SİBER ANALİZ MERKEZİ (CANLI) =================
else:
    st.sidebar.success(f"Lisans Aktif: {st.session_state.key}")
    if st.sidebar.button("🔴 ÇIKIŞ YAP"): st.session_state.clear(); st.rerun()
    
    # Canlı Maç Analizleri ve Muhakeme Motoru Buraya Gelecek...
    st.title("🛡️ Siber Muhakeme Canlı Akış")
    st.info("Yapay zeka sinyalleri tarıyor. Lütfen 'Analizleri Güncelle' butonuna basın.")
