import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. AYARLAR VE API MÜHÜRLERİ =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 200), ("3-AY", 90, 200), ("6-AY", 180, 200), ("SINIRSIZ", 36500, 200)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. TASARIM DÜZELTME (FIXED UI) =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu, header, footer, .stDeployButton {visibility: hidden; display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background-color: #020617; color: #f1f5f9; }
        
        /* Paket Kartları */
        .pkg-card {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-bottom: 15px;
            transition: 0.3s;
        }
        .pkg-card:hover { border-color: #38bdf8; background: rgba(15, 23, 42, 1); }
        .price-tag { font-size: 1.5rem; color: #4ade80; font-weight: bold; margin: 10px 0; }
        
        .success-box { 
            background: rgba(74, 222, 128, 0.1); 
            border: 2px dashed #4ade80; 
            padding: 20px; 
            border-radius: 12px; 
            text-align: center; 
            color: #4ade80; 
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master Terminal", layout="wide")
apply_fixed_ui()

# ================= 3. ÖDEME FONKSİYONU =================
def redirectToShopier(pkg_name):
    # BURASI ÇOK ÖNEMLİ: Kendi Shopier dükkan linklerinizi buraya ekleyin
    links = {
        "1-AY": "https://www.shopier.com/SizinDukkan_1Ay",
        "3-AY": "https://www.shopier.com/SizinDukkan_3Ay",
        "6-AY": "https://www.shopier.com/SizinDukkan_6Ay",
        "SINIRSIZ": "https://www.shopier.com/SizinDukkan_Sinirsiz"
    }
    target_link = links.get(pkg_name, "https://www.shopier.com/SizinDukkan")
    
    # JavaScript ile yeni sekmede ödeme sayfasını açar
    js = f"window.open('{target_link}')"
    st.components.v1.html(f"<script>{js}</script>", height=0)

# ================= 4. GİRİŞ VE SATIŞ EKRANI =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "key": None, "purchased_key": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🛡️ SİBER MASTER TERMİNAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Erişim için bir paket seçin ve ödemeyi tamamlayın.</p>", unsafe_allow_html=True)

    # PAKET MATRİSİ
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='pkg-card'><h3>1 AY</h3><div class='price-tag'>700 TL</div></div>", unsafe_allow_html=True)
        if st.button("SATIN AL", key="b1"):
            redirectToShopier("1-AY")
            st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "1-AY")

    with col2:
        st.markdown("<div class='pkg-card'><h3>3 AY</h3><div class='price-tag'>2.000 TL</div></div>", unsafe_allow_html=True)
        if st.button("SATIN AL", key="b2"):
            redirectToShopier("3-AY")
            st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "3-AY")

    with col3:
        st.markdown("<div class='pkg-card'><h3>6 AY</h3><div class='price-tag'>5.000 TL</div></div>", unsafe_allow_html=True)
        if st.button("SATIN AL", key="b3"):
            redirectToShopier("6-AY")
            st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "6-AY")

    with col4:
        st.markdown("<div class='pkg-card'><h3>KRAL</h3><div class='price-tag'>15.000 TL</div></div>", unsafe_allow_html=True)
        if st.button("SATIN AL", key="b4"):
            redirectToShopier("SINIRSIZ")
            st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == "SINIRSIZ")

    # BAŞARILI ÖDEME BİLDİRİMİ
    if st.session_state.purchased_key:
        st.markdown(f"""
            <div class='success-box'>
                ✅ ÖDEME SAYFASI AÇILDI!<br>
                Ödeme sonrası lisansınız: <span style='color:white; font-size:1.4rem;'>{st.session_state.purchased_key}</span><br>
                <small>Ödemenizi tamamladıktan sonra kodu kopyalayıp aşağıya girin.</small>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # LİSANS AKTİVASYON
    u_lic = st.text_input("Lisans Anahtarını Girin:", value=st.session_state.purchased_key if st.session_state.purchased_key else "")
    if st.button("🚀 SİSTEME GİRİŞ YAP"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "key": u_lic})
            st.rerun()
        else:
            st.error("Hatalı anahtar.")

# ================= 5. ANALİZ PANELİ (GİRİŞTEN SONRA) =================
else:
    st.sidebar.success(f"Oturum: {st.session_state.key}")
    if st.sidebar.button("ÇIKIŞ"): st.session_state.clear(); st.rerun()
    st.title("🛡️ Canlı Siber Analiz Merkezi")
    st.info("Sinyaller taranıyor... Verileri güncellemek için yan menüyü kullanın.")
