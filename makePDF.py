import streamlit as st
from fpdf import FPDF
import io
from PIL import Image
from streamlit_paste_button import paste_image_button
from datetime import datetime

def create_pdf(text_input, uploaded_image, pasted_image_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Tekst toevoegen (met fix voor speciale tekens)
    if text_input:
        # FPDF1/2 standaard fonts ondersteunen alleen latin-1. 
        # We vervangen onbekende tekens door een '?' om crashes te voorkomen.
        clean_text = text_input.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        pdf.ln(5)
    
    # 2. Geplakte afbeelding toevoegen (Veilige check)
    if pasted_image_data is not None:
        if hasattr(pasted_image_data, 'image') and pasted_image_data.image is not None:
            img_buffer = io.BytesIO()
            # Zet om naar RGB om problemen met transparante PNG's te voorkomen
            rgb_img = pasted_image_data.image.convert('RGB')
            rgb_img.save(img_buffer, format="JPEG")
            img_buffer.seek(0)
            pdf.image(img_buffer, x=10, w=150)
            pdf.ln(5)

    # 3. Geüploade afbeelding toevoegen
    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        img_buffer = io.BytesIO()
        rgb_img = img.convert('RGB')
        rgb_img.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, w=150)

    return pdf.output()

# --- Streamlit Interface ---
st.set_page_config(page_title="PDF Generator", page_icon="📄")

st.title("📄 PDF Generator")
st.info("Plak je tekst en afbeeldingen hieronder om er een PDF van te maken.")

# Stap 1: Tekst invoer
text_data = st.text_area("1. Plak hier je tekst (bijv. van een mail of reservatie):", height=150)

# Stap 2: Afbeelding plakken
st.write("2. Afbeelding plakken van klembord:")
pasted_img = paste_image_button(label="Klik hier en druk op Ctrl+V")

# Stap 3: Handmatige upload
image_file = st.file_uploader("3. Of upload een afbeeldingsbestand:", type=["jpg", "png", "jpeg"])

st.divider()

# Stap 4: PDF Genereren
if st.button("Genereer PDF", type="primary"):
    # Check of er wel iets is ingevoerd
    has_pasted_img = pasted_img is not None and hasattr(pasted_img, 'image') and pasted_img.image is not None
    
    if text_data or image_file or has_pasted_img:
        with st.spinner("PDF wordt gemaakt..."):
            pdf_bytes = create_pdf(text_data, image_file, pasted_img)
            
            # Maak een mooie bestandsnaam met datum en tijd
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"document_{timestamp}.pdf"
            
            st.success(f"Klaar! Je kunt nu '{file_name}' downloaden.")
            st.download_button(
                label="📥 Download PDF bestand",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )
    else:
        st.error("Fout: Voeg eerst tekst toe of plak/upload een afbeelding.")
