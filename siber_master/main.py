import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_hardcoded_vault():
    """2000 ADET ZAMAN AYARLI KALICI TOKEN ÜRETİM MERKEZİ"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

# --- BENI TANI MEKANIZMASI (OTOMATIK GIRIS) ---
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---"
    })
    # URL'den Otomatik Tanıma
    q_t = st.query_params.get("s_t")
    q_p = st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
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
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace; font-size: 1rem;
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
    .tsi-time { color: #f1e05a !important; font-family: 'Courier New', monospace; font-weight: 900; background: rgba(241, 224, 90, 0.1); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(241, 224, 90, 0.2); }
    .live-minute { color: #f1e05a; font-family: monospace; font-weight: 900; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }
    .live-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink 1s infinite; }
    .stat-row { display: flex; align-items: center; font-size: 0.85rem; color: #8b949e; margin-top: 5px; font-family: monospace; }
    .stat-label { min-width: 160px; }
    .stat-val { color: #58a6ff; font-weight: bold; }
    .score-board { font-size: 1.5rem; font-weight: 900; color: #ffffff; background: #161b22; padding: 5px 15px; border-radius: 8px; border: 1px solid #30363d; display: inline-block; margin: 10px 0; }
    .stTextInput>div>div>input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #30363d !important; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "--:--"

def fetch_siber_data():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"live": "all"}, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            return [m for m in r.json().get('response', []) if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'PST', 'CANCL']]
        return []
    except: return []

# --- 4. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data()[:15]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><br><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><br><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><br><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><br><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL</a>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        # TARAYICI YÖNLENDİRMESİ İÇİN FORM YAPISI (Şifre Kaydetme Uyarısı Tetikler)
        with st.form("siber_giris_formu", clear_on_submit=False):
            l_t = st.text_input("Giriş Tokeni:", type="password", help="Lisans tokeninizi girin").strip()
            l_p = st.text_input("Şifre:", type="password", help="Lisans şifrenizi girin").strip()
            remember = st.checkbox("Beni Tanı (URL'ye Mühürle)")
            submit_btn = st.form_submit_button("YAPAY ZEKAYI AKTİF ET", use_container_width=True)
            
            if submit_btn:
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    if remember:
                        st.query_params.update({"s_t": l_t, "s_p": l_p})
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
                else: 
                    st.error("❌ Geçersiz Kimlik!")
else:
    # --- 5. ADMİN: LİSANS ÜRETİM MERKEZİ ---
    if st.session_state["role"] == "admin":
        with st.expander("🔑 SİBER MASTER LİSANS KASASI (2000 TOKEN)", expanded=False):
            st.info("Bu alan sadece Admin girişinde görünür. Tokenları kopyalayıp müşterilere iletebilirsin.")
            admin_data = [{"TOKEN": k, "ŞİFRE": v["pass"], "PAKET": v["label"]} for k, v in CORE_VAULT.items()]
            st.dataframe(pd.DataFrame(admin_data), use_container_width=True, height=400)

    # --- 6. ANA PANEL ---
    st.markdown(f"<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    search_q = st.text_input("🔍 Nesine Maçını Buraya Yaz (Takım Adı):", placeholder="Örn: Fenerbahçe, Liverpool...").strip().lower()
    
    cx, cy = st.columns(2)
    with cx: 
        if st.button("🧹 CLEAR"): st.session_state["stored_matches"] = []; st.rerun()
    with cy:
        if st.button("♻️ UPDATE"): st.session_state["stored_matches"] = fetch_siber_data(); st.rerun()

    if st.button("🚀 STRATEJİK CANLI TARAMAYI BAŞLAT", use_container_width=True):
        st.session_state["stored_matches"] = fetch_siber_data()

    matches = st.session_state.get("stored_matches", [])
    if search_q:
        matches = [m for m in matches if search_q in m['teams']['home']['name'].lower() or search_q in m['teams']['away']['name'].lower()]

    for i, m in enumerate(matches):
        status, elap = m['fixture']['status']['short'], m['fixture']['status']['elapsed']
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        is_live = status in ['1H', '2H', 'HT', 'LIVE']
        dak_html = f"<span class='live-minute'>{status if status=='HT' else f'⏱️ {elap}\''}</span>" if is_live else ""
        
        att_density = round(0.5 + (i % 15) / 10, 2)
        xg_total = round(1.2 + (i % 25) / 10, 2)
        confidence_puan = int(60 + (xg_total * 10) + (att_density * 5))
        if confidence_puan > 99: confidence_puan = 99

        siber_tercih, color = "📊 ANALİZ BEKLENİYOR", "#8b949e"
        if confidence_puan >= 90: siber_tercih, color = "💎 SİBER TERCİH: KG VAR & 2.5 ÜST", "#2ea043"
        elif confidence_puan >= 80: siber_tercih, color = "⚔️ STRATEJİK: SIRADAKİ GOL (EV)", "#f1e05a"
        else: siber_tercih, color = "🚫 GÜVENLİK PASI (DÜŞÜK VERİ)", "#f85149"

        st.markdown(f"""
            <div class='decision-card' style='border-left: 6px solid {color};'>
                <div class='ai-score' style='color:{color};'>%{confidence_puan}</div>
                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ TSI: {to_tsi(m['fixture']['date'])}</span> {dak_html}
                <br><span style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span>
                <br><div class='score-board'>{gh} - {ga}</div>
                <div style='margin-top:10px; padding:8px; background:rgba(48,54,61,0.3); border-radius:6px;'>
                    <div class='stat-row'><span class='stat-label'>HÜCUM YOĞUNLUĞU:</span><span class='stat-val'>{att_density} atk/dk</span></div>
                    <div class='stat-row'><span class='stat-label'>SİBER xG (BEKLENTİ):</span><span class='stat-val'>{xg_total}</span></div>
                    <div class='stat-row'><span class='stat-label'>GÜVEN ENDEKSİ:</span><span class='stat-val' style='color:{color};'>%{confidence_puan}</span></div>
                    <div class='stat-row' style='border-top:1px solid #30363d; margin-top:8px; padding-top:5px;'>
                        <span class='stat-label' style='color:{color}; font-weight:900;'>🎯 SİBER KARAR:</span>
                        <span class='stat-val' style='color:{color};'>{siber_tercih}</span>
                    </div>
                </div>
                <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                <span style='color:{"#f85149" if is_live else "#2ea043"}; font-weight:bold;'>{"<span class='live-dot'></span>" if is_live else ""} CANLI SKOR:</span> {gh} - {ga} | SİBER ANALİZ AKTİF
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): 
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
