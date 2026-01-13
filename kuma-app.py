import streamlit as st
import pandas as pd
import requests
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="Kuma Lexicon - Online Edition", layout="wide")

# --- CHARGEMENT DES DONNÉES (SOURCE EN LIGNE FIABLE) ---
@st.cache_data
def load_data():
    # Source alternative : Lexique du projet Ramses (Open Access)
    # Si cette URL change, le bloc 'except' chargera vos données par défaut.
    URL_ONLINE = "https://raw.githubusercontent.com/josmorduc/JSesh/master/jsesh-utils/src/main/resources/org/qenherkhopeshef/jsesh/utils/signs.csv"
    
    # Données de secours (vos échantillons originaux)
    LOCAL_BACKUP = [
        {"glyph": "𓈖", "mdc": "n", "trans": "n", "en": "of, to", "fr": "de, à", "gardiner": "N35"},
        {"glyph": "𓂋", "mdc": "r", "trans": "r", "en": "mouth", "fr": "bouche, parole", "gardiner": "D21"},
        {"glyph": "𓋹", "mdc": "anx", "trans": "ankh", "en": "life", "fr": "vie, souffle", "gardiner": "S34"},
        {"glyph": "𓄤", "mdc": "nfr", "trans": "nefer", "en": "beautiful", "fr": "perfection", "gardiner": "F35"}
    ]

    try:
        # Tentative de récupération en ligne
        response = requests.get(URL_ONLINE, timeout=5)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            # Adaptation simple des colonnes selon la source
            return df.rename(columns={'sign': 'glyph', 'code': 'gardiner'})
        else:
            return pd.DataFrame(LOCAL_BACKUP)
    except Exception:
        return pd.DataFrame(LOCAL_BACKUP)

DICTIONARY_DF = load_data()

# --- MOTEUR KUMA (D. MBOCK) ---
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

# --- INTERFACE ---
st.title("𓋹 Medu Neter : Kuma Lab")
search = st.text_input("Rechercher un glyphe ou un code (ex: n, anx, N35)...")

if not DICTIONARY_DF.empty:
    # Filtrage de la base
    results = DICTIONARY_DF[
        DICTIONARY_DF['mdc'].str.contains(search, na=False, case=False) | 
        DICTIONARY_DF['gardiner'].str.contains(search, na=False, case=False)
    ].head(20)

    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"{row['glyph']} - {row['mdc']} ({row.get('en', 'Traduction')})"):
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"<h1 style='font-size:80px;'>{row['glyph']}</h1>", unsafe_allow_html=True)
                with c2:
                    st.write(f"**Code Gardiner :** {row['gardiner']}")
                    # Analyse KUMA
                    st.subheader("Analyse Kuma")
                    for char in str(row['mdc']).upper():
                        if char in KUMA_RULES:
                            st.write(f"**{char}** : {KUMA_RULES[char]['principle']}")
    else:
        st.info("Aucun glyphe trouvé pour cette recherche.")
