# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les paquets requis
COPY ./python/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application dans le répertoire de travail
COPY ./python /app

# Copier les fichiers statiques et templates pour Flask
COPY ./web /app/web

# Exposer le port que Flask va utiliser
EXPOSE 5000

# Définir les variables d'environnement pour Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Démarrer l'application Flask
CMD ["flask", "run"]