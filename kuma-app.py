import streamlit as st
import pdfplumber
import re

# Internal Fallback
default_kuma = {
    "𓇇 (Reed)": {"nature": "Vibrating plant", "logic": "Breath of life", "link": "Kôm"}
}

st.set_page_config(page_title="Kuma PDF Scholar v2", page_icon="𓂀", layout="wide")
st.title("𓂀 Kuma Method: Advanced PDF Decoder")

# Sidebar
st.sidebar.header("📁 Source Document")
uploaded_pdf = st.sidebar.file_uploader("Upload PDF Research", type=["pdf"])
debug_mode = st.sidebar.checkbox("Enable Debug (Show Raw Text)")

kuma_data = {}

if uploaded_pdf is not None:
    with pdfplumber.open(uploaded_pdf) as pdf:
        full_text = ""
        for page in pdf.pages:
            # pdfplumber is much better at keeping words together
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
        
        if debug_mode:
            with st.expander("🔍 Raw Text Found in PDF"):
                st.text(full_text)

        # Improved Regex: Finds a Hieroglyph followed by lines of text
        # Looks for Unicode range U+13000 to U+1342F
        pattern = r'([\u13000-\u1342F])\s*(.*?)(?=[\u13000-\u1342F]|$)'
        matches = re.findall(pattern, full_text, re.DOTALL)

        if matches:
            for glyph, content in matches:
                lines = [l.strip() for l in content.strip().split('\n') if l.strip()]
                kuma_data[f"{glyph} (Extracted)"] = {
                    "nature": lines[0] if len(lines) > 0 else "N/A",
                    "logic": lines[1] if len(lines) > 1 else "Extracted from PDF context.",
                    "link": lines[2] if len(lines) > 2 else "Check original document."
                }
            st.sidebar.success(f"Parsed {len(kuma_data)} Kuma entries!")
        else:
            st.sidebar.error("No Hieroglyph characters detected. Is this a scanned image?")
else:
    kuma_data = default_kuma

# Main View
if kuma_data:
    selected_key = st.sidebar.selectbox("Analyze Sign:", list(kuma_data.keys()))
    entry = kuma_data[selected_key]
    glyph = selected_key.split()[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""<div style="background:#1e1e1e; padding:40px; border-radius:15px; text-align:center;">
                    <h1 style="font-size:150px; color:#FFD700;">{glyph}</h1></div>""", unsafe_allow_html=True)
    with col2:
        st.header("Metaphysical Decipherment")
        st.info(f"**Biological Nature:** {entry['nature']}")
        st.success(f"**Symbolic Logic:** {entry['logic']}")
        st.warning(f"**African Context:** {entry['link']}")
