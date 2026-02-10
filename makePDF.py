import streamlit as st
from fpdf import FPDF
import io
from PIL import Image

def create_pdf(text_input, uploaded_image):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Voeg tekst toe
    if text_input:
        pdf.multi_cell(0, 10, txt=text_input)
    
    # Voeg afbeelding toe
    if uploaded_image:
        # Open de afbeelding met PIL om het formaat te controleren
        img = Image.open(uploaded_image)
        # Sla tijdelijk op of gebruik direct als bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        # Voeg toe aan PDF (we schalen de breedte naar 150mm voor de layout)
        pdf.image(img_buffer, x=10, y=pdf.get_y() + 10, w=150)

    return pdf.output()

# Streamlit Interface
st.title("📄 PDF Generator")
st.subheader("Maak een PDF van je tekst en afbeelding")

# Invoer velden
text_data = st.text_area("Typ hier je tekst:", height=150)
image_file = st.file_uploader("Upload een afbeelding (optioneel):", type=["jpg", "png", "jpeg"])

if st.button("Genereer PDF"):
    if text_data or image_file:
        pdf_bytes = create_pdf(text_data, image_file)
        
        st.success("PDF succesvol aangemaakt!")
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="mijn_document.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Voeg eerst wat tekst of een afbeelding toe.")
