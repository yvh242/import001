import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logistieke Analyse", layout="wide")

st.title("📦 Verzendgegevens Analyse")

# 1. Bestand uploaden
uploaded_file = st.file_uploader("Upload je Excel bestand", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    
    required_columns = ['Verzending-ID', 'Type', 'Kg', 'LM']
    if all(col in df.columns for col in required_columns):
        
        # Stap 1: Groeperen en optellen
        df_grouped = df.groupby(['Verzending-ID', 'Type'], as_index=False).agg({
            'Kg': 'sum',
            'LM': 'sum'
        })

        if st.button("Voer Analyse Uit"):
            st.divider()
            
            # --- GEAALISEERDE ANALYSE 1: Theoretisch HOGER dan LM ---
            st.subheader("1. Zware zendingen (Gewicht > LM + 10%)")
            
            # Bereken de theoretische LM op basis van 1800kg per meter
            df_grouped['Theoretische_LM'] = df_grouped['Kg'] / 1800
            
            # FILTER: Toon alleen als de Theoretische_LM meer dan 10% HOGER is dan de LM
            # Dus: Theoretische_LM > (LM * 1.10)
            mask_te_zwaar = df_grouped['Theoretische_LM'] > (df_grouped['LM'] * 1.10)
            
            resultaat_1 = df_grouped[mask_te_zwaar].copy()
            
            if not resultaat_1.empty:
                st.error(f"Gevonden: {len(resultaat_1)} zendingen die zwaarder zijn dan de gereserveerde laadmeters.")
                st.dataframe(resultaat_1[['Verzending-ID', 'Type', 'Kg', 'LM', 'Theoretische_LM']])
            else:
                st.success("Geen zendingen gevonden die te zwaar zijn voor de opgegeven LM.")

            # --- ANALYSE 2: Dubbele Types ---
            st.subheader("2. Zendingen met 2 verschillende Types")
            counts = df_grouped['Verzending-ID'].value_counts()
            dubbele_ids = counts[counts >= 2].index
            resultaat_2 = df_grouped[df_grouped['Verzending-ID'].isin(dubbele_ids)]
            
            if not resultaat_2.empty:
                st.dataframe(resultaat_2.sort_values(by='Verzending-ID'))

            
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
