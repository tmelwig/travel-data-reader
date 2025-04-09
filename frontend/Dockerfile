# Utiliser une image de base officielle Python
FROM python:3.11-slim

# Installer les dépendances
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port que Streamlit utilise (par défaut c'est le 8501)
EXPOSE 8501

# Commande pour démarrer l'application Streamlit
CMD ["streamlit", "run", "app.py"]
