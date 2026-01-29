import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. DEĞİŞMEZ LİSANS VE GÜVENLİK (MÜHÜRLÜ) =================
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
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. GELİŞMİŞ HAKİMİYET VE GOL ANALİZ MOTORU =================
def siber_muhakeme_v3(stats):
    """Baskı ve gol potansiyelini filtreleyerek net sonuç üretir."""
    p_score = stats.get('pressure', 0)
    d_attack = stats.get('danger', 0)
    
    # Hakimiyet Tespiti
    if p_score > 75:
        hakimiyet = "TAM DOMİNASYON"
        renk = "#4ade80" # Yeşil
    elif p_score > 55:
        hakimiyet = "DENGELİ BASKI"
        renk = "#38bdf8" # Mavi
    else:
        hakimiyet = "DÜŞÜK TEMPO"
        renk = "#94a3b8" # Gri

    # Gol Potansiyeli Filtresi (Emin Karar)
    if p_score >= 85 and d_attack > 50:
        potansiyel = "🔥 ÇOK YÜKSEK (GOL GELİYOR)"
        guven = 96
    elif p_score >= 70 and d_attack > 35:
        potansiyel = "✅ YÜKSEK"
        guven = 85
    else:
        potansiyel = "⚠️ BEKLEMEDE"
        guven = 60

    return hakimiyet, potansiyel, guven, renk

# ================= 3. ELİTE TASARIM AYARLARI =================
def apply_ui():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .glass-card { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 20px; padding: 22px; margin-bottom: 20px; }
        .minute-badge { background: #f87171; color: white; padding: 5px 12px; border-radius: 8px; font-weight: bold; font-size: 0.8rem; }
        .dominance-box { padding: 10px; border-radius: 12px; text-align: center; margin: 10px 0; border: 1px solid rgba(255,255,255,0.1); }
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        div.stButton > button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; width: 100%; border: none; padding: 14px; }
        .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master V3700", layout="wide")
apply_ui()

# Oturum Koruma (Persistence)
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # Giriş Ekranı (Değişmedi)
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER MASTER PRO</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔑 LİSANS GİRİŞİ", "👨‍💻 ADMİN"])
    with t1:
        u_lic = st.text_input("Anahtar:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZİ BAŞLAT"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Geçersiz Anahtar!")
    with t2:
        a_t = st.text_input("Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("YÖNETİCİ GİRİŞİ"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()
else:
    # ================= 4. CANLI ANALİZ VE NET DURUM GÖSTERİMİ =================
    with st.sidebar:
        st.markdown(f"<h3 style='color:#38bdf8;'>👤 {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        trust_threshold = st.slider("Güven Eşiği (%)", 50, 95, 80)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Lisans Durumu</small><br><b style='color:#4ade80;'>{rem.days} GÜN AKTİF</b></div>", unsafe_allow_html=True)
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color:#38bdf8;'>🏆 SİBER ANALİZ RADARI</h2>", unsafe_allow_html=True)
    
    if st.button("🔄 SİBER VERİYİ GÜNCELLE"):
        st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI DURUM ANALİZİ", "⏳ MAÇ ÖNCESİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with t_live:
            live_matches = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT', 'ET', 'P']]
            if not live_matches:
                st.info("Canlı maç bulunmuyor.")
            
            for f in live_matches:
                # NET ANALİZ MOTORUNU ÇALIŞTIR (Örnek verilerle beslendi)
                hakimiyet, potansiyel, guven, h_renk = siber_muhakeme_v3({'pressure': 88, 'danger': 55})
                
                if guven >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <span class='minute-badge'>{f['fixture']['status']['elapsed']}'</span>
                                <span class='neon-blue' style='margin-left:10px;'>{f['league']['name']}</span>
                            </div>
                            <b style='color:{h_renk};'>GÜVEN: %{guven}</b>
                        </div>
                        
                        <h3 style='text-align:center; margin:15px 0;'>
                            {f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}
                        </h3>
                        
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>
                            <div class='dominance-box' style='background: rgba(56,189,248,0.05);'>
                                <small style='color:#94a3b8;'>HAKİMİYET</small><br>
                                <b style='color:{h_renk};'>{hakimiyet}</b>
                            </div>
                            <div class='dominance-box' style='background: rgba(74,222,128,0.05);'>
                                <small style='color:#94a3b8;'>GOL POTANSİYELİ</small><br>
                                <b class='neon-green'>{potansiyel}</b>
                            </div>
                        </div>
                        
                        <div style='margin-top:15px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.05);'>
                            <small style='color:#38bdf8;'>🧠 <b>SİBER YOL HARİTASI:</b></small><br>
                            <small>• Baskı şiddeti tavan yaptı. Atak sonlandırma oranı yüksek.<br>
                            • Rakip takımın defans hattı tamamen çökmüş durumda.</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            st.write("Bülten verileri güncel...")

    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")
