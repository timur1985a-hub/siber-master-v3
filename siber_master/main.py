import requests
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

# ================= SİBER AYARLAR & API (V400) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_PASS = "1937timurR&"
MASTER_KEY = "TIMUR-BOSS-2026"

# --- ADMİN MANTIĞINDA 100 ADET SABİT LİSANS ANAHTARI ---
SİBER_HAVUZ = {
    "1 Ay": [f"1AY-SBR-{i:02d}" for i in range(1, 21)],
    "3 Ay": [f"3AY-SBR-{i:02d}" for i in range(1, 21)],
    "6 Ay": [f"6AY-SBR-{i:02d}" for i in range(1, 21)],
    "12 Ay": [f"12AY-SBR-{i:02d}" for i in range(1, 21)],
    "Sınırsız": ["BOSS-UNLTD-01", "BOSS-UNLTD-02", "TIMUR-V400-PRO", "FERDI-KUZEN-VIP", "ULTRALINE-SBR"]
}

HEADERS = {
    "x-apisports-key": API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ALLOWED_LEAGUES = {203, 204, 39, 40, 140, 141, 135, 136, 78, 79, 61, 62, 88, 94, 144, 179, 119, 207, 218, 103, 113, 2, 3, 848}

# --- ANALİZ VE RADAR MOTORU ---
@st.cache_data(ttl=600)
def api_get_cached(endpoint, params=None):
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=20)
        return r.json().get("response", [])
    except: return []

def get_tsi_time(utc_date_str):
    dt_utc = datetime.fromisoformat(utc_date_str.replace("Z", "+00:00"))
    return (dt_utc + timedelta(hours=3)).strftime("%H:%M")

def get_live_radar_engine(fid, h_n, a_n):
    try:
        r = requests.get(f"{BASE_URL}/fixtures/statistics", headers=HEADERS, params={"fixture": fid}, timeout=10)
        res = r.json().get("response", [])
        if not res or len(res) < 2: return None
        s = {item['team']['name']: {i['type']: i['value'] for i in item['statistics']} for item in res}
        def gv(team, key):
            val = s.get(team, {}).get(key, 0)
            return int(str(val).replace("%","")) if val is not None else 0
        hp = (gv(h_n, "Shots on Goal") * 6) + (gv(h_n, "Dangerous Attacks") * 1.8) + (gv(h_n, "Corner Kicks") * 2.5)
        ap = (gv(a_n, "Shots on Goal") * 6) + (gv(a_n, "Dangerous Attacks") * 1.8) + (gv(a_n, "Corner Kicks") * 2.5)
        total = hp + ap
        return {"h_pct": int(hp/total*100) if total > 0 else 50, "a_pct": 100-int(hp/total*100) if total > 0 else 50, "h_sog": gv(h_n, "Shots on Goal"), "a_sog": gv(a_n, "Shots on Goal"), "h_att": gv(h_n, "Dangerous Attacks"), "a_att": gv(a_n, "Dangerous Attacks")}
    except: return None

def get_ultimate_logic_analysis(h_id, a_id, league_id):
    h_m = api_get_cached("fixtures", {"team": h_id, "last": 10})
    a_m = api_get_cached("fixtures", {"team": a_id, "last": 10})
    if not h_m or not a_m: return None
    def deep_scan(matches, tid):
        gf, o15, o25, scoring_m = 0, 0, 0, 0
        for m in matches:
            g = m['goals']; is_home = m['teams']['home']['id'] == tid
            f, a = (g['home'], g['away']) if is_home else (g['away'], g['home'])
            if f is None: continue
            gf += f
            if (f + a) >= 2: o15 += 1
            if (f + a) >= 3: o25 += 1
            if f > 0: scoring_m += 1
        c = len(matches)
        return {"G": gf/c, "U15": (o15/c)*100, "U25": (o25/c)*100, "SR": (scoring_m/c)*100}
    h, a = deep_scan(h_m, h_id), deep_scan(a_m, a_id)
    u15_raw = (h["G"] + a["G"]) * 11 + (h["U15"] + a["U15"]) * 0.25
    u15_final = min(99, int(u15_raw))
    return {"h": h, "a": a, "preds": {"ÜST 1.5": u15_final, "ÜST 2.5": int(u15_final * 0.75), "KG VAR": int((h["U15"] + a["U15"]) / 2)}}

# ================= STREAMLIT ARAYÜZ =================
st.set_page_config(page_title="Siber Master V400 - Timur Edition", layout="wide")

if "auth" not in st.session_state: st.session_state["auth"] = False
if "is_admin" not in st.session_state: st.session_state["is_admin"] = False

if not st.session_state["auth"]:
    # --- TÜRKÇE GÜÇLÜ GİRİŞ EKRANI ---
    st.markdown("<h1 style='text-align: center; color: #00f2ff; font-family: sans-serif;'>🛡️ SİBER MASTER V400</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ffffff;'>Türkiye'nin En Gelişmiş Yapay Zeka Analiz Sistemi</h3>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<div style='background-color: #0e1117; padding: 25px; border-radius: 15px; border: 2px solid #00f2ff; text-align: center;'>"
                "<h2 style='color: #00f2ff; margin-bottom: 10px;'>🤖 Yapay Zeka Muhakeme Motoru Aktif</h2>"
                "<p style='color: #ffffff; font-size: 20px;'>Bu ileri nesil analiz platformu, siber veri uzmanı <b style='color: #ff4b4b;'>TİMUR</b> tarafından siz değerli kullanıcılarımız için özel olarak tasarlanıp kodlanmıştır.</p>"
                "<p style='color: #00f2ff; font-weight: bold;'>Geleceği tahmin etmek için verinin gücünü kullanın.</p>"
                "</div>", unsafe_allow_html=True)
    st.write("")
    
    t1, t2 = st.tabs(["🔑 LİSANS İLE BAĞLAN", "👨‍💻 SİSTEM YÖNETİCİSİ"])
    with t1:
        key = st.text_input("Size Özel Protokol Anahtarını Girin:", type="password", help="Lisans anahtarınız giriş için zorunludur.")
        if st.button("SİSTEME GİRİŞ YAP"):
            all_keys = [k for sublist in SİBER_HAVUZ.values() for k in sublist]
            if key == MASTER_KEY or key in all_keys:
                st.session_state.update({"auth": True, "is_admin": (key == MASTER_KEY)})
                st.rerun()
            else: st.error("❌ HATA: Yetkisiz Giriş Denemesi! Geçersiz Anahtar.")
    with t2:
        if st.text_input("Yönetici Kodunuz:", type="password") == ADMIN_PASS and st.button("YÖNETİCİ OLARAK OTURUM AÇ"):
            st.session_state.update({"auth": True, "is_admin": True}); st.rerun()

else:
    # --- YAN PANEL ---
    with st.sidebar:
        st.markdown("<h2 style='color: #00f2ff; text-align: center;'>⚙️ KOMUTA MERKEZİ</h2>", unsafe_allow_html=True)
        st.write("---")
        st.success(f"Oturum Sahibi: {'👑 TİMUR' if st.session_state['is_admin'] else '👥 Değerli Kullanıcı'}")
        
        if st.button("🔄 VERİLERİ TAZELE (GÜNCELLE)", use_container_width=True):
            st.cache_data.clear()
            st.toast("Veriler Başarıyla Güncellendi!", icon="✅")
            st.rerun()
        
        st.divider()
        if st.session_state["is_admin"]:
            st.header("💎 Lisans Yönetimi")
            sec = st.selectbox("Süre Belirle:", ["1 Ay", "3 Ay", "6 Ay", "12 Ay", "Sınırsız"])
            if st.button("YENİ ANAHTAR ÇIKART"):
                st.code(SİBER_HAVUZ[sec][0], language="text")
        
        min_conf = st.slider("🎯 Başarı Eşiği (%)", 50, 95, 70)
        nesine = st.toggle("Sadece Nesine Bülteni", value=True)
        if st.button("🔴 GÜVENLİ ÇIKIŞ YAP", use_container_width=True):
            st.session_state.clear(); st.rerun()

    # --- ANA ANALİZ PANELİ ---
    st.markdown("<h1 style='color: #00f2ff;'>🏆 SİBER MASTER V400: CANLI ANALİZ RADARI</h1>", unsafe_allow_html=True)
    st.caption("Yapay Zeka ve Veri Madenciliği ile Maç Muhakemesi")

    fixtures = api_get_cached("fixtures", {"date": datetime.now().strftime("%Y-%m-%d")})
    if nesine: fixtures = [f for f in fixtures if f["league"]["id"] in ALLOWED_LEAGUES]

    if not fixtures:
        st.info("📡 Şu an sistemde aktif veri akışı yok. Lütfen daha sonra tekrar deneyin.")

    for f in fixtures:
        h_id, a_id = f["teams"]["home"]["id"], f["teams"]["away"]["id"]
        h_n, a_n = f["teams"]["home"]["name"], f["teams"]["away"]["name"]
        status = f["fixture"]["status"]["short"]
        data = get_ultimate_logic_analysis(h_id, a_id, f["league"]["id"])
        
        if data and data["preds"]["ÜST 1.5"] >= min_conf:
            tsi = get_tsi_time(f["fixture"]["date"])
            label = f"🔴 {f['fixture']['status']['elapsed']}' | {h_n} {f['goals']['home']}-{f['goals']['away']} {a_n}" if status != "NS" else f"⌛ {tsi} | {h_n} vs {a_n}"
            
            with st.expander(f"{label} (GÜVEN ORANI: %{data['preds']['ÜST 1.5']})"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write("🔍 **Siber İstatistikler**")
                    st.table(pd.DataFrame({"Kriter": ["Gol Ortalaması", "Üst 1.5 Olasılığı"], h_n: [f"{data['h']['G']:.2f}", f"%{data['h']['U15']:.0f}"], a_n: [f"{data['a']['G']:.2f}", f"%{data['a']['U15']:.0f}"]}))
                with c2:
                    st.write("🤖 **AI Tahmin Raporu**")
                    for p, v in data["preds"].items(): st.write(f"{p}: %{v}"); st.progress(v)
                with c3:
                    st.write("📡 **Canlı Baskı Radarı**")
                    if status != "NS":
                        live = get_live_radar_engine(f["fixture"]["id"], h_n, a_n)
                        if live:
                            st.write(f"Saldırı Gücü: %{live['h_pct']} - %{live['a_pct']}")
                            st.progress(live['h_pct'])
                            st.write(f"İsabetli Şut: {live['h_sog']}-{live['a_sog']}")
                    else: st.success("✅ Maç Önü Analizi Hazır")
