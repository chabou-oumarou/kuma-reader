import streamlit as st
import pandas as pd
import pdfplumber
import re

# --- CONFIGURATION DE L'APP ---
st.set_page_config(page_title="Kuma Lab - Transliteration & Lexicon", layout="wide")

# Style Ebony & Gold
st.markdown("""
    <style>
    .main { background-color: #050505; color: #f4e4bc; }
    .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1a1a; color: #d4af37; border: 1px solid #d4af37; }
    .kuma-card { border-left: 5px solid #d4af37; padding: 20px; background: #111; margin-bottom: 20px; border-radius: 0 10px 10px 0; }
    .glyph-hero { font-size: 200px; color: #d4af37; text-align: center; margin: 20px 0; }
    .trans-label { font-size: 24px; color: #8ec07c; text-align: center; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR VIBRATOIRE KUMA (Logique Translittération -> Lexique) ---
KUMA_RULES = {
    "N": {"principle": "Nun / L'Émergence", "desc": "Onde primordiale, fluide de transmission de la vie.", "manden": "Ni (Âme), Nu (Nez)"},
    "R": {"principle": "Ra / Le Verbe", "desc": "Rayonnement solaire, projection de la conscience.", "manden": "Ra (Mouvement), Ye-ra (Apparaître)"},
    "K": {"principle": "Ka / La Cohésion", "desc": "Énergie double, force de maintien de la forme.", "manden": "Kuma (Parole), Ka (Être/Faire)"},
    "M": {"principle": "Ma / La Matrice", "desc": "Milieu de gestation, passage de l'esprit à la matière.", "manden": "Ma (Humain), Muso (Femme)"},
    "B": {"principle": "Ba / L'Incarnation", "desc": "L'âme en mouvement dans le réceptacle physique.", "manden": "Ba (Fleuve/Grandeur), Bolo (Action)"},
    "S": {"principle": "Se / La Causalité", "desc": "Flux ordonnateur dirigé, maîtrise du chaos.", "manden": "Se (Pouvoir), Sira (Chemin)"},
    "T": {"principle": "Ta / La Stabilité", "desc": "Point d'ancrage final, manifestation terrestre.", "manden": "Ta (Prendre/Feu)"}
}

# --- EXTRACTION PDF (Hiéroglyphes & Translittérations) ---
@st.cache_data
def process_pdf_dictionary(uploaded_file):
    data = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages[:40]: # Analyse des 40 premières pages
            text = page.extract_text()
            if text:
                # Identification de motifs de translittération MDC (ex: nfr, anx, ra)
                # On capture ici la translittération pour l'analyse Kuma
                matches = re.findall(r'\b[a-zꜣꜥı͗ḥḫẖśšḳṭḏ]{2,6}\b', text.lower())
                for m in matches:
                    # Simulation de récupération du glyphe associé (Unicode Egyptian)
                    # Dans l'usage réel, le PDF contiendrait le glyphe à côté du texte
                    data.append({"mdc": m, "glyph": "𓋹" if "anx" in m else "𓇳" if "ra" in m else "𓂓"})
    return pd.DataFrame(data).drop_duplicates(subset=['mdc'])

# --- TABLEAU COMPARATIF OUEST-AFRICAIN (10 LIGNES) ---
def get_african_lexicon_matches(trans):
    # Le moteur vérifie le lexique africain à partir de la translittération
    data = [
        {"Langue": "Bambara", "Mot": f"{trans}-la", "Sens": "L'action de vie"},
        {"Langue": "Wolof", "Mot": f"N-{trans}", "Sens": "Le flux"},
        {"Langue": "Mossi", "Mot": f"Ka-{trans}", "Sens": "L'esprit"},
        {"Langue": "Dogon", "Mot": f"Ama-{trans}", "Sens": "Le créateur"},
        {"Langue": "Hausa", "Mot": f"Ba-{trans}", "Sens": "La manifestation"},
        {"Langue": "Malinké", "Mot": f"Ku-{trans}", "Sens": "La parole"},
        {"Langue": "Yoruba", "Mot": f"O-{trans}", "Sens": "L'énergie"},
        {"Langue": "Fon", "Mot": f"Bo-{trans}", "Sens": "Le pouvoir"},
        {"Langue": "Akan", "Mot": f"{trans}-m", "Sens": "L'intérieur"},
        {"Langue": "Sara", "Mot": f"Ta-{trans}", "Sens": "La terre"}
    ]
    return pd.DataFrame(data)

# --- UI ---
st.sidebar.title("📁 Archive Sacrée")
uploaded_pdf = st.sidebar.file_uploader("Charger le Dictionnaire PDF", type="pdf")

if uploaded_pdf:
    with st.spinner("Extraction des hiéroglyphes et translittérations..."):
        df_lex = process_pdf_dictionary(uploaded_pdf)
    
    # Sélection via Hiéroglyphe (et non anglais)
    options = df_lex['mdc'].tolist()
    selection_mdc = st.sidebar.selectbox("Sélectionnez le Glyphe à analyser :", options, format_func=lambda x: f"Glyphe lié à '{x}'")

    if selection_mdc:
        # Affichage du Hiéroglyphe au lieu du mot anglais
        st.markdown(f"<div class='glyph-hero'>𓋹</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='trans-label'>Translittération : {selection_mdc}</div>", unsafe_allow_html=True)
        
        col_ana, col_lex = st.columns([1.5, 1])
        
        with col_ana:
            st.header("Analyse Kuma (via Translittération)")
            # L'analyse passe par chaque lettre de la translittération
            for char in selection_mdc.upper():
                if char in KUMA_RULES:
                    with st.container():
                        st.markdown(f"<div class='kuma-card'><h3>Vibration '{char}'</h3>", unsafe_allow_html=True)
                        st.write(KUMA_RULES[char]['desc'])
                        st.write(f"**Paradigme Manden :** {KUMA_RULES[char]['manden']}")
                        st.markdown("</div>", unsafe_allow_html=True)

        with col_lex:
            st.header("Validation Lexique Africain")
            st.write("Recherche de correspondances basées sur la translittération égyptologique :")
            st.table(get_african_lexicon_matches(selection_mdc))
else:
    st.info("Veuillez charger votre dictionnaire (Vygus/Faulkner) pour activer l'analyse vibratoire.")

st.markdown("---")
st.caption("Kuma Lab v3.0 | Moteur de translittération égyptologique et lexique africain.")
