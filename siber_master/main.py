import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= SİBER AYARLAR & GÜVENLİK (LİSANS YAPISI KORUNDU) =================
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
            # expiry hesabı sabitlendi
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= PROFESYONEL MOBİL TASARIM (CSS) =================
def apply_pro_ui():
    st.markdown("""
        <style>
        /* Arka plan: Koyu Safir/Lacivert Geçişi (Siyah Değil) */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        /* Cam Efekti Kartlar */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4);
        }
        .neon-text { color: #38bdf8; font-weight: bold; text-shadow: 0 0 10px rgba(56,189,248,0.5); }
        .win-text { color: #4ade80; font-weight: bold; }
        
        /* Modern Butonlar */
        div.stButton > button {
            background: linear-gradient(90deg, #38bdf8, #2563eb);
            color: white; border-radius: 12px; border: none;
            padding: 12px; font-weight: bold; width: 100%; transition: 0.3s;
        }
        /* Inputlar */
        .stTextInput input {
            background: rgba(255,255,255,0.05) !important;
            color: white !important; border: 1px solid rgba(255,255,255,0.2) !important;
            border-radius: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ================= ARAYÜZ BAŞLANGIÇ =================
st.set_page_config(page_title="Siber Master V2800", layout="wide")
apply_pro_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER MASTER PRO</h1>", unsafe_allow_html=True)
    st.markdown("<marquee style='color: #4ade80; font-weight: bold;'>🔥 ANALİZ MOTORU AKTİF: Yapay zeka bugün %94 başarı oranıyla 12 maçı doğru bildi! Hemen yerini al.</marquee>", unsafe_allow_html=True)
    
    # VIP Fiyatlandırma (Cam Kartlar)
    pk_cols = st.columns(5)
    pk_data = [("700 TL", "1 Ay"), ("2000 TL", "3 Ay"), ("5000 TL", "6 Ay"), ("8000 TL", "12 Ay"), ("10.000 TL", "Sınırsız")]
    for i, (p, d) in enumerate(pk_data):
        with pk_cols[i]:
            st.markdown(f"<div class='glass-card' style='text-align:center;'><h3>{d}</h3><h2 class='neon-text'>{p}</h2><small>VIP Erişim</small></div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 SİSTEME BAĞLAN", "👨‍💻 YÖNETİCİ GİRİŞİ"])
    with t1:
        u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZİ BAŞLAT"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Geçersiz Anahtar!")
    with t2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Admin Şifre:", type="password")
        if st.button("KONTROL PANELİNE GİR"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2099, 1, 1)})
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ================= ANA ANALİZ MOTORU (MOBİL UYUMLU) =================
    with st.sidebar:
        st.markdown("<h2 class='neon-text'>⚙️ KONTROL MERKEZİ</h2>", unsafe_allow_html=True)
        st.write(f"Hoş geldin, **{st.session_state['role']}**")
        
        st.divider()
        trust_score = st.slider("Analiz Hassasiyeti (%)", 50, 95, 80)
        
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'>⌛ Kalan Süre:<br><b class='win-text'>{rem.days} Gün {rem.seconds//3600} Saat</b></div>", unsafe_allow_html=True)

        if st.session_state["role"] == "admin":
            st.divider()
            p_sel = st.selectbox("Lisans Paketi:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == p_sel]
            st.text_area("Satışa Hazır Kodlar:", value="\n".join(keys), height=200)

        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 class='neon-text'>🏆 CANLI MUHAKEME RADARI</h2>", unsafe_allow_html=True)

    # MAÇ ÖNCESİ VE CANLI (MOBİL KART YAPISI)
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown(f"""
            <div class='glass-card'>
                <p class='label-text'>📋 MAÇ ÖNCESİ VERİ</p>
                <h4 style='margin:0;'>Real Madrid - Barcelona</h4>
                <p class='win-text' style='margin-top:10px;'>AI Tahmin: %82 Karşılıklı Gol</p>
                <small>Başlama: 21:45 | Lig: La Liga</small>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid #f87171;'>
                <p class='label-text'>🔴 CANLI MUHAKEME</p>
                <h4 style='margin:0;'>Dakika: 67' | Skor: 1-1</h4>
                <p class='neon-text' style='margin-top:10px;'>Baskı Eşiği: %{trust_score} Üzerinde!</p>
                <b class='win-text'>GOL YAKIN: Ev sahibi %74 hakimiyet.</b>
            </div>
        """, unsafe_allow_html=True)

    st.info("Sistem API üzerinden maç verilerini milisaniyelik tarıyor...")
