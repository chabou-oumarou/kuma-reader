import streamlit as st
import pandas as pd

# Page Setup
st.set_page_config(page_title="Kuma Method Reader - Manden Edition", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfaf3; }
    .kuma-card {
        padding: 25px;
        background-color: #ffffff;
        border-top: 5px solid #d4af37;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-radius: 8px;
    }
    .manden-badge {
        background-color: #4a2c2a;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Multilingual Translation Dict ---
T = {
    "en": {
        "title": "Kuma Method: Manden & Dogon Cosmogony",
        "subtitle": "Analysis of Hieroglyphs via the African Root (Dibombari Mbock)",
        "input_header": "Add New Sign from Kemlex.org",
        "search": "Search a sign or concept...",
        "logic": "Cosmogonic Logic (Manden/Dogon)",
        "root": "Linguistic Root (Bambara/Dogon)",
        "save": "Add to Local Database",
        "export": "Export Research",
        "view": "Lexicon View"
    },
    "fr": {
        "title": "Méthode Kuma : Cosmogonie Manden & Dogon",
        "subtitle": "Analyse des Hiéroglyphes via la Racine Africaine (Dibombari Mbock)",
        "input_header": "Ajouter un signe via Kemlex.org",
        "search": "Rechercher un signe ou un concept...",
        "logic": "Logique Cosmogonique (Manden/Dogon)",
        "root": "Racine Linguistique (Bambara/Dogon)",
        "save": "Ajouter à la base locale",
        "export": "Exporter la recherche",
        "view": "Vue Lexique"
    }
}

# --- Language Selection ---
lang = st.sidebar.selectbox("Language / Langue", ["fr", "en"])

# --- Persistent Data Storage ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {
            "Sign": "𓇳", 
            "Meaning": "Ra / Soleil", 
            "Kuma_Logic": "Principe de l'Amma Dogon; l'oeuf primordial ou l'oeil du créateur.",
            "Manden_Root": "Bambara: 'Tle' (Soleil/Temps)"
        }
    ])

# --- UI Layout ---
st.title(T[lang]["title"])
st.caption(T[lang]["subtitle"])

tab1, tab2 = st.tabs([T[lang]["view"], T[lang]["input_header"]])

with tab1:
    search = st.text_input(T[lang]["search"])
    
    # Filter display
    filtered_df = st.session_state.db[
        st.session_state.db.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)
    ]

    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div class="kuma-card">
            <span class="manden-badge">Manden Cosmogony</span>
            <h1 style="font-size: 80px; margin: 0;">{row['Sign']}</h1>
            <h3>{row['Meaning']}</h3>
            <p><strong>{T[lang]['logic']}:</strong><br>{row['Kuma_Logic']}</p>
            <p><strong>{T[lang]['root']}:</strong><br><em>{row['Manden_Root']}</em></p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader(T[lang]["input_header"])
    with st.form("kemlex_input"):
        col1, col2 = st.columns(2)
        with col1:
            new_sign = st.text_input("Glyph (Copy from Kemlex)")
            new_meaning = st.text_input("Common Meaning / Sens Commun")
        with col2:
            new_root = st.text_input("Bambara/Dogon Root")
            
        new_logic = st.text_area("Kuma Symbolic Logic (Philosophical)")
        
        submit = st.form_submit_button(T[lang]["save"])
        
        if submit:
            new_entry = {
                "Sign": new_sign, 
                "Meaning": new_meaning, 
                "Kuma_Logic": new_logic, 
                "Manden_Root": new_root
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Entry added / Entrée ajoutée !")

# Sidebar Tools
st.sidebar.markdown("---")
st.sidebar.subheader(T[lang]["export"])
st.sidebar.download_button("Download CSV", st.session_state.db.to_csv(index=False), "kuma_research.csv")
