import streamlit as st
import pandas as pd
import requests
import io

# --- APP CONFIG ---
st.set_page_config(page_title="Kuma Lexicon - Online Edition", layout="wide")

# --- KUMA PHONOSEMANTIC ENGINE (Dibombari Mbock) ---
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

# --- ONLINE DICTIONARY LOADER ---
@st.cache_data
def load_online_data():
    # Source: JSesh/Ramses Project open-access sign list
    url = "https://raw.githubusercontent.com/josmorduc/JSesh/master/jsesh-utils/src/main/resources/org/qenherkhopeshef/jsesh/utils/signs.csv"
    try:
        response = requests.get(url)
        df = pd.read_csv(io.StringIO(response.text))
        # Standardize columns to match your existing UI logic
        df = df.rename(columns={'sign': 'glyph', 'code': 'gardiner', 'tag': 'en'})
        df['fr'] = df['en'] # Wikipedia/Online sources often default to English
        df['trans'] = df['mdc']
        df['source'] = "Online Ramses/JSesh Database"
        return df.fillna("?")
    except:
        # Fallback to a tiny sample if offline
        return pd.DataFrame([{"glyph": "𓋹", "mdc": "anx", "trans": "ankh", "en": "life", "fr": "vie", "gardiner": "S34", "source": "Fallback"}])

DICTIONARY_DF = load_online_data()

# --- UI LOGIC ---
if 'lang' not in st.session_state: st.session_state.lang = 'fr'
def swap_lang(): st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'

S = {"fr": {"search": "Recherche (MDC, Français, Glyphe)", "kuma": "ANALYSE KUMA (D. MBOCK)", "comp": "LEXIQUE NÉGRO-AFRICAIN", "details": "Détails Lexicographiques", "btn": "English 🇬🇧"},
     "en": {"search": "Search (MDC, English, Glyph)", "kuma": "KUMA ANALYSIS (D. MBOCK)", "comp": "NEGRO-AFRICAN LEXICON", "details": "Lexicographical Details", "btn": "Français 🇫🇷"}}[st.session_state.lang]

st.sidebar.button(S["btn"], on_click=swap_lang)
st.title("𓋹 Medu Neter: Kuma Lab")

# 1. SEARCH LOGIC
search_query = st.text_input(S["search"], placeholder="Ex: nfr, 𓋹, life...")

# Filtering the DataFrame
mask = (DICTIONARY_DF['mdc'].str.contains(search_query, case=False, na=False) | 
        DICTIONARY_DF['en'].str.contains(search_query, case=False, na=False) |
        DICTIONARY_DF['glyph'].str.contains(search_query, na=False))
filtered_df = DICTIONARY_DF[mask].head(25) # Limit to 25 for selection clarity

if not filtered_df.empty:
    labels = filtered_df.apply(lambda x: f"{x['glyph']} | {x['mdc']} | {x['fr'] if st.session_state.lang == 'fr' else x['en']}", axis=1).tolist()
    selected_label = st.sidebar.radio("Résultats du dictionnaire :", labels)
    
    # Get the specific row
    data = filtered_df[filtered_df.apply(lambda x: f"{x['glyph']} | {x['mdc']} | {x['fr'] if st.session_state.lang == 'fr' else x['en']}" == selected_label, axis=1)].iloc[0]
    
    col_vis, col_ana = st.columns([1, 2])
    
    with col_vis:
        st.markdown(f"<div style='border:4px solid #d4af37; padding:20px; text-align:center; background:#111; border-radius:15px;'>"
                    f"<h1 style='font-size:180px; color:#d4af37; margin:0;'>{data['glyph']}</h1>"
                    f"<p style='color:#777;'>Gardiner: {data['gardiner']}</p></div>", unsafe_allow_html=True)
        st.write(f"**{S['details']}**")
        st.info(f"Transliteration: {data['trans']}\n\nSource: {data['source']}")

    with col_ana:
        st.header(S["kuma"])
        # Kuma Logic: Decompose the MDC string
        for char in str(data['mdc']).upper():
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
    st.warning("Aucun résultat trouvé dans la base de données en ligne.")

st.markdown("---")
st.write("📖 *'Le Medu Neter est le code génétique des langues africaines.'* — Dibombari Mbock")
