# DSCYCLO 2026 🚲

Refonte complète d'un logiciel de gestion de réparations de vélos (initialement développé en 2018 en langage Java pour l'entreprise DSI Atlantique) vers une architecture moderne en Python : API REST + dashboard web.

Projet réalisé dans le cadre d'une transition professionnelle vers l'ingénierie IA, en autoformation.

## Stack technique

- **Backend** : Python, FastAPI
- **Validation des données** : Pydantic
- **ORM / Base de données** : SQLAlchemy, PostgreSQL
- **Authentification** : cookies de session, hash bcrypt (passlib)
- **Frontend** : Jinja2 (templates HTML), Tailwind CSS, JavaScript (fetch API)
- **Environnement** : Docker (PostgreSQL)

## Fonctionnalités

- **Gestion des vélos** : suivi du parc, attribution nominative (facultative)
- **Gestion des pièces** : références, stock, alertes de stock critique
- **Gestion des réparations** : liaison vélo / technicien / pièces utilisées (relation many-to-many avec quantités), décrémentation automatique du stock, statuts (à faire / terminée / suspendue)
- **Utilisateurs et rôles** : authentification, rôles Administrateur / Utilisateur, droits différenciés (un utilisateur simple ne peut pas gérer les autres comptes)
- **Dashboard web** : CRUD complet (création, modification, suppression) sur les 4 entités, accessible sans passer par Swagger
- **Page d'onboarding** : vue d'ensemble à la connexion — dernières réparations, réparations suspendues, alertes de stock, journal d'activité récente
- **Journal d'activité (logs)** : traçabilité des actions (création / modification / suppression) et des connexions / déconnexions

## Architecture

Le projet suit une architecture en couches, où chaque couche ne communique qu'avec sa voisine directe :

```
Routes (FastAPI)  →  Services  →  Repositories  →  Base de données (PostgreSQL)
     ↓                                  ↓
 Pydantic (validation JSON)    SQLAlchemy (modèles de tables)
```

- `models/` : schémas Pydantic (validation des entrées/sorties de l'API)
- `database/` : modèles SQLAlchemy (structure des tables)
- `repositories/` : accès aux données, requêtes SQLAlchemy
- `services/` : logique intermédiaire entre routes et repositories
- `routes/` : endpoints FastAPI (API REST + pages HTML du dashboard)
- `templates/` : pages HTML (Jinja2)
- `static/` : fichiers JavaScript

Ce découpage permet, par exemple, d'être passé de SQLite à PostgreSQL en ne modifiant qu'un seul fichier de configuration, sans toucher au reste du code.

## Installation

### Prérequis

- Python 3.9+
- PostgreSQL (ou un conteneur Docker PostgreSQL)

### Étapes avec Docker

1. Cloner le dépôt
```bash
git clone https://github.com/DavidRichomme/DSCYCLO-2026.git
cd DSCYCLO-2026
```
2. Installer Docker
3. Initialiser le contenair Docker
   A la racine du projet (ou sont les fichers téléchargés depuis github)
```bash
docker-compose up --build 
```
4. Créer le premier administrateur
```bash
python seed.py 
```   

L'API est accessible sur `http://127.0.0.1:8000`, la documentation Swagger sur `http://127.0.0.1:8000/docs`, et le dashboard sur `http://127.0.0.1:8000/login`.


### Étapes sans Docker

1. Cloner le dépôt
```bash
git clone https://github.com/DavidRichomme/DSCYCLO-2026.git
cd DSCYCLO-2026
```

2. Créer et activer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Créer un fichier `.env` à la racine du projet
```
DATABASE_URL=postgresql://utilisateur:mot_de_passe@localhost:5432/nom_de_la_base
```

5. Lancer l'application
```bash
uvicorn main:app --reload
```

6.Créer le premier administrateur
```bash
python seed.py 
``` 

L'API est accessible sur `http://127.0.0.1:8000`, la documentation Swagger sur `http://127.0.0.1:8000/docs`, et le dashboard sur `http://127.0.0.1:8000/login`.

## Captures d'écran

*(à venir)*

## Pistes d'évolution

- Table de faits enrichie (historique détaillé des interventions)
- Dockerisation complète de l'application (API + base de données)
- Déploiement en ligne

## Auteur

David Richomme — [Github](https://github.com/DavidRichomme)
