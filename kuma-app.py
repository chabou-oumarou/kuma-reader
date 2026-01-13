import streamlit as st
import json

# 1. Fallback / Template Data
default_kuma = {
    "𓇇 (Reed)": {
        "phonetic": "i",
        "biological_nature": "Vibrating aquatic plant",
        "kuma_symbolism": "The vibration of the primordial word; movement of the soul.",
        "african_link": "Kôm (Bassa) - to create or speak."
    },
    "𓃀 (Leg)": {
        "phonetic": "b",
        "biological_nature": "Lower limb / Support",
        "kuma_symbolism": "The principle of foundation and implementation of action.",
        "african_link": "Ba/Be (Bantu) - to exist or become."
    }
}

# 2. Page Configuration
st.set_page_config(page_title="Kuma Reader Pro", page_icon="𓂀", layout="wide")

st.title("𓂀 Kuma Method: Symbolic Decoder")
st.markdown("---")

# 3. Sidebar: File Management
st.sidebar.header("📁 Dictionary Management")

# Upload Functionality
uploaded_file = st.sidebar.file_uploader("Upload your Kuma JSON Dictionary", type=["json"])

if uploaded_file is not None:
    try:
        kuma_data = json.load(uploaded_file)
        st.sidebar.success("Custom Dictionary Active")
    except Exception as e:
        st.sidebar.error(f"Format Error: {e}")
        kuma_data = default_kuma
else:
    kuma_data = default_kuma
    st.sidebar.info("Using default template data.")

# Template Download (Handy for the user to get started)
template_json = json.dumps(default_kuma, indent=4)
st.sidebar.download_button(
    label="Download JSON Template",
    data=template_json,
    file_name="kuma_template.json",
    mime="application/json"
)

# 4. Main Interface: Sign Selection
st.sidebar.divider()
st.sidebar.subheader("Navigation")
all_keys = list(kuma_data.keys())
selected_key = st.sidebar.selectbox("Select a sign for analysis:", all_keys)

if selected_key:
    entry = kuma_data[selected_key]
    # Extract just the glyph (the first character)
    glyph = selected_key.split()[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        # High-impact glyph rendering
        st.markdown(
            f"""
            <div style="background-color: #1e1e1e; border-radius: 15px; padding: 20px; text-align: center;">
                <h1 style="font-size: 160px; color: #FFD700; margin: 0;">{glyph}</h1>
                <p style="color: #888;">{selected_key}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col2:
        st.header("Metaphysical Intelligence")
        
        tab1, tab2 = st.tabs(["Biological Identity", "African Context"])
        
        with tab1:
            st.subheader("Nature of the Object")
            st.info(f"**Biology:** {entry['biological_nature']}")
            st.subheader("Kuma Symbolism")
            st.write(entry['kuma_symbolism'])
            
        with tab2:
            st.subheader("Linguistic Roots")
            st.warning(f"**African Cultural Link:** {entry['african_link']}")

# 5. Composition Workspace (Experimental)
st.divider()
st.subheader("🧪 Kuma Composition")
st.write("Combine multiple signs to see the synthesis of their biological principles.")

selected_sequence = st.multiselect("Select signs to combine:", all_keys)

if selected_sequence:
    comp_cols = st.columns(len(selected_sequence))
    combined_logic = []
    
    for i, key in enumerate(selected_sequence):
        with comp_cols[i]:
            st.markdown(f"<h2 style='text-align: center;'>{key.split()[0]}</h2>", unsafe_allow_html=True)
            combined_logic.append(kuma_data[key]['kuma_symbolism'])
    
    with st.expander("See Synthesized Meaning"):
        for logic in combined_logic:
            st.write(f"• {logic}")

st.markdown("---")
st.caption("Conceptualized from the work of Dibombari Mbock on Ethiopian Symbolic Letters.")
