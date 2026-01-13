import streamlit as st
import pandas as pd

# Mock Data Structure - In a production app, this would be a large JSON/SQL database
# representing the merge of Vygus, Faulkner, and Gardiner.
DICTIONARY_DB = [
    {
        "hieroglyph": "𓄤",
        "transliteration": "nfr",
        "translation": "good, beautiful, happy",
        "gardiner_code": "F35",
        "kuma_analysis": "Root: NF + R. In Kuma, relates to the vital breath and harmony. Connection to Bantu 'N-Pher' (perfection).",
        "source": "Gardiner, Faulkner"
    },
    {
        "hieroglyph": "𓂋",
        "transliteration": "r",
        "translation": "mouth, speech, door",
        "gardiner_code": "D21",
        "kuma_analysis": "The opening of the creative verb. Linked to the solar vibration in Dibombari Mbock’s methodology.",
        "source": "Vygus, Mbock"
    }
]

def search_logic(query):
    query = query.lower()
    results = [
        item for item in DICTIONARY_DB 
        if query in item['transliteration'].lower() 
        or query in item['translation'].lower() 
        or query == item['hieroglyph']
    ]
    return results

# --- UI Layout ---
st.set_page_config(page_title="Kemetic Lexicon & Kuma Analysis", layout="wide")

st.title("𓋹 Kemetic Lexicon Explorer")
st.markdown("### Integrated Dictionary (Vygus, Faulkner, Gardiner) & Kuma Method Analysis")

# Sidebar for Hieroglyph Dropdown
st.sidebar.header("Hieroglyph Picker")
all_glyphs = [item['hieroglyph'] for item in DICTIONARY_DB]
selected_glyph = st.sidebar.selectbox("Choose a symbol to analyze:", [""] + all_glyphs)

# Main Search Navigation
search_query = st.text_input("Search by Transliteration (e.g., 'nfr'), Translation ('good'), or Hieroglyph:", value=selected_glyph)

if search_query:
    results = search_logic(search_query)
    
    if results:
        for res in results:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"<h1 style='font-size: 100px; text-align: center;'>{res['hieroglyph']}</h1>", unsafe_allow_html=True)
                st.caption(f"Gardiner Code: {res['gardiner_code']}")
            
            with col2:
                st.subheader(f"Analysis: {res['transliteration']}")
                st.write(f"**Standard Translation:** {res['translation']}")
                st.info(f"**Sources:** {res['source']}")
                
                with st.expander("✨ Kuma Method Analysis (Dibombari Mbock)", expanded=True):
                    st.write(res['kuma_analysis'])
                    st.markdown("*Reference: Principes fondamentaux de la methode Kuma*")
    else:
        st.error("No entries found. Try adjusting your search or transliteration style.")

# Dynamic UX: Table view similar to Kemlex
if st.checkbox("Show Full Comparative Table"):
    df = pd.DataFrame(DICTIONARY_DB)
    st.table(df[['hieroglyph', 'transliteration', 'translation', 'source']])
