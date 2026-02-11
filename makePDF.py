import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

def create_pdf(text_input, image_input):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Voeg tekst toe
    if text_input:
        # Multi_cell zorgt voor tekstomloop
        pdf.multi_cell(0, 10, txt=text_input)
    
    # Voeg afbeelding toe (indien aanwezig)
    if image_input:
        # Sla de afbeelding tijdelijk op in het geheugen
        img_buffer = io.BytesIO()
        image_input.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        # Voeg toe aan PDF (we schalen naar een breedte van 190mm)
        pdf.image(img_buffer, x=10, y=pdf.get_y() + 10, w=190)

    return pdf.output(dest='S').encode('latin-1', 'replace')

# Streamlit Interface
st.title("Tekst & Afbeelding naar PDF")

# 1. Tekstvak
user_text = st.text_area("Schrijf hier je tekst:", height=150)

# 2. Afbeelding (Streamlit ondersteunt 'plakken' via de file_uploader of camera_input)
# Let op: Direct plakken (Ctrl+V) in een widget is in standaard HTML/Streamlit 
# vaak beperkt tot het upload-veld.
uploaded_file = st.file_uploader("Upload of plak een afbeelding", type=['png', 'jpg', 'jpeg'])

image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Voorbeeld van je afbeelding", use_container_width=True)

# 3. Download knop
if st.button("Genereer PDF"):
    if user_text or image:
        pdf_bytes = create_pdf(user_text, image)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="mijn_document.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Voer eerst wat tekst in of upload een afbeelding.")
