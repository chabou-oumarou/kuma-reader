import streamlit as st
import pandas as pd
import requests

# --- APP CONFIG ---
st.set_page_config(page_title="Kuma Lexicon - Online Edition", layout="wide")

# --- DATA LOADING (ONLINE VYGUS/DICTIONARY SOURCE) ---
@st.cache_data
def load_online_dictionary():
    # Fetching a processed version of the Vygus/Dickson/Faulkner dataset from a reliable repo
    # This dataset maps Gardiner codes, transliterations (MDC), and translations.
    url = "https://raw.githubusercontent.com/fayrose/MiddleEgyptianDataset/master/manual_data/manual_faulkner.csv"
    try:
        df = pd.read_csv(url)
        # Standardizing columns for the app logic
        df = df.rename(columns={
            'glyphs': 'glyph',
            'mdc': 'mdc',
            'transliteration': 'trans',
            'translation_en': 'en',
            'translation_fr': 'fr'
        })
        # If French translation is missing in the source, we default to English
        if 'fr' not in df.columns:
            df['fr'] = df['en']
        return df.fillna("")
    except Exception as e:
        st.error(f"Error loading online dictionary: {e}")
        return pd.DataFrame()

DICTIONARY_DF = load_online_dictionary()

# --- KUMA PHONOSEMANTIC ENGINE ---
KUMA_RULES = {
    "N": {"principle": "L'émergence (Nun)", "desc": "L'énergie de l'onde primordiale, la transmission de la vie."},
    "R": {"principle": "Le Verbe (Ra)", "desc": "L'ouverture, le rayonnement solaire, la parole qui crée."},
    "K": {"principle": "La Cohésion (Ka)", "desc": "L'esprit double, la force qui maintient la forme."},
    "M": {"principle": "La Matrice (Mut)", "desc": "Le milieu de transformation, le passage de l'esprit à la matière."},
    "B": {"principle": "L'Incarnation (Ba)", "desc": "Le mouvement de l'âme dans le réceptacle physique."},
    "H": {"principle": "Le Souffle (Heh)", "desc": "L'éternité, l'élément invisible qui anime le tout."},
    "S": {"principle": "La Causalité", "desc": "Le flux qui ordonne et dirige l'énergie."},
    "F": {"principle": "L'Expansion", "desc": "Le déploiement de la force dans l'espace."},
    "T": {"principle": "La Stabilité", "desc": "Le point d'ancrage, la manifestation terrestre."}
}

# --- UI LOGIC ---
if 'lang' not in st.session_state: st.session_state.lang = 'fr'
def swap_lang(): st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'

S = {
    "fr": {"search": "Recherche (MDC, Français, Glyphe)", "kuma": "ANALYSE KUMA (D. MBOCK)", "comp": "LEXIQUE NÉGRO-AFRICAIN", "details": "Détails Lexicographiques", "btn": "English 🇬🇧", "results": "Résultats :"},
    "en": {"search": "Search (MDC, English, Glyph)", "kuma": "KUMA ANALYSIS (D. MBOCK)", "comp": "NEGRO-AFRICAN LEXICON", "details": "Lexicographical Details", "btn": "Français 🇫🇷", "results": "Dictionary Results:"}
}[st.session_state.lang]

st.sidebar.button(S["btn"], on_click=swap_lang)
st.title("𓋹 Medu Neter: Kuma Lab")

# 1. SEARCH LOGIC
search_query = st.text_input(S["search"], placeholder="Ex: nfr, life, 𓋹 ...")

if not DICTIONARY_DF.empty:
    # Filter based on search query
    mask = (
        DICTIONARY_DF['mdc'].str.contains(search_query, case=False) |
        DICTIONARY_DF['en'].str.contains(search_query, case=False) |
        DICTIONARY_DF['glyph'].str.contains(search_query, case=False)
    )
    filtered_df = DICTIONARY_DF[mask].head(50) # Limit to 50 for performance

    if not filtered_df.empty:
        # Sidebar selection
        selection_labels = filtered_df.apply(lambda x: f"{x['glyph']} | {x['mdc']} | {x['en'][:30]}...", axis=1).tolist()
        selected_index = st.sidebar.radio(S["results"], range(len(selection_labels)), format_func=lambda x: selection_labels[x])
        
        data = filtered_df.iloc[selected_index]
        
        # 2. DYNAMIC DISPLAY
        col_vis, col_ana = st.columns([1, 2])
        
        with col_vis:
            st.markdown(f"""<div style='border:4px solid #d4af37; padding:20px; text-align:center; background:#111; border-radius:15px;'>
                        <h1 style='font-size:100px; color:#d4af37; margin:0;'>{data['glyph']}</h1>
                        <p style='color:#777;'>MDC: {data['mdc']}</p></div>""", unsafe_allow_html=True)
            st.write(f"**{S['details']}**")
            st.info(f"Transliteration: {data['trans']}\n\nTranslation: {data['fr' if st.session_state.lang == 'fr' else 'en']}")

        with col_ana:
            st.header(S["kuma"])
            # Kuma Logic: Decompose the MDC string
            clean_mdc = "".join(filter(str.isalpha, str(data['mdc'])))
            for char in clean_mdc.upper():
                if char in KUMA_RULES:
                    with st.expander(f"Radical '{char}' - {KUMA_RULES[char]['principle']}", expanded=True):
                        st.write(KUMA_RULES[char]['desc'])
            
            st.subheader(S["comp"])
            comp_df = pd.DataFrame({
                "Langue": ["Wolof", "Kikongo", "Bambara", "Yoruba", "Dogon"],
                "Terme Cognat": [f"Root-{data['mdc']}", "N-zila", "Da-kuma", "E-mi", "Ama"],
                "Contexte": ["Vibration vitale", "Flux de l'esprit", "Parole sacrée", "Respiration", "Origine"]
            })
            st.table(comp_df)
    else:
        st.warning("Aucun résultat trouvé.")
else:
    st.error("Impossible de charger la base de données en ligne.")

st.markdown("---")
st.write("📖 *'Le Medu Neter est le code génétique des langues africaines.'* — Dibombari Mbock")
