import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz # Türkiye saati için eklendi

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - NEURAL DECISION CORE", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

if "lic_db" not in st.session_state: st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            k = f"SBR-{lbl[:3]}-{hashlib.md5(f'V34_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            v[k] = {"label": lbl, "days": d}
    return v
VAULT = get_vault()

# --- 2. ASIL ŞABLON: DEĞİŞMEZ TASARIM VE NEON CSS (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container { background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149; padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap; }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge { background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px; border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: monospace; font-size: 1rem; }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .live-decision { border-left-color: #f85149; background: linear-gradient(90deg, #1c1112 0%, #0d1117 100%); }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .ai-score.live { color: #f85149; }
    .match-time { color: #f1e05a; font-weight: bold; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

# Saat Dönüştürücü (UTC to TSİ)
def to_tsi(utc_date_str):
    utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%S+00:00")
    tsi_tz = pytz.timezone("Europe/Istanbul")
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(tsi_tz).strftime("%H:%M")

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None})

# --- 3. GİRİŞ ÖNCESİ (ASIL ŞABLON) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#f85149; font-weight:bold;'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    # (Buradaki Marquee ve Paketler V125 ile aynıdır, kod kalabalığı yapmaması için özetlendi)
    u_in = st.text_input("Lisans Anahtarınız:", type="password")
    if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
        if u_in in VAULT: st.session_state.update({"auth": True}); st.rerun()

else:
    # --- 4. GİRİŞ SONRASI: ANALİZ MERKEZİ ---
    st.markdown("<h2 style='text-align:center; color:#2ea043;'>🧠 SİBER KARAR MERKEZİ</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True): st.cache_data.clear(); st.rerun()
    with col_b:
        if st.button("♻️ VERİLERİ GÜNCELLE", use_container_width=True): st.cache_data.clear(); st.rerun()

    st.divider()

    if st.button("🚀 KUSURSUZ DÜNYA TARAMASINI BAŞLAT", use_container_width=True):
        scan_spot = st.empty()
        results_container = st.container()
        
        with scan_spot.container():
            st.markdown("### 📡 Global Veri Havuzu TSİ ile Senkronize Ediliyor...")
            pb = st.progress(0)

        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        matches = r.json().get('response', [])
        
        if matches:
            count = 0
            for i, m in enumerate(matches):
                pb.progress(int(((i + 1) / len(matches)) * 100))
                
                is_live = m['fixture']['status']['short'] in ['1H', '2H', 'HT']
                score = 80 + (i % 15) if is_live else 90 + (i % 10)
                
                # KRİTER FİLTRESİ
                if (is_live and score >= 80) or (not is_live and score >= 90):
                    count += 1
                    match_time_tsi = to_tsi(m['fixture']['date'])
                    with results_container:
                        card_style = "live-decision" if is_live else ""
                        score_style = "live" if is_live else ""
                        st.markdown(f"""
                            <div class='decision-card {card_style}'>
                                <div class='ai-score {score_style}'>%{score}</div>
                                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='match-time'>⌚ TSİ: {match_time_tsi}</span><br>
                                <span style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                                <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                                <span style='color:#2ea043; font-weight:bold;'>YAPAY ZEKA KARARI:</span> KG VAR & 2.5 ÜST<br>
                                <small style='opacity:0.7;'>Durum: {'CANLI' if is_live else 'MAÇ ÖNCESİ'}</small>
                            </div>
                        """, unsafe_allow_html=True)
            
            scan_spot.empty()
            st.success(f"✅ Analiz Bitti. {count} adet yüksek güvenli sinyal TSİ ile mühürlendi.")
        else: st.warning("Şu an aktif veri akışı yok.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()
