import streamlit as st
import pandas as pd

st.title('🔍 Rittenvergelijking: OK / NIET OK')

# Bestand 1 uploaden
st.subheader("Upload Hoofdbestand (te controleren ritten)")
uploaded_file1 = st.file_uploader("Kies bestand 1", type=['xlsx', 'xls'], key="file1")

# Bestand 2 uploaden
st.subheader("Upload Referentiebestand (vergelijkingsdata)")
uploaded_file2 = st.file_uploader("Kies bestand 2", type=['xlsx', 'xls'], key="file2")

if uploaded_file1 is not None and uploaded_file2 is not None:
    try:
        # Lees beide Excel-bestanden
        df1 = pd.read_excel(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2)

        # Controleer of de benodigde kolommen bestaan
        required_columns = ['Ritdatum', 'Ritnr.', 'Chauffeur naam']
        if not all(col in df1.columns for col in required_columns):
            st.error("❌ Bestand 1 moet 'Ritdatum', 'Ritnr' en 'Chauffeur naam' bevatten!")
        elif not all(col in df2.columns for col in ['Ritdatum', 'Ritnr.']):  # Chauffeur naam niet verplicht in bestand 2
            st.error("❌ Bestand 2 moet minstens 'Ritdatum' en 'Ritnr' bevatten!")
        else:
            # Zet 'Ritdatum' om naar datum (voor consistente vergelijking)
            df1['Ritdatum'] = pd.to_datetime(df1['Ritdatum']).dt.date
            df2['Ritdatum'] = pd.to_datetime(df2['Ritdatum']).dt.date

            # Maak een sleutelkolom voor matching
            df1['Match_key'] = df1['Ritdatum'].astype(str) + "_" + df1['Ritnr.'].astype(str)
            df2['Match_key'] = df2['Ritdatum'].astype(str) + "_" + df2['Ritnr.'].astype(str)

            # Voeg statuskolom toe
            df1['Status'] = df1['Match_key'].isin(df2['Match_key']).map({True: '✅ OK', False: '❌ NIET OK'})

            # Selecteer alleen de gewenste kolommen voor output
            output_columns = ['Ritdatum', 'Ritnr', 'Chauffeur naam', 'Status']
            result_df = df1[output_columns]

            # Toon het resultaat
            st.success("✅ Vergelijking voltooid!")
            st.dataframe(result_df)

            # Download optie
            csv = result_df.to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                label="📥 Download resultaat (CSV)",
                data=csv,
                file_name='ritten_status.csv',
                mime='text/csv'
            )

    except Exception as e:
        st.error(f"❌ Fout: {str(e)}")
elif uploaded_file1 is not None or uploaded_file2 is not None:
    st.warning("⚠ Upload beide bestanden om te vergelijken!")
else:
    st.info("📤 Upload twee Excel-bestanden om te beginnen")
