import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= SİBER CAM TASARIM (HİÇ SİYAH YOK) =================
def apply_elite_glass_theme():
    st.markdown("""
        <style>
        /* Arka Plan: Koyu Lacivert ve Gece Mavisi Geçişi */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
        }
        
        /* Glassmorphism Kartlar: Şeffaf, Cam Efekti */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        /* Yazı Renkleri */
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        .label-text { color: #94a3b8; font-size: 0.9rem; }
        
        /* Butonlar: Modern Degrade */
        div.stButton > button {
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            color: white; border: none; border-radius: 12px;
            padding: 10px; font-weight: bold; transition: 0.3s;
        }
        
        /* Inputlar */
        .stTextInput input {
            background: rgba(255, 255, 255, 0.05) !important;
            color: white !important; border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ================= KİLİTLİ LİSANS SİSTEMİ (ASLA DEĞİŞMEZ) =================
@st.cache_resource
def get_frozen_vault():
    vault = {}
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            # Sabit Seed: Sayfa yenilense de kodlar asla değişmez
            seed = f"TIMUR_PERMANENT_V27_{label}_{i}"
            h = hashlib.md5(seed.encode()).hexdigest().upper()
            key = f"SBR-{label}-{h[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_frozen_vault()
MASTER_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
MASTER_PASS = "1937timurR&"

# ================= ARAYÜZ MİMARİSİ =================
apply_elite_glass_theme()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER MASTER PRO</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 LİSANS GİRİŞİ", "👨‍💻 ADMİN"])
    
    with tab1:
        u_lic = st.text_input("Anahtarınızı Yapıştırın:", placeholder="SBR-XXXX-TM")
        if st.button("SİSTEMİ AÇ"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Geçersiz veya hatalı anahtar!")
            
    with tab2:
        a_t = st.text_input("Yönetici Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("ADMİN OLARAK GİR"):
            if a_t == MASTER_TOKEN and a_p == MASTER_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ================= CANLI PANEL (CAM TASARIM) =================
    with st.sidebar:
        st.markdown("<h2 style='color:#38bdf8;'>⚙️ PANEL</h2>", unsafe_allow_html=True)
        trust_level = st.slider("Güven Oranı (%)", 50, 95, 85)
        
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Kalan Süre</small><br><b class='neon-blue'>{rem.days} Gün</b></div>", unsafe_allow_html=True)
        
        if st.session_state["role"] == "admin":
            st.divider()
            p_sel = st.selectbox("Paket Listesi:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == p_sel]
            st.text_area("Kopyalanabilir Kodlar:", value="\n".join(keys), height=200)
            
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color: #38bdf8;'>🏆 CANLI ANALİZ MERKEZİ</h2>", unsafe_allow_html=True)
    
    

    # MAÇ KARTI ÖRNEĞİ
    st.markdown(f"""
        <div class='glass-card'>
            <div style='display: flex; justify-content: space-between;'>
                <span class='label-text'>74' Dakika | Türkiye Süper Lig</span>
                <span class='neon-green'>%{trust_level} GÜVEN</span>
            </div>
            <div style='text-align: center; margin: 15px 0;'>
                <h3 style='color: white; margin:0;'>GALATASARAY 2 - 1 FENERBAHÇE</h3>
                <p class='neon-blue' style='margin-top:10px;'>YAPAY ZEKA: Ev sahibi %72 hakimiyette. Korner beklentisi yüksek!</p>
            </div>
            <div style='display: flex; justify-content: space-around; border-top: 1px solid rgba(255,255,255,0.1); padding-top:10px;'>
                <div style='text-align:center;'>
                    <span class='label-text'>Tehlikeli Atak</span><br><b class='neon-blue'>45 - 28</b>
                </div>
                <div style='text-align:center;'>
                    <span class='label-text'>İsabetli Şut</span><br><b class='neon-green'>6 - 3</b>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.info("Canlı veriler siber hattan akıyor. Tüm sistem mobil cihazlara tam uyumludur.")
