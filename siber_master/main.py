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
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

@st.cache_resource
def get_persistent_archive(): return {}

CORE_VAULT = get_hardcoded_vault()
PERMANENT_ARCHIVE = get_persistent_archive()

# --- HAFIZA MEKANİZMASI (RECALL SYSTEM) ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []

# URL'den kullanıcıyı tanıma (Sayfa yenilense de çıkış yapmaz)
q_t = st.query_params.get("s_t")
q_p = st.query_params.get("s_p")

if not st.session_state["auth"] and q_t and q_p:
    if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
        st.session_state.update({
            "auth": True, 
            "role": "admin" if q_t == ADMIN_TOKEN else "user", 
            "current_user": q_t
        })

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}"
    ".marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}"
    ".match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-family:'Courier New',monospace;font-size:1rem}"
    "@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}"
    ".marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}"
    ".marketing-subtitle{text-align:center;color:#f85149;font-size:1.1rem;font-weight:700;margin-bottom:15px}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}"
    ".pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}"
    ".pkg-price{color:#f1e05a;font-weight:800;font-size:0.9rem;margin-top:5px}"
    ".wa-small{display:block;width:100%;max-width:300px;margin:10px auto 20px auto;background:#238636;color:#fff!important;text-align:center;padding:12px;border-radius:8px;font-weight:700;text-decoration:none;border:1px solid #2ea043}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".tsi-time{color:#f1e05a!important;font-family:'Courier New',monospace;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px;border:1px solid rgba(241,224,90,0.2)}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".archive-badge{display:inline-block;background:rgba(248,81,73,0.1);color:#f85149;border:1px solid #f85149;padding:2px 8px;border-radius:4px;font-size:0.75rem;margin-bottom:5px;font-weight:bold}"
    ".status-win{color:#2ea043;font-weight:bold;border:1px solid #2ea043;padding:2px 5px;border-radius:4px;margin-left:10px}"
    ".status-lost{color:#f85149;font-weight:bold;border:1px solid #f85149;padding:2px 5px;border-radius:4px;margin-left:10px}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite;margin-bottom:5px}"
    ".live-min-badge{background:rgba(241,224,90,0.1);color:#f1e05a;border:1px solid #f1e05a;padding:2px 8px;border-radius:4px;font-weight:bold;margin-left:10px;font-family:monospace}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:15px;border-radius:12px;margin-bottom:20px;display:flex;justify-content:space-around;text-align:center;border-top:3px solid #58a6ff;box-shadow: 0 0 10px rgba(88,166,255,0.1)}"
    ".stat-val{font-size:1.8rem;font-weight:900;color:#2ea043}"
    ".stat-lbl{font-size:0.7rem;color:#8b949e;text-transform:uppercase;font-weight:bold;letter-spacing:1px}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. ANALİZ MOTORU ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def check_success(emir, gh, ga):
    total = gh + ga
    if "2.5 ÜST" in emir: return total > 2
    if "1.5 ÜST" in emir: return total > 1
    if "0.5 ÜST" in emir: return total > 0
    if "KG VAR" in emir: return gh > 0 and ga > 0
    return False

def advanced_decision_engine(m):
    league = m['league']['name'].upper()
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total = gh + ga
    elapsed = m['fixture']['status']['elapsed'] or 0
    
    high_leagues = ["BUNDESLIGA", "EREDIVISIE", "ELITESERIEN", "AUSTRIA", "BELGIUM"]
    is_high = any(x in league for x in high_leagues)
    
    pre_emir = "2.5 ÜST" if is_high else "0.5 ÜST"
    conf = 94 if is_high else 89
    
    if elapsed > 0:
        if elapsed < 35 and total == 0: live_emir = "İLK YARI 0.5 ÜST"
        elif elapsed > 60 and total < 2: live_emir = "MAÇ SONU 1.5 ÜST"
        else: live_emir = "KG VAR"
    else: live_emir = "0.5 ÜST"
    
    return conf, pre_emir, live_emir

# --- 4. PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>Kesintisiz Siber Analiz Erişimi</div>", unsafe_allow_html=True)
    
    with st.form("auth_f"):
        l_t = st.text_input("Giriş Tokeni:", type="password").strip()
        l_p = st.text_input("Şifre:", type="password").strip()
        if st.form_submit_button("AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                # Giriş bilgilerini URL'ye mühürle (Yenilemede çıkış yapmaz)
                st.query_params["s_t"] = l_t
                st.query_params["s_p"] = l_p
                st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}); st.rerun()
    with c2:
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre"}); st.rerun()
    with c3:
        if st.button("🔄 GÜNCELLE", use_container_width=True):
            st.session_state["stored_matches"] = fetch_siber_data(st.session_state["view_mode"] == "live"); st.rerun()
    with c4:
        if st.button("📜 SİBER ARŞİV", use_container_width=True):
            st.session_state["view_mode"] = "archive"; st.rerun()
    with c5:
        if st.button("🧹 EKRANI TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.session_state["view_mode"] = "clear"; st.rerun()

    mode = st.session_state["view_mode"]
    
    # Veri Kayıt İşlemi
    for m in st.session_state.get("stored_matches", []):
        fid = str(m['fixture']['id'])
        if fid not in PERMANENT_ARCHIVE:
            conf, p_e, l_e = advanced_decision_engine(m)
            PERMANENT_ARCHIVE[fid] = {
                "fid": fid, "conf": conf, "league": m['league']['name'], "home": m['teams']['home']['name'], 
                "away": m['teams']['away']['name'], "date": to_tsi(m['fixture']['date']), 
                "pre_emir": p_e, "live_emir": l_e, "score": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", 
                "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0
            }
        PERMANENT_ARCHIVE[fid].update({"score": f"{m['goals']['home'] or 0}-{m['goals']['away'] or 0}", "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0})

    display_list = list(PERMANENT_ARCHIVE.values()) if mode == "archive" else [PERMANENT_ARCHIVE[str(m['fixture']['id'])] for m in st.session_state.get("stored_matches", []) if str(m['fixture']['id']) in PERMANENT_ARCHIVE]

    # --- ARŞİV BAŞARI PANELİ (DOKUNULMAZ) ---
    if mode == "archive" and display_list:
        fin = [d for d in display_list if d['status'] in ['FT', 'AET', 'PEN']]
        if fin:
            p_ok = sum(1 for d in fin if check_success(d['pre_emir'], int(d['score'].split('-')[0]), int(d['score'].split('-')[1])))
            l_ok = sum(1 for d in fin if check_success(d['live_emir'], int(d['score'].split('-')[0]), int(d['score'].split('-')[1])))
            st.markdown(f"""<div class='stats-panel'><div><div class='stat-val'>{len(fin)}</div><div class='stat-lbl'>Siber Kayıt</div></div><div><div class='stat-val' style='color:#58a6ff;'>%{ (p_ok/len(fin))*100:.1f}</div><div class='stat-lbl'>Cansız Başarı</div></div><div><div class='stat-val' style='color:#2ea043;'>%{ (l_ok/len(fin))*100:.1f}</div><div class='stat-lbl'>Canlı Başarı</div></div></div>""", unsafe_allow_html=True)

    # Maç Kartları
    for arc in display_list:
        gh_v, ga_v = map(int, arc['score'].split('-'))
        is_fin = arc['status'] in ['FT', 'AET', 'PEN']
        win_p = f"<span class='status-win'>✅</span>" if check_success(arc['pre_emir'], gh_v, ga_v) else (f"<span class='status-lost'>❌</span>" if is_fin else "")
        win_l = f"<span class='status-win'>✅</span>" if check_success(arc['live_emir'], gh_v, ga_v) else (f"<span class='status-lost'>❌</span>" if is_fin else "")
        st.markdown(f"""<div class='decision-card'><div class='ai-score'>%{arc['conf']}</div><b style='color:#58a6ff;'>⚽ {arc['league']}</b><br><span>{arc['home']} vs {arc['away']}</span><br><div class='score-board'>{arc['score']}</div><div style='display:flex; gap:10px;'><div style='flex:1;'><b>{arc['pre_emir']}</b> {win_p}</div><div style='flex:1;'><b>{arc['live_emir']}</b> {win_l}</div></div></div>""", unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.query_params.clear(); st.session_state.clear(); st.rerun()
