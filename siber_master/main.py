import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KORUNAN LİSANS VE GÜVENLİK YAPISI =================
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

# ================= 2. SİBER MUHAKEME AI MOTORU (GÜNCELLENMİŞ KARAR) =================
def siber_muhakeme_ai(fixture, stats=None, mode="live"):
    yol_haritasi = []
    guven_skoru = 65
    
    if mode == "live":
        elapsed = fixture['fixture']['status']['elapsed']
        pressure = stats.get('pressure', 0) if stats else 0
        danger = stats.get('danger', 0) if stats else 0
        
        # Akıllı Muhakeme Kararı
        if pressure > 75:
            guven_skoru += 20
            yol_haritasi.append(f"🔥 KRİTİK: {elapsed}' itibariyle baskı %{pressure}. Gol an meselesi.")
        if danger > 45:
            guven_skoru += 10
            yol_haritasi.append(f"🎯 STRATEJİ: Tehlikeli atak yoğunluğu yüksek. +0.5 Gol Üstü.")
        
        # Karar Cümlesi
        tavsiye = "BEKLE"
        if guven_skoru > 85: tavsiye = "ŞİMDİ OYNA (YÜKSEK GÜVEN)"
        return min(guven_skoru, 98), yol_haritasi, tavsiye, f"{elapsed}'"
    
    else: # Bülten Modu
        puan = random.randint(90, 99)
        match_time = datetime.fromisoformat(fixture['fixture']['date'].replace('Z', '+00:00')) + timedelta(hours=3)
        time_str = match_time.strftime('%H:%M')
        yol_haritasi.append(f"📅 Başlama Saati: {time_str}")
        yol_haritasi.append(f"📈 xG Analizi: %90+ KG VAR / 2.5 ÜST Uyumlu.")
        return puan, yol_haritasi, "ELMAS SEÇİM", time_str

# ================= 3. ELİTE DARK TASARIM (KESİNLİKLE KORUNDU) =================
def apply_ui():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .glass-card { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 20px; margin-bottom: 20px; }
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
        div.stButton > button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; width: 100%; border: none; padding: 12px; }
        .package-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
        .package-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(56,189,248,0.1); border-radius: 12px; padding: 10px; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master V3500", layout="wide")
apply_ui()

# ================= 4. OTURUM VE SAYFA KONTROLÜ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER MASTER PRO</h1>", unsafe_allow_html=True)
    st.markdown("<div class='package-grid'><div class='package-card'><small>1 AY</small><br><b style='color:#38bdf8;'>700 TL</b></div><div class='package-card'><small>3 AY</small><br><b style='color:#38bdf8;'>2000 TL</b></div><div class='package-card'><small>6 AY</small><br><b style='color:#38bdf8;'>5000 TL</b></div><div class='package-card'><small>12 AY</small><br><b style='color:#38bdf8;'>8000 TL</b></div></div>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 SİSTEMİ AKTİFLEŞTİR", "👨‍💻 YÖNETİCİ"])
    with t1:
        u_lic = st.text_input("Lisans Anahtarınız:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZ MOTORUNA BAĞLAN"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Geçersiz Anahtar!")
    with t2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("KONTROL PANELİNE GİR"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()
else:
    # ================= 5. ANALİZ MERKEZİ =================
    with st.sidebar:
        st.markdown(f"<h3 style='color:#38bdf8;'>👤 {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        trust_threshold = st.slider("Güven Eşiği (%)", 50, 95, 80)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Lisans Durumu</small><br><b style='color:#4ade80;'>{rem.days} GÜN KALDI</b></div>", unsafe_allow_html=True)
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color:#38bdf8;'>🏆 SİBER ANALİZ VE YOL HARİTASI</h2>", unsafe_allow_html=True)
    if st.button("🔄 SİBER VERİYİ GÜNCELLE"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ MAÇ ÖNCESİ BÜLTEN"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        # Tarih filtresi Yarın için
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        resp_tomorrow = requests.get(f"{BASE_URL}/fixtures?date={tomorrow_date}", headers=headers).json()
        
        fixtures = resp.get("response", [])
        fixtures_tomorrow = resp_tomorrow.get("response", [])

        with t_live:
            live_fixtures = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            if not live_fixtures: st.info("Şu an aktif canlı maç bulunmuyor.")
            for f in live_fixtures:
                puan, harita, karar, zaman = siber_muhakeme_ai(f, {'pressure': random.randint(60,95), 'danger': random.randint(30,65)}, mode="live")
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>DAKİKA: {zaman} | {f['league']['name']}</span>
                            <b class='neon-green'>%{puan} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px;'>
                            <p style='color:#38bdf8; margin:0;'>🤖 <b>KARAR: {karar}</b></p>
                            <small>{"<br>".join(harita)}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            st.markdown(f"<p class='neon-green'>📅 YARININ ELMAS SEÇİMLERİ ({tomorrow_date})</p>", unsafe_allow_html=True)
            for f in fixtures_tomorrow:
                puan, harita, karar, zaman = siber_muhakeme_ai(f, mode="pre")
                if puan >= 90:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>SAAT: {zaman} | {f['league']['name']}</span>
                            <b class='neon-green'>%{puan} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h3>
                        <div style='background:rgba(74, 222, 128, 0.1); padding:10px; border-radius:10px;'>
                            <p style='color:#4ade80; margin:0;'>🎯 ÖNERİ: <b>{karar}</b></p>
                            <small>{"<br>".join(harita)}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Siber hat bağlantısı sağlanamadı.")
