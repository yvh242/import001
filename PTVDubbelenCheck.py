import streamlit as st
import pandas as pd

st.set_page_config(page_title="Logistieke Analyse v3", layout="wide")

st.title("📦 Verzendgegevens Analyse")

# --- SIDEBAR VOOR INSTELLINGEN ---
st.sidebar.header("Instellingen Filters")

# 1. Percentage drempel
marge_percentage = st.sidebar.slider(
    "1. Minimale afwijking in %", 
    min_value=0, 
    max_value=100, 
    value=10,
    help="Hoeveel procent moet het berekende gewicht boven de LM liggen?"
)

# 2. Absolute drempel (Vaste drempel)
min_lm_verschil = st.sidebar.slider(
    "2. Minimale afwijking in Laadmeter (Vaste drempel)", 
    min_value=0.0, 
    max_value=2.0, 
    value=0.2, 
    step=0.05,
    help="De zending wordt pas getoond als het verschil groter is dan dit aantal meters (bijv. 0.2 LM)."
)

# Berekening factoren
factor = 1 + (marge_percentage / 100)

# --- BESTAND UPLOADEN ---
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
            
            # --- ANALYSE 1: De gecombineerde filter ---
            st.subheader(f"1. Te zware zendingen (> {marge_percentage}% én > {min_lm_verschil} LM afwijking)")
            
            # Bereken de theoretische LM (1800kg per meter)
            df_grouped['Theoretische_LM'] = (df_grouped['Kg'] / 1800).round(2)
            df_grouped['Verschil_LM'] = (df_grouped['Theoretische_LM'] - df_grouped['LM']).round(2)
            
            # FILTER LOGICA:
            # A: Meer dan X procent zwaarder
            # B: Meer dan X laadmeter verschil
            mask_percentage = df_grouped['Theoretische_LM'] > (df_grouped['LM'] * factor)
            mask_fixed = df_grouped['Verschil_LM'] > min_lm_verschil
            
            resultaat_1 = df_grouped[mask_percentage & mask_fixed].copy()
            
            if not resultaat_1.empty:
                st.warning(f"Gevonden: {len(resultaat_1)} zendingen die beide drempels overschrijden.")
                st.dataframe(resultaat_1[['Verzending-ID', 'Type', 'Kg', 'LM', 'Theoretische_LM', 'Verschil_LM']])
            else:
                st.success("Geen zendingen gevonden die aan beide criteria voldoen.")

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
        st.error(f"Kolommen ontbreken. Nodig: {required_columns}")
else:
    st.info("Upload een Excel bestand om te beginnen.")
