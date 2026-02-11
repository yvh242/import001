import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logistieke Analyse", layout="wide")

st.title("📦 Verzendgegevens Analyse")

# 1. Bestand uploaden
uploaded_file = st.file_uploader("Upload je Excel bestand", type=['xlsx'])

if uploaded_file:
    # Inlezen van data
    df = pd.read_excel(uploaded_file)
    
    # Check of de nodige kolommen aanwezig zijn
    required_columns = ['Verzending-ID', 'Type', 'Kg', 'LM']
    if all(col in df.columns for col in required_columns):
        
        # STAP 1: Groeperen op ID en Type om dubbelen samen te tellen
        # We tellen Kg en LM op voor rijen met hetzelfde ID en Type
        df_grouped = df.groupby(['Verzending-ID', 'Type'], as_index=False).agg({
            'Kg': 'sum',
            'LM': 'sum'
        })
        
        st.success("Bestand succesvol verwerkt en dubbele rijen (ID+Type) samengevoegd.")

        if st.button("Voer Analyse Uit"):
            st.divider()
            
            # --- ANALYSE 1: Gewicht/1800 vs LM ---
            # Logica: (Kg / 1800) < (LM * 0.90)
            st.subheader("1. Zendingen met afwijkende Kg/LM verhouding")
            st.info("Zendingen waar (Totaal Gewicht / 1800) meer dan 10% kleiner is dan de opgegeven LM.")
            
            df_grouped['Berekende_LM'] = df_grouped['Kg'] / 1800
            mask_afwijking = df_grouped['Berekende_LM'] < (df_grouped['LM'] * 0.90)
            resultaat_1 = df_grouped[mask_afwijking].copy()
            
            if not resultaat_1.empty:
                st.dataframe(resultaat_1)
            else:
                st.write("Geen afwijkingen gevonden.")

            # --- ANALYSE 2: Dubbele Types per ID ---
            st.subheader("2. Zendingen met meerdere Types")
            st.info("Zendingen waar hetzelfde 'Verzending-ID' voorkomt bij 2 verschillende 'Types'.")
            
            # Tel hoe vaak een ID voorkomt in de gegroepeerde lijst
            id_counts = df_grouped['Verzending-ID'].value_counts()
            dubbele_ids = id_counts[id_counts >= 2].index
            
            resultaat_2 = df_grouped[df_grouped['Verzending-ID'].isin(dubbele_ids)]
            
            if not resultaat_2.empty:
                st.dataframe(resultaat_2.sort_values(by='Verzending-ID'))
            else:
                st.write("Geen zendingen gevonden met meerdere types.")
                
    else:
        st.error(f"Het bestand mist een van de volgende kolommen: {required_columns}")

else:
    st.info("Wacht op upload van Excel bestand...")
