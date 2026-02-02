import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_hardcoded_vault():
    """50.000 LİSANSLIK DEV SİBER HAVUZ - SADECE BİR KEZ ÜRETİLİR"""
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

if "auth" not in st.session_state: st.session_state["auth"] = False
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
    ".status-win{color:#2ea043;font-weight:bold;border:1px solid #2ea043;padding:2px 5px;border-radius:4px;margin-left:5px}"
    ".status-lost{color:#f85149;font-weight:bold;border:1px solid #f85149;padding:2px 5px;border-radius:4px;margin-left:5px}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite;margin-bottom:5px}"
    ".live-min-badge{background:rgba(241,224,90,0.1);color:#f1e05a;border:1px solid #f1e05a;padding:2px 8px;border-radius:4px;font-weight:bold;margin-left:10px;font-family:monospace}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #58a6ff;box-shadow:0 10px 20px rgba(0,0,0,0.4)}"
    ".stat-val{font-size:2.2rem;font-weight:900;color:#2ea043;line-height:1}"
    ".stat-lbl{font-size:0.8rem;color:#8b949e;text-transform:uppercase;font-weight:bold;margin-top:8px;letter-spacing:1px}"
    ".archive-badge{display:inline-block;background:rgba(248,81,73,0.1);color:#f85149;border:1px solid #f85149;padding:2px 8px;border-radius:4px;font-size:0.75rem;margin-bottom:5px;font-weight:bold}"
    "@keyframes pulse-red{0%{box-shadow:0 0 0 0 rgba(248,81,73,0.7)}70%{box-shadow:0 0 0 10px rgba(248,81,73,0)}100%{box-shadow:0 0 0 0 rgba(248,81,73,0)}}"
    ".lic-item{background:#161b22; padding:10px; border-radius:6px; margin-bottom:5px; border-left:3px solid #f1e05a; font-family:monospace; font-size:0.85rem;}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. SİBER ANALİZ MOTORU (ORİJİNAL - DOKUNULMAZ) ---
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

def siber_engine(m):
    league = m['league']['name'].upper()
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    total = gh + ga
    elapsed = m['fixture']['status']['elapsed'] or 0
    high_leagues = ["EREDIVISIE", "BUNDESLIGA", "LALIGA", "PREMIER LEAGUE", "J1 LEAGUE", "ELITESERIEN", "AUSTRIA", "BELGIUM", "CHAMPIONSHIP"]
    is_high = any(x in league for x in high_leagues)
    pre_emir = "2.5 ÜST" if is_high else "0.5 ÜST"
    conf = 94 if is_high else 89
    if elapsed > 0:
        if elapsed < 35 and total == 0: live_emir = "İLK YARI 0.5 ÜST"
        elif elapsed > 60 and total < 2: live_emir = "MAÇ SONU 1.5 ÜST"
        else: live_emir = "KG VAR"
    else: live_emir = "KG VAR"
    return conf, pre_emir, live_emir

# --- 4. PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>Siber Analiz ve Yapay Zeka Stratejileri</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(True)[:10]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>PAKET</small><br><b>1-AY</b><div class='pkg-price'>700 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>3-AY</b><div class='pkg-price'>2.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>6-AY</b><div class='pkg-price'>5.000 TL</div></div><div class='pkg-box'><small>PAKET</small><br><b>12-AY</b><div class='pkg-price'>9.000 TL</div></div><div class='pkg-box'><small>KAMPANYA</small><br><b>SINIRSIZ</b><div class='pkg-price'>20.000 TL</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>💬 BİZE ULAŞIN (WHATSAPP)</a>", unsafe_allow_html=True)
    
    with st.form("auth_f"):
        l_t = st.text_input("Giriş Tokeni:", type="password").strip()
        l_p = st.text_input("Şifre:", type="password").strip()
        if st.form_submit_button("AKTİF ET"):
            now = datetime.now(pytz.timezone("Europe/Istanbul"))
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS):
                st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"}); st.rerun()
            elif l_t in st.session_state["CORE_VAULT"]:
                ud = st.session_state["CORE_VAULT"][l_t]
                if ud["pass"] == l_p:
                    if ud["issued"] and (ud["exp"] is None or now < ud["exp"]):
                        st.session_state.update({"auth": True, "role": "user", "current_user": l_t}); st.rerun()
                    elif not ud["issued"]: st.error("⚠️ LİSANS AKTİF DEĞİL (DAĞITILMAMIŞ).")
                    else: st.error("❌ LİSANS SÜRESİ DOLMUŞ.")
                else: st.error("❌ ŞİFRE HATALI")
            else: st.error("❌ GEÇERSİZ TOKEN")
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    # --- ADMIN KONTROL PANELİ ---
    if st.session_state.get("role") == "admin":
        with st.expander("🔑 SİBER LİSANS VE HAFIZA YÖNETİMİ"):
            t1, t2, t3, t4, t5 = st.tabs(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            for i, pkg in enumerate(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"]):
                with [t1, t2, t3, t4, t5][i]:
                    subset = {k: v for k, v in st.session_state["CORE_VAULT"].items() if v["label"] == pkg}
                    for tk in list(subset.keys())[:15]:
                        v = subset[tk]
                        col1, col2 = st.columns([3, 1])
                        with col1: st.markdown(f"<div class='lic-item'><b>{tk}</b><br>Pass: {v['pass']} | {'✅ AKTİF' if v['issued'] else '⚪ BEKLEMEDE'}</div>", unsafe_allow_html=True)
                        with col2:
                            if not v["issued"] and st.button("DAĞIT", key=f"d_{tk}"):
                                st.session_state["CORE_VAULT"][tk].update({"issued": True, "exp": datetime.now(pytz.timezone("Europe/Istanbul")) + timedelta(days=v["days"])})
                                st.rerun()
            st.divider()
            if st.button("🔥 TÜM ARŞİVİ SIFIRLA (ROOT)", use_container_width=True):
                PERMANENT_ARCHIVE.clear()
                st.session_state["stored_matches"] = []
                st.success("Tüm siber hafıza temizlendi!")
                st.rerun()

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

    # --- SİBER ARAMA MOTORU (DOKUNULMAZ API YOLLARIYLA ENTEGRE) ---
    search_q = st.text_input("🔍 Siber Arama:", placeholder="Takım/Lig...").strip().lower()
    mode = st.session_state["view_mode"]
    display_list = []

    # Veri Kayıt İşlemi (API YOLLARI BURADA ÇALIŞIR)
    if mode != "clear":
        for m in st.session_state.get("stored_matches", []):
            fid = str(m['fixture']['id'])
            gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
            status = m['fixture']['status']['short']
            elapsed = m['fixture']['status']['elapsed'] or 0
            conf, p_emir, l_emir = siber_engine(m)
            if fid not in PERMANENT_ARCHIVE:
                PERMANENT_ARCHIVE[fid] = {
                    "fid": fid, "conf": conf, "league": m['league']['name'],
                    "home": m['teams']['home']['name'], "away": m['teams']['away']['name'],
                    "date": to_tsi(m['fixture']['date']), "pre_emir": p_emir, "live_emir": l_emir,
                    "score": f"{gh}-{ga}", "status": status, "min": elapsed
                }
            PERMANENT_ARCHIVE[fid].update({"score": f"{gh}-{ga}", "status": status, "min": elapsed})

    # MODA GÖRE LİSTE OLUŞTURMA
    if mode == "archive": 
        display_list = list(PERMANENT_ARCHIVE.values())
    elif mode != "clear":
        display_list = [PERMANENT_ARCHIVE[str(m['fixture']['id'])] for m in st.session_state.get("stored_matches", []) if str(m['fixture']['id']) in PERMANENT_ARCHIVE]

    # FİLTRELEME (ARAMA KUTUSU) - LİSTEYİ BOZMADAN ÇALIŞIR
    if search_q:
        display_list = [d for d in display_list if search_q in d['home'].lower() or search_q in d['away'].lower() or search_q in d['league'].lower()]

    # ARŞİV İSTATİSTİKLERİ
    if mode == "archive" and display_list:
        fin = [d for d in display_list if d['status'] in ['FT', 'AET', 'PEN']]
        if fin:
            p_ok = sum(1 for d in fin if check_success(d['pre_emir'], int(d['score'].split('-')[0]), int(d['score'].split('-')[1])))
            l_ok = sum(1 for d in fin if check_success(d['live_emir'], int(d['score'].split('-')[0]), int(d['score'].split('-')[1])))
            st.markdown(f"""<div class='stats-panel'><div><div class='stat-val'>{len(fin)}</div><div class='stat-lbl'>SİBER KAYIT</div></div><div><div class='stat-val' style='color:#58a6ff;'>%{ (p_ok/len(fin))*100:.1f}</div><div class='stat-lbl'>CANSIZ BAŞARI</div></div><div><div class='stat-val' style='color:#2ea043;'>%{ (l_ok/len(fin))*100:.1f}</div><div class='stat-lbl'>CANLI BAŞARI</div></div></div>""", unsafe_allow_html=True)

    # GÖRSELLEŞTİRME
    for arc in display_list:
        gh_v, ga_v = map(int, arc['score'].split('-'))
        is_fin = arc['status'] in ['FT', 'AET', 'PEN']
        win_pre = f"<span class='status-win'>✅</span>" if check_success(arc['pre_emir'], gh_v, ga_v) else (f"<span class='status-lost'>❌</span>" if is_fin else "")
        win_live = f"<span class='status-win'>✅</span>" if check_success(arc['live_emir'], gh_v, ga_v) else (f"<span class='status-lost'>❌</span>" if is_fin else "")
        color = "#2ea043" if arc['conf'] >= 92 else "#f1e05a"
        is_live = arc['status'] not in ['TBD', 'NS', 'FT', 'AET', 'PEN', 'P', 'CANC', 'ABD', 'AWD', 'WO']
        live_tag = "<div class='live-pulse'>📡 CANLI SİSTEM AKTİF</div>" if is_live else "<div class='archive-badge'>🔒 SİBER MÜHÜR</div>"
        min_tag = f"<span class='live-min-badge'>{arc['min']}'</span>" if is_live else ""
        st.markdown(f"""<div class='decision-card' style='border-left:6px solid {color};'><div class='ai-score' style='color:{color};'>%{arc['conf']}</div>{live_tag}<br><b style='color:#58a6ff;'>⚽ {arc['league']}</b> | <span class='tsi-time'>⌚ {arc['date']}</span><br><span style='font-size:1.3rem; font-weight:bold;'>{arc['home']} vs {arc['away']}</span><br><div class='score-board'>{arc['score']} {min_tag}</div><div style='display:flex; gap:10px; margin-top:10px;'><div style='flex:1; padding:8px; background:rgba(88,166,255,0.1); border:1px solid #58a6ff; border-radius:6px;'><small style='color:#58a6ff;'>CANSIZ EMİR</small><br><b>{arc['pre_emir']}</b> {win_pre}</div><div style='flex:1; padding:8px; background:rgba(46,160,67,0.1); border:1px solid #2ea043; border-radius:6px;'><small style='color:#2ea043;'>CANLI EMİR</small><br><b>{arc['live_emir']}</b> {win_live}</div></div></div>""", unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state["auth"] = False; st.rerun()
