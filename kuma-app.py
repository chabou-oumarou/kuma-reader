import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Kuma Method Lexicon", layout="wide")

# --- KUMA METHOD LOGIC ENGINE ---
# According to Mbock, sounds have inherent meanings. 
# This helper simulates the "Kuma breakdown" for any word based on its consonants.
KUMA_VIBRATIONS = {
    "N": "Emergence, Primordial Water (Nun), Transmission of Life force.",
    "R": "The Word (Ra), Opening, Solar Vibration, Radiation.",
    "K": "Energy of Cohesion, Spirit/Double (Ka), The container.",
    "M": "Transition, Transformation, The Mother/Origin (Mut).",
    "B": "Incarnation, The Soul (Ba), Movement of the Spirit.",
    "H": "Breath, Spirit, Invisible force.",
    "S": "Causality, Direction, Flow of time."
}

# --- EXTENDED DATABASE ---
# In a production environment, this would be a CSV with 5,000+ rows.
# Includes Vygus/Faulkner data but prioritized through a Kuma lens.
MASTER_DICTIONARY = [
    {"glyph": "𓈖", "mdc": "n", "trans": "n", "fr": "de / à", "en": "of / to", "cat": "Vibration"},
    {"glyph": "𓂋", "mdc": "r", "trans": "r", "fr": "bouche / parole", "en": "mouth / speech", "cat": "Action"},
    {"glyph": "𓋹", "mdc": "anx", "trans": "ꜥnḫ", "fr": "vie / souffle", "en": "life / breath", "cat": "Principle"},
    {"glyph": "𓄤", "mdc": "nfr", "trans": "nfr", "fr": "perfection / beauté", "en": "perfection / beauty", "cat": "Quality"},
    {"glyph": "𓀭", "mdc": "ntr", "trans": "ntr", "fr": "divinité / force", "en": "divinity / force", "cat": "Principle"},
    {"glyph": "𓃀", "mdc": "b", "trans": "b", "fr": "âme / pied", "en": "soul / foot", "cat": "Action"},
    {"glyph": "𓅓", "mdc": "m", "trans": "m", "fr": "dans / par", "en": "in / through", "cat": "Vibration"},
    {"glyph": "𓏠", "mdc": "mn", "trans": "mn", "fr": "stable / durable", "en": "stable / durable", "cat": "Quality"},
    {"glyph": "𓇳", "mdc": "ra", "trans": "rꜥ", "fr": "soleil / créateur", "en": "sun / creator", "cat": "Cosmos"},
    {"glyph": "𓂓", "mdc": "ka", "trans": "kꜣ", "fr": "énergie / double", "en": "energy / double", "cat": "Principle"},
]

# --- UI LANGUAGE DATA ---
UI = {
    "fr": {
        "title": "Lexique Kemet & Méthode Kuma",
        "search": "Rechercher (MDC, Français, Anglais, Hiéroglyphe)",
        "list_title": "Dictionnaire Complet",
        "kuma_header": "Analyse Approfondie (Dibombari Mbock)",
        "comp_header": "Tableau Comparatif Soudanais (Négro-Africain)",
        "vibr_label": "Vibration Phonique :",
        "logic_label": "Logique Cosmogonique :",
    },
    "en": {
        "title": "Kemet Lexicon & Kuma Method",
        "search": "Search (MDC, French, English, Hieroglyph)",
        "list_title": "Full Dictionary",
        "kuma_header": "In-depth Kuma Analysis (Dibombari Mbock)",
        "comp_header": "Sudanese (Negro-African) Comparative Table",
        "vibr_label": "Phonic Vibration:",
        "logic_label": "Cosmogonic Logic:",
    }
}

# --- STATE MANAGEMENT ---
if 'lang' not in st.session_state: st.session_state.lang = 'fr'
def swap_lang(): st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'

# --- UI LAYOUT ---
T = UI[st.session_state.lang]
st.sidebar.button("Français / English", on_click=swap_lang)
st.title(T["title"])

# 1. THE DYNAMIC SELECTOR (List all words)
# We create a label for the dropdown showing Glyphs + Translation
labels = [f"{d['glyph']} | {d['mdc']} | {d['fr'] if st.session_state.lang == 'fr' else d['en']}" for d in MASTER_DICTIONARY]

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader(T["list_title"])
    search_input = st.text_input(T["search"], placeholder="Ex: nfr, life, 𓈖")
    
    # Filter list based on search
    filtered_list = [l for l in labels if search_input.lower() in l.lower()]
    selected_label = st.radio("Sélecteur de mots :", filtered_list, label_visibility="collapsed")

# 2. SELECTION LOGIC
if selected_label:
    glyph_char = selected_label.split(" | ")[0]
    data = next(item for item in MASTER_DICTIONARY if item["glyph"] == glyph_char)
    
    with col_right:
        # Drawing the hieroglyph
        st.markdown(f"""
            <div style="text-align:center; padding:20px; border:2px solid #D4AF37; border-radius:15px; background-color:#111;">
                <h1 style="font-size:120px; color:#D4AF37; margin:0;">{data['glyph']}</h1>
                <p style="color:#aaa;">MDC: {data['mdc']} | Trans: {data['trans']}</p>
            </div>
        """, unsafe_allow_html=True)

        # 3. KUMA METHOD ANALYSIS
        st.subheader(T["kuma_header"])
        
        # Breakdown the word using Mbock's phonosemantics
        analysis_cols = st.columns(len(data['mdc']))
        for i, char in enumerate(data['mdc'].upper()):
            if char in KUMA_VIBRATIONS:
                with st.expander(f"Racine '{char}'", expanded=True):
                    st.write(KUMA_VIBRATIONS[char])

        # Deep Contextual Analysis (Dibombari Mbock Style)
        st.info(f"**{T['logic_label']}**\n\nDans la pensée de Dibombari Mbock, '{data['trans']}' ne décrit pas seulement un objet, "
                f"mais un processus de manifestation. Chaque signe est un 'Kuma' (une parole agissante) qui relie le monde "
                f"visible aux lois invisibles de l'univers Negro-Africain.")

        # 4. AFRICAN LEXIC TABLE (Top 10 Languages)
        st.subheader(T["comp_header"])
        # Simulating the comparative data found on Kemlex.org
        comparative_data = [
            {"Famille": "Sénégambien", "Langue": "Wolof", "Cognat": f"Root-{data['mdc']}", "Sens": data['fr']},
            {"Famille": "Bantou", "Langue": "Kikongo", "Cognat": "N-zila", "Sens": "Flow/Path"},
            {"Famille": "Soudanais", "Langue": "Dogon", "Cognat": "Ama", "Sens": "Creation"},
            {"Famille": "Mandingue", "Langue": "Bambara", "Cognat": "Da", "Sens": "Opening"},
            {"Famille": "Nilotique", "Langue": "Dinka", "Cognat": "Ran", "Sens": "Being"},
        ]
        st.table(pd.DataFrame(comparative_data))

st.markdown("---")
st.caption("Source: Méthode Kuma de Dibombari Mbock / Dictionnaires Faulkner, Vygus, Gardiner.")
