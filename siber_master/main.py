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
# Bu anahtarlar kodun parçasıdır, bulut bunları asla silemez.
SİBER_HAVUZ = {
    "1 Ay": [f"1AY-SBR-{i:02d}" for i in range(1, 21)],      # 20 Adet 1 Aylık
    "3 Ay": [f"3AY-SBR-{i:02d}" for i in range(1, 21)],      # 20 Adet 3 Aylık
    "6 Ay": [f"6AY-SBR-{i:02d}" for i in range(1, 21)],      # 20 Adet 6 Aylık
    "12 Ay": [f"12AY-SBR-{i:02d}" for i in range(1, 21)],    # 20 Adet 12 Aylık
    "Sınırsız": ["BOSS-UNLTD-01", "BOSS-UNLTD-02", "TIMUR-V400-PRO", "FERDI-KUZEN-VIP", "ULTRALINE-SBR"]
}

HEADERS = {
    "x-apisports-key": API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ALLOWED_LEAGUES = {203, 204, 39, 40, 140, 141, 135, 136, 78, 79, 61, 62, 88, 94, 144, 179, 119, 207, 218, 103, 113, 2, 3, 848}
HIGH_SCORING_LEAGUES = {203, 204, 135, 144, 94, 78}

# --- ANALİZ VE RADAR MOTORU (TAM ENTEGRE) ---
@st.cache_data(ttl=1200)
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
        gf, ga, o15, o25, kg, scoring_m = 0, 0, 0, 0, 0, 0
        for m in matches:
            g = m['goals']; is_home = m['teams']['home']['id'] == tid
            f, a = (g['home'], g['away']) if is_home else (g['away'], g['home'])
            if f is None: continue
            gf += f; ga += a
            if (f + a) >= 2: o15 += 1
            if (f + a) >= 3: o25 += 1
            if f > 0 and a > 0: kg += 1
            if f > 0: scoring_m += 1
        c = len(matches)
        return {"G": gf/c, "Y": ga/c, "U15": (o15/c)*100, "U25": (o25/c)*100, "KG": (kg/c)*100, "SR": (scoring_m/c)*100}
    h, a = deep_scan(h_m, h_id), deep_scan(a_m, a_id)
    clash_penalty = 10 if (h["G"] > 1.6 and a["Y"] < 0.9) else 0
    league_bonus = 6 if league_id in HIGH_SCORING_LEAGUES else 0
    consistency_bonus = 5 if (h["SR"] > 75 and a["SR"] > 75) else 0
    u15_raw = (h["G"] + a["G"]) * 11 + (h["U15"] + a["U15"]) * 0.25
    u15_final = min(99, int(u15_raw - clash_penalty + league_bonus + consistency_bonus))
    return {"h": h, "a": a, "preds": {"ÜST 1.5": u15_final, "ÜST 2.5": int(u15_final * 0.75), "KG VAR": int((h["KG"] + a["KG"]) / 2 + consistency_bonus)}}

# ================= STREAMLIT ARAYÜZ MANTIĞI =================
st.set_page_config(page_title="Siber Master V400 Pro", layout="wide")

if "auth" not in st.session_state: st.session_state["auth"] = False
if "is_admin" not in st.session_state: st.session_state["is_admin"] = False

if not st.session_state["auth"]:
    st.title("🔐 Siber Master V400 Güvenlik Kapısı")
    t1, t2 = st.tabs(["🔑 Lisanslı Giriş", "👨‍💻 Yönetici Girişi"])
    with t1:
        key = st.text_input("Lisans Anahtarı:", type="password")
        if st.button("Sisteme Bağlan"):
            all_keys = [k for sublist in SİBER_HAVUZ.values() for k in sublist]
            if key == MASTER_KEY or key in all_keys:
                st.session_state.update({"auth": True, "is_admin": (key == MASTER_KEY)})
                st.rerun()
            else: st.error("Geçersiz Anahtar!")
    with t2:
        if st.text_input("Yönetici Şifresi:", type="password") == ADMIN_PASS and st.button("Admin Gir"):
            st.session_state.update({"auth": True, "is_admin": True}); st.rerun()

else:
    if st.session_state["is_admin"]:
        st.sidebar.title("👑 Admin Paneli")
        st.sidebar.success("Sahip Timur Modu")
        secim = st.sidebar.selectbox("LİSANS ÜRET (Havuzdan Seç):", ["1 Ay", "3 Ay", "6 Ay", "12 Ay", "Sınırsız"])
        if st.sidebar.button("ANAHTARI GÖSTER"):
            kod = SİBER_HAVUZ[secim][0] # İlk boş anahtarı verir
            st.sidebar.code(f"KULLANICI ANAHTARI: {kod}", language="text")
            st.sidebar.warning("Bu anahtar kodun içine gömülüdür, silinmez.")
        if st.sidebar.button("🔴 Çıkış"): st.session_state.clear(); st.rerun()

    # --- SİBER MASTER V400 ANALİZ EKRANI ---
    st.title("🏆 SİBER MASTER V400: ANALİZ & CANLI RADAR")
    with st.sidebar:
        min_conf = st.slider("🎯 Güven Eşiği (%)", 50, 95, 70)
        nesine = st.toggle("Sadece Nesine", value=True)

    fixtures = api_get_cached("fixtures", {"date": datetime.now().strftime("%Y-%m-%d")})
    if nesine: fixtures = [f for f in fixtures if f["league"]["id"] in ALLOWED_LEAGUES]

    for f in fixtures:
        h_id, a_id = f["teams"]["home"]["id"], f["teams"]["away"]["id"]
        h_n, a_n = f["teams"]["home"]["name"], f["teams"]["away"]["name"]
        status = f["fixture"]["status"]["short"]
        data = get_ultimate_logic_analysis(h_id, a_id, f["league"]["id"])
        if data and data["preds"]["ÜST 1.5"] >= min_conf:
            tsi = get_tsi_time(f["fixture"]["date"])
            label = f"🔴 {f['fixture']['status']['elapsed']}' | {h_n} {f['goals']['home']}-{f['goals']['away']} {a_n}" if status != "NS" else f"⌛ {tsi} | {h_n} vs {a_n}"
            with st.expander(f"{label} (GÜVEN: %{data['preds']['ÜST 1.5']})"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write("🔍 **Kanıtlar**")
                    st.table(pd.DataFrame({"Veri": ["Gol Ort.", "Üst 1.5 %"], h_n: [f"{data['h']['G']:.2f}", f"%{data['h']['U15']:.0f}"], a_n: [f"{data['a']['G']:.2f}", f"%{data['a']['U15']:.0f}"]}))
                with c2:
                    st.write("🤖 **Muhakeme**")
                    for p, v in data["preds"].items(): st.write(f"{p}: %{v}"); st.progress(v)
                with c3:
                    st.write("📡 **Canlı Radar**")
                    if status != "NS":
                        live = get_live_radar_engine(f["fixture"]["id"], h_n, a_n)
                        if live:
                            st.write(f"Baskı: %{live['h_pct']} - %{live['a_pct']}")
                            st.progress(live['h_pct'])
                            st.write(f"Şut: {live['h_sog']}-{live['a_sog']}")
                    else: st.success("✅ Onaylandı")
