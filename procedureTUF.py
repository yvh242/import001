import streamlit as st
from googletrans import Translator
from PIL import Image

# Initialiseer de vertaler
translator = Translator()

st.set_page_config(page_title="Transuniverse Vertaler", layout="wide")

# Titel en originele afbeelding
st.title("🚚 Logistieke Proces Vertaler")

# Afbeelding inladen en tonen
try:
    image = Image.open('tijdlijn.png')
    st.image(image, caption='Originele Werkinstructie', use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ Plaats 'tijdlijn.png' in de map om de afbeelding hier te zien.")

st.divider()

# Sidebar voor instellingen
st.sidebar.header("Taalinstellingen")
target_lang = st.sidebar.selectbox(
    "Vertaal naar:",
    ["en", "fr", "de", "es", "pl", "ro", "tr"],
    format_func=lambda x: {"en": "Engels", "fr": "Frans", "de": "Duits", "es": "Spaans", "pl": "Pools", "ro": "Roemeens", "tr": "Turks"}[x]
)

# De data (gebaseerd op jouw afbeelding)
stappen = {
    "Titel": "Aankomst na de rit op Transuniverse",
    "Stap 1": {"titel": "Riemen losmaken", "tekst": "Riemen losmaken indien nodig"},
    "Stap 2": {"titel": "CMR's afgeven", "tekst": "Alle CMR's (exemplaar 3 voor leveringen, exemplaar 2 voor afhalingen) afgeven aan Handling"},
    "Stap 3": {"titel": "Afmelden op computer", "tekst": "Afmelden op computer aan de hand van rit nummer (=I nummer)"}
}

def vertaal(tekst):
    return translator.translate(tekst, dest=target_lang).text

if st.sidebar.button("Genereer Vertaling"):
    vertaalde_titel = vertaal(stappen["Titel"])
    st.markdown(f"<h2 style='text-align: center;'>📍 {vertaalde_titel}</h2>", unsafe_allow_width=True)
    
    # Gebruik kolommen voor de visuele weergave
    c1, c2, c3 = st.columns(3)

    with c1:
        # Blauwe styling voor stap 1
        st.markdown(f"""
        <div style="background-color: #e8f0fe; padding: 20px; border-radius: 10px; border-left: 5px solid #4285f4; min-height: 250px;">
            <h3 style="color: #4285f4;">1. {vertaal(stappen["Stap 1"]["titel"])}</h3>
            <p>{vertaal(stappen["Stap 1"]["tekst"])}</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Groene styling voor stap 2
        st.markdown(f"""
        <div style="background-color: #e6f4ea; padding: 20px; border-radius: 10px; border-left: 5px solid #34a853; min-height: 250px;">
            <h3 style="color: #34a853;">2. {vertaal(stappen["Stap 2"]["titel"])}</h3>
            <p>{vertaal(stappen["Stap 2"]["tekst"])}</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        # Gele/Oranje styling voor stap 3
        st.markdown(f"""
        <div style="background-color: #fef7e0; padding: 20px; border-radius: 10px; border-left: 5px solid #fbbc04; min-height: 250px;">
            <h3 style="color: #fbbc04;">3. {vertaal(stappen["Stap 3"]["titel"])}</h3>
            <p>{vertaal(stappen["Stap 3"]["tekst"])}</p>
        </div>
        """, unsafe_allow_html=True)
