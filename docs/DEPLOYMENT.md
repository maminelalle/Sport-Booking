# 🚀 Guide de Déploiement - SportBooking

## Prérequis

- AWS ou VPS avec Docker
- Domaine configuré
- Certificat SSL
- Clés Stripe

## Déploiement sur AWS

### 1. Créer une instance EC2

```bash
# AMI: Ubuntu 22.04 LTS
# Type: t3.medium
# Storage: 30GB
```

### 2. Configuration initiale

```bash
# Connecter à l'instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Mise à jour du système
sudo apt-get update
sudo apt-get upgrade -y

# Installer Docker et Docker Compose
sudo apt-get install -y docker.io docker-compose

# Ajouter l'utilisateur ubuntu au groupe docker
sudo usermod -aG docker ubuntu
newgrp docker

# Installer PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Configurer PostgreSQL
sudo -u postgres psql
CREATE DATABASE sportsbooking;
CREATE USER sportsbooking_user WITH PASSWORD 'secure_password_here';
ALTER ROLE sportsbooking_user SET client_encoding TO 'utf8';
ALTER ROLE sportsbooking_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sportsbooking_user SET default_transaction_deferrable TO on;
ALTER ROLE sportsbooking_user SET default_transaction_read_committed TO on;
ALTER USER sportsbooking_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE sportsbooking TO sportsbooking_user;
\q
```

### 3. Cloner et configurer le projet

```bash
# Cloner le repository
git clone <repository-url> /home/ubuntu/sportsbooking
cd /home/ubuntu/sportsbooking

# Créer les fichiers .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Éditer les fichiers .env avec vos valeurs de production
nano backend/.env
nano frontend/.env
```

### 4. Configuration du .env pour production

```env
# backend/.env
DEBUG=False
SECRET_KEY=your-super-secret-key-generate-new-one
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=sportsbooking
DB_USER=sportsbooking_user
DB_PASSWORD=secure_password_here
DB_HOST=localhost
DB_PORT=5432

STRIPE_PUBLIC_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_live_xxxxx

CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 5. Configurer Nginx

```bash
# Installer Nginx
sudo apt-get install -y nginx

# Créer la configuration
sudo nano /etc/nginx/sites-available/sportsbooking
```

```nginx
upstream django_app {
    server backend:8000;
}

upstream react_app {
    server frontend:3000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirection HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # API Backend
    location /api/ {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin Django
    location /admin/ {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/ubuntu/sportsbooking/backend/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /home/ubuntu/sportsbooking/backend/media/;
    }

    # Frontend React
    location / {
        proxy_pass http://react_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Cache busting pour les fichiers JS/CSS
        location ~* \.(js|css)$ {
            expires 1m;
        }
    }
}
```

### 6. Configurer SSL avec Let's Encrypt

```bash
# Installer certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtenir le certificat
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com
```

### 7. Activer Nginx

```bash
# Activer la configuration
sudo ln -s /etc/nginx/sites-available/sportsbooking /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx
```

### 8. Docker Compose pour production

Créer un fichier `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    image: sportsbooking-backend:latest
    command: gunicorn sportsbooking.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DEBUG=False
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=sportsbooking
      - DB_USER=sportsbooking_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=postgres
      - DB_PORT=5432
    depends_on:
      - postgres
    restart: always

  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=sportsbooking
      - POSTGRES_USER=sportsbooking_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    restart: always

  frontend:
    image: sportsbooking-frontend:latest
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=https://your-domain.com/api
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 9. Démarrer les services

```bash
# Build les images
docker build -t sportsbooking-backend:latest ./backend
docker build -t sportsbooking-frontend:latest ./frontend

# Démarrer avec docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Appliquer les migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Créer les données de base
docker-compose -f docker-compose.prod.yml exec backend python manage.py initialize_data

# Collecter les fichiers statiques
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

## Monitoring et Maintenance

### Logs

```bash
# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Logs système
sudo journalctl -u nginx -f
```

### Sauvegarde

```bash
# Sauvegarder la base de données
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U sportsbooking_user sportsbooking > backup.sql

# Restaurer
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U sportsbooking_user sportsbooking < backup.sql
```

### Mise à jour

```bash
# Faire un pull
git pull origin main

# Rebuild les images
docker build -t sportsbooking-backend:latest ./backend
docker build -t sportsbooking-frontend:latest ./frontend

# Redémarrer
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# Appliquer les nouvelles migrations si nécessaire
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

## VPS Alternative (DigitalOcean, Linode, etc.)

Les étapes sont similaires:

1. Créer une instance Ubuntu 22.04
2. Suivre les étapes 2-9 ci-dessus
3. Configurer un domaine pointant vers l'IP du VPS
4. Utiliser Let's Encrypt pour SSL

## Optimisations Production

### Frontend
- Activer gzip compression
- Utiliser un CDN pour les assets statiques
- Minifier CSS/JS
- Optimiser les images

### Backend
- Utiliser Gunicorn avec plusieurs workers
- Ajouter un cache Redis
- Configurer un load balancer
- Utiliser une CDN pour les images

### Base de données
- Activer les backups automatiques
- Configurer la réplication
- Monitorer les performances
- Indexer les colonnes interrogées

## Checklist avant production

- [ ] Secret key changé
- [ ] DEBUG = False
- [ ] Clés Stripe configurées
- [ ] CORS configuré
- [ ] SSL/HTTPS activé
- [ ] Base de données sécurisée
- [ ] Backups configurées
- [ ] Monitoring mis en place
- [ ] Logging configuré
- [ ] Email d'erreurs configuré

## Support

Pour toute question sur le déploiement, consultez:
- Documentation Docker
- Documentation Django
- Documentation Nginx
- Communities AWS / DigitalOcean
