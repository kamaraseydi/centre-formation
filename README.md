# Centre de Formation — Django

Application web de gestion d'un centre de formation, développée avec Django et PostgreSQL.

## Fonctionnalités

- Gestion des formations (création, modification, suppression, consultation).
- Gestion des comptes et profils étudiants.
- Inscription des étudiants aux formations.
- Validation et annulation des inscriptions.
- Authentification et gestion des permissions.
- Recherche, filtres et pagination.
- Tableau de bord administratif.
- Gestion des images des formations.
- Tests automatisés Django.

## Technologies utilisées

- Python
- Django
- PostgreSQL
- HTML / CSS
- Git et GitHub

## Installation locale

Cloner le dépôt :

```bash
git clone https://github.com/kamaraseydi/centre-formation.git
cd centre-formation
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Créer un fichier `.env` à partir de `.env.example` et renseigner les paramètres PostgreSQL ainsi qu'une clé secrète Django.

Créer la base PostgreSQL locale et configurer les droits de l'utilisateur correspondant.

Appliquer les migrations :

```bash
python manage.py migrate
```

Démarrer le serveur :

```bash
python manage.py runserver
```

## Tests

Exécuter les tests automatisés :

```bash
python manage.py test formations
```

La suite comporte actuellement 42 tests automatisés.

## Déploiement

Déploiement prévu avec Render et Supabase.

## Auteur

Projet personnel de développement web réalisé dans le cadre de l'apprentissage de Django et des bonnes pratiques backend.