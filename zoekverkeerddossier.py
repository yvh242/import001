import streamlit as st
import pandas as pd

st.title('📅 Dossieranalyse: Laaddatum vs. Einddatum')

# Bestand uploaden
uploaded_file = st.file_uploader("Upload Excel-bestand", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Lees het Excel-bestand
        df = pd.read_excel(uploaded_file)
        
        # Controleer of de benodigde kolommen bestaan
        required_columns = ['Dossiernr', 'Laad datum', 'Einddatum']
        if not all(col in df.columns for col in required_columns):
            st.error("❌ Het bestand moet 'Dossiernr', 'Laaddatum' en 'Einddatum' bevatten!")
        else:
            # Zet datums om naar datetime (voor correcte vergelijking)
            df['Laad datum'] = pd.to_datetime(df['Laad datum']).dt.date
            df['Einddatum'] = pd.to_datetime(df['Einddatum']).dt.date
            
            # Voeg een kolom toe die aangeeft of Laaddatum == Einddatum
            df['Gelijke_datum'] = df['Laad datum'] == df['Einddatum']
            
            # Filter alleen de rijen waar Laaddatum == Einddatum
            result_df = df[df['Gelijke_datum']][['Dossiernr', 'Laad datum', 'Einddatum']]
            
            # Toon het resultaat
            st.success(f"✅ {len(result_df)} dossiers met gelijke Laad- en Einddatum gevonden:")
            st.dataframe(result_df)
            
            # Download optie (CSV)
            csv = result_df.to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                label="📥 Download resultaat (CSV)",
                data=csv,
                file_name='dossiers_gelijke_datum.csv',
                mime='text/csv'
            )
            
            # Optioneel: toon een markdown tabel voor beter overzicht
            st.markdown("### Samenvatting:")
            st.write(f"- **Totaal dossiers:** {len(df)}")
            st.write(f"- **Dossiers met gelijke datum:** {len(result_df)}")
    
    except Exception as e:
        st.error(f"❌ Fout: {str(e)}")
else:
    st.info("📤 Upload een Excel-bestand om te beginnen")
