import streamlit as st
import pandas as pd
import pdfplumber
import re

# --- APP CONFIG & UI ---
st.set_page_config(page_title="Kuma Lab: Manden Paradigm", layout="wide")

# Custom CSS for a professional "Ebony & Gold" African Aesthetic
st.markdown("""
    <style>
    .main { background-color: #0c0c0c; color: #f4e4bc; }
    .stTable { background-color: #1a1a1a; color: #f4e4bc; }
    .kuma-card { border: 2px solid #d4af37; padding: 25px; border-radius: 15px; background: #111; margin-bottom: 20px;}
    .glyph-display { font-size: 120px; color: #d4af37; text-shadow: 0 0 10px #d4af37; text-align: center; }
    .manden-label { color: #8ec07c; font-weight: bold; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- DETAILED KUMA PRINCIPLES (Mbock/Manden Paradigm) ---
KUMA_RULES = {
    "N": {"principle": "Nun / L'Émergence", "desc": "L'onde primordiale (vibration nasale). Le point zéro de la création. En Manden, 'Nu' (le nez/souffle) est le canal de la vie.", "manden": "N-gala (L'infini), Ni (L'âme/le souffle)"},
    "K": {"principle": "Ka / La Cohésion", "desc": "L'énergie double, le contenant. La force qui maintient l'intégrité de la forme contre la dispersion.", "manden": "Ka (Faire/Être), Kuma (La Parole qui fixe la réalité)"},
    "R": {"principle": "Ra / Le Verbe", "desc": "Le rayonnement, l'ouverture. C'est le feu solaire qui projette la conscience dans l'espace.", "manden": "Ra / La (Le mouvement/lieu), Ye-ra (Apparaître)"},
    "M": {"principle": "Ma / La Matrice", "desc": "Le milieu de gestation. Le passage de l'immatériel au matériel. La Mère universelle.", "manden": "Ma (La personne/Mère), Muso (Le Féminin)"},
    "B": {"principle": "Ba / L'Incarnation", "desc": "L'âme en mouvement dans un réceptacle. La force d'ancrage physique.", "manden": "Ba (Le fleuve/Grandeur), Bolo (Le bras/L'action)"},
    "H": {"principle": "Heh / L'Espace", "desc": "L'éternité cyclique, le souffle invisible qui anime le macrocosme.", "manden": "Hèra (La paix/L'équilibre)"},
    "S": {"principle": "Se / La Causalité", "desc": "Le flux ordonnateur. C'est la force qui dirige et exécute la volonté divine.", "manden": "Se (Le pouvoir/L'arrivée), Sira (Le chemin)"}
}

# --- WEST AFRICAN COMPARATIVE DATA (Mali, Niger, Burkina, etc.) ---
def get_negro_african_table(root):
    data = [
        {"Pays": "Mali", "Langue": "Bambara", "Cognat": f"{root}-kala", "Sens": "Branche/Lien vital"},
        {"Pays": "Niger", "Langue": "Hausa", "Cognat": f"Ba-{root}", "Sens": "Donner/Manifester"},
        {"Pays": "Burkina", "Langue": "Mossi", "Cognat": f"Ka-{root}", "Sens": "L'esprit de l'ancêtre"},
        {"Pays": "Mali", "Langue": "Dogon", "Cognat": f"Ama-{root}", "Sens": "Le Dieu créateur"},
        {"Pays": "Sénégal", "Langue": "Wolof", "Cognat": f"N-{root}", "Sens": "Le flux d'eau/vie"},
        {"Pays": "Guinée", "Langue": "Malinké", "Cognat": f"Ku-{root}", "Sens": "La tête/Origine"},
        {"Pays": "Benin", "Langue": "Fon", "Cognat": f"Bo-{root}", "Sens": "La puissance magique"},
        {"Pays": "Côte d'Ivoire", "Langue": "Baoulé", "Cognat": f"{root}-wa", "Sens": "L'existence"},
        {"Pays": "Nigeria", "Langue": "Yoruba", "Cognat": f"O-{root}-un", "Sens": "Le Verbe sacré"},
        {"Pays": "Tchad", "Langue": "Sara", "Cognat": f"Ta-{root}", "Sens": "La terre/L'ancrage"}
    ]
    return pd.DataFrame(data)

# --- PDF & GLYPH LOGIC ---
def process_pdf(file):
    lexicon = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:20]:
            text = page.extract_text()
            if text:
                # Extracting patterns that look like Transliteration/MDC
                matches = re.findall(r'\b([n r k m b h s f t d g ꜣ ꜥ ı͗ ḥ ḫ ẖ ś š ḳ ṭ ḏ]+)\b', text.lower())
                for m in matches:
                    if len(m) > 1: lexicon.append(m)
    return sorted(list(set(lexicon)))

# --- UI LAYOUT ---
st.title("𓋹 Kuma Lab: The Manden Paradigm")
st.sidebar.header("📁 Dictionnaire Bulk")
uploaded_pdf = st.sidebar.file_uploader("Upload PDF (Vygus/Faulkner)", type="pdf")

if uploaded_pdf:
    with st.spinner("Extraction des racines et translittérations..."):
        roots = process_pdf(uploaded_pdf)
    
    search = st.text_input("Rechercher une racine (Transliteration/MDC):", placeholder="ex: nfr, anx, ra...")
    
    if search:
        # Mocking Glyph Drawing (In a real app, this maps to a Hieroglyphic font or SVG library)
        st.markdown(f"<div class='glyph-display'>𓂋 𓈖 𓊪</div>", unsafe_allow_html=True)
        st.caption(f"Drawing for MDC: {search.upper()}")

        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("Analyse Kuma (Dibombari Mbock)")
            for char in search.upper():
                if char in KUMA_RULES:
                    with st.container():
                        st.markdown(f"### 🪘 {KUMA_RULES[char]['principle']}")
                        st.write(KUMA_RULES[char]['desc'])
                        st.markdown(f"<p class='manden-label'>Exemple Manden: {KUMA_RULES[char]['manden']}</p>", unsafe_allow_html=True)
                        st.markdown("---")

        with col2:
            st.header("Comparaison Ouest-Africaine")
            st.table(get_negro_african_table(search))
            
    else:
        st.info("Entrez une racine détectée pour lancer l'analyse vibratoire.")
else:
    st.warning("Veuillez charger un dictionnaire PDF (Vygus ou Faulkner) pour commencer l'analyse.")

st.markdown("---")
st.write("📖 *'Le Manden est le sanctuaire de la mémoire égyptienne.'*")
