import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logistieke Analyse", layout="wide")

st.title("📦 Verzendgegevens Analyse")

# 1. Bestand uploaden
uploaded_file = st.file_uploader("Upload je Excel bestand", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Kolomnamen opschonen (spaties verwijderen)
    df.columns = df.columns.str.strip()
    
    required_columns = ['Verzending-ID', 'Type', 'Kg', 'LM']
    if all(col in df.columns for col in required_columns):
        
        # Groeperen en optellen
        df_grouped = df.groupby(['Verzending-ID', 'Type'], as_index=False).agg({
            'Kg': 'sum',
            'LM': 'sum'
        })

        if st.button("Voer Analyse Uit"):
            st.divider()
            
            # --- GEAALISEERDE ANALYSE 1 ---
            st.subheader("1. Afwijkingen tussen berekende en werkelijke LM")
            
            # We berekenen de theoretische LM op basis van gewicht
            df_grouped['Theoretische_LM'] = df_grouped['Kg'] / 1800
            
            # We berekenen het procentuele verschil ten opzichte van de ingegeven LM
            # Formule: |(Theoretisch - Werkelijk) / Werkelijk|
            df_grouped['Afwijking_Percentage'] = (
                (df_grouped['Theoretische_LM'] - df_grouped['LM']).abs() / df_grouped['LM']
            )

            # Filter: Toon alles waar de afwijking groter is dan 10% (0.10)
            resultaat_1 = df_grouped[df_grouped['Afwijking_Percentage'] > 0.10].copy()
            
            # Netjes formatteren voor weergave
            resultaat_1['Afwijking_Percentage'] = (resultaat_1['Afwijking_Percentage'] * 100).round(2).astype(str) + '%'
            
            if not resultaat_1.empty:
                st.write(f"Er zijn {len(resultaat_1)} zendingen gevonden met meer dan 10% afwijking:")
                st.dataframe(resultaat_1[['Verzending-ID', 'Type', 'Kg', 'LM', 'Theoretische_LM', 'Afwijking_Percentage']])
            else:
                st.success("Geen zendingen gevonden met een afwijking groter dan 10%.")

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
