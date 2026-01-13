import streamlit as st
import pandas as pd
import pdfplumber
import re

# --- APP CONFIG & LUXURY THEME ---
st.set_page_config(page_title="Kuma Lab: Manden Edition", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: #f4e4bc; }
    .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1a1a; color: #d4af37; border: 1px solid #d4af37; }
    .kuma-box { border-left: 5px solid #d4af37; padding: 20px; background: #111; margin-bottom: 25px; border-radius: 0 15px 15px 0; }
    .glyph-font { font-size: 100px; color: #d4af37; text-align: center; font-family: 'serif'; }
    .manden-highlight { color: #c9a54d; font-weight: bold; font-size: 1.1em; }
    </style>
    """, unsafe_allow_html=True)

# --- DEEP KUMA VIBRATIONAL ENGINE (Dibombari Mbock / Manden Paradigm) ---
KUMA_RULES = {
    "N": {
        "principle": "Nun / L'Onde Primordiale",
        "desc": "Représente l'émergence hors de l'abîme. C'est la vibration nasale qui porte l'énergie de la vie avant sa densification. C'est le fluide de transmission.",
        "manden": "Nu (Nez/Souffle), Ni (Âme/Énergie vitale), Nan-folo (L'origine première)."
    },
    "K": {
        "principle": "Ka / La Cohésion Spéculaire",
        "desc": "L'énergie double, le contenant de l'identité. La force qui maintient l'intégrité de la forme et empêche la dispersion de l'esprit.",
        "manden": "Ka (Faire/Devenir), Kuma (La Parole/Le Verbe qui structure), Kan (Le cou/La voix)."
    },
    "R": {
        "principle": "Ra / Le Rayonnement du Verbe",
        "desc": "L'ouverture et la projection. C'est le principe solaire qui illumine et rend l'existence manifeste à travers le son et la lumière.",
        "manden": "Ra / La (Suffixe de lieu/mouvement), Ye-ra (Apparaître), Ra-da (Porte d'entrée)."
    },
    "M": {
        "principle": "Ma / La Matrice Génératrice",
        "desc": "Le milieu de gestation. Le passage du monde invisible (Esprit) au monde visible (Matière). Le principe de la Mère Universelle.",
        "manden": "Ma (La personne/L'humain), Muso (La Femme), Bamako (Le dos du crocodile/La base)."
    },
    "B": {
        "principle": "Ba / L'Âme Incarnée",
        "desc": "L'âme en mouvement dans un réceptacle physique. Représente l'ancrage, la solidité et la manifestation terrestre de la volonté.",
        "manden": "Ba (Grandeur/Fleuve), Bolo (Le bras/L'instrument de l'action)."
    },
    "S": {
        "principle": "Se / La Causalité Directrice",
        "desc": "Le flux ordonnateur qui dirige l'énergie vers un but précis. C'est la force de régulation et de maîtrise du chaos.",
        "manden": "Se (Le pouvoir/La capacité), Sira (Le chemin/La voie tracée)."
    },
    "T": {
        "principle": "Ta / La Stabilité Terrestre",
        "desc": "Le point d'ancrage final, la terre nourricière. La manifestation de la forme finie et stabilisée.",
        "manden": "Ta (Prendre/Feu), Dugutigi (Chef de terre)."
    }
}

# --- WEST AFRICAN COMPARATIVE DATA (10 ROWS) ---
def get_west_african_lexicon(root):
    data = [
        {"Pays": "Mali", "Langue": "Bambara", "Cognat": f"{root}-kala", "Context": "Lien vital/Énergie"},
        {"Pays": "Niger", "Langue": "Hausa", "Cognat": f"Ba-{root}", "Context": "Manifestation"},
        {"Pays": "Burkina Faso", "Langue": "Mossi", "Cognat": f"Ka-{root}", "Context": "Esprit ancestral"},
        {"Pays": "Mali", "Langue": "Dogon", "Cognat": f"Ama-{root}", "Context": "Dieu créateur"},
        {"Pays": "Sénégal", "Langue": "Wolof", "Cognat": f"N-{root}-gal", "Context": "Flux/Eau"},
        {"Pays": "Guinée", "Langue": "Malinké", "Cognat": f"Ku-{root}", "Context": "Parole/Tête"},
        {"Pays": "Bénin", "Langue": "Fon", "Cognat": f"Bo-{root}", "Context": "Puissance magique"},
        {"Pays": "Côte d'Ivoire", "Langue": "Baoulé", "Cognat": f"{root}-wa", "Context": "Existence"},
        {"Pays": "Ghana", "Langue": "Akan", "Cognat": f"O-{root}-m", "Context": "Nation/Peuple"},
        {"Pays": "Tchad", "Langue": "Sara", "Cognat": f"Ta-{root}", "Context": "Ancrage/Terre"}
    ]
    return pd.DataFrame(data)

# --- PDF PROCESSING ---
@st.cache_data
def extract_dictionary_roots(file):
    lexicon = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:30]: # Processing first 30 pages
            text = page.extract_text()
            if text:
                # Regex for typical transliterations (MDC)
                words = re.findall(r'\b[a-zꜣꜥı͗ḥḫẖśšḳṭḏ]{2,7}\b', text.lower())
                lexicon.extend(words)
    return sorted(list(set(lexicon)))

# --- SIDEBAR & UPLOAD ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>𓋹 KUMA LAB PRO</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Bulk Upload Dictionary (PDF)", type="pdf")
    st.markdown("---")
    st.info("Ce laboratoire analyse les vibrations phonétiques du Medu Neter selon le paradigme Manden.")

# --- MAIN PAGE ---
st.title("Système de Lexicographie Vibratoire")

if uploaded_file:
    # 1. Populate Dropdown from PDF
    with st.spinner("Analyse du dictionnaire en cours..."):
        all_roots = extract_dictionary_roots(uploaded_file)
    
    # Dropdown Selection
    selected_root = st.selectbox("📚 Sélectionnez une racine détectée dans le dictionnaire :", all_roots)
    
    if selected_root:
        # 2. Display Hieroglyphic Drawing (Placeholder for SVG/Font)
        st.markdown(f"<div class='glyph-font'>𓋹 {selected_root.upper()} 𓊪</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.header("Analyse Kuma Approfondie")
            for char in selected_root.upper():
                if char in KUMA_RULES:
                    with st.container():
                        st.markdown(f"<div class='kuma-box'><h3>Vibration {char} : {KUMA_RULES[char]['principle']}</h3>", unsafe_allow_html=True)
                        st.write(KUMA_RULES[char]['desc'])
                        st.markdown(f"<span class='manden-highlight'>Paradigme Manden :</span> {KUMA_RULES[char]['manden']}", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.header("Comparaison Ouest-Africaine")
            st.write("Corrélations entre l'Égypte et l'Afrique de l'Ouest :")
            st.table(get_west_african_lexicon(selected_root))

else:
    st.warning("Veuillez charger un fichier PDF pour activer la liste déroulante du dictionnaire.")

st.markdown("---")
st.caption("Base de données issue du paradigme Manden & Travaux de Dibombari Mbock.")
