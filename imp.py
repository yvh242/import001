import streamlit as st
import pandas as pd

def main():
    st.title("Excel-bestanden viewer")
    st.write("Upload een Excel-bestand om de inhoud te bekijken")

    # Bestand uploader
    uploaded_file = st.file_uploader("Kies een Excel-bestand", type=['xlsx', 'xls'])

    if uploaded_file is not None:
        try:
            # Lees het Excel-bestand
            df = pd.read_excel(uploaded_file)
            
            # Toon de data
            st.success("Bestand succesvol geüpload!")
            st.write("Voorbeeld van de data:")
            st.dataframe(df)
            
            # Optionele extra's
            st.subheader("Data informatie")
            st.write(f"Aantal rijen: {df.shape[0]}")
            st.write(f"Aantal kolommen: {df.shape[1]}")
            
            st.subheader("Kolommen")
            st.write(list(df.columns))
            
        except Exception as e:
            st.error(f"Fout bij het lezen van het bestand: {e}")

if __name__ == "__main__":
    main()
