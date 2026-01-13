import streamlit as st
import PyPDF2
import re

# 1. Fallback / Default Data
default_kuma = {
    "𓇇 (Reed)": {
        "biological_nature": "Vibrating aquatic plant",
        "kuma_symbolism": "Movement of the soul.",
        "african_link": "Kôm (Bassa)"
    }
}

st.set_page_config(page_title="Kuma PDF Scholar", page_icon="𓂀", layout="wide")

st.title("𓂀 Kuma Method: PDF Intelligence")
st.markdown("Upload a PDF document containing your research on Ethiopian letters.")

# 2. Sidebar: PDF Upload
st.sidebar.header("📁 Source Document")
uploaded_pdf = st.sidebar.file_uploader("Upload Kuma Research (PDF)", type=["pdf"])

kuma_data = {}

if uploaded_pdf is not None:
    try:
        # Extract Text from PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n"
        
        # 3. Logic: Extracting Hieroglyphic Data
        # This regex looks for a Hieroglyph character followed by a description
        # It assumes a format like: 𓃀 Description...
        # Hieroglyph unicode range is roughly \u13000-\u1342F
        glyphs_found = re.findall(r'([\u13000-\u1342F])\s*(.*?)(?=[\u13000-\u1342F]|$)', full_text, re.DOTALL)
        
        if glyphs_found:
            for glyph, content in glyphs_found:
                # Clean up the extracted text
                clean_content = content.strip().split('\n')
                kuma_data[f"{glyph} (Extracted)"] = {
                    "biological_nature": clean_content[0] if len(clean_content) > 0 else "N/A",
                    "kuma_symbolism": " ".join(clean_content[1:3]) if len(clean_content) > 1 else "Extracted from text",
                    "african_link": clean_content[-1] if len(clean_content) > 2 else "See PDF"
                }
            st.sidebar.success(f"Extracted {len(kuma_data)} signs from PDF!")
        else:
            st.sidebar.warning("No hieroglyphs detected. Ensure the PDF contains Unicode hieroglyphs.")
            kuma_data = default_kuma

    except Exception as e:
        st.sidebar.error(f"Error processing PDF: {e}")
        kuma_data = default_kuma
else:
    kuma_data = default_kuma

# 4. Main Interface
if kuma_data:
    all_keys = list(kuma_data.keys())
    selected_key = st.sidebar.selectbox("Analyze Extracted Sign:", all_keys)

    col1, col2 = st.columns([1, 2])

    with col1:
        glyph = selected_key.split()[0]
        st.markdown(
            f"""
            <div style="background-color: #262730; border-radius: 15px; padding: 30px; text-align: center; border: 2px solid #FFD700;">
                <h1 style="font-size: 150px; color: #FFD700; margin: 0;">{glyph}</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col2:
        st.header("Metaphysical Decipherment")
        entry = kuma_data[selected_key]
        
        st.subheader("Biological Signature")
        st.info(entry['biological_nature'])
        
        st.subheader("Symbolic Logic")
        st.write(entry['kuma_symbolism'])
        
        st.subheader("African Connection")
        st.warning(entry['african_link'])

st.divider()
st.caption("Note: PDF extraction works best if the hieroglyphs are actual text characters, not images.")
