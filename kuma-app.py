import streamlit as st
import pandas as pd

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="Kuma Lexicon Pro", layout="wide")

# --- DATA INITIALIZATION ---
# In a full-scale app, this would be: pd.read_csv('vygus_faulkner_merged.csv')
# Here we simulate the depth of the dictionaries
MASTER_DB = [
    {
        "hieroglyph": "𓈖",
        "mdc": "n",
        "transliteration": "n",
        "translation_en": "of, to, in, for",
        "translation_fr": "de, à, dans, pour",
        "gardiner": "N35",
        "dictionary_ref": "Vygus p.1520, Faulkner p.120",
        "kuma_deep_analysis": {
            "root_vibration": "N- (Energy of Movement)",
            "cosmogony": "Represents the Nun (Primordial Waters). The wave is the initial vibration of the universe.",
            "phonosemantics": "The 'N' sound in Kuma represents 'Emergence' or 'Transmission'. It is the link between the spirit and the matter.",
            "bantu_logic": "Linked to the Bantu prefix 'N-' denoting a being or a living force (e.g., Ntu, Nyambe)."
        },
        "african_comparative": [
            {"lang": "Wolof", "term": "Ndox", "meaning": "Water / Eau"},
            {"lang": "Kikongo", "term": "Maza", "meaning": "Water (as vital flow) / Eau"},
            {"lang": "Lingala", "term": "Nini", "meaning": "What/Identity / Quoi"},
            {"lang": "Fang", "term": "Enim", "meaning": "Life-force / Force vitale"}
        ]
    },
    {
        "hieroglyph": "𓋹",
        "mdc": "anx",
        "transliteration": "ꜥnḫ",
        "translation_en": "life, to live",
        "translation_fr": "vie, vivre",
        "gardiner": "S34",
        "dictionary_ref": "Vygus p.240, Gardiner p.508",
        "kuma_deep_analysis": {
            "root_vibration": "NX (Breath/Expansion)",
            "cosmogony": "The union of opposites (Masculine/Feminine). The key that unlocks the door of the afterlife.",
            "phonosemantics": "Analysis of the 'NX' (Ankh) as the vital friction that produces heat and consciousness.",
            "bantu_logic": "Cognate with 'H-N-K' roots in West Africa meaning 'to breathe' or 'to grant' (Hink)."
        },
        "african_comparative": [
            {"lang": "Bambara", "term": "Nkwa", "meaning": "Life / Vie"},
            {"lang": "Yoruba", "term": "Emi", "meaning": "Spirit/Breath / Esprit"},
            {"lang": "Zulu", "term": "Inyoni", "meaning": "Vital spark / Étincelle"},
            {"lang": "Mende", "term": "Ngeya", "meaning": "Binding of life / Lien de vie"}
        ]
    }
]

# --- UI TRANSLATIONS ---
UI_TEXT = {
    "en": {
        "search_label": "Search (MDC, English, French, or Hieroglyph)",
        "pick_label": "Or Select from Full Dictionary (Vygus/Faulkner/Gardiner)",
        "kuma_title": "Deeper Kuma Method Analysis",
        "tab_comp": "Sudanese/Negro-African Comparative Table",
        "sidebar_info": "Methodology: Dibombari Mbock"
    },
    "fr": {
        "search_label": "Recherche (MDC, Français, Anglais ou Hiéroglyphe)",
        "pick_label": "Ou sélectionnez dans le dictionnaire complet",
        "kuma_title": "Analyse Approfondie Méthode Kuma",
        "tab_comp": "Table Comparative Soudanaise/Négro-Africaine",
        "sidebar_info": "Méthodologie : Dibombari Mbock"
    }
}

# --- SESSION STATE ---
if 'lang' not in st.session_state: st.session_state.lang = 'fr'
def toggle_lang(): st.session_state.lang = 'en' if st.session_state.lang == 'fr' else 'fr'

# --- SIDEBAR ---
with st.sidebar:
    st.button("Toggle Language / Changer de Langue", on_click=toggle_lang)
    st.markdown(f"### {UI_TEXT[st.session_state.lang]['sidebar_info']}")
    st.info("Integrating Vygus, Faulkner, Gardiner Sign Lists with Kuma Phonosemantics.")

# --- MAIN INTERFACE ---
st.title("𓆃 Kemet Lexicon Pro")
L = UI_TEXT[st.session_state.lang]

# 1. SEARCH NAVIGATION
search_col1, search_col2 = st.columns([1, 1])
with search_col1:
    query = st.text_input(L["search_label"], placeholder="Ex: anx, life, 𓋹...")
with search_col2:
    # Full Dictionary List from Vygus/Faulkner
    all_labels = [f"{d['hieroglyph']} | {d['mdc']} | {d['translation_en' if st.session_state.lang=='en' else 'translation_fr']}" for d in MASTER_DB]
    selected_label = st.selectbox(L["pick_label"], options=[""] + all_labels)

# Filtering logic
selected_entry = None
if query:
    for entry in MASTER_DB:
        if query.lower() in [entry['mdc'], entry['translation_en'].lower(), entry['translation_fr'].lower(), entry['hieroglyph']]:
            selected_entry = entry
            break
elif selected_label:
    glyph_part = selected_label.split(" | ")[0]
    selected_entry = next(d for d in MASTER_DB if d['hieroglyph'] == glyph_part)

# 2. DYNAMIC DISPLAY
if selected_entry:
    st.divider()
    
    # 2. Draw Symbol + Basic Data
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"<div style='background-color:#1e1e1e; padding:30px; border-radius:10px; border: 2px solid #d4af37;'>"
                    f"<h1 style='font-size:150px; text-align:center; color:#d4af37;'>{selected_entry['hieroglyph']}</h1>"
                    f"</div>", unsafe_allow_html=True)
        st.caption(f"Ref: {selected_entry['dictionary_ref']}")
        st.metric("Gardiner", selected_entry['gardiner'])

    with c2:
        st.header(f"{selected_entry['transliteration']} - {selected_entry['translation_fr' if st.session_state.lang=='fr' else 'translation_en']}")
        
        # 3. Deep Kuma Analysis
        st.subheader(L["kuma_title"])
        kuma = selected_entry['kuma_deep_analysis']
        
        with st.expander("Vibration & Phonosemantics", expanded=True):
            st.write(f"**Root Vibration:** {kuma['root_vibration']}")
            st.write(f"**Cosmogony:** {kuma['cosmogony']}")
            st.markdown(f"**Mbock Analysis:** {kuma['phonosemantics']}")
        
        with st.expander("Bantu/African Structural Link"):
            st.write(kuma['bantu_logic'])

    # 4. Comparative Table (Top 10 Sudanese/Sub-saharan)
    st.divider()
    st.subheader(L["tab_comp"])
    comp_df = pd.DataFrame(selected_entry['african_comparative'])
    st.dataframe(comp_df, use_container_width=True)

else:
    st.write("Please search or select a term to begin analysis.")
