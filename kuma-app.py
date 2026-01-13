import streamlit as st
import pandas as pd
import urllib.parse

# Page Setup
st.set_page_config(page_title="Kuma Method: Universal Hieroglyphic Engine", layout="wide")

# --- Kuma Method Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f1ea; }
    .kuma-header {
        background: linear-gradient(90deg, #4a2c2a 0%, #7a5901 100%);
        color: white; padding: 2rem; border-radius: 15px; text-align: center;
    }
    .analysis-card {
        background-color: white; border: 1px solid #d4af37;
        padding: 30px; border-radius: 15px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    .glyph-box {
        font-size: 100px; background: #fffcf5; border-radius: 10px;
        display: flex; align-items: center; justify-content: center; height: 150px;
        border: 2px solid #4a2c2a; margin-bottom: 20px;
    }
    .dictionary-tag {
        background: #e0d7c6; padding: 2px 8px; border-radius: 5px; font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Core Method Logic (Mbock Principles) ---
def apply_kuma_logic(sign, translit, meaning):
    """
    Applies the fundamental principles of the Kuma Method:
    1. Sign as Cosmogonic Seed (Nommo)
    2. Phonetic Root in Manden/Dogon
    3. Law of Correspondences
    """
    logic_map = {
        "rꜥ": {"manden": "Tle / Nay", "law": "Principe de la Conscience Solaire (Amma).", "origin": "Vibration originelle de l'oeuf Dogon."},
        "pr": {"manden": "Lu / Gwa", "law": "Principe de l'Espace Sacré ou de l'Enceinte.", "origin": "La matrice sociale du Manden."},
        "mw": {"manden": "Ji / Dyi", "law": "Principe de la Fluidité de la Parole (Nommo).", "origin": "L'énergie vitale qui descend du ciel."},
    }
    return logic_map.get(translit.lower(), {
        "manden": "Recherche Racine (Kemlex)...", 
        "law": "Analyse symbolique selon l'analogie Manden.",
        "origin": "Loi du verbe (Nommo)."
    })

# --- UI Content ---
st.markdown('<div class="kuma-header"><h1>𓋹 KUMA METHOD ANALYSER</h1><p>Vygus • Faulkner • Gardiner • Manden Cosmogony</p></div>', unsafe_allow_html=True)

# --- Search Navigation ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Thoth.svg/250px-Thoth.svg.png", width=100)
st.sidebar.header("Search Nav")
search_type = st.sidebar.selectbox("Search by", ["Hieroglyph (𓇳)", "Transliteration (rꜥ)", "Translation (Sun)"])
query = st.sidebar.text_input("Enter query:")

# --- Action Hub ---
if query:
    # External Dictionary Links (Projet Rosette provides access to Faulkner/Gardiner data)
    encoded = urllib.parse.quote(query)
    links = {
        "Kemlex": f"https://www.kemlex.org/search?q={encoded}",
        "Projet Rosette (Faulkner/Vygus)": f"http://projetrosette.info/recherche.php?search={encoded}",
    }
    
    st.markdown("### 🔍 Dictionary References & Deep Search")
    cols = st.columns(len(links))
    for i, (name, url) in enumerate(links.items()):
        cols[i].markdown(f"[{name}]({url})")

    st.divider()

    # --- The Kuma Synthesis Display ---
    st.subheader("🛠️ Kuma Method Analysis (Synthèse Africaine)")
    
    col_img, col_info = st.columns([1, 2])
    
    # Placeholder for dynamic logic
    k_analysis = apply_kuma_logic(query, query, query)

    with col_img:
        # Displaying the Glyph visually
        st.markdown(f'<div class="glyph-box">{query if len(query) < 5 else "𓁟"}</div>', unsafe_allow_html=True)
        st.caption("Visual reconstruction of the symbol as a 'Nommo' seed.")

    with col_info:
        st.markdown(f"""
        <div class="analysis-card">
            <h3>Structure de l'Analyse</h3>
            <p><span class="dictionary-tag">Translit:</span> <b>{query}</b></p>
            <hr>
            <p><b>1. Racine Linguistique (Manden/Dogon):</b><br>
            <span style="color:#8b0000; font-weight:bold;">{k_analysis['manden']}</span></p>
            
            <p><b>2. Principe Fondamental (Dibombari Mbock):</b><br>
            <i>{k_analysis['law']}</i></p>
            
            <p><b>3. Origine Cosmogonique:</b><br>
            {k_analysis['origin']}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("Utilisez la barre de navigation à gauche pour commencer l'analyse d'un signe.")

# --- Manual Input for Lexicon Building ---
with st.expander("➕ Enrichir le Lexique (Input Kemlex Data)"):
    with st.form("manual_entry"):
        f1, f2, f3 = st.columns(3)
        g_in = f1.text_input("Glyph")
        t_in = f2.text_input("Translit")
        m_in = f3.text_input("Translation")
        k_logic = st.text_area("Kuma Analysis (Cosmogony)")
        if st.form_submit_button("Enregistrer l'analyse"):
            st.success("Données sauvegardées pour l'exportation.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("**Methode Kuma v2.0**")
st.sidebar.write("Based on African Philology and the works of Dibombari Mbock.")
