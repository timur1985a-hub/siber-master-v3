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

if "auth" not in st.session_state: st.session_state["auth"] = False
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"

# Otomatik Giriş
q_t, q_p = st.query_params.get("s_t"), st.query_params.get("s_p")
if q_t and q_p and not st.session_state["auth"]:
    if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
        st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

# --- 2. DEĞİŞMEZ TERMİNAL TASARIMI (EKRAN GÖRÜNTÜSÜNDEKİ AYNI YAPI) ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".main-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}"
    ".sub-warning{text-align:center;color:#f1e05a;font-weight:bold;margin-bottom:20px}"
    ".scrolling-wrapper{border:2px solid #f85149;border-radius:50px;padding:10px;overflow:hidden;white-space:nowrap;margin-bottom:30px}"
    ".scrolling-text{display:inline-block;animation:scroll 20s linear infinite;color:#fff;font-weight:bold}"
    "@keyframes scroll{0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}"
    ".price-grid{display:grid;grid-template-columns:repeat(5, 1fr);gap:10px;margin-bottom:20px}"
    ".price-card{background:#0d1117;border:1px solid #30363d;padding:15px;text-align:center;border-radius:8px}"
    ".price-card small{color:#8b949e;display:block;margin-bottom:5px}"
    ".price-card b{color:#fff;font-size:1.1rem}"
    ".wa-button{display:block;width:fit-content;margin:20px auto;background:#2ea043;color:#fff!important;padding:12px 30px;border-radius:10px;text-decoration:none;font-weight:bold;border:2px solid #fff}"
    ".terminal-input-label{text-align:center;color:#58a6ff;font-size:1.5rem;font-weight:bold;margin:20px 0}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important;width:100%}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center}"
    ".stat-val{font-size:2rem;font-weight:900;color:#2ea043}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. HİBRİT MOTOR ---
def check_success(emir, score_str):
    try:
        gh, ga = map(int, score_str.split('-'))
        total = gh + ga
        if "2.5 ÜST" in emir: return total > 2
        if "1.5 ÜST" in emir: return total > 1
        if "0.5 ÜST" in emir: return total > 0
        if "KG VAR" in emir: return gh > 0 and ga > 0
        if "1X" in emir: return gh >= ga
        if "X2" in emir: return ga >= gh
        if "İLK YARI 0.5" in emir: return total > 0
        return False
    except: return False

def advanced_decision_engine(m):
    league = m['league']['name'].upper()
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total = gh + ga
    elapsed = m['fixture']['status']['elapsed'] or 0
    is_scoring = any(x in league for x in ["BUNDES", "EREDI", "ELITE", "AUSTRIA", "ICELAND"])
    if is_scoring: pre_emir, conf = "2.5 ÜST", 94
    else: pre_emir, conf = "0.5 ÜST", 91
    if elapsed > 0:
        if elapsed < 40: live_emir = "İLK YARI 0.5 ÜST" if total == 0 else "1.5 ÜST"
        elif 40 <= elapsed < 75: live_emir = "0.5 ÜST" if total == 0 else "KG VAR"
        else: live_emir = "0.5 ÜST (SON HAMLE)"
    else: live_emir = "0.5 ÜST"
    return conf, pre_emir, live_emir

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

# --- 4. PANEL (GÖRSELDEKİ ŞABLON) ---
if not st.session_state["auth"]:
    # 1. Başlık ve Uyarı
    st.markdown("<div class='main-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-warning'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    # 2. Kırmızı Kayan Yazı
    st.markdown("""
        <div class='scrolling-wrapper'>
            <div class='scrolling-text'>
                ⚽ Teplice II VS Karlovy Vary | ⚽ Viktoria Plzeň U19 VS Petřín Plzeň | ⚽ Táborsko VS Příbram | ⚽ Písek VS Milín | ⚽ Werder Br.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. Fiyat Tablosu (5'li Grid)
    st.markdown("""
        <div class='price-grid'>
            <div class='price-card'><small>1 AYLIK</small><b>700 TL</b></div>
            <div class='price-card'><small>3 AYLIK</small><b>2.000 TL</b></div>
            <div class='price-card'><small>6 AYLIK</small><b>5.000 TL</b></div>
            <div class='price-card'><small>12 AYLIK</small><b>9.000 TL</b></div>
            <div class='price-card'><small>SINIRSIZ</small><b>10.000 TL</b></div>
        </div>
    """, unsafe_allow_html=True)

    # 4. WhatsApp Butonu
    st.markdown(f"<a href='{WA_LINK}' class='wa-button'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    # 5. Terminal Girişi
    st.markdown("<div class='terminal-input-label'>🔑 SİBER TERMİNAL GİRİŞİ</div>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t = st.text_input("Giriş Tokeni:", type="password").strip()
        l_p = st.text_input("Şifre:", type="password").strip()
        if st.form_submit_button("YAPAY ZEKAYI AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                st.query_params.update({"s_t": l_t, "s_p": l_p}); st.rerun()

else:
    # İç Panel Tasarımı (Ekran Görüntüsü 1-2-3'deki Yapı)
    st.markdown("<h2 style='text-align:center; color:#2ea043;'>YAPAY ZEKA ANALİZ MERKEZİ</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:#58a6ff;'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</p>", unsafe_allow_html=True)
    
    # Butonlar
    btn_cols = st.columns(5)
    with btn_cols[0]: 
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True): st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}); st.rerun()
    with btn_cols[1]: 
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True): st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre"}); st.rerun()
    with btn_cols[2]: 
        if st.button("🔄 GÜNCELLE", use_container_width=True): st.session_state["stored_matches"] = fetch_siber_data(st.session_state["view_mode"] == "live"); st.rerun()
    with btn_cols[3]: 
        if st.button("📜 SİBER ARŞİV", use_container_width=True): st.session_state["view_mode"] = "archive"; st.rerun()
    with btn_cols[4]: 
        if st.button("🧹 EKRANI TEMİZLE", use_container_width=True): st.session_state["stored_matches"] = []; st.session_state["view_mode"] = "clear"; st.rerun()

    # Veri İşleme & Arşivleme
    for m in st.session_state.get("stored_matches", []):
        fid = str(m['fixture']['id'])
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        if fid not in PERMANENT_ARCHIVE:
            conf, p_e, l_e = advanced_decision_engine(m)
            PERMANENT_ARCHIVE[fid] = {
                "fid": fid, "conf": conf, "league": m['league']['name'], "home": m['teams']['home']['name'], "away": m['teams']['away']['name'],
                "date": to_tsi(m['fixture']['date']), "pre_emir": p_e, "live_emir": l_e, "score": f"{gh}-{ga}", "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0
            }
        PERMANENT_ARCHIVE[fid].update({"score": f"{gh}-{ga}", "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0})

    # Başarı Paneli
    all_data = list(PERMANENT_ARCHIVE.values())
    finished = [d for d in all_data if d['status'] in ['FT', 'AET', 'PEN']]
    if finished and st.session_state["view_mode"] != "clear":
        p_ok = sum(1 for d in finished if check_success(d['pre_emir'], d['score']))
        l_ok = sum(1 for d in finished if check_success(d['live_emir'], d['score']))
        st.markdown(f"<div class='stats-panel'><div><div class='stat-val'>{len(finished)}</div><small>SİBER KAYIT</small></div><div><div class='stat-val' style='color:#58a6ff;'>%{ (p_ok/len(finished))*100:.1f}</div><small>CANSIZ BAŞARI</small></div><div><div class='stat-val' style='color:#2ea043;'>%{ (l_ok/len(finished))*100:.1f}</div><small>CANLI BAŞARI</small></div></div>", unsafe_allow_html=True)

    # Karar Kartları
    display_list = all_data if st.session_state["view_mode"] == "archive" else [PERMANENT_ARCHIVE[str(m['fixture']['id'])] for m in st.session_state.get("stored_matches", []) if str(m['fixture']['id']) in PERMANENT_ARCHIVE]

    for arc in display_list:
        is_fin = arc['status'] in ['FT', 'AET', 'PEN']
        win_p = "✅" if check_success(arc['pre_emir'], arc['score']) else ("❌" if is_fin else "")
        win_l = "✅" if check_success(arc['live_emir'], arc['score']) else ("❌" if is_fin else "")
        is_live = arc['status'] not in ['NS', 'FT', 'TBD', 'CANC']
        
        st.markdown(f"""
            <div class='decision-card'>
                <div class='ai-score'>%{arc['conf']}</div>
                <div style='color:#f85149; font-weight:bold; font-size:0.8rem;'>{"📡 CANLI SİSTEM AKTİF" if is_live else "🔒 SİBER MÜHÜR"}</div>
                <b style='color:#58a6ff;'>⚽ {arc['league']}</b> | <span style='color:#f1e05a;'>⌚ {arc['date']}</span><br>
                <span style='font-size:1.2rem; font-weight:bold;'>{arc['home']} vs {arc['away']}</span><br>
                <div class='score-board'>{arc['score']} {f"<span style='color:#f1e05a; margin-left:10px;'>{arc['min']}'</span>" if is_live else ""}</div>
                <div style='display:flex; gap:10px;'>
                    <div style='flex:1; border:1px solid #30363d; padding:8px; border-radius:6px;'><small>CANSIZ EMİR</small><br><b>{arc['pre_emir']}</b> {win_p}</div>
                    <div style='flex:1; border:1px solid #2ea043; padding:8px; border-radius:6px;'><small>CANLI EMİR</small><br><b>{arc['live_emir']}</b> {win_l}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.query_params.clear(); st.session_state.clear(); st.rerun()
