import streamlit as st
import pandas as pd
import pdfplumber
import re

# --- APP CONFIG ---
st.set_page_config(page_title="Kuma Lab - Pro Edition", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a Premium UX/UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #d4af37; color: black; font-weight: bold; border: none; }
    .stTextInput>div>div>input { background-color: #1a1c23; border: 1px solid #d4af37; color: white; }
    .glyph-card { border: 2px solid #d4af37; padding: 30px; text-align: center; background: rgba(212, 175, 55, 0.05); border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .kuma-header { color: #d4af37; font-family: 'serif'; text-transform: uppercase; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- KUMA PHONOSEMANTIC ENGINE ---
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

# --- PDF PROCESSING ENGINE ---
def extract_pdf_data(file):
    text_data = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:50]:  # Limit to 50 pages for performance; remove limit for full bulk
            content = page.extract_text()
            if content:
                # Basic logic to split lines and find potential MDC codes (lowercase letters)
                lines = content.split('\n')
                for line in lines:
                    # Look for words that look like MDC (lowercase with specific Egyptian phonemes)
                    match = re.search(r'([a-zꜣꜥı͗ḥḫẖśšḳṭḏ]+)', line)
                    if match:
                        text_data.append({
                            "mdc": match.group(1),
                            "context": line[:100],
                            "page": page.page_number
                        })
    return pd.DataFrame(text_data)

# --- SIDEBAR & UPLOAD ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Ankh_solid.svg/100px-Ankh_solid.svg.png", width=80)
    st.title("Settings")
    
    if 'lang' not in st.session_state: st.session_state.lang = 'fr'
    if st.button("Change Language / Changer Langue"):
        st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Dictionary (PDF)", type="pdf")
    st.info("Upload your Vygus or Faulkner PDF to populate the engine.")

# --- MAIN INTERFACE ---
S = {
    "fr": {"search": "Recherche MDC / Radical", "kuma": "ANALYSE VIBRATOIRE KUMA", "comp": "LEXIQUE COMPARÉ", "empty": "Veuillez charger un PDF pour commencer."},
    "en": {"search": "Search MDC / Radical", "kuma": "KUMA VIBRATIONAL ANALYSIS", "comp": "COMPARATIVE LEXICON", "empty": "Please upload a PDF to begin." }
}[st.session_state.lang]

st.title("𓋹 Medu Neter: Kuma Lab")

if uploaded_file is not None:
    with st.spinner('Extraction des racines en cours...'):
        df = extract_pdf_data(uploaded_file)
    
    search_q = st.text_input(S["search"], placeholder="Ex: nfr, anx, ka...")
    
    if search_q:
        results = df[df['mdc'].str.contains(search_q.lower())].drop_duplicates(subset=['mdc'])
        
        if not results.empty:
            # Layout
            col_res, col_space, col_det = st.columns([1, 0.1, 2])
            
            with col_res:
                st.subheader("Résultats")
                selection = st.radio("Sélectionnez une entrée:", results['mdc'].tolist())
            
            with col_det:
                st.markdown(f"""<div class='glyph-card'>
                    <h1 style='font-size:80px; color:#d4af37; margin:0;'>{selection.upper()}</h1>
                    <p style='color:#777;'>MDC Detected in PDF</p>
                </div>""", unsafe_allow_html=True)
                
                st.markdown(f"<h2 class='kuma-header'>{S['kuma']}</h2>", unsafe_allow_html=True)
                
                # Analysis Logic
                for char in selection.upper():
                    if char in KUMA_RULES:
                        with st.expander(f"Vibration '{char}' - {KUMA_RULES[char]['principle']}", expanded=True):
                            st.write(KUMA_RULES[char]['desc'])
                
                st.markdown(f"<h3 class='kuma-header'>{S['comp']}</h3>", unsafe_allow_html=True)
                comp_data = {
                    "Langue": ["Wolof", "Kikongo", "Bambara"],
                    "Terme": [f"Root-{selection}", f"N-{selection}", f"Ka-{selection}"],
                    "Sens": ["Force de vie", "Flux", "Esprit"]
                }
                st.table(pd.DataFrame(comp_data))
        else:
            st.warning("Aucune correspondance trouvée dans le PDF.")
else:
    st.markdown(f"""
        <div style='text-align:center; padding:100px;'>
            <h2 style='color:#555;'>{S['empty']}</h2>
            <p>Le système analysera automatiquement les racines phonétiques selon les principes de Dibombari Mbock.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© Kuma Lab - Dibombari Mbock Edition | Powered by Streamlit")
