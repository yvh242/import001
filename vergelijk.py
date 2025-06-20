import streamlit as st
import pandas as pd

st.title('🔗 Rittenvergelijking tussen twee Excel-bestanden')

# Bestand 1 uploaden
st.subheader("Upload Eerste Excel-bestand (Hoofdbestand)")
uploaded_file1 = st.file_uploader("Kies bestand 1", type=['xlsx', 'xls'], key="file1")

# Bestand 2 uploaden
st.subheader("Upload Tweede Excel-bestand (Vergelijkingsbestand)")
uploaded_file2 = st.file_uploader("Kies bestand 2", type=['xlsx', 'xls'], key="file2")

if uploaded_file1 is not None and uploaded_file2 is not None:
    try:
        # Lees beide Excel-bestanden
        df1 = pd.read_excel(uploaded_file1)
        df2 = pd.read_excel(uploaded_file2)

        # Controleer of de benodigde kolommen bestaan
        required_columns = ['Ritdatum', 'Ritnr.']
        if not all(col in df1.columns for col in required_columns):
            st.error("❌ Bestand 1 moet 'Ritdatum' en 'Ritnr.' bevatten!")
        elif not all(col in df2.columns for col in required_columns):
            st.error("❌ Bestand 2 moet 'Ritdatum' en 'Ritnr.' bevatten!")
        else:
            # Zet 'Ritdatum' om naar datum (voor consistente vergelijking)
            df1['Ritdatum'] = pd.to_datetime(df1['Ritdatum']).dt.date
            df2['Ritdatum'] = pd.to_datetime(df2['Ritdatum']).dt.date

            # Maak een sleutelkolom voor matching
            df1['Match_key'] = df1['Ritdatum'].astype(str) + "_" + df1['Ritnr.'].astype(str)
            df2['Match_key'] = df2['Ritdatum'].astype(str) + "_" + df2['Ritnr.'].astype(str)

            # Voeg een kolom toe aan df1 die aangeeft of de rit in df2 voorkomt
            df1['Bestand 2 Match'] = df1['Match_key'].isin(df2['Match_key']).map({True: '✅ GEVONDEN', False: '❌ NO DATA'})

            # Toon het resultaat
            st.success("✅ Bestanden succesvol vergeleken!")
            st.dataframe(df1)

            # Download optie
            csv = df1.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download resultaat als CSV",
                data=csv,
                file_name='vergeleken_ritten.csv',
                mime='text/csv'
            )

    except Exception as e:
        st.error(f"❌ Fout: {e}")
elif uploaded_file1 is not None or uploaded_file2 is not None:
    st.warning("⚠ Upload beide bestanden om te vergelijken!")
else:
    st.info("📤 Upload twee Excel-bestanden om te beginnen")
