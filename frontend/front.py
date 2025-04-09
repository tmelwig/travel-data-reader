import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Chargement des données
with open("data.json", "r") as f:  # ou remplacer par la variable directement si tu n'as pas de fichier
    data = json.load(f)

df = pd.DataFrame(data)

# Titre
st.title("Prix médian en fonction de l'avance d'achat")
st.markdown("Sélectionne une ou plusieurs compagnies pour afficher l'évolution du prix médian.")

# Sélecteur de compagnies
airlines = df['main_airline'].unique()
selected_airlines = st.multiselect("Compagnies aériennes", sorted(airlines), default=airlines[:3])

# Filtrage des données
filtered_df = df[df['main_airline'].isin(selected_airlines)]

# Tracé
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_df, x="advance_purchase", y="median_price_eur", hue="main_airline", marker="o")
plt.xlabel("Nombre de jours d'avance")
plt.ylabel("Prix médian (€)")
plt.title("Évolution du prix médian par compagnie")
plt.grid(True)

st.pyplot(plt)
