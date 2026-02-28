import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(layout="wide", page_title="Comparatif Housses de Vélo")

st.title("🚲 Comparateur interactif de housses de vélo pour l'avion")
st.markdown("Utilisez les filtres ci-dessous pour comparer les modèles selon vos besoins (Poids, Compatibilité, Maintien...).")

# 2. Chargement des données
@st.cache_data
def load_data():
    # Le fameux combo gagnant pour lire votre fichier Excel exporté
    df = pd.read_csv("tab_comparatif.csv", sep=";", encoding="latin-1", on_bad_lines="skip")
    
    # Nettoyage des noms de colonnes (au cas où il y ait des espaces cachés)
    df.columns = df.columns.str.strip()
    
    # Conversion en texte pour éviter que Streamlit ne plante sur les virgules des notes
    df = df.astype(str) 
    
    # Remplacement des cases vides par du vrai vide (au lieu de "nan")
    df = df.replace("nan", "") 
    
    return df

# C'EST LA LIGNE QUI MANQUAIT : on lance la fonction et on crée le tableau "df" !
df = load_data()

# 3. Création des filtres (Boutons / Multi-sélection)
st.sidebar.header("🎯 Filtres de recherche")

# Sélection des critères (les lignes de votre CSV)
tous_les_criteres = df['Critère'].dropna().unique().tolist()
criteres_selectionnes = st.sidebar.multiselect(
    "Quels critères sont importants pour vous ?",
    options=tous_les_criteres,
    default=["Compatibilité Route / VTT", "Poids / risque de supplément bagage", "Maintien interne / stabilité"]
)

# Filtrer le tableau selon les critères choisis
df_filtre = df[df['Critère'].isin(criteres_selectionnes)]

# 4. Affichage du tableau interactif
st.dataframe(
    df_filtre,
    use_container_width=True,
    hide_index=True
)

st.markdown("*(Faites défiler vers la droite pour voir tous les modèles et les notes)*")
