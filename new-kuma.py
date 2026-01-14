# kuma_streamlit_app.py
"""
Application Streamlit pour utiliser la Méthode Kuma à partir d'un dictionnaire hiéroglyphique Vygus en PDF.

Fonctionnalités principales
- Upload d'un PDF (Vygus)
- Extraction texte via pdfplumber
- Détection automatique d'entrées hiéroglyphiques (heuristique)
- Sélection d'un terme / hiéroglyphe
- Affichage du signe, translittération, traduction
- Tableau comparatif des traductions dans 10 langues subsahariennes
- Possibilité d'ajouter / corriger manuellement les traductions et de les sauvegarder localement

Limites
- Le format exact du dictionnaire Vygus peut varier. Le parser est heuristique et peut nécessiter ajustements.
- Les traductions automatiques nécessitent une API externe (optionnelle). Sinon, on utilise un fichier CSV local pour les traductions.
"""

import streamlit as st
import io
import re
import csv
import json
from typing import List, Dict, Tuple, Optional

# PDF extraction
try:
    import pdfplumber
except Exception:
    pdfplumber = None

# Utilities

DEFAULT_LANGUAGES = [
    "Hausa",
    "Zarma",
    "Wolof",
    "Bambara",
    "Fula",
    "Yoruba",
    "Igbo",
    "Swahili",
    "Kinyarwanda",
    "Lingala"
]

TRANSLATION_CSV = "kuma_translations.csv"

st.set_page_config(page_title="Méthode Kuma — Dictionnaire Vygus", layout="wide")

# Parsing heuristics
ENTRY_REGEXES = [
    # Heuristic: Sign glyph or code then transliteration then translation
    # Example lines (heuristic): "G17 𓂋 r r 'mouth'  (translation: bouche)"
    r"^(?P<sign>[\w\-\u1300-\uFFFF]+)\s+[-–]?\s*(?P<translit>[A-Za-z0-9'ˁˀ]+)\s+[-–]?\s*(?P<translation>.+)$",
    # Another heuristic: "Sign: translit — translation"
    r"^(?P<sign>.+?)\s*[:]\s*(?P<translit>[^—\-–]+)\s*[—\-–]\s*(?P<translation>.+)$"
]

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber non installé. Installez-le avec pip install pdfplumber.")
    text_pages = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                text_pages.append(txt)
    return "\n\n".join(text_pages)

def find_entries_from_text(text: str) -> List[Dict]:
    """
    Heuristique pour extraire des entrées du dictionnaire.
    Retourne une liste d'objets {id, sign, translit, translation, raw}.
    """
    entries = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    id_counter = 1
    for ln in lines:
        matched = False
        for rx in ENTRY_REGEXES:
            m = re.match(rx, ln)
            if m:
                sign = m.groupdict().get("sign", "").strip()
                translit = m.groupdict().get("translit", "").strip()
                translation = m.groupdict().get("translation", "").strip()
                entries.append({
                    "id": str(id_counter),
                    "sign": sign,
                    "transliteration": translit,
                    "translation": translation,
                    "raw": ln
                })
                id_counter += 1
                matched = True
                break
        if not matched:
            # Optionally treat single-line words as possible translations lines
            # Skip for now
            pass
    return entries

# Translation management

def load_translations_csv(path: str) -> Dict[str, Dict[str, str]]:
    """
    CSV format expected:
    entry_id;language;translation
    or
    sign;language;translation
    """
    data = {}
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) < 3:
                    continue
                key = row[0].strip()
                lang = row[1].strip()
                tr = row[2].strip()
                if key not in data:
                    data[key] = {}
                data[key][lang] = tr
    except FileNotFoundError:
        # Return empty mapping if file absent
        return {}
    return data

def save_translations_csv(path: str, mapping: Dict[str, Dict[str, str]]):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for key, langs in mapping.items():
            for lang, tr in langs.items():
                writer.writerow([key, lang, tr])

# Optional: simple placeholder translator (no external API)
def placeholder_translate(text: str, target_lang: str) -> str:
    # This is a placeholder: it returns the original text prefixed by language code.
    # Replace with real API calls if desired.
    return f"[{target_lang}] {text}"

# Streamlit UI

st.title("Méthode Kuma — Explorateur de dictionnaire Vygus")
st.markdown("Uploadez un PDF du dictionnaire Vygus, sélectionnez une entrée et comparez les traductions dans 10 langues subsahariennes.")

with st.sidebar:
    st.header("Paramètres")
    uploaded_file = st.file_uploader("Upload PDF Vygus", type=["pdf"])
    st.markdown("**Langues comparatives**")
    langs = st.multiselect("Choisir 10 langues (ou moins)", DEFAULT_LANGUAGES, default=DEFAULT_LANGUAGES)
    st.markdown("**Traductions**")
    use_local_csv = st.checkbox("Charger traductions depuis fichier local kuma_translations.csv", value=True)
    allow_auto_translate = st.checkbox("Autoriser traduction automatique placeholder", value=True)
    if use_local_csv:
        st.markdown("Le fichier local doit être au format CSV avec séparateur ';' : clé;langue;traduction")
    st.markdown("---")
    st.markdown("**Sauvegarde**")
    save_button = st.button("Sauvegarder traductions locales maintenant")

# Load existing translations
translations_map = {}
if use_local_csv:
    translations_map = load_translations_csv(TRANSLATION_CSV)

# Process upload
entries = []
raw_text = ""
if uploaded_file is not None:
    try:
        pdf_bytes = uploaded_file.read()
        raw_text = extract_text_from_pdf_bytes(pdf_bytes)
        st.success("PDF traité, extraction texte terminée.")
        entries = find_entries_from_text(raw_text)
        if not entries:
            st.warning("Aucune entrée détectée automatiquement. Le parser est heuristique. Vous pouvez coller manuellement des entrées ci-dessous.")
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du PDF : {e}")

# Manual paste fallback
st.subheader("Aperçu du texte extrait")
if raw_text:
    st.text_area("Texte extrait (aperçu)", raw_text[:5000], height=200)
else:
    st.info("Aucun PDF chargé ou extraction vide. Vous pouvez coller ici un extrait du dictionnaire pour le parser.")
    manual_text = st.text_area("Coller un extrait du dictionnaire ici", height=200)
    if manual_text:
        raw_text = manual_text
        entries = find_entries_from_text(raw_text)
        if entries:
            st.success(f"{len(entries)} entrées détectées dans le texte collé.")
        else:
            st.warning("Aucune entrée détectée dans le texte collé.")

# Show entries list and selection
st.subheader("Entrées détectées")
if entries:
    options = [f"{e['id']} — {e['sign']} — {e['transliteration']} — {e['translation']}" for e in entries]
    choice = st.selectbox("Sélectionner une entrée", options)
    selected_id = choice.split(" — ")[0]
    selected_entry = next((e for e in entries if e['id'] == selected_id), None)
else:
    st.info("Aucune entrée détectée. Vous pouvez créer une entrée manuellement.")
    if st.button("Créer une entrée manuelle"):
        # Provide fields
        new_sign = st.text_input("Signe hiéroglyphique")
        new_translit = st.text_input("Translittération")
        new_translation = st.text_input("Traduction en français")
        if new_sign and new_translit:
            nid = str(len(entries) + 1)
            new_entry = {"id": nid, "sign": new_sign, "transliteration": new_translit, "translation": new_translation, "raw": ""}
            entries.append(new_entry)
            st.success("Entrée ajoutée. Sélectionnez-la dans la liste.")
    selected_entry = None

# Display selected entry details
if selected_entry:
    st.markdown("### Détails de l'entrée sélectionnée")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**Signe**")
        st.code(selected_entry["sign"])
        st.markdown("**ID**")
        st.write(selected_entry["id"])
    with col2:
        st.markdown("**Translittération**")
        st.write(selected_entry["transliteration"])
        st.markdown("**Traduction française**")
        st.write(selected_entry["translation"])

    st.markdown("**Texte source brut**")
    st.write(selected_entry.get("raw", ""))

    # Comparative table
    st.markdown("### Tableau comparatif des traductions")
    if not langs:
        st.warning("Sélectionnez au moins une langue dans la barre latérale.")
    else:
        # Build table data
        key = selected_entry["id"]  # use id as key for translations_map
        row = {"Signe": selected_entry["sign"], "Translittération": selected_entry["transliteration"], "Français": selected_entry["translation"]}
        # For each language, get translation from map or placeholder
        lang_translations = {}
        for L in langs:
            tr = ""
            if key in translations_map and L in translations_map[key]:
                tr = translations_map[key][L]
            else:
                if allow_auto_translate:
                    tr = placeholder_translate(selected_entry["translation"] or selected_entry["transliteration"], L)
                else:
                    tr = ""
            lang_translations[L] = tr

        # Display as two-column table: attribute and translations
        # We'll render a simple table
        table_cols = ["Attribut"] + langs
        # Build rows
        attribs = ["Signe", "Translittération", "Traduction française"]
        table_rows = []
        for a in attribs:
            row_vals = [a]
            for L in langs:
                if a == "Signe":
                    row_vals.append(selected_entry["sign"])
                elif a == "Translittération":
                    row_vals.append(selected_entry["transliteration"])
                else:
                    row_vals.append(lang_translations.get(L, ""))
            table_rows.append(row_vals)

        # Render table using st.table
        import pandas as pd
        df = pd.DataFrame(table_rows, columns=table_cols)
        st.table(df)

        # Allow manual edits for each language
        st.markdown("#### Édition manuelle des traductions")
        edited = False
        if key not in translations_map:
            translations_map[key] = {}
        for L in langs:
            current = translations_map.get(key, {}).get(L, lang_translations.get(L, ""))
            new_val = st.text_input(f"Traduction en {L}", value=current, key=f"{key}_{L}")
            if new_val != current:
                translations_map[key][L] = new_val
                edited = True

        if edited:
            st.success("Modifications enregistrées en mémoire locale (pensez à sauvegarder sur disque).")

# Save translations button
if save_button:
    try:
        save_translations_csv(TRANSLATION_CSV, translations_map)
        st.success(f"Traductions sauvegardées dans {TRANSLATION_CSV}")
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde : {e}")

st.markdown("---")
st.markdown("**Notes techniques**")
st.markdown(
    "- Le parser est heuristique. Si le dictionnaire Vygus a une structure particulière (colonnes, tableaux, images), il faudra adapter la logique d'extraction.\n"
    "- Pour des traductions automatiques réelles, remplacez `placeholder_translate` par un appel à une API (LibreTranslate, Google Translate, etc.) en respectant les clés et quotas.\n"
    "- Le fichier `kuma_translations.csv` est utilisé pour stocker les traductions manuelles. Format : clé;langue;traduction."
)

st.markdown("Fin de l'application. Pour toute adaptation (extraction d'images hiéroglyphiques, parsing avancé, intégration d'API de traduction), je peux fournir une version améliorée sur demande.")
