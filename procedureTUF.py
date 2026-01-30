# FIX VOOR PYTHON 3.13 (Cruciaal voor Streamlit Cloud)
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

# Tijdlijn 0: Vertrekprocedure (tijdlijn0.png)
data_vertrek_tuf = {
    "title": "Vertrekprocedure op Transuniverse",
    "steps": [
        {"t": "Rittenblad en CMR's ophalen", "d": "Chauffeur haalt rittenblad en CMR's op bij Transuniverse."},
        {"t": "Computer aanmelden", "d": "Chauffeur meldt zich aan op computer met ritnummer (=I nummer)."},
        {"t": "Lading controleren", "d": "Chauffeur controleert lading zo goed mogelijk en meldt opmerkingen aan dispatch."},
        {"t": "Voorgeladen lading opmerken", "d": "Indien voorgeladen: schrijf 'chauffeur niet aanwezig bij belading' in vak 9 op de CMR."},
        {"t": "CMR's tekenen", "d": "Teken in vak 15 en leg exemplaar 1 in de bak aan Handling voor vertrek."}
    ]
}

# Tijdlijn 1: Laden en lossen bij klant (tijdlijn1.png) - NU OOK ALS TIJDLIJN
data_cmr_klant = {
    "title": "Laden en lossen bij de klant (CMR regels)",
    "steps": [
        {"t": "CMR TIJDEN", "d": "Altijd het uur van aankomst en vertrek invullen. Wachttijd > 1u? Meld direct aan dispatch."},
        {"t": "RUILEURO", "d": "Enkel pallets ruilen als 'RUILEURO' op CMR staat. Geen pallets bij klant? Meld aan dispatch."},
        {"t": "SCHADE", "d": "Schrijf in VAK 9 wat er niet correct is of waar er schade is. Meld aan dispatch."},
        {"t": "MEER/MINDER", "d": "Nooit zomaar meer of minder laden dan voorzien. Contacteer altijd eerst de dispatch."}
    ]
}

# Tijdlijn 2: Aankomst na rit (tijdlijn2.png)
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
    ["en", "fr", "de", "pl", "ro", "bg", "tr", "es", "lt"],
    format_func=lambda x: {
        "en": "English", "fr": "Français", "de": "Deutsch", 
        "pl": "Polski", "ro": "Română", "bg": "Български (Bulgaars)", 
        "tr": "Türkçe", "es": "Español", "lt": "Lietuvių"
    }[x]
)

# Keuze menu
choice = st.radio(
    "Selecteer de gewenste procedure:",
    ["1. Vertrek TUF", "2. Bij de Klant (CMR)", "3. Aankomst TUF (Einde rit)"],
    horizontal=True
)

st.divider()

# --- DISPLAY LOGICA ---

def render_timeline(data, image_file, color_list=None):
    # Toon de afbeelding
    try:
        st.image(Image.open(image_file), use_container_width=True)
    except:
        st.warning(f"Bestand '{image_file}' niet gevonden.")
    
    st.header(f"📋 {safe_translate(data['title'], target_lang)}")
    
    # Maak kolommen op basis van aantal stappen
    steps = data['steps']
    cols = st.columns(len(steps))
    
    # Standaard kleuren als er geen lijst is meegegeven
    if not color_list:
        color_list = ["#f1f3f4"] * len(steps)
        border_list = ["#4285f4"] * len(steps)
    else:
        border_list = color_list # Gebruik dezelfde kleur voor de rand

    for idx, step in enumerate(steps):
        with cols[idx]:
            t = safe_translate(step['t'], target_lang)
            d = safe_translate(step['d'], target_lang)
            st.markdown(f"""
            <div style="background-color: {color_list[idx % len(color_list)]}; padding: 15px; border-radius: 10px; border-top: 6px solid {border_list[idx % len(border_list)]}; min-height: 220px; color: black; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-top:0; color: black;">{idx+1}. {t}</h4>
                <hr style="margin: 10px 0; border: 0; border-top: 1px solid #ccc;">
                <p style="font-size: 14px; line-height: 1.4;">{d}</p>
            </div>
            """, unsafe_allow_html=True)

# Uitvoering op basis van keuze
if choice == "1. Vertrek TUF":
    render_timeline(data_vertrek_tuf, 'tijdlijn0.png', ["#e8f0fe", "#e6f4ea", "#fef7e0", "#fce8e6", "#f3e5f5"])

elif choice == "2. Bij de Klant (CMR)":
    # Nu ook als tijdlijn weergegeven
    render_timeline(data_cmr_klant, 'tijdlijn1.png', ["#e1f5fe", "#e8f5e9", "#fff3e0", "#fce4ec"])

else: # 3. Aankomst TUF
    render_timeline(data_aankomst_tuf, 'tijdlijn2.png', ["#e8f0fe", "#e6f4ea", "#fef7e0"])
