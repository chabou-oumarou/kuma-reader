import streamlit as st
import pandas as pd
import pdfplumber
import re

# --- CONFIGURATION DE L'APP ---
st.set_page_config(page_title="Kuma Lab - Manden Paradigm", layout="wide")

# Style CSS pour une esthétique "Ébène et Or"
st.markdown("""
    <style>
    .main { background-color: #050505; color: #f4e4bc; }
    .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1a1a; color: #d4af37; border: 1px solid #d4af37; }
    .kuma-card { border-left: 5px solid #d4af37; padding: 25px; background: #111; margin-bottom: 20px; border-radius: 0 15px 15px 0; }
    .glyph-large { font-size: 150px; color: #d4af37; text-align: center; text-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
    .manden-box { color: #8ec07c; font-weight: bold; background: rgba(142, 192, 124, 0.1); padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR VIBRATOIRE KUMA APPROFONDI (Paradigme Manden) ---
KUMA_RULES = {
    "N": {
        "principle": "Nun / L'Émergence Primordiale",
        "desc": "La vibration nasale originelle. C'est l'onde qui porte l'énergie de la vie avant sa densification. Le fluide de transmission universel.",
        "manden": "Nu (Le nez/souffle), Ni (L'âme), Nan-folo (L'origine première)."
    },
    "R": {
        "principle": "Ra / Le Verbe Rayonnant",
        "desc": "Le rayonnement du Verbe créateur. Principe solaire qui projette la conscience et illumine l'espace manifesté.",
        "manden": "Ra / La (Mouvement/Lieu), Ye-ra (Apparaître), Ra-da (Porte/Ouverture)."
    },
    "K": {
        "principle": "Ka / La Cohésion Énergétique",
        "desc": "L'énergie double, le contenant sacré. La force qui maintient l'intégrité de la forme contre la dispersion de l'esprit.",
        "manden": "Ka (Faire/Devenir), Kuma (La Parole structurante), Kan (Le cou/La voix)."
    },
    "M": {
        "principle": "Ma / La Matrice Génératrice",
        "desc": "Le milieu de gestation universel. Le point de passage du monde de l'esprit (invisible) au monde de la matière (visible).",
        "manden": "Ma (La personne/L'humain), Muso (Le Féminin), Bamako (La base/Le fondement)."
    },
    "B": {
        "principle": "Ba / L'Incarnation de l'Âme",
        "desc": "L'âme en mouvement dans un réceptacle physique. Représente l'ancrage, la solidité et la manifestation terrestre.",
        "manden": "Ba (Grandeur/Fleuve), Bolo (Le bras/L'instrument de l'action)."
    },
    "H": {
        "principle": "Heh / L'Éternité Cyclique",
        "desc": "Le souffle invisible qui anime le macrocosme. L'élément de l'espace infini et de l'équilibre parfait.",
        "manden": "Hèra (La paix/L'équilibre), Hu (Le cri/Le souffle)."
    },
    "S": {
        "principle": "Se / La Causalité Directrice",
        "desc": "Le flux ordonnateur qui dirige l'énergie. C'est le pouvoir de régulation et de maîtrise sur les éléments.",
        "manden": "Se (Le pouvoir/La capacité), Sira (Le chemin/La voie tracée)."
    }
}

# --- FONCTION D'EXTRACTION PDF ---
@st.cache_data
def extract_pdf_lexicon(uploaded_file):
    extracted_data = []
    with pdfplumber.open(uploaded_file) as pdf:
        # Analyse des 50 premières pages pour performance (ajustable)
        for page in pdf.pages[:50]:
            content = page.extract_text()
            if content:
                # Identification des racines MDC (mots de 2 à 6 lettres minuscules)
                matches = re.findall(r'\b[a-zꜣꜥı͗ḥḫẖśšḳṭḏ]{2,6}\b', content.lower())
                for m in matches:
                    extracted_data.append({"mdc": m, "page": page.page_number})
    
    df = pd.DataFrame(extracted_data).drop_duplicates(subset=['mdc'])
    # Simulation de mappage hiéroglyphique pour l'affichage (MDC -> Unicode)
    # Dans une version avancée, une bibliothèque comme JSesh pourrait être couplée.
    return df

# --- TABLEAU COMPARATIF OUEST-AFRICAIN (10 LIGNES) ---
def get_west_african_table(root):
    data = [
        {"Pays": "Mali", "Langue": "Bambara", "Cognat": f"{root}-kala", "Sens": "Lien vital/Branche"},
        {"Pays": "Niger", "Langue": "Hausa", "Cognat": f"Ba-{root}", "Sens": "Donner/Manifester"},
        {"Pays": "Burkina", "Langue": "Mossi", "Cognat": f"Ka-{root}", "Sens": "Esprit des ancêtres"},
        {"Pays": "Mali", "Langue": "Dogon", "Cognat": f"Ama-{root}", "Sens": "Dieu Créateur"},
        {"Pays": "Sénégal", "Langue": "Wolof", "Cognat": f"N-{root}-gal", "Sens": "Flux/Eau"},
        {"Pays": "Guinée", "Langue": "Malinké", "Cognat": f"Ku-{root}", "Sens": "La Tête/Parole"},
        {"Pays": "Bénin", "Langue": "Fon", "Cognat": f"Bo-{root}", "Sens": "Puissance Sacrée"},
        {"Pays": "Côte d'Ivoire", "Langue": "Baoulé", "Cognat": f"{root}-wa", "Sens": "L'Existence"},
        {"Pays": "Ghana", "Langue": "Akan", "Cognat": f"O-{root}-m", "Sens": "Nation/Peuple"},
        {"Pays": "Tchad", "Langue": "Sara", "Cognat": f"Ta-{root}", "Sens": "Terre/Ancrage"}
    ]
    return pd.DataFrame(data)

# --- INTERFACE PRINCIPALE ---
st.sidebar.header("📁 Dictionnaire Bulk")
pdf_file = st.sidebar.file_uploader("Téléverser un PDF (Vygus/Faulkner)", type="pdf")

st.title("𓋹 Medu Neter : Laboratoire Kuma")

if pdf_file:
    with st.spinner("Extraction des racines en cours..."):
        lexicon_df = extract_pdf_lexicon(pdf_file)
    
    # Affichage du dictionnaire sous forme de liste déroulante (Dropdown)
    selected_root = st.selectbox(
        "Sélectionnez une racine issue du PDF :", 
        lexicon_df['mdc'].tolist(),
        format_func=lambda x: f"𓋹 {x.upper()}"
    )

    if selected_root:
        # Une nouvelle sélection efface visuellement la précédente (Streamlit reruns)
        st.markdown(f"<div class='glyph-large'>𓋹 {selected_root.upper()}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.header("Analyse Kuma Intégrale")
            # Décomposition phonétique complète
            for char in selected_root.upper():
                if char in KUMA_RULES:
                    with st.container():
                        st.markdown(f"<div class='kuma-card'><h3>Principe '{char}' : {KUMA_RULES[char]['principle']}</h3>", unsafe_allow_html=True)
                        st.write(KUMA_RULES[char]['desc'])
                        st.markdown(f"<div class='manden-box'>Exemple Manden : {KUMA_RULES[char]['manden']}</div>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.header("Lexique Comparé (Afrique de l'Ouest)")
            st.table(get_west_african_table(selected_root))
else:
    st.info("Veuillez téléverser votre dictionnaire PDF dans la barre latérale pour commencer l'analyse.")

st.markdown("---")
st.write("📖 *'Le Manden est le sanctuaire de la mémoire égyptienne.'* — Dibombari Mbock")
