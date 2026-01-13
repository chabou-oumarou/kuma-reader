import streamlit as st
import pandas as pd
import urllib.parse

# Page Config
st.set_page_config(page_title="Kuma Lexicon Pro", page_icon="𓃠", layout="wide")

# Custom CSS for the "Scribe's Desk" look
st.markdown("""
    <style>
    .stApp { background-color: #f9f5f0; }
    .search-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d4af37;
        margin-bottom: 25px;
    }
    .lexicon-card {
        background-color: #ffffff;
        padding: 20px;
        border-left: 10px solid #4a2c2a;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .manden-text { color: #8b0000; font-weight: bold; font-size: 1.1em; }
    .external-link { color: #0066cc; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- Language Selection ---
lang = st.sidebar.radio("Langue / Language", ["Français", "English"])
is_fr = lang == "Français"

# --- Database Setup ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {
            "glyph": "𓇳",
            "translit": "rꜥ",
            "classic": "Ra / Soleil",
            "manden": "Tle (Bambara) / Nay (Dogon)",
            "kuma": "Principe d'Amma; l'oeuf primordial en vibration."
        }
    ])

# --- UI Header ---
st.title("𓋹 Kuma Method: Lexique Manden-Égyptien")
st.markdown(f"**Integrations:** Kemlex.org | ProjetRosette.info | Manden Cosmogony")

# --- Step 1: External Research (The "Direct Search" Feature) ---
st.markdown(f"### 1. { 'Recherche Directe Sources' if is_fr else 'Direct Source Search' }")
query = st.text_input("Enter a word / Entrez un mot (e.g. Ra, Water, 𓈖):", key="main_search")

if query:
    encoded_query = urllib.parse.quote(query)
    # Constructing deep links
    kemlex_url = f"https://www.kemlex.org/search?q={encoded_query}"
    rosette_url = f"http://projetrosette.info/recherche.php?search={encoded_query}"
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"🔗 [Search '{query}' on Kemlex.org]({kemlex_url})")
    with col_b:
        st.markdown(f"🔗 [Search '{query}' on ProjetRosette]({rosette_url})")

st.divider()

# --- Step 2: Kuma Synthesis ---
tab1, tab2 = st.tabs(["📖 Lexicon / Bibliothèque", "✍️ Add Synthesis / Ajouter Analyse"])

with tab1:
    search_local = st.text_input("Filtrer mon lexique local :")
    display_df = st.session_state.db
    if search_local:
        display_df = display_df[display_df.apply(lambda r: search_local.lower() in r.astype(str).str.lower().values, axis=1)]

    for _, row in display_df.iterrows():
        st.markdown(f"""
        <div class="lexicon-card">
            <h1 style="margin:0;">{row['glyph']}</h1>
            <p><i>{row['translit']}</i> | <b>{row['classic']}</b></p>
            <p><span class="manden-text">Manden/Dogon:</span> {row['manden']}</p>
            <p><b>Kuma Logic:</b> {row['kuma']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("Synthèse Kuma (Transition Kemlex -> Manden)")
    with st.form("add_form"):
        c1, c2, c3 = st.columns(3)
        with c1: g = st.text_input("Glyph")
        with c2: t = st.text_input("Transliteration")
        with c3: c = st.text_input("Classic Meaning")
        
        m = st.text_input("Manden Word (Bambara/Dogon)")
        k = st.text_area("Kuma Cosmogonic Interpretation (Philosophie de Mbock)")
        
        if st.form_submit_button("Sauvegarder l'Analyse"):
            new_data = {"glyph": g, "translit": t, "classic": c, "manden": m, "kuma": k}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
            st.success("Analyse ajoutée !")

# Sidebar
st.sidebar.markdown("### Export")
st.sidebar.download_button("Download CSV", st.session_state.db.to_csv(index=False), "kuma_lexicon.csv")
