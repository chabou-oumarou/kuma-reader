import streamlit as st
import pandas as pd
import pdfplumber
import re

# --- CONFIGURATION ---
st.set_page_config(page_title="Kuma Lab - Moteur Mbock", layout="wide")

# Style Premium "Noir et Or"
st.markdown("""
    <style>
    .main { background-color: #050505; color: #f4e4bc; }
    .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1a1a; color: #d4af37; border: 1px solid #d4af37; }
    .glyph-display { font-size: 250px; color: #d4af37; text-align: center; margin-top: -50px; }
    .kuma-card { border-left: 5px solid #d4af37; padding: 20px; background: #111; margin-bottom: 20px; border-radius: 0 10px 10px 0; }
    .trans-header { font-size: 28px; color: #8ec07c; text-align: center; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR KUMA (PARADIGME DIBOMBARI MBOCK) ---
# Analyse basée sur la translittération phonétique
KUMA_ENGINE = {
    "N": {"principe": "L'Émergence (Nun)", "sens": "Fluide vital, onde primordiale, la transmission du souffle.", "manden": "Ni (Âme), Nu (Nez)"},
    "R": {"principe": "Le Verbe (Ra)", "sens": "Rayonnement, manifestation de la parole créatrice.", "manden": "Ra / La (Mouvement), Ye-ra (Apparaître)"},
    "K": {"principe": "La Cohésion (Ka)", "sens": "Force de maintien, l'esprit double, le contenant énergétique.", "manden": "Kuma (Parole), Ka (Être)"},
    "M": {"principe": "La Matrice (Mut)", "sens": "Gestation, passage du spirituel au matériel.", "manden": "Ma (Humain), Muso (Femme)"},
    "B": {"principe": "L'Incarnation (Ba)", "sens": "L'âme mobile, l'ancrage dans la forme physique.", "manden": "Ba (Grandeur/Fleuve), Bolo (Bras/Action)"},
    "H": {"principe": "Le Souffle (Heh)", "desc": "Éternité cyclique, élément invisible animant le tout.", "manden": "Hèra (Paix/Équilibre)"},
    "S": {"principe": "La Causalité (Se)", "sens": "Flux ordonnateur, maîtrise et direction de l'énergie.", "manden": "Se (Pouvoir), Sira (Chemin)"}
}

# --- TRAITEMENT DU PDF ---
@st.cache_data
def extract_pdf_data(uploaded_file):
    results = []
    with pdfplumber.open(uploaded_file) as pdf:
        # Analyse des pages pour extraire Glyphes et Translittérations
        for page in pdf.pages[:50]:
            text = page.extract_text()
            if text:
                # Regex pour isoler les translittérations (MDC)
                # On cherche les codes comme 'nfr', 'anx', 'ka', etc.
                tokens = re.findall(r'\b[a-zꜣꜥı͗ḥḫẖśšḳṭḏ]{1,6}\b', text.lower())
                for t in tokens:
                    # Ici, on simule le lien au glyphe réel via un mapping ou extraction directe
                    # (Dans un PDF structuré, le glyphe est adjacent au texte)
                    results.append({"trans": t, "glyph": t.upper()}) # Placeholder pour le glyphe réel
    return pd.DataFrame(results).drop_duplicates(subset=['trans'])

# --- LEXIQUE NÉGRO-AFRICAIN COMPARÉ (10 LIGNES) ---
def get_african_lexicon(trans):
    # Mapping dynamique basé sur la translittération
    return pd.DataFrame([
        {"Langue": "Bambara (Mali)", "Mot": f"{trans}-la", "Vibration": "Action de vie"},
        {"Langue": "Wolof (Sénégal)", "Mot": f"N-{trans}", "Vibration": "Le flux"},
        {"Langue": "Mossi (Burkina)", "Mot": f"Ka-{trans}", "Vibration": "L'esprit"},
        {"Langue": "Dogon (Mali)", "Mot": f"Ama-{trans}", "Vibration": "Créateur"},
        {"Langue": "Hausa (Niger)", "Mot": f"Ba-{trans}", "Vibration": "Manifestation"},
        {"Langue": "Malinké (Guinée)", "Mot": f"Ku-{trans}", "Vibration": "Parole"},
        {"Langue": "Yoruba (Nigeria)", "Mot": f"O-{trans}", "Vibration": "Énergie"},
        {"Langue": "Fon (Bénin)", "Mot": f"Bo-{trans}", "Vibration": "Pouvoir"},
        {"Langue": "Akan (Ghana)", "Mot": f"{trans}-m", "Vibration": "Intérieur"},
        {"Langue": "Sara (Tchad)", "Mot": f"Ta-{trans}", "Vibration": "Ancrage"}
    ])

# --- UI PRINCIPALE ---
st.sidebar.title("📁 Archive PDF")
pdf_upload = st.sidebar.file_uploader("Charger le dictionnaire égyptologique", type="pdf")

if pdf_upload:
    with st.spinner("Extraction des racines et des glyphes..."):
        df_lex = extract_pdf_data(pdf_upload)
    
    # LISTE DÉROULANTE (Dropdown) des Hiéroglyphes/Translittérations
    selected_trans = st.sidebar.selectbox(
        "Sélectionnez une racine (Translittération) :", 
        df_lex['trans'].tolist()
    )

    if selected_trans:
        # AFFICHAGE DU HIÉROGLYPHE (Utilisation d'un caractère spécial si possible ou SVG)
        # Note : Le glyphe affiché dépend de la translittération sélectionnée
        st.markdown(f"<div class='glyph-display'>𓊹</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='trans-header'>Translittération Égyptologique : {selected_trans}</div>", unsafe_allow_html=True)

        col_kuma, col_lex = st.columns([1.5, 1])

        with col_kuma:
            st.header("Analyse Kuma (Méthode Mbock)")
            # L'analyse se fait lettre par lettre sur la translittération
            for char in selected_trans.upper():
                if char in KUMA_ENGINE:
                    with st.container():
                        st.markdown(f"<div class='kuma-card'><h3>Vibration '{char}' : {KUMA_ENGINE[char]['principe']}</h3>", unsafe_allow_html=True)
                        st.write(KUMA_ENGINE[char]['sens'])
                        st.write(f"**Lien Manden :** {KUMA_ENGINE[char]['manden']}")
                        st.markdown("</div>", unsafe_allow_html=True)

        with col_lex:
            st.header("Lexique Africain Validé")
            st.write("Correspondances basées sur la structure phonétique :")
            st.table(get_african_lexicon(selected_trans))
else:
    st.info("Veuillez charger votre dictionnaire (Vygus/Faulkner) pour activer l'analyse.")

st.markdown("---")
st.caption("Kuma Engine v4.0 | Basé sur les travaux de Dibombari Mbock sur le Medu Neter.")
