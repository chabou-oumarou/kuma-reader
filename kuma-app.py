import streamlit as st

# Data Dictionary: Mapping Hieroglyphs to Traditional and Kuma Interpretations
kuma_data = {
    "𓀀 (Man)": {
        "phonetic": "None (Determinate)",
        "biological_nature": "Human Being / Consciousness",
        "kuma_symbolism": "The 'I' or the Creator's representative. Represents the principle of social order and verticality.",
        "african_link": "Connected to the root 'muntu' or 'ntu' (humanity/being) found in Bantu languages."
    },
    "𓃠 (Cat)": {
        "phonetic": "miw",
        "biological_nature": "Feline / Predator with night vision",
        "kuma_symbolism": "The principle of vigilance and protection. The ability to see in the dark (the unseen world).",
        "african_link": "Linked to the concept of 'Mau' - the divine light that strikes the shadows."
    },
    "𓇇 (Reed Leaf)": {
        "phonetic": "i / a",
        "biological_nature": "Vibrating aquatic plant",
        "kuma_symbolism": "The Breath of Life. Symbolizes the vibration of the word (Kuma) moving through the atmosphere.",
        "african_link": "Relates to the 'vibration' of creation found in Dogon and Bassa cosmogonies."
    },
    "𓃀 (Leg)": {
        "phonetic": "b",
        "biological_nature": "Lower limb / Support",
        "kuma_symbolism": "The principle of Foundation and Locomotion. That which carries the 'Ka' (spirit) forward.",
        "african_link": "Linked to the 'B' root in many languages signifying 'to become' or 'to exist' (e.g., Ba/Be)."
    },
    "𓐍 (Placenta/Sieve)": {
        "phonetic": "kh",
        "biological_nature": "Filter / Organ of nutrition",
        "kuma_symbolism": "The principle of discernment and filtering. Separating the pure from the impure.",
        "african_link": "Commonly associated with the 'Khe' or 'Khu' ancestral spirit logic."
    }
}

# App UI
st.set_page_config(page_title="Kuma Method Practice", page_icon="𓂀", layout="wide")

st.title("𓂀 Kuma Method Practice Tool")
st.markdown("""
Traditional Egyptology focuses on *how* a sign sounds. The **Kuma Method** focuses on *what* a sign is biologically and symbolically.
""")

st.divider()

# Sidebar / Input
st.sidebar.header("Navigation")
selected_sign = st.sidebar.selectbox("Choose a sign to analyze:", list(kuma_data.keys()))

# Main Display
col1, col2 = st.columns([1, 2])

with col1:
    st.header("The Sign")
    # FIXED: Changed unsafe_allow_name to unsafe_allow_html
    glyph_char = selected_sign.split()[0]
    st.markdown(f"<h1 style='text-align: center; font-size: 150px; color: #E67E22;'>{glyph_char}</h1>", unsafe_allow_html=True)

with col2:
    st.header("Decipherment")
    data = kuma_data[selected_sign]
    
    st.write("**Traditional Phonetic:**")
    st.code(data['phonetic'])
    
    st.write("**Biological Nature:**")
    st.info(data['biological_nature'])

st.divider()

# Kuma Specific Analysis Section
st.header("Kuma Method Insight")
st.success(f"**Symbolic Meaning:** {data['kuma_symbolism']}")
st.warning(f"**African Cultural Link:** {data['african_link']}")

# Footer
st.markdown("---")
st.caption("Application logic based on Dibombari Mbock's Kuma Method.")
