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
    
    # 1. Tekst toevoegen
    if text_input:
        # Fix voor speciale tekens
        clean_text = text_input.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        pdf.ln(5)
    
    # 2. Geplakte afbeelding toevoegen
    if pasted_image_data is not None and hasattr(pasted_image_data, 'image') and pasted_image_data.image is not None:
        img_buffer = io.BytesIO()
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

    # CRUCIAL: Gebruik dest='S' om bytes terug te geven aan Streamlit
    return pdf.output(dest='S')

# --- Streamlit Interface ---
st.set_page_config(page_title="PDF Generator", page_icon="📄")

st.title("📄 PDF Generator")

text_data = st.text_area("1. Plak hier je tekst:", height=150)
st.write("2. Afbeelding plakken (Ctrl+V):")
pasted_img = paste_image_button(label="Klik hier om te plakken")
image_file = st.file_uploader("3. Of upload een bestand:", type=["jpg", "png", "jpeg"])

if st.button("Genereer PDF", type="primary"):
    has_pasted = pasted_img is not None and hasattr(pasted_img, 'image') and pasted_img.image is not None
    
    if text_data or image_file or has_pasted:
        try:
            # We vangen de output op als bytes
            pdf_output = create_pdf(text_data, image_file, pasted_img)
            
            # Zorg dat het echt bytes zijn voor de download_button
            if isinstance(pdf_output, str):
                pdf_bytes = pdf_output.encode('latin-1')
            else:
                pdf_bytes = pdf_output

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"document_{timestamp}.pdf"
            
            st.success("PDF gegenereerd!")
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Er is een fout opgetreden: {e}")
    else:
        st.error("Voeg eerst inhoud toe.")
