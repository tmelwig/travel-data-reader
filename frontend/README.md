Construire l'image Docker :

Depuis le terminal, dans le répertoire où se trouvent le Dockerfile et requirements.txt, exécuter la commande suivante pour construire l'image Docker :

docker build -t streamlit-app .

Lancer le conteneur Docker :

Une fois l'image construite, tester l'application localement en exécutant le conteneur Docker :

docker run -p 8501:8501 streamlit-app

L'application sera accessible à http://localhost:8501 dans ton navigateur.