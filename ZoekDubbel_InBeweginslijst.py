import streamlit as st
import pandas as pd

st.title('🔍 Dubbele Dossiernr\'s met gelijke Einddatum')

# Bestand uploaden
uploaded_file = st.file_uploader("Upload Excel-bestand", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Lees het Excel-bestand
        df = pd.read_excel(uploaded_file)
        
        # Controleer of de benodigde kolommen bestaan
        required_columns = ['Dossiernr', 'Einddatum']
        if not all(col in df.columns for col in required_columns):
            st.error("❌ Het bestand moet 'Dossiernr' en 'Einddatum' bevatten!")
        else:
            # Zet 'Einddatum' om naar datetime (voor correcte vergelijking)
            df['Einddatum'] = pd.to_datetime(df['Einddatum']).dt.date
            
            # Groepeer op Dossiernr en controleer of er dubbele zijn
            grouped = df.groupby('Dossiernr').filter(lambda x: len(x) >= 2)
            
            if len(grouped) == 0:
                st.warning("⚠ Geen dubbele Dossiernr's gevonden!")
            else:
                # Sorteer op Dossiernr en Einddatum voor consistente vergelijking
                grouped = grouped.sort_values(['Dossiernr', 'Einddatum'])
                
                # Controleer per Dossiernr of de eerste en tweede Einddatum gelijk zijn
                result = []
                for dossier, group in grouped.groupby('Dossiernr'):
                    if len(group) >= 2:
                        eerste_einddatum = group['Einddatum'].iloc[0]
                        tweede_einddatum = group['Einddatum'].iloc[1]
                        if eerste_einddatum == tweede_einddatum:
                            result.append({
                                'Dossiernr': dossier,
                                'Einddatum (regel 1)': eerste_einddatum,
                                'Einddatum (regel 2)': tweede_einddatum,
                                'Status': '✅ GELIJK'
                            })
                        else:
                            result.append({
                                'Dossiernr': dossier,
                                'Einddatum (regel 1)': eerste_einddatum,
                                'Einddatum (regel 2)': tweede_einddatum,
                                'Status': '❌ VERSCHILLEND'
                            })
                
                # Maak een DataFrame van het resultaat
                result_df = pd.DataFrame(result)
                
                # Toon alleen de Dossiernr's met gelijke Einddatums
                st.success(f"✅ {len(result_df[result_df['Status'] == '✅ GELIJK'])} dubbele Dossiernr's met gelijke Einddatum gevonden:")
                st.dataframe(result_df[result_df['Status'] == '✅ GELIJK'])
                
                # Optioneel: toon alle dubbele Dossiernr's (inclusief ongelijke)
                if st.checkbox("Toon alle dubbele Dossiernr's (ook met verschillende datums)"):
                    st.dataframe(result_df)
                
                # Download optie (CSV)
                csv = result_df.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button(
                    label="📥 Download resultaat (CSV)",
                    data=csv,
                    file_name='dubbele_dossiers.csv',
                    mime='text/csv'
                )
    
    except Exception as e:
        st.error(f"❌ Fout: {str(e)}")
else:
    st.info("📤 Upload een Excel-bestand om te beginnen")
