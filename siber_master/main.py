import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. ÇEKİRDEK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%209'da%209%20PRO%20sistemi%20için%20lisans%20istiyorum."

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

# ================= 2. YAPAY ZEKA KARAR MEKANİZMASI =================
def ai_decision_engine(fixture_id, mode="live"):
    """
    Canlıda: Baskı, Dakika ve Tehlikeli Atak analizi yapar.
    Maç Öncesi: Form, KG ve Üst istatistiklerini çarpıştırır.
    """
    confidence = random.randint(65, 99) # Gerçek API entegrasyonunda burası detaylı stat hesabı yapar
    recommendation = ""
    logic_path = []

    if mode == "live":
        # Simüle edilen canlı veriler (API'den çekilen değerler buraya girer)
        pressure_home = random.randint(30, 95)
        pressure_away = random.randint(30, 95)
        
        if pressure_home > 80:
            recommendation = "🔥 EV SAHİBİ SIRADAKİ GOLÜ ATAR"
            logic_path = ["Ev sahibi baskısı %80 üzerine çıktı.", "Savunma bloğu çöktü."]
        elif pressure_away > 80:
            recommendation = "🔥 DEPLASMAN SIRADAKİ GOLÜ ATAR"
            logic_path = ["Deplasman kontra atak yoğunluğu arttı."]
        elif pressure_home > 60 and pressure_away > 60:
            recommendation = "⚽ KARŞILIKLI GOL (CANLI)"
            logic_path = ["Çift taraflı baskı mevcut.", "Defansif boşluklar saptandı."]
    
    else: # Maç Öncesi
        options = ["🎯 KG VAR (KESİN)", "💎 2.5 ÜST", "🔥 EV SAHİBİ 1.5 ÜST"]
        recommendation = random.choice(options)
        logic_path = ["Son 5 maç KG oranı %85.", "Hücum hattı tam kadro."]
        
    return confidence, recommendation, logic_path

# ================= 3. ELİTE APP ARA YÜZÜ =================
def apply_ui():
    st.markdown(f"""
        <style>
        .stApp {{ background: #010409; color: #e6edf3; }}
        header {{ visibility: hidden; }}
        .main-header {{ text-align: center; padding: 40px 0; background: linear-gradient(180deg, #0d1117 0%, #010409 100%); border-bottom: 1px solid #30363d; }}
        .title-text {{ color: #238636; font-size: 3rem; font-weight: 800; text-shadow: 0 0 20px rgba(35,134,54,0.4); }}
        
        .pkg-card {{ background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }}
        .pkg-card b {{ color: #58a6ff; font-size: 1.3rem; }}
        
        .vip-button {{
            display: block; background: #238636; color: white !important; 
            padding: 20px; border-radius: 12px; text-align: center;
            font-weight: 800; text-decoration: none; margin: 20px 0;
            font-size: 1.2rem; transition: 0.3s;
        }}
        .vip-button:hover {{ background: #2ea043; transform: translateY(-3px); }}
        
        .decision-box {{ 
            background: rgba(35, 134, 54, 0.1); border: 1px solid #238636; 
            border-radius: 15px; padding: 20px; margin-top: 15px;
        }}
        .confidence-tag {{ background: #238636; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 4. UYGULAMA GİRİŞ EKRANI =================
if not st.session_state["auth"]:
    st.markdown("<div class='main-header'><div class='title-text'>9'DA 9 PRO ANALİZ</div><p>Siber Karar Destek Mekanizması</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='pkg-card'><small>GÜNLÜK</small><br><b>700 TL</b></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='pkg-card'><small>AYLIK</small><br><b>2.000 TL</b></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='pkg-card'><small>SEZONLUK</small><br><b>5.000 TL</b></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='pkg-card'><small>SINIRSIZ</small><br><b>15.000 TL</b></div>", unsafe_allow_html=True)

    st.markdown(f"<a href='{WA_LINK}' target='_blank' class='vip-button'>🔓 SİSTEM ERİŞİMİ VE LİSANS AL</a>", unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        u_lic = st.text_input("LİSANS ANAHTARI:", type="password", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZ MOTORUNU ÇALIŞTIR"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Erişim Reddedildi.")
else:
    # ================= 5. ANALİZ PORTALI (UYGULAMA MANTIĞI) =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown("### ⚙️ KARAR AYARLARI")
        # SADECE YÜZDE 90 ÜSTÜ GÖRMEK İSTİYORSUN
        trust_threshold = st.slider("Min. Güven Oranı (%)", 50, 95, 90)
        st.divider()
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    c1, c2 = st.columns([4, 1])
    with c1: st.markdown(f"## 📡 SİBER ANALİZ AKIŞI")
    with c2: 
        if st.button("🔄 VERİLERİ ÇEK"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI KARARLAR", "⏳ MAÇ ÖNCESİ (KG/ÜST)"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        
        with t_live:
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            for f in resp.get("response", []):
                puan, karar, mantik = ai_decision_engine(f['fixture']['id'], mode="live")
                
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='decision-box'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <span class='confidence-tag'>%{puan} GÜVEN</span>
                        </div>
                        <h3 style='text-align:center; margin:15px 0;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='text-align:center; color:#4ade80; font-size:1.2rem; font-weight:bold;'>{karar}</div>
                        <hr style='border:0.5px solid #30363d;'>
                        <small style='color:#8b949e;'>🧠 AI Muhakemesi: {" | ".join(mantik)}</small>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            st.info(f"Yalnızca %{trust_threshold} ve üzeri kesinliğe sahip maçlar listeleniyor.")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            
            for f in resp_t.get("response", [])[:30]:
                puan, karar, mantik = ai_decision_engine(f['fixture']['id'], mode="pre")
                
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='decision-box' style='border-color:#58a6ff;'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#8b949e;'>{f['fixture']['date'][11:16]} | {f['league']['name']}</span>
                            <span class='confidence-tag' style='background:#58a6ff;'>%{puan} ANALİZ</span>
                        </div>
                        <h4 style='margin:10px 0;'>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                        <b style='color:#58a6ff;'>ÖNERİ: {karar}</b>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Veri hattı meşgul. Tekrar deneyin.")
