# Guide d'Installation - SportBooking

## Prérequis

- Python 3.11+
- Node.js 18+
- PostgreSQL 13+ (optionnel, SQLite pour développement)
- pip et npm

## Installation Locale (Développement)

### 1. Cloner le projet

```bash
git clone <repository-url>
cd Python_Project
```

### 2. Backend Django

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env

# Appliquer les migrations
python manage.py migrate

# Initialiser les données
python manage.py initialize_data

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

Le backend sera accessible sur `http://localhost:8000`

### 3. Frontend React

```bash
cd frontend

# Installer les dépendances
npm install

# Créer le fichier .env
cp .env.example .env

# Lancer le serveur de développement
npm start
```

Le frontend sera accessible sur `http://localhost:3000`

## Installation avec Docker

### 1. Prérequis
- Docker
- Docker Compose

### 2. Démarrer les services

```bash
docker-compose up -d
```

### 3. Appliquer les migrations

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py initialize_data
```

### 4. Accéder aux applications

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs/
- Admin Django: http://localhost:8000/admin/

## Configuration de Stripe

1. Créer un compte sur [Stripe](https://stripe.com)
2. Récupérer les clés API (Public et Secret)
3. Ajouter à votre fichier `.env`:

```
STRIPE_PUBLIC_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

## Variables d'environnement

### Backend (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sportsbooking
DB_USER=sportsbooking_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
STRIPE_PUBLIC_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_STRIPE_PUBLIC_KEY=pk_test_xxxxx
```

## Commandes utiles

### Backend

```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer les tests
python manage.py test

# Lancer le serveur
python manage.py runserver

# Initialiser les données de base
python manage.py initialize_data
```

### Frontend

```bash
# Installer les dépendances
npm install

# Lancer en mode développement
npm start

# Build pour la production
npm run build

# Lancer les tests
npm test
```

## Accès aux interfaces

### Développement

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Vous pouvez créer un compte |
| API REST | http://localhost:8000/api/ | Token JWT |
| API Docs | http://localhost:8000/api/docs/ | Public |
| Admin | http://localhost:8000/admin | admin / admin123 |

### Production

Voir le guide de déploiement dans `/docs/DEPLOYMENT.md`

## Dépannage

### Erreur de migration

```bash
python manage.py migrate --run-syncdb
```

### Réinitialiser la base de données

```bash
# ⚠️ ATTENTION: Cela supprimera toutes les données
rm db.sqlite3
python manage.py migrate
python manage.py initialize_data
```

### Problèmes CORS

Vérifiez que votre `CORS_ALLOWED_ORIGINS` dans `.env` inclut l'URL de votre frontend.

## Support

Pour toute question ou bug, veuillez ouvrir une issue sur GitHub.
