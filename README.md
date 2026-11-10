# Centre de Formation Seydi

Application web de gestion d'un centre de formation, développée avec Django et PostgreSQL.

**Application en production :** https://centre-formation-5932.onrender.com

**Dépôt GitHub :** https://github.com/kamaraseydi/centre-formation

---

## Présentation

Centre de Formation Seydi est une application web permettant de gérer les activités d'un établissement de formation.

Elle centralise la gestion des formations, des étudiants et des inscriptions, avec un système d'authentification, de permissions et un tableau de bord.

Ce projet a été développé pour mettre en pratique Django, la gestion des bases de données relationnelles, les tests automatisés et le déploiement d'une application web en production.

## Fonctionnalités

### Gestion des formations
- Création, consultation, modification et suppression des formations.
- Gestion des descriptions, durées, prix et disponibilités.
- Ajout et gestion des images.
- Recherche et filtrage des formations.
- Pagination des résultats.

### Gestion des étudiants
- Inscription et authentification des utilisateurs.
- Gestion des profils étudiants.
- Consultation des informations des étudiants.
- Modification des profils et des mots de passe.

### Gestion des inscriptions
- Inscription des étudiants aux formations.
- Gestion des demandes d'inscription.
- Validation et annulation des inscriptions.
- Prévention des inscriptions en double.

### Administration et sécurité
- Interface d'administration Django.
- Gestion des permissions et des accès.
- Protection des fonctionnalités réservées aux utilisateurs autorisés.
- Validation des formulaires et des données.

### Tableau de bord
- Vue centralisée des principales informations.
- Suivi des formations, étudiants et inscriptions.

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3 | Langage principal |
| Django 6.1.2 | Framework backend |
| PostgreSQL | Base de données |
| Django ORM | Gestion des données |
| HTML5 / CSS3 | Interface utilisateur |
| JavaScript | Interactions frontend |
| Pillow | Traitement des images |
| django-storages | Gestion du stockage distant |
| Supabase | PostgreSQL et stockage des images |
| WhiteNoise | Gestion des fichiers statiques en production |
| Gunicorn | Serveur WSGI |
| Render | Hébergement de l'application |
| Git / GitHub | Gestion du code source |

## Architecture du projet

```text
centre-formation/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── formations/
│   ├── migrations/
│   ├── static/
│   │   └── formations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Installation locale

### Prérequis

- Python
- PostgreSQL
- Git
- pip

### 1. Cloner le dépôt

```bash
git clone https://github.com/kamaraseydi/centre-formation.git
cd centre-formation
```

### 2. Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créer un fichier `.env` à partir de `.env.example` :

```powershell
Copy-Item .env.example .env
```

Renseigner les informations de connexion à PostgreSQL et les autres paramètres nécessaires.

Exemple de configuration locale :

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=centre_formation
DB_USER=django_user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
DB_SSLMODE=disable

SUPABASE_STORAGE_ENABLED=False
```

Les identifiants réels et les clés secrètes ne doivent jamais être publiés sur GitHub.

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un administrateur

```bash
python manage.py createsuperuser
```

### 7. Démarrer le serveur

```bash
python manage.py runserver
```

L'application est accessible à l'adresse :

http://127.0.0.1:8000/

L'administration Django est accessible à :

http://127.0.0.1:8000/admin/

## Tests automatisés

Le projet dispose d'une suite de tests automatisés couvrant notamment :

- Les modèles et leurs contraintes.
- Les formulaires.
- Les vues et les fonctionnalités CRUD.
- L'authentification et les profils.
- Les inscriptions.
- Les permissions.
- Le tableau de bord.

Exécuter les tests :

```bash
python manage.py test formations
```

**Dernier résultat validé : 42 tests réussis.**

## Déploiement en production

L'application est déployée sur Render avec une architecture basée sur Supabase.

| Service | Rôle |
|---|---|
| Render | Hébergement Django |
| Gunicorn | Exécution de l'application |
| WhiteNoise | Distribution des fichiers statiques |
| Supabase PostgreSQL | Base de données de production |
| Supabase Storage | Stockage des images |
| GitHub | Dépôt du code source |

### Configuration de production

Les principales variables d'environnement utilisées en production sont :

```env
DJANGO_SECRET_KEY=
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_SSLMODE=require

SUPABASE_STORAGE_ENABLED=True
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_ENDPOINT_URL=
AWS_S3_REGION_NAME=
```

Les variables sont configurées directement dans l'environnement Render. Les valeurs sensibles ne sont pas stockées dans le dépôt GitHub.

### Commandes de production

Collecte des fichiers statiques :

```bash
python manage.py collectstatic --noinput
```

Démarrage de l'application :

```bash
python manage.py migrate --noinput && gunicorn config.wsgi:application
```

## Améliorations futures

Quelques pistes d'évolution envisagées :

- Amélioration du tableau de bord et des statistiques.
- Évolution des fonctionnalités de gestion des formations.
- Amélioration de l'expérience utilisateur.
- Renforcement de la couverture des tests.
- Ajout de nouvelles fonctionnalités métier.

## Auteur

**Kamara Seydi**

Étudiant en Génie Logiciel, intéressé par le développement backend, Python et Django.

GitHub : https://github.com/kamaraseydi

---

*Projet réalisé dans le cadre de mon apprentissage du développement web backend avec Django.*