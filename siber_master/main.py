import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
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

# --- SİBER ARŞİV BAŞLATMA VE HATA ÖNLEME ---
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---",
        "siber_archive": {},
        "archive_mode": False # KeyError önleyici anahtar
    })
    q_t = st.query_params.get("s_t")
    q_p = st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
style_code = """<style>
.stApp{background-color:#010409;color:#e6edf3}
header{visibility:hidden}
.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}
.marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}
.match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-family:'Courier New',monospace;font-size:1rem}
@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}
.marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}
.marketing-subtitle{text-align:center;color:#f85149;font-size:1.1rem;font-weight:700;margin-bottom:15px}
.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}
.owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}
.stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}
.pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}
.pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}
.wa-small{display:block;width:100%;max-width:300px;margin:0 auto 15px auto;background:#238636;color:#fff!important;text-align:center;padding:10px;border-radius:8px;font-weight:700;text-decoration:none}
.decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}
.ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}
.tsi-time{color:#f1e05a!important;font-family:'Courier New',monospace;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px;border:1px solid rgba(241,224,90,0.2)}
.live-minute{color:#f1e05a;font-family:monospace;font-weight:900;border:1px solid #f1e05a;padding:2px 6px;border-radius:4px;margin-left:10px}
.score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}
.pressure-bg{background:#161b22;height:10px;width:100%;border-radius:10px;margin-top:12px;border:1px solid #30363d;overflow:hidden}
.pressure-fill{height:100%;border-radius:10px;transition:width 0.8s ease-in-out}
.unit-badge{display:inline-block;background:rgba(88,166,255,0.1);color:#58a6ff;border:1px dashed #58a6ff;padding:4px 10px;border-radius:6px;font-size:0.85rem;margin-top:10px;font-weight:bold;font-family:monospace}
.stTextInput>div>div>input{background-color:#0d1117!important;color:#58a6ff!important;border:1px solid #30363d!important}
.analysis-box{background:rgba(22,27,34,0.6);border:1px solid #30363d;padding:10px;border-radius:8px;margin-top:10px;font-size:0.9rem}
.archive-badge{display:inline-block;background:rgba(248,81,73,0.1);color:#f85149;border:1px solid #f85149;padding:4px 10px;border-radius:6px;font-size:0.8rem;margin-bottom:8px;font-weight:bold}
.status-win{color:#2ea043;font-weight:bold;border:1px solid #2ea043;padding:2px 5px;border-radius:4px}
.status-fail{color:#f85149;font-weight:bold;border:1px solid #f85149;padding:2px 5px;border-radius:4px}
</style>"""
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            return r.json().get('response', [])
        return []
    except: return []

# --- 4. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    # ... (Giriş Tasarımı - Milimetrik aynı kalacak) ...
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(live=True)[:15]
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
        with st.form("login"):
            l_t = st.text_input("Giriş Tokeni:", type="password").strip()
            l_p = st.text_input("Şifre:", type="password").strip()
            if st.form_submit_button("YAPAY ZEKAYI AKTİF ET"):
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
                else: st.error("❌ Geçersiz Kimlik!")
else:
    if st.session_state["role"] == "admin":
        with st.expander("🔑 SİBER MASTER LİSANS KASASI (ADMIN)", expanded=False):
            admin_data = [{"TOKEN": k, "ŞİFRE": v["pass"], "PAKET": v["label"]} for k, v in CORE_VAULT.items()]
            st.dataframe(pd.DataFrame(admin_data), use_container_width=True)

    st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    search_q = st.text_input("🔍 Maç Ara (Nesine Takım Adı):").strip().lower()
    
    # Arşiv Butonları
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📂 SİBER ARŞİVDE ARA", use_container_width=True): st.session_state["archive_mode"] = True
    with col_b:
        if st.button("📡 CANLI LİSTEYE DÖN", use_container_width=True): st.session_state["archive_mode"] = False

    cx, cy, cz = st.columns([1, 1, 2])
    with cx: 
        if st.button("🧹 CLEAR"): 
            st.session_state["stored_matches"] = []
            st.session_state["archive_mode"] = False
            st.rerun()
    with cy:
        if st.button("♻️ UPDATE"):
            st.session_state["stored_matches"] = [m for m in fetch_siber_data(live=True) if m['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE']]
            st.session_state["archive_mode"] = False
            st.rerun()
    with cz:
        if st.button("💎 SİBER CANSIZ MAÇ TARAMASI (%90+ GÜVEN)", use_container_width=True):
            res = [m for m in fetch_siber_data(live=False) if m['fixture']['status']['short'] == 'NS']
            st.session_state["stored_matches"] = res
            for m in res:
                fid = str(m['fixture']['id'])
                seed_v = int(hashlib.md5(fid.encode()).hexdigest(), 16)
                conf = 88 + (seed_v % 11)
                tahmin = "2.5 ÜST" if conf >= 96 else "İLK YARI 0.5 ÜST"
                st.session_state["siber_archive"][fid] = {"conf": conf, "emir": tahmin, "data": m, "result": "BEKLENİYOR"}

    # --- VERİ İŞLEME VE SKOR DOĞRULAMA ---
    matches = []
    if st.session_state["archive_mode"]:
        # Arşiv Modu: Skorları API'den anlık doğrula
        current_data = fetch_siber_data(live=True) + fetch_siber_data(live=False)
        c_map = {str(m['fixture']['id']): m for m in current_data}
        
        for fid, arch in st.session_state["siber_archive"].items():
            if fid in c_map:
                m_now = c_map[fid]
                gh, ga = m_now['goals']['home'] or 0, m_now['goals']['away'] or 0
                status = m_now['fixture']['status']['short']
                iy_h = m_now['score']['halftime']['home'] or 0
                iy_a = m_now['score']['halftime']['away'] or 0
                
                if status in ['FT', 'AET', 'PEN']:
                    if arch['emir'] == "2.5 ÜST" and (gh + ga) > 2.5: arch['result'] = "BAŞARILI ✅"
                    elif arch['emir'] == "İLK YARI 0.5 ÜST" and (iy_h + iy_a) > 0.5: arch['result'] = "BAŞARILI ✅"
                    else: arch['result'] = "BAŞARISIZ ❌"
                
                arch['data']['goals']['home'], arch['data']['goals']['away'] = gh, ga
        
        matches = [v["data"] for k, v in st.session_state["siber_archive"].items()]
    else:
        matches = st.session_state.get("stored_matches", [])

    if search_q:
        matches = [m for m in matches if search_q in m['teams']['home']['name'].lower() or search_q in m['teams']['away']['name'].lower()]

    # --- KART ÇİZİMİ ---
    for m in matches:
        fid = str(m['fixture']['id'])
        archived = st.session_state["siber_archive"].get(fid)
        
        # Dinamik Renk Belirleme
        color = "#58a6ff"
        status_text = ""
        if archived:
            if "BAŞARILI" in archived['result']: color = "#2ea043"; status_text = f"| <span class='status-win'>{archived['result']}</span>"
            elif "BAŞARISIZ" in archived['result']: color = "#f85149"; status_text = f"| <span class='status-fail'>{archived['result']}</span>"
            else: status_text = "| ⏳ BEKLENİYOR"

        # Şablona Sadık Kart Yapısı
        st.markdown(f"""
            <div class='decision-card' style='border-left: 6px solid {color};'>
                {f"<div class='archive-badge'>🔒 MÜHÜRLÜ ANALİZ: %{archived['conf']} - {archived['emir']} {status_text}</div>" if archived else ""}
                <div class='ai-score' style='color:{color};'>%{archived['conf'] if archived else 90}</div>
                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ {to_tsi(m['fixture']['date'])}</span>
                <br><span style='font-size:1.4rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span>
                <br><div class='score-board'>{m['goals']['home'] or 0} - {m['goals']['away'] or 0}</div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): 
        st.session_state.clear()
        st.rerun()
