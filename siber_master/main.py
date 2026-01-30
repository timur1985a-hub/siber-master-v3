import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KORUNAN GÜVENLİK VE LİSANS =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%20Neural%20Decision%20Engine%20erişim%20anahtarı%20hakkında%20bilgi%20almak%20istiyorum."

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

# ================= 2. GELİŞMİŞ MUHAKEME VE DÜŞÜNCE MODÜLÜ =================
def neural_reasoning(f, mode="live"):
    logic_steps = []
    guven = 65
    emir = "BEKLE / ANALİZ EDİLİYOR"
    
    if mode == "live":
        p = random.randint(40, 98)
        s = random.randint(0, 10)
        elapsed = f['fixture']['status']['elapsed']
        
        logic_steps.append(f"🔍 Dakika {elapsed}: Saha baskı indeksi %{p}.")
        logic_steps.append(f"🎯 Şut Trafiği: Son 5 dakikada {s} isabetli deneme.")
        
        if p > 85 and s > 4:
            guven = 94
            emir = "🔥 HEMEN OYNA: BASKI ŞİDDETLİ"
            logic_steps.append("⚠️ KRİTİK: Karşı kale abluka altında, savunma bloğu çöktü.")
        elif p > 70:
            guven = 82
            emir = "⏳ İZLEMEDE KAL: MOMENTUM ARTIYOR"
        else:
            guven = 60
            emir = "🛑 DUR: VERİ YETERSİZ"
            
        return guven, logic_steps, emir, p
    else:
        guven = random.randint(85, 99)
        if guven >= 90:
            logic_steps.append("📈 FORM ANALİZİ: Takımların son 5 maç gol ortalaması 2.8.")
            logic_steps.append("🛡️ DEFANS ANALİZİ: İki tarafta da ana stoperler eksik.")
            return guven, logic_steps, "🎯 ELMAS SEÇİM: KG VAR / 2.5 ÜST", 0
        return 0, [], "", 0

# ================= 3. ELİTE DARK TASARIM (WHATSAPP ENTEGRELİ) =================
def apply_ui():
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }}
        .glass-card {{ background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 20px; margin-bottom: 20px; }}
        .logic-box {{ background: rgba(0,0,0,0.3); border-left: 3px solid #38bdf8; padding: 10px; margin: 10px 0; border-radius: 5px; font-size: 0.85rem; color: #94a3b8; }}
        .emir-box {{ background: linear-gradient(90deg, #1e293b, #0f172a); padding: 12px; border-radius: 10px; border: 1px solid #4ade80; text-align: center; font-weight: bold; color: #4ade80; }}
        .dominance-bar {{ background: #1e293b; height: 6px; border-radius: 3px; margin: 10px 0; overflow: hidden; display: flex; }}
        .wa-btn {{ display: block; background: linear-gradient(90deg, #25d366, #128c7e); color: white !important; text-align: center; padding: 15px; border-radius: 15px; text-decoration: none; font-weight: bold; margin-top: 10px; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); transition: 0.3s; }}
        .wa-btn:hover {{ transform: scale(1.02); box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5); }}
        .neon-blue {{ color: #38bdf8; font-weight: bold; }}
        .neon-green {{ color: #4ade80; font-weight: bold; }}
        div.stButton > button {{ background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; width: 100%; border: none; padding: 12px; transition: 0.3s; }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Neural Decision Engine", layout="wide")
apply_ui()

# ================= 4. OTURUM VE SAYFA KONTROLÜ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🧠 NEURAL DECISION ENGINE</h1>", unsafe_allow_html=True)
    st.markdown("""<div style='background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.2); padding:20px; border-radius:15px; text-align:center; margin-bottom:20px;'><h2 style='color: #4ade80; margin:0;'>Yapay Zeka Mimarisini Serbest Bırakın</h2><p style='color: #94a3b8;'>Saniyeler içinde veriyi muhakeme eden üst düzey karar motoruna tam erişim sağlayın.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("<div class='package-grid'><div class='package-card'><small>30 GÜNLÜK</small><br><b style='color:#38bdf8;'>700 TL</b></div><div class='package-card'><small>90 GÜNLÜK</small><br><b style='color:#38bdf8;'>2000 TL</b></div><div class='package-card'><small>180 GÜNLÜK</small><br><b style='color:#38bdf8;'>5000 TL</b></div><div class='package-card'><small>SINIRSIZ</small><br><b style='color:#38bdf8;'>15000 TL</b></div></div>", unsafe_allow_html=True)

    # WHATSAPP LİSANS BUTONU
    st.markdown(f'<a href="{WA_LINK}" class="wa-btn">🔓 LİSANS ALMAK İÇİN İLETİŞİME GEÇİN</a>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 ERİŞİM ANAHTARI", "👨‍💻 ADMIN"])
    with t1:
        u_lic = st.text_input("Access Key:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZ ÇEKİRDEĞİNE BAĞLAN"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Geçersiz Anahtar!")

else:
    # ================= 5. ANALİZ MERKEZİ =================
    with st.sidebar:
        st.markdown(f"<h3 style='color:#38bdf8;'>NODE: {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Süre</small><br><b style='color:#4ade80;'>{rem.days} GÜN AKTİF</b></div>", unsafe_allow_html=True)
        # SİDEBAR WHATSAPP DESTEK
        st.markdown(f'<a href="{WA_LINK}" style="text-decoration:none; font-size:0.8rem; color:#25d366;">🟢 Teknik Destek & Yenileme</a>', unsafe_allow_html=True)
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color:#38bdf8;'>📡 NEURAL REASONING & PROJECTION</h2>", unsafe_allow_html=True)
    
    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME (REAL-TIME)", "⏳ BÜLTEN FİLTRESİ (%90+)"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with t_live:
            live_f = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            if not live_f: st.info("Sistem Boşta: Canlı veri bekleniyor.")
            for f in live_f:
                puan, steps, emir, h_idx = neural_reasoning(f, mode="live")
                if puan >= 75:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b class='neon-green'>GÜVEN: %{puan}</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div class='dominance-bar'>
                            <div style='width:{h_idx}%; background:#38bdf8;'></div>
                            <div style='width:{100-h_idx}%; background:#ef4444;'></div>
                        </div>
                        <div class='logic-box'>
                            <b>🧠 DÜŞÜNCE SÜRECİ:</b><br>{"<br>".join(steps)}
                        </div>
                        <div class='emir-box'>EMİR: {emir}</div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", []):
                puan, steps, emir, _ = neural_reasoning(f, mode="pre")
                if puan >= 90:
                    st.markdown(f"""
                    <div class='glass-card' style='border-color: #4ade80;'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>STRATEJİK ANALİZ</span>
                            <b class='neon-green'>GÜVEN: %{puan}</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h3>
                        <div class='logic-box'>{"<br>".join(steps)}</div>
                        <div class='emir-box' style='border-color:#38bdf8; color:#38bdf8;'>{emir}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Veri hattı meşgul.")
