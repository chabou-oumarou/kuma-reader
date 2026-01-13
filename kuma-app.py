import streamlit as st
import pandas as pd

# --- TRANSLATION DICTIONARY ---
LANG_DATA = {
    "en": {
        "title": "𓋹 Kemet Lexicon & Kuma Analysis",
        "search_label": "Choose a Word from the Combined Dictionaries:",
        "search_placeholder": "Select a hieroglyph...",
        "kuma_header": "✨ Kuma Method Analysis (Dibombari Mbock)",
        "comparative_header": "🌍 Sub-Saharan / Sudanese Comparative Table",
        "details_label": "Philological Details",
        "source_label": "Academic Sources",
        "lang_btn": "Version Française 🇫🇷",
        "col_lang": "Language",
        "col_term": "Cognate/Term",
        "col_meaning": "Contextual Meaning"
    },
    "fr": {
        "title": "𓋹 Lexique Kemet & Analyse Kuma",
        "search_label": "Choisissez un mot dans les dictionnaires combinés :",
        "search_placeholder": "Sélectionnez un hiéroglyphe...",
        "kuma_header": "✨ Analyse Méthode Kuma (Dibombari Mbock)",
        "comparative_header": "🌍 Table Comparative (Langues Soudanaises / Négro-Africaines)",
        "details_label": "Détails Philologiques",
        "source_label": "Sources Académiques",
        "lang_btn": "English Version 🇬🇧",
        "col_lang": "Langue",
        "col_term": "Terme Cognat",
        "col_meaning": "Signification Contextuelle"
    }
}

# --- EXTENDED DATASET (Vygus, Faulkner, Gardiner + Kuma + African Lexics) ---
DICTIONARY_DB = [
    {
        "hieroglyph": "𓄤",
        "transliteration": "nfr",
        "translation_en": "good, beautiful, perfect",
        "translation_fr": "bon, beau, parfait",
        "gardiner": "F35",
        "kuma_analysis_en": "The 'NFR' root represents the heart and windpipe. In Kuma logic, 'N' is the energy of emergence and 'FR' is the vibration of expansion. It signifies the vital breath reaching harmony with the heart.",
        "kuma_analysis_fr": "La racine 'NFR' représente le cœur et la trachée. En logique Kuma, 'N' est l'énergie d'émergence et 'FR' est la vibration d'expansion. Signifie le souffle vital atteignant l'harmonie avec le cœur.",
        "african_cognates": [
            {"lang": "Wolof", "term": "Rafet", "meaning": "Beautiful / Beau"},
            {"lang": "Dagara", "term": "Vla", "meaning": "Good / Bon"},
            {"lang": "Kikongo", "term": "Mpila", "meaning": "Quality / Qualité"},
            {"lang": "Yoruba", "term": "Dara", "meaning": "Good / Bien"},
            {"lang": "Zulu", "term": "Fanele", "meaning": "Appropriate / Convenable"},
            {"lang": "Bambara", "term": "Nyie", "meaning": "Beauty / Beauté"},
            {"lang": "Lingala", "term": "Kitoko", "meaning": "Beautiful / Joli"},
            {"lang": "Pulaar", "term": "Lobbo", "meaning": "Good / Bon"},
            {"lang": "Mende", "term": "Nyalî", "meaning": "Beautiful / Beau"},
            {"lang": "Hausa", "term": "Nagari", "meaning": "Good / Bon"}
        ],
        "sources": "Vygus (p.1242), Faulkner (p.131), Mbock (Method Kuma)"
    },
    {
        "hieroglyph": "𓂋",
        "transliteration": "r",
        "translation_en": "mouth, speech, door",
        "translation_fr": "bouche, parole, porte",
        "gardiner": "D21",
        "kuma_analysis_en": "Symbolizes the solar opening. The 'R' vibration in Kuma is the principle of 'Ra' - the word that creates reality through the opening of the void.",
        "kuma_analysis_fr": "Symbolise l'ouverture solaire. La vibration 'R' en Kuma est le principe de 'Ra' - la parole qui crée la réalité par l'ouverture du vide.",
        "african_cognates": [
            {"lang": "Wolof", "term": "Rami", "meaning": "To speak / Parler"},
            {"lang": "Dogon", "term": "Ra", "meaning": "Sun / Soleil"},
            {"lang": "Kikongo", "term": "Ri", "meaning": "Sound / Son"},
            {"lang": "Bambara", "term": "Da", "meaning": "Mouth/Door / Bouche/Porte"}
        ],
        "sources": "Gardiner (p.450), Mbock (Kuma Principle)"
    }
]

# --- APP LOGIC ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

def toggle_lang():
    st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'

L = LANG_DATA[st.session_state.lang]

# Sidebar with language switch
st.sidebar.button(L["lang_btn"], on_click=toggle_lang)
st.sidebar.markdown("---")
st.sidebar.write("Dictionaries: Vygus, Faulkner, Gardiner")

# UI Header
st.title(L["title"])

# 1. Full Dropdown List
options = {f"{d['hieroglyph']} - {d['transliteration']} ({d['translation_fr'] if st.session_state.lang == 'fr' else d['translation_en']})": d for d in DICTIONARY_DB}
selected_label = st.selectbox(L["search_label"], options=list(options.keys()), index=0)

if selected_label:
    data = options[selected_label]
    
    # 2. Dynamic UI: Display only related data
    st.divider()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Drawing the hieroglyph word
        st.markdown(f"<div style='background-color: #f0ede4; border-radius: 15px; padding: 20px; text-align: center; border: 2px solid #d4af37;'>"
                    f"<h1 style='font-size: 120px; color: #1a1a1a; margin: 0;'>{data['hieroglyph']}</h1>"
                    f"<p style='color: #888;'>Gardiner: {data['gardiner']}</p></div>", unsafe_allow_html=True)
        
        st.write(f"**{L['details_label']}**")
        st.write(f"Transliteration: `{data['transliteration']}`")
        st.write(f"Source: *{data['sources']}*")

    with col2:
        # 3. Kuma Method Analysis
        st.subheader(L["kuma_header"])
        analysis = data['kuma_analysis_fr'] if st.session_state.lang == 'fr' else data['kuma_analysis_en']
        st.markdown(f"> {analysis}")
        
        # 4. Comparative African Lexic Table
        st.subheader(L["comparative_header"])
        comp_df = pd.DataFrame(data['african_cognates'])
        comp_df.columns = [L["col_lang"], L["col_term"], L["col_meaning"]]
        st.table(comp_df)

st.markdown("---")
st.caption("Application interactive basée sur les travaux de Dibombari Mbock et la lexicographie africaine.")
