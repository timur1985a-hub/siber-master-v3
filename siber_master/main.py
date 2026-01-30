import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE ÇEKİRDEK KİMLİK (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"

# ADMİN (SENİN) BİLGİLERİN - ZAMANSIZ VE SINIRSIZ
MASTER_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
MASTER_PASS = "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# ZAMAN AYARLI KULLANICI VERİTABANI
if "user_db" not in st.session_state:
    st.session_state["user_db"] = {}

# --- 2. ASIL ŞABLON: DEĞİŞMEZ TASARIM VE NEON CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        box-shadow: 0px 0px 15px rgba(248, 81, 73, 0.2); padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace;
        box-shadow: inset 0px 0px 5px rgba(248, 81, 73, 0.3); font-size: 1rem;
    }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043; }
    .wa-small { display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto; background: #238636; color: white !important; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

def fetch_data():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        return r.json().get('response', [])
    except: return []

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None})

# --- 4. GİRİŞ ÖNCESİ (EVRENSEL PANEL) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    m_data = fetch_data()[:15]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} <span>VS</span> {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div><div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div><div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div><div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div><div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🔑 SİBER GİRİŞ</h3>", unsafe_allow_html=True)
        in_token = st.text_input("Giriş Tokeni:", type="password", key="main_token").strip()
        in_pass = st.text_input("Şifre:", type="password", key="main_pass").strip()
        
        if st.button("SİSTEME BAĞLAN", use_container_width=True):
            # 1. ADMİN KONTROLÜ
            if in_token == MASTER_TOKEN and in_pass == MASTER_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()
            
            # 2. KULLANICI KONTROLÜ
            elif in_token in st.session_state["user_db"]:
                udata = st.session_state["user_db"][in_token]
                if udata["pass"] == in_pass:
                    # ZAMAN KONTROLÜ
                    now = datetime.now()
                    if now > udata["expire"]:
                        st.error(f"❌ LİSANS SÜRENİZ DOLMUŞTUR! (Bitiş: {udata['expire'].strftime('%Y-%m-%d')})")
                        st.markdown(f"<a href='{WA_LINK}' style='color:#f85149; text-decoration:none; font-weight:bold;'>👉 YENİLEMEK İÇİN TIKLAYIN</a>", unsafe_allow_html=True)
                    else:
                        st.session_state.update({"auth": True, "role": "user", "expire_info": udata["expire"]})
                        st.rerun()
                else:
                    st.error("❌ Şifre Hatalı!")
            else:
                st.error("❌ Geçersiz Token!")

else:
    # --- 5. GİRİŞ SONRASI ---
    if st.session_state["role"] == "admin":
        st.markdown("<div class='internal-welcome'>ADMİN MASTER PANEL</div>", unsafe_allow_html=True)
        with st.expander("🎫 ZAMAN AYARLI KULLANICI ÜRET", expanded=True):
            new_utoken = st.text_input("Kullanıcı Tokeni (Örn: SBR-USR-101):")
            new_upass = st.text_input("Kullanıcı Şifresi:")
            p_type = st.selectbox("Paket Süresi", ["1 GÜN (TEST)", "1 AY", "3 AY", "6 AY", "12 AY", "SINIRSIZ"])
            
            days_map = {"1 GÜN (TEST)": 1, "1 AY": 30, "3 AY": 90, "6 AY": 180, "12 AY": 365, "SINIRSIZ": 36500}
            
            if st.button("⚡ SİSTEME MÜHÜRLE VE BAŞLAT"):
                if new_utoken and new_upass:
                    expire_date = datetime.now() + timedelta(days=days_map[p_type])
                    st.session_state["user_db"][new_utoken] = {
                        "pass": new_upass, 
                        "expire": expire_date,
                        "pkg": p_type
                    }
                    st.success(f"Kullanıcı aktif! Bitiş Tarihi: {expire_date.strftime('%Y-%m-%d')}")
                else:
                    st.warning("Eksik bilgi girmeyin.")
        
        st.write("### 👥 Aktif Lisans Listesi")
        if st.session_state["user_db"]:
            df = pd.DataFrame.from_dict(st.session_state["user_db"], orient='index')
            st.dataframe(df)

    else:
        st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
        st.info(f"🛡️ Lisansınız şu tarihe kadar geçerlidir: {st.session_state['expire_info'].strftime('%Y-%m-%d')}")
        # Analiz kodları buraya...

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()
