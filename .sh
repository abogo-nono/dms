#!/bin/bash

# Nom du projet
PROJECT_NAME="."

echo "📁 Création du projet '$PROJECT_NAME'..."

# Création des dossiers
mkdir -p $PROJECT_NAME/app/models
mkdir -p $PROJECT_NAME/app/resources
mkdir -p $PROJECT_NAME/migrations

# Création des fichiers init pour que Python reconnaisse les packages
touch $PROJECT_NAME/app/__init__.py
touch $PROJECT_NAME/app/models/__init__.py
touch $PROJECT_NAME/app/models/item.py
touch $PROJECT_NAME/app/models/category.py
touch $PROJECT_NAME/app/resources/__init__.py
touch $PROJECT_NAME/app/resources/item.py
touch $PROJECT_NAME/app/resources/category.py
touch $PROJECT_NAME/app/routes.py
touch $PROJECT_NAME/config.py
touch $PROJECT_NAME/run.py
touch $PROJECT_NAME/requirements.txt

echo "✅ Structure du projet Flask créée avec succès !"
