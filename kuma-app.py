import streamlit as st
import pandas as pd
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Kuma Method Universal Lexicon",
    page_icon="𓋹",
    layout="wide"
)

# --- ADVANCED STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&display=swap');
    
    .stApp { background-color: #f8f1e7; }
    .main-title { font-family: 'Playfair Display', serif; color: #4a2c2a; text-align: center; font-size: 3rem; }
    .kuma-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        border-top: 8px solid #c5a059;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .glyph-display {
        font-size: 120px;
        color: #1a1a1a;
        background: #fff;
        border: 2px dashed #c5a059;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 200px;
    }
    .manden-logic {
        background-color: #fdf2f2;
        padding: 15px;
        border-left: 5px solid #8b0000;
        font-style: italic;
    }
    .dictionary-ref {
        font-size: 0.85em;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KUMA CORE LOGIC (Dibombari Mbock) ---
# This dictionary simulates the combined data of Vygus/Faulkner mapped to Kuma
lexicon_data = [
    {
        "glyph": "𓇳",
        "translit": "rꜥ",
        "translation": "Sun / Soleil",
        "dictionaries": "Gardiner N5, Faulkner p.145, Vygus p.1204",
        "kuma_analysis": "Principe de l'Amma (Dieu Créateur Dogon). Représente l'œuf primordial ou la conscience pure. Ce n'est pas seulement un astre, mais le feu interne (Bambara: 'Tle').",
        "manden_cognate": "Tle (Bambara), Nay (Dogon)",
        "cosmogony": "Loi de la Vibration Initiale"
    },
    {
        "glyph": "𓈖",
        "translit": "n",
        "translation": "Water / Eau",
        "dictionaries": "Gardiner N35, Faulkner p.123, Vygus p.882",
        "kuma_analysis": "Le flux du Nommo. L'énergie ondulatoire qui transporte la parole divine. En Manden, l'eau est le support du verbe (Bambara: 'Ji').",
        "manden_cognate": "Ji (Bambara), Dyi (Dogon)",
        "cosmogony": "Loi de la Fluidité du Verbe"
    },
    {
        "glyph": "𓉐",
        "translit": "pr",
        "translation": "House / Maison",
        "dictionaries": "Gardiner O1, Faulkner p.89, Vygus p.1501",
        "kuma_analysis": "L'enceinte sacrée (Bambara: 'Gwa'). Représente la matrice sociale et le temple du corps humain où réside l'esprit.",
        "manden_cognate": "Gwa / Lu (Bambara)",
        "cosmogony": "Loi de l'Espace Manifesté"
    }
]

df_lexicon = pd.DataFrame(lexicon_data)

# --- UI LAYOUT ---
st.markdown('<h1 class="main-title">𓋹 MÉTHODE KUMA 𓋹</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Lexique Universel : Vygus, Faulkner, Gardiner & Cosmogonie Manden-Dogon</p>", unsafe_allow_html=True)

# --- SEARCH NAVIGATION ---
st.sidebar.header("🔍 Navigation de Recherche")
search_input = st.sidebar.text_input("Rechercher (Glyphe, Translit, ou Traduction):")
st.sidebar.markdown("---")
st.sidebar.caption("Sources : Principes fondamentaux de Dibombari Mbock")

# --- MAIN ANALYSIS ENGINE ---
if search_input:
    # Filter through the combined lexicon
    results = df_lexicon[
        df_lexicon['glyph'].str.contains(search_input) | 
        df_lexicon['translit'].str.contains(search_input, case=False) |
        df_lexicon['translation'].str.contains(search_input, case=False)
    ]

    if not results.empty:
        for idx, row in results.iterrows():
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f'<div class="glyph-display">{row["glyph"]}</div>', unsafe_allow_html=True)
                st.caption(f"Visualisation : {row['translation']}")
                
                # External Quick Links
                encoded = urllib.parse.quote(row['translation'])
                st.markdown(f"**Sources Externes :**")
                st.markdown(f"🔗 [Kemlex Research](https://www.kemlex.org/search?q={encoded})")
                st.markdown(f"🔗 [Projet Rosette](http://projetrosette.info/recherche.php?search={encoded})")

            with col2:
                st.markdown(f"""
                <div class="kuma-card">
                    <div class="dictionary-ref">{row['dictionaries']}</div>
                    <h2 style="color:#4a2c2a;">{row['translit']} — {row['translation']}</h2>
                    <hr>
                    <h4>Analyse Kuma (Dibombari Mbock)</h4>
                    <div class="manden-logic">
                        <strong>Logique Manden/Dogon :</strong> {row['kuma_analysis']}
                    </div>
                    <p style="margin-top:15px;">
                        <b>Racine Manden :</b> <span style="color:#8b0000;">{row['manden_cognate']}</span><br>
                        <b>Principe Cosmique :</b> {row['cosmogony']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Aucun résultat trouvé. Veuillez utiliser le module d'importation ci-dessous pour ajouter ce signe.")

else:
    st.info("Utilisez la barre de navigation à gauche pour explorer le lexique.")

# --- MANUAL KEMLEX-STYLE INPUT ---
st.divider()
with st.expander("📥 Ajouter une Analyse de Signe (Interface Scribe)"):
    st.write("Combinez les données de Vygus/Faulkner avec votre analyse Kuma personnelle.")
    with st.form("scribe_form"):
        c1, c2, c3 = st.columns(3)
        with c1: in_glyph = st.text_input("Hiéroglyphe (𓀀)")
        with c2: in_trans = st.text_input("Translittération")
        with c3: in_mean = st.text_input("Traduction")
        
        in_logic = st.text_area("Analyse Kuma & Correspondance Manden (Cosmogonie)")
        in_refs = st.text_input("Références Dictionnaires (Vygus/Gardiner/Faulkner)")
        
        if st.form_submit_button("Enregistrer dans le Lexique"):
            st.success("Analyse prête pour l'exportation CSV.")

# --- FOOTER & EXPORT ---
st.sidebar.markdown("### 🛠️ Outils")
csv = df_lexicon.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Télécharger le Lexique (CSV)", data=csv, file_name="kuma_universal_lexicon.csv", mime='text/csv')
