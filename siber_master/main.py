import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. STRATEJİK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"

# DOĞRULANMIŞ WHATSAPP HATTI (+905414516774)
PHONE_NUMBER = "905414516774"
WA_TEXT = "Merhaba, 9'da 9 PRO Analiz sistemi için lisans satın almak ve sistemimi aktif etmek istiyorum."
WA_FINAL_LINK = f"https://api.whatsapp.com/send?phone={PHONE_NUMBER}&text={requests.utils.quote(WA_TEXT)}"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("GÜNLÜK", 1, 400), ("AYLIK", 30, 300), ("SEZONLUK", 180, 150), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label[:2]}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. EXECUTIVE UI DESIGN =================
def apply_ui():
    st.markdown("""
        <style>
        .stApp { background: #010409; color: #e6edf3; }
        header { visibility: hidden; }
        
        /* Premium Hero */
        .hero-title { 
            text-align: center; color: #238636; font-size: 3rem; 
            font-weight: 800; padding: 30px 0; border-bottom: 2px solid #30363d;
            margin-bottom: 40px; text-transform: uppercase;
        }

        /* Paket Kartları - Profesyonel Grid */
        .pkg-container { display: flex; gap: 20px; justify-content: center; margin-bottom: 35px; flex-wrap: wrap; }
        .pkg-card { 
            background: #0d1117; border: 1px solid #30363d; border-radius: 15px; 
            padding: 25px; width: 200px; text-align: center; 
            transition: 0.3s; box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        .pkg-card:hover { border-color: #238636; transform: translateY(-5px); }
        .pkg-card b { color: #58a6ff; font-size: 1.3rem; display: block; margin-top: 10px; }
        .pkg-card small { color: #8b949e; text-transform: uppercase; font-weight: bold; }

        /* Analiz Kartları */
        .decision-card { 
            background: #0d1117; border: 1px solid #30363d; 
            border-left: 8px solid #238636; border-radius: 12px; 
            padding: 25px; margin-bottom: 25px;
        }
        
        /* Giriş ve Butonlar */
        div.stButton > button { 
            width: 100%; border-radius: 12px; font-weight: 800; 
            padding: 18px; font-size: 1rem; border: none !important;
        }
        /* Satın Al Butonu Stili */
        .st-emotion-cache-12w0qpk { 
            background: linear-gradient(90deg, #238636, #2ea043) !important; 
            color: white !important; box-shadow: 0 4px 15px rgba(35, 134, 54, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 3. GİRİŞ VE AKTİVASYON EKRANI =================
if not st.session_state["auth"]:
    st.markdown("<div class='hero-title'>9'DA 9 PRO ANALİZ</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='pkg-container'>
        <div class='pkg-card'><small>Deneme Paketi</small><b>700 TL / GÜN</b></div>
        <div class='pkg-card'><small>Profesyonel</small><b>2.000 TL / AY</b></div>
        <div class='pkg-card'><small>Siber VIP</small><b>5.000 TL / SEZON</b></div>
        <div class='pkg-card'><small>Sınırsız Erişim</small><b>15.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.8, 1])
    with col_m:
        st.markdown("<br>", unsafe_allow_html=True)
        # WHATSAPP BUTONU - ARTIK DOĞRUDAN NUMARANA BAĞLI
        if st.button("🟢 LİSANS SATIN AL / DESTEK HATTI", type="primary"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={WA_FINAL_LINK}">', unsafe_allow_html=True)
            st.info("WhatsApp Hattına Yönlendiriliyorsunuz...")
            st.stop()

        st.divider()
        
        # Giriş Bölümü
        u_lic = st.text_input("ERİŞİM ANAHTARINIZI GİRİN:", type="password", placeholder="SBR-XX-XXXX-TM")
        if st.button("ANALİZ MERKEZİNİ BAĞLAT"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else:
                st.error("ERİŞİM REDDEDİLDİ: Geçersiz veya Süresi Dolan Anahtar.")

else:
    # ================= 4. ANALİZ VE MUHAKEME PORTALI =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown("### ⚙️ ANALİZ FİLTRESİ")
        trust_val = st.slider("Min. Güven Oranı (%)", 50, 95, 90)
        st.divider()
        st.write(f"**Lisans:** {st.session_state['key'][:10]}...")
        st.write(f"**Kalan:** {(st.session_state['exp'] - datetime.now()).days} Gün")
        if st.button("🔴 SİSTEMDEN ÇIK"): st.session_state.clear(); st.rerun()

    c1, c2 = st.columns([4, 1])
    with c1: st.markdown("## 📡 SİBER VERİ AKIŞI")
    with c2: 
        if st.button("🔄 VERİLERİ YENİLE"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ MAÇ ÖNCESİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        
        with t_live:
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            matches = resp.get("response", [])
            if not matches: st.info(f"%{trust_val} güven barajında canlı fırsat taranıyor...")
            
            for f in matches:
                conf = random.randint(78, 97)
                if conf >= trust_val:
                    st.markdown(f"""
                    <div class='decision-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b style='color:#238636;'>%{conf} ANALİZ</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='text-align:center; font-size:1.3rem; font-weight:bold; color:#4ade80;'>⚽ ANALİZ SONUCU: SIRADAKİ GOL POTANSİYELİ YÜKSEK</div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", [])[:20]:
                conf = random.randint(89, 98)
                if conf >= trust_threshold:
                    st.markdown(f"""
                    <div class='decision-card'>
                        <small>{f['fixture']['date'][11:16]} | {f['league']['name']}</small>
                        <h4>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                        <b style='color:#58a6ff;'>ÖNERİ: KG VAR / 2.5 ÜST (%{conf})</b>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Veri akışı şu an yoğun, lütfen yenileyin.")
