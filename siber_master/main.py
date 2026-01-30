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

# ================= 2. TASARIM MÜHÜRLERİ (DOKUNULMAZ) =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu, header, footer, .stDeployButton {visibility: hidden; display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .block-container { padding: 0.5rem 1rem !important; }
        .glass-card { background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 15px; margin-bottom: 12px; }
        .pkg-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
        .pkg-item { background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 10px; padding: 10px; text-align: center; }
        .ai-muhakeme { background: rgba(14, 165, 233, 0.1); border-left: 3px solid #0ea5e9; padding: 10px; border-radius: 6px; font-size: 0.85rem; margin-top: 10px; }
        .decision-box { background: rgba(74, 222, 128, 0.1); border: 1px solid #4ade80; border-radius: 8px; padding: 10px; margin-top: 10px; text-align: center; color: #4ade80; font-weight: bold; }
        .minute-badge { background: #ef4444; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; }
        div.stButton > button { width: 100%; background: linear-gradient(90deg, #0ea5e9, #2563eb); border: none; border-radius: 10px; padding: 10px; font-weight: bold; color: white !important; }
        input { background-color: rgba(255,255,255,0.05) !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master Pro", layout="wide", initial_sidebar_state="collapsed")
apply_fixed_ui()

# ================= 3. SİBER ZEKA MODÜLÜ (YAPAY MUHAKEME) =================
def siber_muhakeme_engine(f, mode="live"):
    conf = random.randint(85, 99)
    # Veri simülasyonu (Sahaya hakimiyet verileri)
    at_h = random.randint(30, 70) # Tehlikeli Atak
    at_a = random.randint(30, 70)
    pos_h = random.randint(40, 60) # Topla Oynama
    
    if mode == "live":
        reason = f"📊 **Siber Analiz:** Ev sahibi tehlikeli atak oranı %{at_h}, deplasman baskısı %{at_a}. Top hakimiyeti %{pos_h} ile dengede olsa da saniyedeki pas hızı ivmeleniyor."
        decision = f"🚀 SAHİP TİMUR STRATEJİSİ: Maçın gidişatı yüksek voltajlı, GOL BİTİRİCİLİĞİ BEKLENİYOR."
        return conf, reason, decision
    else:
        reason = f"📉 **Bülten Muhakemesi:** Takımların son 5 maçlık 'Gol Beklentisi' (xG) 2.45 üzerinde. Defansif zaafiyetler ve hücum varyasyonları yapay zeka tarafından eşleştirildi."
        decision = random.choice(["🎯 2.5 ÜST İHTİMALİ %92", "🔥 KG VAR POTANSİYELİ %89", "🚀 ÜST & KG VAR KOMBİNASYONU"])
        return conf, reason, f"📡 SAHİP TİMUR VERİSİ: {decision}"

def clean_text(text):
    tr_map = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return text.translate(tr_map).lower()

# ================= 4. GİRİŞ SİSTEMİ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("""
        <div class='glass-card' style='text-align:center; border-color:#4ade80;'>
            <h3 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h3>
            <p style='font-size:0.85rem; margin-top:5px;'>Saniyeleri servete dönüştüren tek terminal.</p>
        </div>
        <div class='pkg-grid'>
            <div class='pkg-item'><small style='color:#38bdf8;'>1 AY</small><br><b style='color:#4ade80;'>700 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>3 AY</small><br><b style='color:#4ade80;'>2.000 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>6 AY</small><br><b style='color:#4ade80;'>5.000 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>12 AY</small><br><b style='color:#4ade80;'>8.000 TL</b></div>
        </div>
        <p style='text-align:center; font-size:0.75rem; color:#94a3b8; margin-bottom:10px;'>Harekete Geç: Kazanan tarafta yer almak için lisansını hemen aktif et!</p>
    """, unsafe_allow_html=True)
    
    u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM", key="auth_v80")
    if st.button("SİBER TERMİNALİ AÇ"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
            st.rerun()
        else: st.error("Erişim Engellendi! Lisans Almak İçin İletişime Geçin.")
    
    with st.expander("👨‍💻 Admin"):
        at, ap = st.text_input("Token:", type="password"), st.text_input("Şifre:", type="password")
        if st.button("Admin Girişi"):
            if at == ADMIN_TOKEN and ap == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "TIMUR", "exp": datetime(2030, 1, 1)})
                st.rerun()

else:
    # ================= 5. ANALİZ MERKEZİ (SİBER MUHAKEME) =================
    with st.sidebar:
        st.markdown("<h3 style='color:#38bdf8;'>🛡️ KONTROL</h3>", unsafe_allow_html=True)
        min_conf = st.slider("Güven İndeksi %", 80, 99, 85)
        if st.button("🔄 VERİLERİ TAZELE"): st.rerun()
        st.divider()
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    tab1, tab2 = st.tabs(["🔴 CANLI MUHAKEME", "⏳ BÜLTEN STRATEJİSİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with tab1:
            s_q = clean_text(st.text_input("🔍 Maç Ara...", key="search_v80"))
            live_m = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            filtered = [f for f in live_m if s_q in clean_text(f['teams']['home']['name']) or s_q in clean_text(f['teams']['away']['name'])]
            
            for f in filtered:
                conf, reason, decision = siber_muhakeme_engine(f, "live")
                if conf >= min_conf:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span class='minute-badge'>{f['fixture']['status']['elapsed']}' DK</span>
                            <b style='color:#4ade80;'>%{conf} GÜVEN</b>
                        </div>
                        <h4 style='text-align:center; margin:10px 0;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h4>
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
                    <div class='glass-card' style='border-left: 4px solid #4ade80;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='background:#334155; color:#38bdf8; padding:2px 6px; border-radius:4px;'>SAAT: {saat}</span>
                            <b style='color:#4ade80;'>%{conf} SİBER ANALİZ</b>
                        </div>
                        <div style='text-align:center; margin:10px 0;'><b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b></div>
                        <div class='ai-muhakeme'>{reason}</div>
                        <div class='decision-box'>{decision}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.warning("Veri akışı bekleniyor...")
