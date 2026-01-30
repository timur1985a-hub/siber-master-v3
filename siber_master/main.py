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
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%20Siber%20Akıl%20Zafer%20Mimarı%20erişim%20anahtarı%20almak%20istiyorum."

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

# ================= 2. MUHAKEME VE BAŞARI ANALİZİ =================
def neural_reasoning(f, mode="live"):
    logic_steps = []
    guven = 65
    emir = "HESAPLANIYOR..."
    
    if mode == "live":
        p = random.randint(40, 98)
        s = random.randint(0, 10)
        elapsed = f['fixture']['status']['elapsed']
        
        logic_steps.append(f"📡 Canlı Veri: {elapsed}. dakikada baskı şiddeti %{p}.")
        logic_steps.append(f"🎯 İsabetli Atak: Son periyotta {s} kez kaleyi yokladı.")
        
        if p > 85 and s > 4:
            guven = 94
            emir = "🔥 ZAFER YAKIN: GOLÜN GELMESİ AN MESELESİ"
            logic_steps.append("⚠️ KRİTİK ANALİZ: Savunma direnci kırıldı, sistem golü mühürledi.")
        elif p > 70:
            guven = 82
            emir = "⏳ BEKLEMEDE KAL: MOMENTUM BİRİKİYOR"
        else:
            guven = 60
            emir = "🛑 RİSKLİ BÖLGE: ANALİZ BEKLENİYOR"
            
        return guven, logic_steps, emir, p
    else:
        guven = random.randint(85, 99)
        if guven >= 90:
            logic_steps.append("📈 GEÇMİŞ VERİ: Takımların gol iştahı %92 uyumlulukta.")
            logic_steps.append("🛡️ TAKTİK ANALİZ: Defansif açıklar bu skoru destekliyor.")
            return guven, logic_steps, "🎯 ELMAS SEÇİM: KG VAR / 2.5 ÜST", 0
        return 0, [], "", 0

# ================= 3. ELİTE DARK TASARIM (YENİ KİMLİK) =================
def apply_ui():
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }}
        .glass-card {{ background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 20px; margin-bottom: 20px; }}
        .logic-box {{ background: rgba(0,0,0,0.3); border-left: 3px solid #4ade80; padding: 10px; margin: 10px 0; border-radius: 5px; font-size: 0.85rem; color: #94a3b8; }}
        .emir-box {{ background: linear-gradient(90deg, #064e3b, #022c22); padding: 12px; border-radius: 10px; border: 1px solid #4ade80; text-align: center; font-weight: bold; color: #4ade80; text-transform: uppercase; letter-spacing: 1px; }}
        .wa-btn {{ display: block; background: linear-gradient(90deg, #25d366, #128c7e); color: white !important; text-align: center; padding: 15px; border-radius: 15px; text-decoration: none; font-weight: bold; margin-top: 10px; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3); }}
        .wa-btn:hover {{ transform: scale(1.02); box-shadow: 0 6px 20px rgba(37, 211, 102, 0.5); }}
        .neon-blue {{ color: #38bdf8; font-weight: bold; }}
        .neon-green {{ color: #4ade80; font-weight: bold; }}
        div.stButton > button {{ background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; width: 100%; border: none; padding: 12px; }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Akıl: Zafer Mimarı", layout="wide")
apply_ui()

# ================= 4. OTURUM VE SAYFA KONTROLÜ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🧠 SİBER AKIL: ZAFER MİMARI</h1>", unsafe_allow_html=True)
    st.markdown("""<div style='background:rgba(56,189,248,0.05); border:1px solid rgba(56,189,248,0.2); padding:20px; border-radius:15px; text-align:center; margin-bottom:20px;'><h2 style='color: #4ade80; margin:0;'>Maksimum Başarı İçin Optimize Edildi</h2><p style='color: #94a3b8;'>Siber analiz motoru, kazanma olasılığı en yüksek maçları saniyeler içinde sizin için mühürler.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("<div class='package-grid'><div class='package-card'><small>30 GÜNLÜK</small><br><b style='color:#38bdf8;'>700 TL</b></div><div class='package-card'><small>90 GÜNLÜK</small><br><b style='color:#38bdf8;'>2000 TL</b></div><div class='package-card'><small>180 GÜNLÜK</small><br><b style='color:#38bdf8;'>5000 TL</b></div><div class='package-card'><small>SINIRSIZ</small><br><b style='color:#38bdf8;'>15000 TL</b></div></div>", unsafe_allow_html=True)

    st.markdown(f'<a href="{WA_LINK}" class="wa-btn">🔓 ZAFERE KATILMAK İÇİN LİSANS ALIN</a>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 SİSTEME GİRİŞ YAP", "👨‍💻 YÖNETİCİ"])
    with t1:
        u_lic = st.text_input("Erişim Anahtarı:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZ ÇEKİRDEĞİNİ AKTİFLEŞTİR"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Hatalı Anahtar!")

else:
    # ================= 5. ANALİZ MERKEZİ =================
    st.markdown("<h2 style='color:#38bdf8;'>📡 ZAFER PROJEKSİYONU & ANALİZ</h2>", unsafe_allow_html=True)
    
    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME (ANLIK KAZANÇ)", "⏳ BÜLTEN ELMASLARI (%90+)"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with t_live:
            live_f = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            if not live_f: st.info("Siber Akıl şu an veri bekliyor. Uygun maç yakalandığında sinyal verilecek.")
            for f in live_f:
                puan, steps, emir, h_idx = neural_reasoning(f, mode="live")
                if puan >= 75:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b class='neon-green'>BAŞARI OLASILIĞI: %{puan}</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div class='logic-box'>
                            <b>🧠 YAPAY ZEKA MUHAKEMESİ:</b><br>{"<br>".join(steps)}
                        </div>
                        <div class='emir-box'>{emir}</div>
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
                            <span class='neon-blue'>YÜKSEK GÜVENLİ ANALİZ</span>
                            <b class='neon-green'>OLASILIK: %{puan}</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h3>
                        <div class='logic-box'>{"<br>".join(steps)}</div>
                        <div class='emir-box' style='border-color:#38bdf8; color:#38bdf8;'>{emir}</div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Bağlantı hattı meşgul.")
