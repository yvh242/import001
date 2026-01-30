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
from fpdf import FPDF
import io

# Initialiseer de vertaler
translator = Translator()

st.set_page_config(page_title="Transuniverse Procedure Helper", layout="wide")

# --- DATA DEFINITIES ---
data_vertrek_tuf = {
    "title": "Vertrekprocedure op Transuniverse",
    "steps": [{"t": "Rittenblad en CMR's ophalen", "d": "Chauffeur haalt rittenblad en CMR's op bij Transuniverse."},
              {"t": "Computer aanmelden", "d": "Chauffeur meldt zich aan op computer met ritnummer (=I nummer)."},
              {"t": "Lading controleren", "d": "Chauffeur controleert lading zo goed mogelijk en meldt opmerkingen aan dispatch."},
              {"t": "Voorgeladen lading opmerken", "d": "Indien voorgeladen: schrijf 'chauffeur niet aanwezig bij belading' in vak 9 op de CMR."},
              {"t": "CMR's tekenen", "d": "Teken in vak 15 en leg exemplaar 1 in de bak aan Handling voor vertrek."}]
}

data_cmr_klant = {
    "title": "Laden en lossen bij de klant (CMR regels)",
    "steps": [{"t": "CMR TIJDEN", "d": "Altijd het uur van aankomst en vertrek invullen. Wachttijd > 1u? Meld direct aan dispatch."},
              {"t": "RUILEURO", "d": "Enkel pallets ruilen als 'RUILEURO' op CMR staat. Geen pallets bij klant? Meld aan dispatch."},
              {"t": "SCHADE", "d": "Schrijf in VAK 9 wat er niet correct is of waar er schade is. Meld aan dispatch."},
              {"t": "MEER/MINDER", "d": "Nooit zomaar meer of minder laden dan voorzien. Contacteer altijd eerst de dispatch."}]
}

data_aankomst_tuf = {
    "title": "Aankomst na de rit op Transuniverse",
    "steps": [{"t": "Riemen losmaken", "d": "Riemen losmaken indien nodig."},
              {"t": "CMR's afgeven", "d": "Alle CMR's (expl. 3 levering, expl. 2 afhaling) afgeven aan Handling."},
              {"t": "Afmelden op computer", "d": "Afmelden op computer aan de hand van rit nummer (=I nummer)."}]
}

def safe_translate(text, target):
    if not text: return ""
    try:
        return translator.translate(text, dest=target).text
    except:
        return text 

# --- PDF GENERATIE FUNCTIE ---
def create_pdf(title, steps, lang_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Transuniverse Logistics - {lang_name}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.multi_cell(0, 10, title)
    pdf.ln(10)
    
    for i, step in enumerate(steps):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{i+1}. {step['t']}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, step['d'])
        pdf.ln(5)
    
    return pdf.output()

# --- UI INTERFACE ---
st.title("🚚 Transuniverse Logistics Assistant")

# Sidebar
st.sidebar.header("Taal / Language")
languages = {
    "en": "English", "fr": "Français", "de": "Deutsch", "pl": "Polski", 
    "ro": "Română", "bg": "Bulgarian", "tr": "Türkçe", "es": "Español", "lt": "Lietuvių"
}
target_lang = st.sidebar.selectbox("Kies taal", list(languages.keys()), format_func=lambda x: languages[x])

choice = st.radio("Selecteer de gewenste procedure:", ["1. Vertrek TUF", "2. Bij de Klant (CMR)", "3. Aankomst TUF (Einde rit)"], horizontal=True)
st.divider()

# Selecteer de juiste data
current_data = data_vertrek_tuf if choice == "1. Vertrek TUF" else data_cmr_klant if choice == "2. Bij de Klant (CMR)" else data_aankomst_tuf
img_file = 'tijdlijn0.png' if choice == "1. Vertrek TUF" else 'tijdlijn1.png' if choice == "2. Bij de Klant (CMR)" else 'tijdlijn2.png'

# --- VERTALING VOORBEREIDEN ---
v_title = safe_translate(current_data['title'], target_lang)
v_steps = []
for s in current_data['steps']:
    v_steps.append({"t": safe_translate(s['t'], target_lang), "d": safe_translate(s['d'], target_lang)})

# --- DISPLAY ---
try:
    st.image(Image.open(img_file), use_container_width=True)
except:
    st.warning(f"Afbeelding {img_file} niet gevonden.")

st.header(f"📋 {v_title}")

# Download knop in de sidebar
pdf_data = create_pdf(v_title, v_steps, languages[target_lang])
st.sidebar.download_button(
    label="📩 Download PDF",
    data=bytes(pdf_data),
    file_name=f"procedure_{target_lang}.pdf",
    mime="application/pdf"
)

cols = st.columns(len(v_steps))
for idx, step in enumerate(v_steps):
    with cols[idx]:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-top: 6px solid #4285f4; min-height: 220px; color: black; border: 1px solid #ddd;">
            <h4 style="margin-top:0; color: black;">{idx+1}. {step['t']}</h4>
            <p style="font-size: 14px;">{step['d']}</p>
        </div>
        """, unsafe_allow_html=True)
