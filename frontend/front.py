import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

st.title("Analyse des prix de billets d'avion")

API_URL = "http://13.60.37.163:8000"

@st.cache_data
def get_ond_list():
    response = requests.get(f"{API_URL}/ond")
    if response.status_code == 200:
        return response.json()["ond"]
    else:
        st.error("Erreur lors de la récupération des OnD")
        return []

ond_list = get_ond_list()
selected_ond = st.selectbox("Sélectionnez un OnD", ond_list)
trip_type = st.radio("Type de voyage", ["OW", "RT"])

# Filtres optionnels
st.markdown("### Filtres optionnels")
col1, col2 = st.columns(2)

with col1:
    search_country = st.text_input("Pays de recherche (ex: FR)")
    search_date_min = st.date_input("Date min de recherche", value=None, key="search_min")
    request_dep_date_min = st.date_input("Départ min", value=None, key="dep_min")
    stay_duration_min = st.number_input("Durée minimale du séjour (jours)", min_value=0, step=1, format="%d")

with col2:
    search_date_max = st.date_input("Date max de recherche", value=None, key="search_max")
    request_dep_date_max = st.date_input("Départ max", value=None, key="dep_max")
    stay_duration_max = st.number_input("Durée max du séjour (jours)", min_value=0, step=1, format="%d")
    nb_connections = st.number_input("Nombre de correspondances exact", min_value=0, step=1, format="%d")

# Variable pour stocker les données récupérées
if 'data' not in st.session_state:
    st.session_state.data = None

# Bouton pour lancer la requête
if st.button("Analyser les prix"):
    params = {
        "ond": selected_ond,
        "trip_type": trip_type,
    }

    # Ajout conditionnel des filtres
    if search_country:
        params["search_country"] = search_country

    if isinstance(search_date_min, date):
        params["search_date_min"] = search_date_min.isoformat()
    if isinstance(search_date_max, date):
        params["search_date_max"] = search_date_max.isoformat()
    if isinstance(request_dep_date_min, date):
        params["request_dep_date_min"] = request_dep_date_min.isoformat()
    if isinstance(request_dep_date_max, date):
        params["request_dep_date_max"] = request_dep_date_max.isoformat()

    if stay_duration_min:
        params["stay_duration_min"] = int(stay_duration_min)
    if stay_duration_max:
        params["stay_duration_max"] = int(stay_duration_max)

    if nb_connections > 0:
        params["nb_connections"] = int(nb_connections)

    # Appel de l'API et stockage des données dans st.session_state
    with st.spinner("Chargement des résultats..."):
        response = requests.get(f"{API_URL}/price-evolution", params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                st.session_state.data = pd.DataFrame(data)  # Stocker les données
                st.dataframe(st.session_state.data)
            else:
                st.warning("Aucune donnée trouvée pour les filtres sélectionnés.")
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")

# Si les données ont été chargées, on peut afficher le graphique
if st.session_state.data is not None:
    st.markdown("### Prix médian par advance purchase et compagnie")
    
    # Sélecteur graphique pour exclure certaines compagnies
    unique_airlines = st.session_state.data['main_airline'].unique()
    excluded_airlines = st.multiselect("Sélectionner les compagnies à exclure", unique_airlines)

    # Filtrer les données pour exclure les compagnies sélectionnées
    filtered_df = st.session_state.data[~st.session_state.data['main_airline'].isin(excluded_airlines)]

    # Tracer le graphique avec les compagnies restantes
    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=filtered_df,
        x="advance_purchase",
        y="median_price_eur",
        hue="main_airline",
        marker="o"
    )

    # Inverser l'axe des jours
    plt.gca().invert_xaxis()

    plt.xlabel("Advance Purchase (jours)")
    plt.ylabel("Prix médian (€)")
    plt.title(f"{selected_ond} - {trip_type}")
    
    st.pyplot(plt)
