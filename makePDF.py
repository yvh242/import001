import streamlit as st
from fpdf import FPDF
import io
from PIL import Image
from streamlit_paste_button import paste_image_button

def create_pdf(text_input, uploaded_image, pasted_image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Tekst toevoegen
    if text_input:
        pdf.multi_cell(0, 10, txt=text_input)
        pdf.ln(10) # Extra witregel
    
    # 2. Geplakte afbeelding toevoegen
    if pasted_image:
        # De 'pasted_image' is al een Image object van de library
        img_buffer = io.BytesIO()
        pasted_image.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, w=150)
        pdf.ln(10)

    # 3. Geüploade afbeelding toevoegen
    if uploaded_image:
        img = Image.open(uploaded_image)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, w=150)

    return pdf.output()

# Streamlit Interface
st.set_page_config(page_title="Smart PDF Maker", layout="centered")
st.title("📄 PDF Maker met Plak-functie")

# Sectie 1: Tekst
text_data = st.text_area("Stap 1: Typ of plak hier je tekst:", height=150)

# Sectie 2: Afbeelding plakken (Nieuw!)
st.write("Stap 2: Klik op de knop hieronder en druk op Ctrl+V om een afbeelding te plakken:")
pasted_img = paste_image_button("Klik om afbeelding te plakken")

# Sectie 3: Bestand uploaden (Reserve optie)
image_file = st.file_uploader("Of upload handmatig een bestand:", type=["jpg", "png", "jpeg"])

if st.button("Genereer en Download PDF"):
    if text_data or image_file or pasted_img.image:
        pdf_bytes = create_pdf(text_data, image_file, pasted_img)
        
        st.success("PDF is klaar!")
        st.download_button(
            label="Download nu je PDF",
            data=pdf_bytes,
            file_name="mijn_document.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Voer eerst wat tekst in of plak/upload een afbeelding.")
