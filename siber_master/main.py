import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re
import json

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

def persist_auth_js():
    st.markdown("""
        <script>
        const t = localStorage.getItem('sbr_token');
        const p = localStorage.getItem('sbr_pass');
        if (t && p && !window.location.search.includes('auth=true')) {
            const u = new URL(window.location);
            u.searchParams.set('t', t);
            u.searchParams.set('p', p);
            u.searchParams.set('auth', 'true');
            window.location.href = u.href;
        }
        </script>
    """, unsafe_allow_html=True)

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
        for i in range(1, 10001): 
            seed = f"V16_ULTRA_FIXED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d, "issued": False, "exp": None}
    return v

@st.cache_resource
def get_persistent_archive(): return {}

if "CORE_VAULT" not in st.session_state:
    st.session_state["CORE_VAULT"] = get_hardcoded_vault()

PERMANENT_ARCHIVE = get_persistent_archive()

params = st.query_params
if "auth" not in st.session_state:
    if params.get("auth") == "true":
        t_param, p_param = params.get("t"), params.get("p")
        if t_param == ADMIN_TOKEN and p_param == ADMIN_PASS:
            st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
        elif t_param in st.session_state["CORE_VAULT"]:
            ud = st.session_state["CORE_VAULT"][t_param]
            if ud["pass"] == p_param and ud["issued"]:
                st.session_state.update({"auth": True, "role": "user", "current_user": t_param})
    else:
        st.session_state["auth"] = False

if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}"
    ".marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}"
    ".match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-size:1rem}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #58a6ff}"
    ".stat-val{font-size:2.2rem;font-weight:900;color:#2ea043;line-height:1}"
    ".stat-lbl{font-size:0.8rem;color:#8b949e;text-transform:uppercase;font-weight:bold;margin-top:8px;letter-spacing:1px}"
    ".dominance-bar{background:rgba(88,166,255,0.1); border-radius:4px; height:8px; margin:10px 0; overflow:hidden; display:flex}"
    ".dom-home{background:#58a6ff; height:100%}"
    ".dom-away{background:#f85149; height:100%}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. AKILLI SİBER ANALİZ MOTORU ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

def check_success(emir, gh, ga):
    total = gh + ga
    e = str(emir).upper()
    if "EV 0.5" in e: return gh > 0
    if "DEP 0.5" in e: return ga > 0
    if "2.5 ÜST" in e: return total > 2
    if "1.5 ÜST" in e: return total > 1
    if "0.5 ÜST" in e: return total > 0
    if "KG VAR" in e: return gh > 0 and ga > 0
    if "İY 0.5" in e: return total > 0
    return False

def siber_engine(m):
    # Veri Hazırlama
    league = m['league']['name'].upper()
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total = gh + ga
    elapsed = m['fixture']['status']['elapsed'] or 0
    
    # Lig Katsayısı (Gol Potansiyeli)
    high_score_leagues = ["BUNDESLIGA", "EREDIVISIE", "ELITESERIEN", "U21", "ICELAND", "AUSTRIA"]
    is_high = any(l in league for l in high_score_leagues)
    
    # Dinamik Dominans (Baskı Analizi)
    # Gol atan takımın dominansı artar, ama baskı yapanın da etkisi hesaba katılır
    dom_home = 50 + (gh * 5) - (ga * 5)
    if elapsed > 0:
        # Rastgelelik yerine lig ve zamana bağlı stabilizasyon
        dom_home += (5 if is_high else 2) 
    dom_home = max(20, min(80, dom_home))
    dom_away = 100 - dom_home

    # --- AKILLI KARAR MEKANİZMASI ---
    conf = 90
    pre_emir = "1.5 ÜST"
    live_emir = "ANALİZ BEKLENİYOR"
    baski_notu = "DENGELİ ANALİZ"

    # 1. Cansız (Maç Öncesi) Mantığı
    if is_high:
        pre_emir = "2.5 ÜST" if "U21" in league else "KG VAR"
    else:
        pre_emir = "1.5 ÜST" if "TURKEY" not in league else "EV 0.5 ÜST"

    # 2. Canlı Karar Mantığı
    if elapsed > 0:
        if elapsed < 40:
            if total == 0:
                live_emir, conf, baski_notu = "İY 0.5 ÜST", 94, "İLK YARI BASKISI"
            else:
                live_emir, conf, baski_notu = "1.5 ÜST (İY)", 96, "GOL TEMPOSU YÜKSEK"
        elif 45 <= elapsed < 75:
            if total == 0:
                live_emir, conf, baski_notu = "0.5 ÜST", 97, "🔥 KESİN GOL BÖLGESİ"
            elif total == 1:
                live_emir, conf, baski_notu = "1.5 ÜST", 95, "İKİNCİ GOL YAKIN"
            else:
                live_emir, conf, baski_notu = f"{total+0.5} ÜST", 92, "SKOR DEVAM EDER"
        elif elapsed >= 80:
            if total <= 1:
                live_emir, conf, baski_notu = "0.5 ÜST / RİSK", 88, "SON DAKİKA BASKISI"
            else:
                live_emir, conf, baski_notu = "SKOR KORUNUR", 100, "ANALİZ TAMAMLANDI"
    
    # Güven Skorunu Lig Kalitesine Göre Revize Et
    if is_high: conf = min(100, conf + 3)

    return conf, pre_emir, live_emir, dom_home, dom_away, baski_notu

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

# --- 4. PANEL ---
if not st.session_state["auth"]:
    # Giriş sayfası (Dokunulmadı)
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t = st.text_input("Kullanıcı adı").strip()
        l_p = st.text_input("Şifre", type="password").strip()
        if st.form_submit_button("AKTİF ET"):
            if l_t == ADMIN_TOKEN and l_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
                st.rerun()
            elif l_t in st.session_state["CORE_VAULT"]:
                ud = st.session_state["CORE_VAULT"][l_t]
                if ud["pass"] == l_p and ud["issued"]:
                    st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                    st.rerun()
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)

    # BUTONLAR
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: 
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"}); st.rerun()
    with c2:
        if st.button("💎 MAÇ ÖNCESİ", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(False), "view_mode": "pre"}); st.rerun()
    with c3:
        if st.button("🔄 GÜNCELLE", use_container_width=True): st.rerun()
    with c4:
        if st.button("📜 SİBER ARŞİV", use_container_width=True):
            st.session_state["view_mode"] = "archive"; st.rerun()
    with c5:
        if st.button("🧹 EKRANI TEMİZLE", use_container_width=True):
            st.session_state["stored_matches"] = []; st.session_state["view_mode"] = "clear"; st.rerun()

    # İSTATİSTİK PANELİ (EN ÜSTTE)
    archive_list = list(PERMANENT_ARCHIVE.values())
    fin_matches = [d for d in archive_list if d['status'] in ['FT', 'AET', 'PEN']]
    if fin_matches:
        p_ok = sum(1 for d in fin_matches if check_success(d['pre_emir'], int(d['score'].split('-')[0]), int(d['score'].split('-')[1])))
        l_ok = sum(1 for d in fin_matches if check_success(d['live_emir'], int(d['score'].split('-')[0]), int(d['score'].split('-')[1])))
        st.markdown(f"""
        <div class='stats-panel'>
            <div><div class='stat-val'>{len(archive_list)}</div><div class='stat-lbl'>SİBER KAYIT</div></div>
            <div><div class='stat-val' style='color:#58a6ff;'>%{(p_ok/len(fin_matches))*100:.1f}</div><div class='stat-lbl'>CANSIZ BAŞARI</div></div>
            <div><div class='stat-val' style='color:#2ea043;'>%{(l_ok/len(fin_matches))*100:.1f}</div><div class='stat-lbl'>CANLI BAŞARI</div></div>
        </div>
        """, unsafe_allow_html=True)

    # Veri İşleme
    if st.session_state["view_mode"] in ["live", "pre"] and st.session_state["stored_matches"]:
        for m in st.session_state["stored_matches"]:
            fid = str(m['fixture']['id'])
            gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
            conf, p_e, l_e, d_h, d_a, b_n = siber_engine(m)
            if fid not in PERMANENT_ARCHIVE:
                PERMANENT_ARCHIVE[fid] = {"fid": fid, "conf": conf, "league": m['league']['name'], "home": m['teams']['home']['name'], "away": m['teams']['away']['name'], "date": to_tsi(m['fixture']['date']), "pre_emir": p_e, "live_emir": l_e, "score": f"{gh}-{ga}", "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0, "dom_h": d_h, "dom_a": d_a, "b_not": b_n}
            else:
                PERMANENT_ARCHIVE[fid].update({"score": f"{gh}-{ga}", "status": m['fixture']['status']['short'], "min": m['fixture']['status']['elapsed'] or 0, "live_emir": l_e, "conf": conf, "dom_h": d_h, "dom_a": d_a, "b_not": b_n})

    search_q = st.text_input("🔍 Siber Arama:", placeholder="Takım/Lig...").strip().lower()
    mode = st.session_state["view_mode"]
    display_list = archive_list if mode == "archive" else [PERMANENT_ARCHIVE[str(m['fixture']['id'])] for m in st.session_state["stored_matches"] if str(m['fixture']['id']) in PERMANENT_ARCHIVE]

    if search_q:
        display_list = [d for d in display_list if search_q in d['home'].lower() or search_q in d['away'].lower()]

    for arc in display_list:
        gh_v, ga_v = map(int, arc['score'].split('-'))
        is_fin = arc['status'] in ['FT', 'AET', 'PEN']
        p_win = check_success(arc['pre_emir'], gh_v, ga_v)
        l_win = check_success(arc['live_emir'], gh_v, ga_v)
        win_pre = "✅" if p_win else ("❌" if is_fin else "")
        win_live = "✅" if l_win else ("❌" if is_fin else "")
        
        st.markdown(f"""
        <div class='decision-card'>
            <div class='ai-score'>%{arc['conf']}</div>
            <div class='live-pulse'>📡 SİSTEM AKTİF</div> <b style='color:#58a6ff; margin-left:10px;'>{arc['b_not']}</b><br>
            <b style='color:#58a6ff;'>⚽ {arc['league']}</b> | <span style='color:#f1e05a;'>⌚ {arc['date']}</span><br>
            <span style='font-size:1.2rem; font-weight:bold;'>{arc['home']} vs {arc['away']}</span><br>
            <div class='score-board'>{arc['score']} <span style='color:#f1e05a; font-size:1rem; margin-left:10px;'>{arc['min']}'</span></div>
            <div class='dominance-bar'><div class='dom-home' style='width:{arc['dom_h']}%'></div><div class='dom-away' style='width:{arc['dom_a']}%'></div></div>
            <div style='display:flex; gap:10px; margin-top:10px;'>
                <div style='flex:1; padding:8px; border:1px solid #58a6ff; border-radius:6px; background:rgba(88,166,255,0.05)'>
                    <small>CANSIZ EMİR</small><br><b>{arc['pre_emir']}</b> {win_pre}
                </div>
                <div style='flex:1; padding:8px; border:1px solid #2ea043; border-radius:6px; background:rgba(46,160,67,0.05)'>
                    <small>CANLI EMİR</small><br><b>{arc['live_emir']}</b> {win_live}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
