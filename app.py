import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(layout="wide", page_title="Comparatif Housses de Vélo")

st.title("🚲 Comparateur interactif de housses de vélo pour l'avion")
st.markdown("Utilisez les filtres ci-dessous pour comparer les modèles selon vos besoins.")

# 2. Fonction de chargement "Blindée" (avec correction pour Excel sur Mac)
@st.cache_data
def load_data():
    try:
        # On essaie d'abord l'encodage classique
        df = pd.read_csv("tab_comparatif.csv", sep=None, engine="python", encoding="utf-8")
    except Exception:
        # Si ça plante, on utilise l'encodage spécifique aux MAC pour retrouver les bons accents !
        df = pd.read_csv("tab_comparatif.csv", sep=None, engine="python", encoding="mac_roman")
    
    # Nettoyage global
    df.columns = df.columns.str.strip() # Enlève les espaces cachés dans les titres des colonnes
    df = df.astype(str).replace("nan", "") # Convertit tout en texte pour éviter les bugs et supprime les "nan"
    return df

# On charge le tableau
df = load_data()

# 3. L'astuce magique : on prend la 1ère colonne dynamiquement sans chercher le mot exact "Critère"
col_critere = df.columns[0]

st.sidebar.header("🎯 Filtres de recherche")

# On liste tous les critères présents dans la première colonne
tous_les_criteres = df[col_critere].dropna().unique().tolist()

# Création du menu déroulant (avec les 3 premiers critères sélectionnés par défaut)
criteres_selectionnes = st.sidebar.multiselect(
    "Quels critères sont importants pour vous ?",
    options=tous_les_criteres,
    default=tous_les_criteres[:3] 
)

# 4. On filtre le tableau selon les choix de l'utilisateur
df_filtre = df[df[col_critere].isin(criteres_selectionnes)]

# 5. Affichage du tableau final interactif
st.dataframe(
    df_filtre,
    use_container_width=True,
    hide_index=True
)
