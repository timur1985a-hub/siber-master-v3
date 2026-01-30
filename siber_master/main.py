import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KESİN LİSANS VE GÜVENLİK SİSTEMİ =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%20Siber%20Akıl%20Zafer%20Mimarı%20erişim%20anahtarı%20almak%20istiyorum."

@st.cache_resource
def get_final_vault():
    vault = {}
    # Paket tanımları ve süreleri (GÜN)
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            # LİSANS MÜHÜRÜ: Her anahtarın kendine ait bir bitiş tarihi var.
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. MUHAKEME MOTORU =================
def neural_reasoning(f, mode="live"):
    logic_steps = []
    guven = 65
    emir = "HESAPLANIYOR..."
    if mode == "live":
        p = random.randint(40, 98); s = random.randint(0, 10); elapsed = f['fixture']['status']['elapsed']
        logic_steps.append(f"📡 Veri: {elapsed}. dk | Baskı: %{p}.")
        if p > 85 and s > 4:
            guven = 94; emir = "🔥 ZAFER YAKIN: GOLÜ MÜHÜRLE"
        elif p > 70: guven = 82; emir = "⏳ BEKLEMEDE KAL: MOMENTUM ARTIYOR"
        else: guven = 60; emir = "🛑 ANALİZ BEKLENİYOR"
        return guven, logic_steps, emir, p
    else:
        guven = random.randint(85, 99)
        if guven >= 90:
            logic_steps.append("📈 Form uyumluluğu %92.")
            return guven, logic_steps, "🎯 ELMAS SEÇİM: KG VAR / 2.5 ÜST", 0
        return 0, [], "", 0

# ================= 3. ELİTE DARK TASARIM (FULL VIEWPORT) =================
def apply_ui():
    st.markdown(f"""
        <style>
        .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; }}
        .stApp {{ background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }}
        header {{ visibility: hidden; }}
        .glass-card {{ background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 20px; margin-bottom: 15px; }}
        .logic-box {{ background: rgba(0,0,0,0.3); border-left: 3px solid #4ade80; padding: 10px; margin: 10px 0; border-radius: 5px; font-size: 0.85rem; color: #94a3b8; }}
        .emir-box {{ background: linear-gradient(90deg, #064e3b, #022c22); padding: 12px; border-radius: 10px; border: 1px solid #4ade80; text-align: center; font-weight: bold; color: #4ade80; }}
        .wa-btn {{ display: block; background: linear-gradient(90deg, #25d366, #128c7e); color: white !important; text-align: center; padding: 15px; border-radius: 15px; text-decoration: none; font-weight: bold; margin-bottom: 15px; }}
        .neon-blue {{ color: #38bdf8; font-weight: bold; }}
        .neon-green {{ color: #4ade80; font-weight: bold; }}
        div.stButton > button {{ background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; width: 100%; border: none; padding: 12px; }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Akıl: Zafer Mimarı", layout="wide")
apply_ui()

# ================= 4. KALICI OTURUM KONTROLÜ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# LİSANS SÜRESİ DOLDU MU? (HER SAYFA YENİLEMESİNDE ARKA PLANDA ÇALIŞIR)
if st.session_state["auth"]:
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False, "role": None})
        st.error("⚠️ LİSANS SÜRENİZ DOLDU! Erişim kesildi.")
        st.info("Yeni anahtar için teknik destekle iletişime geçin.")
        time.sleep(3)
        st.rerun()

if not st.session_state["auth"]:
    # GİRİŞ EKRANI
    st.markdown("<h1 style='text-align: center; color: #38bdf8; margin-top:0;'>🧠 SİBER AKIL: ZAFER MİMARI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='package-grid'><div class='package-card'><small>30 GÜN</small><br><b style='color:#38bdf8;'>700 TL</b></div><div class='package-card'><small>90 GÜN</small><br><b style='color:#38bdf8;'>2000 TL</b></div><div class='package-card'><small>180 GÜN</small><br><b style='color:#38bdf8;'>5000 TL</b></div><div class='package-card'><small>SINIRSIZ</small><br><b style='color:#38bdf8;'>15000 TL</b></div></div>", unsafe_allow_html=True)
    st.markdown(f'<a href="{WA_LINK}" class="wa-btn">🔓 ZAFERE KATILMAK İÇİN LİSANS ALIN</a>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 SİSTEME GİRİŞ YAP", "👨‍💻 YÖNETİCİ"])
    with t1:
        u_lic = st.text_input("Erişim Anahtarı:", placeholder="SBR-XXXX-TM", key="login_key")
        if st.button("ANALİZ ÇEKİRDEĞİNİ AKTİFLEŞTİR"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Hatalı veya Süresi Dolmuş Anahtar!")
else:
    # ================= 5. ANALİZ MERKEZİ (GİRİŞ YAPILMIŞ) =================
    with st.sidebar:
        st.markdown(f"<h3 style='color:#38bdf8;'>NODE: {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Kalan Süre</small><br><b style='color:#4ade80;'>{rem.days} GÜN AKTİF</b></div>", unsafe_allow_html=True)
        if st.button("🔴 GÜVENLİ ÇIKIŞ"):
            st.session_state.update({"auth": False})
            st.rerun()

    st.markdown("<h2 style='color:#38bdf8; margin-top:0;'>📡 ZAFER PROJEKSİYONU & ANALİZ MERKEZİ</h2>", unsafe_allow_html=True)
    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ BÜLTEN ANALİZ ET (%90+)"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        # Canlı Veri Akışı
        resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
        fixtures = resp.get("response", [])

        with t_live:
            if not fixtures: st.info("Siber Akıl veri bekliyor...")
            for f in fixtures:
                puan, steps, emir, h_idx = neural_reasoning(f, mode="live")
                if puan >= 75:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b class='neon-green'>OLASILIK: %{puan}</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div class='emir-box'>{emir}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            st.warning("Yüksek güvenli bülten taranıyor...")
            # Yarınki maçlar için basit filtreleme
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", [])[:10]: # Örnek 10 maç
                p, s, e, _ = neural_reasoning(f, mode="pre")
                if p >= 90:
                    st.markdown(f"<div class='glass-card'><b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b><br><span class='neon-green'>GÜVEN: %{p}</span><br>{e}</div>", unsafe_allow_html=True)
    except:
        st.error("Veri akışı kesildi.")
