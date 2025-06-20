import streamlit as st
import pandas as pd

st.title('🚗 Rittenanalyse per Chauffeur')

# Bestand uploaden
uploaded_file = st.file_uploader("Upload Excel-bestand", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Excel lezen
        df = pd.read_excel(uploaded_file)
        
        # Controleren of de benodigde kolommen aanwezig zijn
        required_columns = ['Chauffeur naam', 'Ritdatum']
        if all(col in df.columns for col in required_columns):
            # Datum kolom omzetten naar datumtype
            df['Ritdatum'] = pd.to_datetime(df['Ritdatum']).dt.date
            
            # Aantal ritten per chauffeur per datum tellen
            result = df.groupby(['Chauffeur naam', 'Ritdatum']).size().reset_index(name='Aantal ritten')
            
            # Sorteren op datum en chauffeur
            result = result.sort_values(by=['Ritdatum', 'Chauffeur naam'])
            
            # Resultaat tonen
            st.success("✅ Bestand succesvol verwerkt!")
            st.dataframe(result)
            
            # Download knop voor resultaat (CSV)
            csv = result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download resultaat als CSV",
                data=csv,
                file_name='ritten_per_chauffeur.csv',
                mime='text/csv'
            )
        else:
            st.error("❌ Het Excel-bestand moet 'Chauffeur naam' en 'Ritdatum' kolommen bevatten.")
    
    except Exception as e:
        st.error(f"❌ Fout: {e}")
else:
    st.info("📤 Upload een Excel-bestand om te beginnen")
