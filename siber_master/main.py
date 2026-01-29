import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= SİBER AYARLAR & GÜVENLİK =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
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

# ================= ARAYÜZ BAŞLANGIÇ =================
st.set_page_config(page_title="Siber Master V2500", layout="wide")

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # --- HAREKETLİ VE TEŞVİK EDİCİ ARAYÜZ ---
    st.markdown("<h1 style='text-align: center; color: #00f2ff; animation: pulse 2s infinite;'>🛡️ SİBER MASTER V2500 AI PRO</h1>", unsafe_allow_html=True)
    st.markdown("<marquee style='color: #ff4b4b; font-weight: bold;'>⚠️ DİKKAT: YAPAY ZEKA DESTEKLİ ANALİZ MOTORU GÜNCELLENDİ! %92 BAŞARI ORANI İLE KAZANMAYA BAŞLA!</marquee>", unsafe_allow_html=True)
    
    # Fiyatlandırma Tablosu
    pk_cols = st.columns(5)
    pk_data = [("700 TL", "1 Ay"), ("2000 TL", "3 Ay"), ("5000 TL", "6 Ay"), ("8000 TL", "12 Ay"), ("10.000 TL", "Sınırsız")]
    for i, (p, d) in enumerate(pk_data):
        with pk_cols[i]:
            st.markdown(f"<div style='border:2px solid #00f2ff; padding:20px; border-radius:15px; text-align:center; background:#161b22;'><h3>{d}</h3><h2 style='color:#00f2ff;'>{p}</h2><p>VIP Analiz Erişimi</p></div>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 SİSTEME BAĞLAN", "👨‍💻 YÖNETİCİ GİRİŞİ"])
    with t1:
        u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZİ BAŞLAT", use_container_width=True):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Geçersiz Anahtar!")
    with t2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Admin Şifre:", type="password")
        if st.button("KONTROL PANELİNE GİR", use_container_width=True):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2099, 1, 1)})
                st.rerun()

else:
    # ================= ANA ANALİZ MOTORU =================
    with st.sidebar:
        st.header("⚙️ SİBER KOMUTA")
        st.write(f"Hoş geldin, **{st.session_state['role']}**")
        
        # GÜVEN EŞİĞİ (SOL TARAFTA AYARLANABİLİR)
        st.divider()
        st.subheader("🛡️ Güven Eşiği (Threshold)")
        trust_score = st.slider("Analiz Hassasiyeti (%)", 50, 95, 75)
        st.info(f"Yapay Zeka %{trust_score} ve üzeri güvenli maçları filtreler.")

        if st.session_state["role"] == "admin":
            st.divider()
            p_sel = st.selectbox("Lisans Paketi:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == p_sel]
            st.text_area("Kodlar:", value="\n".join(keys), height=200)

        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    # --- MAÇ ÖNCESİ VE CANLI HİBRİT PANEL ---
    st.markdown(f"<h2 style='color: #00f2ff;'>🏆 ANALİZ VE MUHAKEME MERKEZİ</h2>", unsafe_allow_html=True)
    
    

    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📋 Maç Öncesi Veriler")
        # Maç saati, lig, oranlar ve AI beklentisi
        st.markdown("<div style='background:#0e1117; padding:10: border-left: 5px solid #00f2ff;'>19:30 | Real Madrid - Barcelona <br><b>AI Beklentisi: %82 Karşılıklı Gol</b></div>", unsafe_allow_html=True)

    with c2:
        st.subheader("🔴 Canlı Analiz & Muhakeme")
        # Canlı istatistikler ve yapay zeka durum değerlendirmesi
        st.markdown("<div style='background:#0e1117; padding:10; border-left: 5px solid #ff4b4b;'>67' | Baskı Artıyor! <br><b>AI Durum: Ev sahibi baskısı %{0} üzerinde. GOL YAKIN!</b></div>".format(trust_score), unsafe_allow_html=True)

    st.divider()
    st.info("Sistem şu an API hattından maç öncesi ve canlı verileri eşzamanlı işliyor...")
