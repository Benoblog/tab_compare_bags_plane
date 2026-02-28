import streamlit as st
import pandas as pd

# 1. Configuration
st.set_page_config(layout="wide", page_title="Comparatif Housses de Vélo")
st.title("🚲 Comparateur interactif de housses de vélo pour l'avion")
st.markdown("Utilisez les filtres ci-dessous pour comparer les modèles selon vos besoins.")

# 2. Fonction de chargement "Blindée"
@st.cache_data
def load_data():
    # On laisse Pandas deviner le séparateur (sep=None) 
    # et on essaie d'abord l'encodage classique
    try:
        df = pd.read_csv("tab_comparatif.csv", sep=None, engine="python", encoding="utf-8")
    except Exception:
        # Si ça plante (format Excel français), on utilise l'encodage européen
        df = pd.read_csv("tab_comparatif.csv", sep=None, engine="python", encoding="latin-1")
    
    # Nettoyage global
    df = df.astype(str).replace("nan", "")
    return df

df = load_data()

# 3. L'astuce magique : on prend la 1ère colonne dynamiquement sans l'appeler "Critère"
col_critere = df.columns[0]

st.sidebar.header("🎯 Filtres de recherche")

# On liste tous les critères de cette première colonne
tous_les_criteres = df[col_critere].dropna().unique().tolist()

# Création du menu déroulant (avec les 3 premiers critères sélectionnés par défaut pour éviter les erreurs)
criteres_selectionnes = st.sidebar.multiselect(
    "Quels critères sont importants pour vous ?",
    options=tous_les_criteres,
    default=tous_les_criteres[:3] 
)

# 4. On filtre et on affiche
df_filtre = df[df[col_critere].isin(criteres_selectionnes)]

st.dataframe(
    df_filtre,
    use_container_width=True,
    hide_index=True
)
