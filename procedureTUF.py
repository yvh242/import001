# 1. FIX VOOR PYTHON 3.13 (MOET BOVENAAN)
try:
    import cgi
except ImportError:
    import legacy_cgi as cgi
    import sys
    sys.modules['cgi'] = cgi

import streamlit as st
from googletrans import Translator
from PIL import Image

# Initialiseer de vertaler
translator = Translator()

st.set_page_config(page_title="Transuniverse Vertaler", layout="wide")

st.title("🚚 Transuniverse Driver Instructions")

# 2. Foto tonen
try:
    image = Image.open('tijdlijn.png')
    st.image(image, use_container_width=True)
except:
    st.info("Upload 'tijdlijn.png' om de visuele gids te zien.")

# 3. Taalinstelling
target_lang = st.sidebar.selectbox(
    "Select Language / Kies Taal",
    ["en", "fr", "de", "pl", "ro", "tr", "es"],
    format_func=lambda x: {"en": "English", "fr": "Français", "de": "Deutsch", "pl": "Polski", "ro": "Română", "tr": "Türkçe", "es": "Español"}[x]
)

# 4. Data definities
data = {
    "section1": {
        "title": "Aankomst na de rit op Transuniverse",
        "steps": [
            {"t": "Riemen losmaken", "d": "Riemen losmaken indien nodig"},
            {"t": "CMR's afgeven", "d": "Alle CMR's (expl. 3 levering, expl. 2 afhaling) afgeven aan Handling"},
            {"t": "Afmelden op computer", "d": "Afmelden op computer aan de hand van rit nummer (=I nummer)"}
        ]
    },
    "section2": {
        "title": "Laden en lossen bij klant",
        "items": [
            {"k": "CMR", "v": "Altijd het uur van aankomst en vertrek invullen. Wachttijd > 1u? Meld aan dispatch."},
            {"k": "RUILEURO", "v": "Enkel ruilen als 'RUILEURO' op CMR staat. Geen pallets? Meld aan dispatch."},
            {"k": "SCHADE", "v": "Schrijf in VAK 9 wat er niet correct is, meld aan dispatch."},
            {"k": "MEER/MINDER", "v": "Nooit zomaar meer of minder laden. Contacteer eerst dispatch."}
        ]
    }
}

def safe_translate(text):
    if not text: return ""
    try:
        return translator.translate(text, dest=target_lang).text
    except Exception:
        return text 

# 5. Vertaling en Weergave
if st.sidebar.button("Vertaal / Translate"):
    # Sectie 1: De Tijdlijn
    vertaalde_titel_1 = safe_translate(data['section1']['title'])
    st.markdown(f"<h2 style='text-align: center;'>📍 {vertaalde_titel_1}</h2>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    colors = ["#e8f0fe", "#e6f4ea", "#fef7e0"]
    borders = ["#4285f4", "#34a853", "#fbbc04"]
    
    for idx, step in enumerate(data['section1']['steps']):
        with cols[idx]:
            t = safe_translate(step['t'])
            d = safe_translate(step['d'])
            st.markdown(f"""
            <div style="background-color: {colors[idx]}; padding: 15px; border-radius: 10px; border-left: 5px solid {borders[idx]}; min-height: 180px; color: black;">
                <h4 style="margin:0; color: black;">{idx+1}. {t}</h4>
                <p style="font-size: 14px; color: #333;">{d}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Sectie 2: Laden en Lossen
    vertaalde_titel_2 = safe_translate(data['section2']['title'])
    st.header(f"📦 {vertaalde_titel_2}")
    
    for item in data['section2']['items']:
        k = safe_translate(item['k'])
        v = safe_translate(item['v'])
        with st.expander(f"🔹 {k}"):
            st.write(v)
