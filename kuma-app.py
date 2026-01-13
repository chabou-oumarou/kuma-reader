import streamlit as st

# Data Dictionary: Mapping Hieroglyphs to Traditional and Kuma Interpretations
# Note: In a production app, you would use more extensive image assets.
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
    }
}

# App UI
st.set_page_config(page_title="Kuma Method Practice", page_icon="𓂀")

st.title("𓂀 Kuma Method Practice Tool")
st.markdown("""
Traditional Egyptology focuses on *how* a sign sounds. The **Kuma Method** focuses on *what* a sign is. 
Use this tool to practice seeing the 'Biological Signature' of the Ethiopian letters.
""")

st.divider()

# Sidebar / Input
st.sidebar.header("Select a Hieroglyph")
selected_sign = st.sidebar.selectbox("Choose a sign to analyze:", list(kuma_data.keys()))

# Main Display
col1, col2 = st.columns([1, 2])

with col1:
    st.header("The Sign")
    # Displaying the sign large
    st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{selected_sign.split()[0]}</h1>", unsafe_allow_name=True)

with col2:
    st.header("Decipherment")
    data = kuma_data[selected_sign]
    
    st.subheader("Traditional (Phonetic)")
    st.code(data['phonetic'])
    
    st.subheader("Biological Nature")
    st.info(data['biological_nature'])

st.divider()

# Kuma Specific Analysis
st.header("Kuma Method Insight")
st.write(f"**Symbolic Meaning:** {data['kuma_symbolism']}")
st.write(f"**African Cultural Link:** {data['african_link']}")

# Practice Section
st.sidebar.divider()
st.sidebar.subheader("Practice Mode")
user_reflection = st.sidebar.text_area("Observation: What else does this object symbolize in nature?")

if st.sidebar.button("Submit Reflection"):
    st.success("Reflection saved. Remember: To the Kuma initiate, the image is the reality!")

st.markdown("---")
st.caption("Based on 'Principes Généraux des lettres symboliques éthiopiennes' by Dibombari Mbock.")
