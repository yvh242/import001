def create_pdf(text_input, uploaded_image, pasted_image_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Tekst toevoegen
    if text_input:
        # We gebruiken latin-1 encoding omdat standaard FPDF soms moeite heeft met speciale tekens
        clean_text = text_input.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        pdf.ln(5)
    
    # 2. Geplakte afbeelding toevoegen (Verbeterde check)
    if pasted_image_data is not None and pasted_image_data.image is not None:
        img_buffer = io.BytesIO()
        pasted_image_data.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        # Bepaal positie: x=10, huidige y, breedte=150mm
        pdf.image(img_buffer, x=10, w=150)
        pdf.ln(5)

    # 3. Geüploade afbeelding toevoegen
    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, w=150)

    return pdf.output()
