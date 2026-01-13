import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Kuma Lexicon Web App", layout="wide", initial_sidebar_state="expanded")

# --- KUMA METHOD PHILOSOPHY DATA ---
# Rooted in Mbock's "Principes fondamentaux de la méthode Kuma"
KUMA_ROOTS = {
    "N": {"vibe": "Emergence / L'Eau Primordiale (Nun)", "logic": "Principe de transmission et de mouvement continu."},
    "R": {"vibe": "Le Verbe Créateur / Rayonnement", "logic": "Ouverture de la conscience et vibration solaire (Ra)."},
    "K": {"vibe": "Cohésion / L'Esprit (Ka)", "logic": "Principe de densification de l'énergie dans la forme."},
    "M": {"vibe": "Transformation / Matrice (Mut)", "logic": "Passage de l'invisible au visible; le milieu."},
    "B": {"vibe": "Incarnation / L'Âme (Ba)", "logic": "Déplacement de la force vitale dans le réceptacle."},
    "S": {"vibe": "Causalité / Fluidité", "logic": "Le principe qui ordonne le chaos en flux."},
    "H": {"vibe": "Souffle / Vie (Heh)", "logic": "L'élément impalpable qui anime la structure."},
    "X": {"vibe": "Friction / Chaleur", "logic": "Le point de contact entre deux forces opposées."}
}

# --- DICTIONARY DATA SOURCE ---
# This structure is designed to hold data from Vygus, Faulkner, and Gardiner.
# For a live app, this list should be imported from a .csv or .json file.
DICTIONARY_DB = [
    {"glyph": "𓈖", "mdc": "n", "trans": "n", "en": "of, to", "fr": "de, à", "gardiner": "N35", "origin": "Vygus p.1520"},
    {"glyph": "𓂋", "mdc": "r", "trans": "r", "en": "mouth, speech", "fr": "bouche, parole", "gardiner": "D21", "origin": "Faulkner p.151"},
    {"glyph": "𓋹", "mdc": "anx", "trans": "ꜥnḫ", "en": "life, breath", "fr": "vie, souffle", "gardiner": "S34", "origin": "Gardiner p.508"},
    {"glyph": "𓄤", "mdc": "nfr", "trans": "nfr", "en": "beautiful, good", "fr": "beau, parfait", "gardiner": "F35", "origin": "Vygus p.1242"},
    {"glyph": "𓀭", "mdc": "ntr", "trans": "ntr", "en": "divine, power", "fr": "divin, force", "gardiner": "R8", "origin": "Faulkner p.141"},
    {"glyph": "𓃀", "mdc": "b", "trans": "b", "en": "foot, place", "fr": "pied, lieu", "gardiner": "D58", "origin": "Vygus p.450"},
    {"glyph": "𓏠", "mdc": "mn", "trans": "mn", "en": "stable, remain", "fr": "stable, demeurer", "gardiner": "Y1", "origin": "Faulkner p.106"},
    {"glyph": "𓇳", "mdc": "ra", "trans": "rꜥ", "en": "sun, creator", "fr": "soleil, créateur", "gardiner": "N5", "origin": "Gardiner p.485"},
    {"glyph": "𓂓", "mdc": "ka", "trans": "kꜣ", "en": "spirit, double", "fr": "esprit, double", "gardiner": "D28", "origin": "Vygus p.1100"},
]

# --- UI TRANSLATION ---
STRINGS = {
    "fr": {
        "nav": "Navigation Lexicale",
        "search_hint": "Recherche par MDC, Fr, En ou Hiéroglyphe",
        "kuma_sec": "ANALYSE MÉTHODE KUMA",
        "comp_sec": "COMPARAISON NÉGRO-AFRICAINE (SOUDANAIS)",
        "logic": "Logique Cosmogonique",
        "vibe": "Vibration",
        "details": "Détails Lexicographiques",
        "lang_switch": "Switch to English 🇬🇧"
    },
    "en": {
        "nav": "Lexical Navigation",
        "search_hint": "Search by MDC, Fr, En or Hieroglyph",
        "kuma_sec": "KUMA METHOD ANALYSIS",
        "comp_sec": "NEGRO-AFRICAN COMPARISON (SUDANESE)",
        "logic": "Cosmogonic Logic",
        "vibe": "Vibration",
        "details": "Lexicographical Details",
        "lang_switch": "Passer au Français 🇫🇷"
    }
}

# --- SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = 'fr'
def toggle_lang(): st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'

S = STRINGS[st.session_state.lang]

# --- SIDEBAR & SEARCH ---
with st.sidebar:
    st.button(S["lang_switch"], on_click=toggle_lang)
    st.header(S["nav"])
    
    # Dynamic Search Bar
    search_query = st.text_input(S["search_hint"], placeholder="Ex: nfr, 𓈖, life...")
    
    # Full Dictionary List (Filtered by Search)
    full_list = [f"{d['glyph']} | {d['mdc']} | {d['fr'] if st.session_state.lang == 'fr' else d['en']}" for d in DICTIONARY_DB]
    filtered_list = [item for item in full_list if search_query.lower() in item.lower()]
    
    selected_item = st.radio("Dictionnaire Complet :", filtered_list if filtered_list else ["Aucun résultat"])

# --- MAIN DISPLAY ---
st.title("𓋹 Kemet Lexicon Pro")
st.markdown("---")

if selected_item and selected_item != "Aucun résultat":
    # Extract data from selection
    glyph_symbol = selected_item.split(" | ")[0]
    data = next(d for d in DICTIONARY_DB if d["glyph"] == glyph_symbol)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Hieroglyph Drawing Box
        st.markdown(f"""
            <div style="background-color:#1a1a1a; border:3px solid #d4af37; border-radius:15px; padding:30px; text-align:center;">
                <h1 style="font-size:180px; color:#d4af37; margin:0;">{data['glyph']}</h1>
                <p style="color:#888;">MDC: {data['mdc']} | {data['gardiner']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader(S["details"])
        st.write(f"**Transliteration:** {data['trans']}")
        st.write(f"**Source:** {data['origin']}")

    with col2:
        # Kuma Method Deep Analysis
        st.header(S["kuma_sec"])
        st.caption("Basé sur les travaux de Dibombari Mbock")
        
        # Vibratory Breakdown
        mdc_upper = data['mdc'].upper()
        for char in mdc_upper:
            if char in KUMA_ROOTS:
                with st.expander(f"Vibration du radical '{char}'", expanded=True):
                    st.write(f"**{S['vibe']}:** {KUMA_ROOTS[char]['vibe']}")
                    st.write(f"**{S['logic']}:** {KUMA_ROOTS[char]['logic']}")
        
        # Comparative Table (Focus on Sub-Saharan/Sudanese languages)
        st.header(S["comp_sec"])
        # Sample comparative data inspired by Kemlex logic
        comparative_data = {
            "Langue": ["Wolof", "Kikongo", "Dogon", "Bambara", "Yoruba", "Zulu", "Pulaar", "Sereer", "Mende", "Dinka"],
            "Cognat": [f"R-{data['mdc']}", "N-zila", "Ama-tu", "Da-kuma", "E-mi", "In-yoni", "Lob-bo", "O-ref", "Ng-eya", "Ran"],
            "Signification": [data['fr'] if st.session_state.lang == 'fr' else data['en']] * 10
        }
        st.table(pd.DataFrame(comparative_data))

else:
    st.info("Utilisez la barre de recherche ou la liste à gauche pour explorer le dictionnaire.")

st.markdown("---")
st.markdown("### Méthodologie Kuma :")
st.write("> *'La langue n'est pas un outil de communication, c'est un outil de connexion aux lois de l'univers.'* — Dibombari Mbock")
