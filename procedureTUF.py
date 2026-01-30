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

# Section 0: Vertrekprocedure (tijdlijn0.png)
data_vertrek_tuf = {
    "title": "Vertrekprocedure op Transuniverse",
    "steps": [
        {"t": "Rittenblad en CMR's ophalen", "d": "Chauffeur haalt rittenblad en CMR's op bij Transuniverse."},
        {"t": "Computer aanmelden", "d": "Chauffeur meldt zich aan op computer met ritnummer (=I nummer)."},
        {"t": "Lading controleren", "d": "Chauffeur controleert lading zo goed mogelijk en meldt opmerkingen aan dispatch."},
        {"t": "Voorgeladen lading opmerken", "d": "Indien voorgeladen: schrijf 'chauffeur niet aanwezig bij belading' in vak 9."},
        {"t": "CMR's tekenen", "d": "Teken in vak 15 en leg exemplaar 1 in de bak aan Handling voor vertrek."}
    ]
}

# Section 1: Laden en lossen bij klant (tijdlijn1.png)
data_cmr_klant = {
    "title": "Laden en lossen bij de klant (CMR regels)",
    "items": [
        {"k": "CMR TIJDEN", "v": "Altijd het uur van aankomst en vertrek invullen op de CMR. Wachttijd > 1u? Meld direct aan dispatch."},
        {"k": "RUILEURO", "v": "Enkel pallets ruilen als 'RUILEURO' op CMR staat. Geen pallets bij klant? Meld aan dispatch."},
        {"k": "SCHADE", "v": "Schrijf in VAK 9 wat er niet correct is of waar er schade is. Meld aan dispatch."},
        {"k": "MEER/MINDER", "v": "Nooit zomaar meer of minder laden dan voorzien. Contacteer altijd eerst de dispatch."}
    ]
}

# Section 2: Aankomst na rit (tijdlijn2.png)
data_aankomst_tuf = {
    "title": "Aankomst na de rit op Transuniverse",
    "steps": [
        {"t": "Riemen losmaken", "d": "Riemen losmaken indien nodig."},
        {"t": "CMR's afgeven", "d": "Alle CMR's (expl. 3 levering, expl. 2 afhaling) afgeven aan Handling."},
        {"t": "Afmelden op computer", "d": "Afmelden op computer aan de hand van rit nummer (=I nummer)."}
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

# Sidebar
st.sidebar.header("Taal / Language")
target_lang = st.sidebar.selectbox(
    "Kies taal",
    ["en", "fr", "de", "pl", "ro", "tr", "es", "lt"],
    format_func=lambda x: {"en": "English", "fr": "Français", "de": "Deutsch", "pl": "Polski", "ro": "Română", "tr": "Türkçe", "es": "Español", "lt": "Lietuvių"}[x]
)

# Keuze menu
choice = st.radio(
    "Selecteer de gewenste procedure:",
    ["1. Vertrek TUF", "2. Bij de Klant (CMR)", "3. Aankomst TUF (Einde rit)"],
    horizontal=True
)

st.divider()

# --- DISPLAY LOGICA ---

if choice == "1. Vertrek TUF":
    st.image(Image.open('tijdlijn0.png'), use_container_width=True)
    st.header(f"🚀 {safe_translate(data_vertrek_tuf['title'], target_lang)}")
    
    # Weergave in 5 kolommen voor de 5 stappen
    cols = st.columns(len(data_vertrek_tuf['steps']))
    for idx, step in enumerate(data_vertrek_tuf['steps']):
        with cols[idx]:
            st.markdown(f"""
            <div style="background-color: #f1f3f4; padding: 10px; border-radius: 8px; border-top: 5px solid #4285f4; min-height: 200px; color: black;">
                <b style="color: #4285f4;">{idx+1}. {safe_translate(step['t'], target_lang)}</b><br><br>
                <span style="font-size: 13px;">{safe_translate(step['d'], target_lang)}</span>
            </div>
            """, unsafe_allow_html=True)

elif choice == "2. Bij de Klant (CMR)":
    st.image(Image.open('tijdlijn1.png'), use_container_width=True)
    st.header(f"📦 {safe_translate(data_cmr_klant['title'], target_lang)}")
    for item in data_cmr_klant['items']:
        with st.expander(f"🔹 {safe_translate(item['k'], target_lang)}"):
            st.write(safe_translate(item['v'], target_lang))

else: # Aankomst TUF
    st.image(Image.open('tijdlijn2.png'), use_container_width=True)
    st.header(f"🏁 {safe_translate(data_aankomst_tuf['title'], target_lang)}")
    cols = st.columns(3)
    colors = ["#e8f0fe", "#e6f4ea", "#fef7e0"]
    for idx, step in enumerate(data_aankomst_tuf['steps']):
        with cols[idx]:
            st.markdown(f"""
            <div style="background-color: {colors[idx]}; padding: 15px; border-radius: 10px; min-height: 150px; color: black; border: 1px solid #ccc;">
                <h4 style="margin:0; color: black;">{idx+1}. {safe_translate(step['t'], target_lang)}</h4>
                <p style="font-size: 14px;">{safe_translate(step['d'], target_lang)}</p>
            </div>
            """, unsafe_allow_html=True)
