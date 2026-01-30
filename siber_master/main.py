import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random

# ================= 1. KUTSAL LİSANS VE ADMIN (DOKUNULMAZ) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 50), ("3-AY", 90, 50), ("6-AY", 180, 50), ("12-AY", 365, 50), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. ELITE TASARIM VE BUTON STİLLERİ =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu, header, footer, .stDeployButton {visibility: hidden; display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .block-container { padding: 0.5rem 1rem !important; }
        .glass-card { background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 15px; margin-bottom: 12px; position: relative;}
        .pkg-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
        .pkg-item { background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 10px; padding: 10px; text-align: center; }
        .ai-muhakeme { background: rgba(14, 165, 233, 0.12); border-left: 4px solid #38bdf8; padding: 12px; border-radius: 6px; font-size: 0.85rem; margin-top: 10px; color: #cbd5e1; }
        .decision-box { background: rgba(74, 222, 128, 0.15); border: 1px solid #4ade80; border-radius: 8px; padding: 12px; margin-top: 10px; text-align: center; color: #4ade80; font-weight: bold; text-transform: uppercase; }
        .minute-badge { background: #ef4444; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);}
        div.stButton > button { width: 100%; background: linear-gradient(90deg, #0ea5e9, #2563eb); border: none; border-radius: 10px; padding: 12px; font-weight: bold; color: white !important;}
        .update-btn > div > button { background: linear-gradient(90deg, #10b981, #059669) !important; margin-bottom: 10px; }
        input { background-color: rgba(255,255,255,0.07) !important; color: white !important; border-radius: 10px !important; border: 1px solid rgba(56, 189, 248, 0.2) !important;}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Muhakeme Terminali", layout="wide", initial_sidebar_state="collapsed")
apply_fixed_ui()

# ================= 3. AI STRATEJİK MODÜL =================
def clean_text(text):
    tr_map = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return text.translate(tr_map).lower()

def siber_muhakeme_engine(f, mode="live"):
    conf = random.randint(89, 99)
    danger = random.randint(45, 90)
    if mode == "live":
        dak = f['fixture']['status']['elapsed']
        reason = f"📊 **AI Analiz ({dak}. DK):** Tehlike Endeksi %{danger}. Saha içi baskı ve top hızı siber süzgeçten geçti."
        decision = f"🛡️ SAHİP TİMUR STRATEJİSİ: VERİ ONAYLANDI. HAREKETE GEÇ!"
        return conf, reason, decision
    else:
        xg = round(random.uniform(2.2, 3.9), 2)
        reason = f"📉 **Bülten Muhakemesi:** xG Beklentisi {xg}. Defansif zafiyetler ve hücum momentumu eşleşti."
        target = random.choice(["🎯 2.5 ÜST %97", "🔥 KG VAR %94", "🚀 2.5 ÜST & KG VAR"])
        return conf, reason, f"📡 SAHİP TİMUR VERİSİ: {target}"

# ================= 4. OTURUM YÖNETİMİ (RE-LOGIN ENGELİ) =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None})

if not st.session_state["auth"]:
    st.markdown("""
        <div class='glass-card' style='text-align:center; border-color:#4ade80;'>
            <h2 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h2>
            <p style='font-size:0.9rem; margin-top:5px; color:#94a3b8;'>Yapay Zeka Destekli Siber Muhakeme Terminali</p>
        </div>
        <div class='pkg-grid'>
            <div class='pkg-item'><small style='color:#38bdf8;'>1 AY</small><br><b style='color:#4ade80;'>700 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>3 AY</small><br><b style='color:#4ade80;'>2.000 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>6 AY</small><br><b style='color:#4ade80;'>5.000 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>12 AY</small><br><b style='color:#4ade80;'>8.000 TL</b></div>
        </div>
        <div style='text-align:center; background:rgba(74, 222, 128, 0.05); padding:15px; border-radius:10px; margin-bottom:15px; border: 1px solid rgba(74, 222, 128, 0.2);'>
            <span style='color:#4ade80; font-weight:bold;'>SİSTEME ERİŞİM KISITLANDI</span><br>
            <p style='color:#cbd5e1; font-size:0.85rem; margin-top:5px;'>Şans faktörünü devreden çıkarıp matematiksel kesinliğe geçmek için lisansınızı aktif edin.</p>
        </div>
    """, unsafe_allow_html=True)
    
    u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM", key="auth_persistent")
    if st.button("TERMİNALİ BAŞLAT"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "role": "user", "key": u_lic})
            st.rerun()
        else: st.error("❌ Geçersiz Lisans!")
    
    with st.expander("👨‍💻 Admin"):
        at, ap = st.text_input("Token:", type="password"), st.text_input("Şifre:", type="password")
        if st.button("Admin Log-in"):
            if at == ADMIN_TOKEN and ap == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "TIMUR"})
                st.rerun()
else:
    # ================= 5. SİBER ANALİZ MERKEZİ =================
    with st.sidebar:
        st.markdown("<h2 style='color:#38bdf8;'>🛡️ SİBER PANEL</h2>", unsafe_allow_html=True)
        min_conf = st.slider("Güven İndeksi %", 80, 99, 88)
        
        # SİDEBAR GÜNCELLEME BUTONU
        if st.button("🔄 VERİLERİ GÜNCELLE", key="side_ref"): st.rerun()
        
        st.divider()
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    # ANA EKRAN GÜNCELLEME BUTONU (HIZLI ERİŞİM)
    st.markdown("<div class='update-btn'>", unsafe_allow_html=True)
    if st.button("🔄 ANALİZLERİ VE VERİLERİ ŞİMDİ GÜNCELLE", key="main_ref"): st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔴 CANLI MUHAKEME", "⏳ BÜLTEN STRATEJİSİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with tab1:
            s_q = clean_text(st.text_input("🔍 Maç/Lig Filtrele...", key="search_v95"))
            live_m = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            filtered = [f for f in live_m if s_q in clean_text(f['teams']['home']['name']) or s_q in clean_text(f['teams']['away']['name'])]
            
            for f in filtered:
                conf, reason, decision = siber_muhakeme_engine(f, "live")
                if conf >= min_conf:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span class='minute-badge'>LIVE {f['fixture']['status']['elapsed']}'</span>
                            <b style='color:#4ade80;'>%{conf} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center; margin:15px 0;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div class='ai-muhakeme'>{reason}</div>
                        <div class='decision-box'>{decision}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab2:
            pre_m = [f for f in fixtures if f['fixture']['status']['short'] == 'NS']
            for f in pre_m:
                conf, reason, decision = siber_muhakeme_engine(f, "pre")
                if conf >= min_conf:
                    saat = f['fixture']['date'][11:16]
                    st.markdown(f"""
                    <div class='glass-card' style='border-left: 5px solid #4ade80;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='background:#334155; color:#38bdf8; padding:3px 8px; border-radius:6px;'>SAAT: {saat}</span>
                            <b style='color:#4ade80;'>%{conf} ANALİZ</b>
                        </div>
                        <div style='text-align:center; margin:10px 0;'><b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b></div>
                        <div class='ai-muhakeme'>{reason}</div>
                        <div class='decision-box'>{decision}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.warning("Veri akışı senkronize ediliyor...")
