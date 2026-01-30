# FIX VOOR PYTHON 3.13
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

st.set_page_config(page_title="Transuniverse Procedure Helper", layout="wide")

# --- DATA DEFINITIES ---
# Section 1 (nu voor Vertrek TUF / tijdlijn2.png)
data_vertrek = {
    "title": "Aankomst na de rit op Transuniverse (Vertrek procedure)",
    "steps": [
        {"t": "Riemen losmaken", "d": "Riemen losmaken indien nodig"},
        {"t": "CMR's afgeven", "d": "Alle CMR's (expl. 3 levering, expl. 2 afhaling) afgeven aan Handling"},
        {"t": "Afmelden op computer", "d": "Afmelden op computer aan de hand van rit nummer (=I nummer)"}
    ]
}

# Section 2 (nu voor CMR Procedure / tijdlijn1.png)
data_cmr = {
    "title": "Laden en lossen bij de klant (CMR regels)",
    "items": [
        {"k": "CMR TIJDEN", "v": "Altijd het uur van aankomst en vertrek invullen. Wachttijd > 1u? Meld aan dispatch."},
        {"k": "RUILEURO", "v": "Enkel ruilen als 'RUILEURO' op CMR staat. Geen pallets? Meld aan dispatch."},
        {"k": "SCHADE", "v": "Schrijf in VAK 9 wat er niet correct is, meld aan dispatch."},
        {"k": "MEER/MINDER", "v": "Nooit zomaar meer of minder laden. Contacteer eerst dispatch."}
    ]
}

def safe_translate(text, target):
    if not text: return ""
    try:
        return translator.translate(text, dest=target).text
    except:
        return text 

# --- UI INTERFACE ---
st.title("🚚 Transuniverse Logistics Assistant")

# Sidebar instellingen
st.sidebar.header("Instellingen")
target_lang = st.sidebar.selectbox(
    "Taal / Language",
    ["en", "fr", "de", "pl", "ro", "tr", "es"],
    format_func=lambda x: {"en": "English", "fr": "Français", "de": "Deutsch", "pl": "Polski", "ro": "Română", "tr": "Türkçe", "es": "Español"}[x]
)

# Keuze van de procedure
procedure_choice = st.radio(
    "Welke procedure wil je zien?",
    ["CMR Procedure (Laden/Lossen)", "Vertrek TUF (Na de rit)"],
    horizontal=True
)

st.divider()

# --- LOGICA VOOR WEERGAVE ---

if procedure_choice == "CMR Procedure (Laden/Lossen)":
    # Toon afbeelding 1
    try:
        st.image(Image.open('tijdlijn1.png'), use_container_width=True)
    except:
        st.warning("Bestand 'tijdlijn1.png' niet gevonden.")
    
    # Toon Data Section 2 (Vragen over CMR)
    st.header(f"📦 {safe_translate(data_cmr['title'], target_lang)}")
    for item in data_cmr['items']:
        k = safe_translate(item['k'], target_lang)
        v = safe_translate(item['v'], target_lang)
        with st.expander(f"🔹 {k}"):
            st.write(v)

else:
    # Toon afbeelding 2
    try:
        st.image(Image.open('tijdlijn2.png'), use_container_width=True)
    except:
        st.warning("Bestand 'tijdlijn2.png' niet gevonden.")

    # Toon Data Section 1 (Tijdlijn stappen)
    st.header(f"📍 {safe_translate(data_vertrek['title'], target_lang)}")
    cols = st.columns(3)
    colors, borders = ["#e8f0fe", "#e6f4ea", "#fef7e0"], ["#4285f4", "#34a853", "#fbbc04"]
    
    for idx, step in enumerate(data_vertrek['steps']):
        with cols[idx]:
            t = safe_translate(step['t'], target_lang)
            d = safe_translate(step['d'], target_lang)
            st.markdown(f"""
            <div style="background-color: {colors[idx]}; padding: 15px; border-radius: 10px; border-left: 5px solid {borders[idx]}; min-height: 160px; color: black;">
                <h4 style="margin:0; color: black;">{idx+1}. {t}</h4>
                <p style="font-size: 14px; color: #333;">{d}</p>
            </div>
            """, unsafe_allow_html=True)
