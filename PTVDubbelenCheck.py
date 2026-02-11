import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logistieke Analyse v2", layout="wide")

st.title("📦 Verzendgegevens Analyse")

# --- SIDEBAR VOOR INSTELLINGEN ---
st.sidebar.header("Instellingen")
# Gebruiker kan percentage kiezen, standaard 10%
marge_percentage = st.sidebar.slider(
    "Selecteer de marge voor afwijking (%)", 
    min_value=0, 
    max_value=100, 
    value=10,
    step=1
)

factor = 1 + (marge_percentage / 100)

# --- BESTAND UPLOADEN ---
uploaded_file = st.file_uploader("Upload je Excel bestand", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip() # Spaties uit kolomnamen halen
    
    required_columns = ['Verzending-ID', 'Type', 'Kg', 'LM']
    if all(col in df.columns for col in required_columns):
        
        # Stap 1: Groeperen en optellen voor identieke ID + Type
        df_grouped = df.groupby(['Verzending-ID', 'Type'], as_index=False).agg({
            'Kg': 'sum',
            'LM': 'sum'
        })

        if st.button("Voer Analyse Uit"):
            st.divider()
            
            # --- ANALYSE 1: Theoretisch HOGER dan LM (met variabele marge) ---
            st.subheader(f"1. Zware zendingen (Theoretische LM > {marge_percentage}% boven LM)")
            
            # Bereken de theoretische LM (1800kg per meter)
            df_grouped['Theoretische_LM'] = df_grouped['Kg'] / 1800
            
            # FILTER: Theoretische_LM > (LM * factor)
            mask_te_zwaar = df_grouped['Theoretische_LM'] > (df_grouped['LM'] * factor)
            
            resultaat_1 = df_grouped[mask_te_zwaar].copy()
            
            if not resultaat_1.empty:
                st.warning(f"Gevonden: {len(resultaat_1)} zendingen die de drempel van {marge_percentage}% overschrijden.")
                # We voegen een kolom toe die toont hoeveel % het gewicht te hoog is
                resultaat_1['Verschil_%'] = (((resultaat_1['Theoretische_LM'] / resultaat_1['LM']) - 1) * 100).round(1)
                st.dataframe(resultaat_1[['Verzending-ID', 'Type', 'Kg', 'LM', 'Theoretische_LM', 'Verschil_%']])
            else:
                st.success(f"Geen zendingen gevonden die meer dan {marge_percentage}% te zwaar zijn.")

            # --- ANALYSE 2: Dubbele Types ---
            st.subheader("2. Zendingen met 2 verschillende Types")
            counts = df_grouped['Verzending-ID'].value_counts()
            dubbele_ids = counts[counts >= 2].index
            resultaat_2 = df_grouped[df_grouped['Verzending-ID'].isin(dubbele_ids)]
            
            if not resultaat_2.empty:
                st.dataframe(resultaat_2.sort_values(by='Verzending-ID'))
            else:
                st.info("Geen zendingen met meerdere types gevonden.")
                
    else:
        st.error(f"Bestand mist kolommen: {set(required_columns) - set(df.columns)}")

else:
    st.info("Upload een bestand om de analyse te starten.")
