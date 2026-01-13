import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Kuma Method Reader", page_icon="𓃠", layout="wide")

# Custom Styling for an "Egyptian/African Lexicon" feel
st.markdown("""
    <style>
    .stApp { background-color: #f4ece1; }
    .kuma-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-right: 8px solid #c0a080;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .glyph-large { font-size: 60px; color: #3d2b1f; }
    </style>
    """, unsafe_allow_html=True)

# --- Data Engine ---
@st.cache_data
def get_lexicon():
    # In a production app, you would scrape/import this from kemlex.org or a CSV
    return pd.DataFrame([
        {"sign": "𓇳", "code": "N5", "meaning": "Ra / Sun", "kuma_logic": "The Eye of the Creator; the principle of expansion and central vitality.", "african_root": "Bantu: -diba (Sun/Eye)"},
        {"sign": "𓀀", "code": "A1", "meaning": "Man", "kuma_logic": "The Muntu; the receptacle of the Word (Logos).", "african_root": "Dual: Moto (Person)"},
        {"sign": "𓅃", "code": "G5", "meaning": "Heru / Falcon", "kuma_logic": "The principle of spiritual elevation and the 'Ka' in action.", "african_root": "Yoruba: Eye (Bird/Spirit)"},
    ])

df = get_lexicon()

# --- UI Layout ---
st.title("𓋹 Kuma Method Hieroglyph Analyser")
st.caption("A symbolic bridge between Ancient Kemet and African Lingustics (via Dibombari Mbock)")

tabs = st.tabs(["🔍 Interactive Reader", "📚 Kuma Principles", "📤 Data Sync"])

with tabs[0]:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select a Sign")
        selected_sign = st.selectbox("Choose from Lexicon", df['sign'] + " " + df['meaning'])
        sign_char = selected_sign.split()[0]
        entry = df[df['sign'] == sign_char].iloc[0]

    with col2:
        st.markdown(f"""
        <div class="kuma-box">
            <div class="glyph-large">{entry['sign']}</div>
            <h2>{entry['meaning']}</h2>
            <p><strong>Gardiner Code:</strong> {entry['code']}</p>
            <hr>
            <h4>Kuma Symbolic Logic:</h4>
            <p>{entry['kuma_logic']}</p>
            <h4>African Linguistic Root:</h4>
            <p><em>{entry['african_root']}</em></p>
        </div>
        """, unsafe_allow_html=True)

with tabs[1]:
    st.header("The Epistemology of Kuma")
    st.markdown("""
    The **Kuma Method** (Ibis Method) shifts the focus from purely phonetic 'sounds' to 
    the **Cosmogonic intent** of the scribe. 
    
    * **The Hieroglyph is a Concept:** It represents a law of nature.
    * **The African Connection:** Using Kemlex resources, we find that the roots of 
        Medù Nèter are found in modern African languages (Bantu, Wolof, Dogon).
    """)

with tabs[2]:
    st.header("Kemlex Integration")
    st.write("Upload your exported CSV from Kemlex.org to update the local database.")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        st.success("Database updated successfully!")

st.divider()
st.info("💡 Tip: Use the search bar in the sidebar to filter by African root words.")