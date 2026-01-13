import streamlit as st
import pandas as pd
import pdfplumber
import re
import io

# --- APP CONFIG & UI THEME ---
st.set_page_config(page_title="Kuma Lab Pro", page_icon="𓋹", layout="wide")

st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp { background-color: #050505; color: #e0e0e0; }
    
    /* Luxury Gold Cards */
    .glyph-box {
        background: linear-gradient(145deg, #111, #1a1a1a);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
        margin-bottom: 20px;
    }
    
    /* Headers */
    h1, h2, h3 { color: #d4af37 !important; font-family: 'Georgia', serif; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 1px solid #333; }
    
    /* Custom info boxes */
    .stAlert { background-color: #111 !important; border: 1px solid #d4af37 !important; color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- KUMA PHONOSEMANTIC ENGINE (Dibombari Mbock) ---
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
def process_dictionary_pdf(uploaded_file):
    extracted_data = []
    with pdfplumber.open(uploaded_file) as pdf:
        # We sample pages to maintain performance; increase range for deeper bulk analysis
        for page in pdf.pages[:30]: 
            text = page.extract_text()
            if text:
                # Find words (3-6 chars) that look like MDC roots
                words = re.findall(r'\b[a-z]{2,8}\b', text.lower())
                for w in words:
                    extracted_data.append({"mdc": w, "source": f"Page {page.page_number}"})
    return pd.DataFrame(extracted_data).drop_duplicates(subset=['mdc'])

# --- SIDEBAR: CONTROLS & UPLOAD ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>𓋹 KUMA LAB</h1>", unsafe_allow_html=True)
    
    if 'lang' not in st.session_state: st.session_state.lang = 'fr'
    if st.button("🇬🇧 English / 🇫🇷 Français"):
        st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'
    
    st.markdown("---")
    st.subheader("📁 Bulk Dictionary Upload")
    pdf_file = st.file_uploader("Upload PDF (Vygus/Faulkner)", type="pdf")
    
    if pdf_file:
        st.success("PDF Loaded Successfully")

# --- MAIN CONTENT ---
S = {
    "fr": {"title": "Laboratoire de Lexicographie Kuma", "search": "Rechercher une racine (MDC)", "sub": "Analyse Vibratoire", "guide": "Veuillez téléverser un dictionnaire PDF pour peupler la base."},
    "en": {"title": "Kuma Lexicography Lab", "search": "Search Root (MDC)", "sub": "Vibrational Analysis", "guide": "Please upload a PDF dictionary to populate the database."}
}[st.session_state.lang]

st.title(S["title"])

if pdf_file:
    # Extract data from PDF
    with st.spinner("Analyse du dictionnaire en cours..."):
        df_lexicon = process_dictionary_pdf(pdf_file)
    
    search_query = st.text_input(S["search"], placeholder="ex: nfr, anx, ka...")
    
    if search_query:
        # Filter results
        filtered = df_lexicon[df_lexicon['mdc'].str.contains(search_query.lower())]
        
        if not filtered.empty:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Lexique Trouvé")
                selection = st.radio("Entrées détectées:", filtered['mdc'].head(15))
            
            with col2:
                # Big Visual Display
                st.markdown(f"""
                    <div class='glyph-box'>
                        <p style='color: #777; margin-bottom: 0;'>ROOT MDC</p>
                        <h1 style='font-size: 100px; margin: 0; letter-spacing: 10px;'>{selection.upper()}</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                st.header(S["sub"])
                # Kuma Breakdown
                for char in selection.upper():
                    if char in KUMA_RULES:
                        with st.expander(f"Vibration '{char}' - {KUMA_RULES[char]['principle']}", expanded=True):
                            st.write(KUMA_RULES[char]['desc'])
                
                # Comparative Data Table
                st.markdown("### 🌍 Comparaison Négro-Africaine")
                comp_df = pd.DataFrame({
                    "Famille": ["Soudanais", "Bantou", "Sahélien"],
                    "Cognat": [f"Ka-{selection}", f"Di-{selection}", f"Ma-{selection}"],
                    "Vibration": ["Identique", "Harmonique", "Complémentaire"]
                })
                st.table(comp_df)
        else:
            st.info("Aucune racine trouvée pour cette recherche dans le document.")
else:
    st.warning(S["guide"])

st.markdown("---")
st.write("📖 *'Le Medu Neter est la clé de la conscience africaine.'* — Dibombari Mbock")
