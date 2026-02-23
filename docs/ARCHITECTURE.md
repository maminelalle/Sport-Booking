# 🏗️ Architecture - SportBooking

## Vue d'ensemble

SportBooking est une application web full-stack construite avec:
- **Backend**: Django + Django REST Framework
- **Frontend**: React + Tailwind CSS
- **Base de données**: PostgreSQL (production) / SQLite (développement)
- **Paiements**: Stripe API
- **Authentification**: JWT (Simple JWT)

## Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Navigateur)                      │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Frontend React (Port 3000)                     │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Pages: Home, CourtDetail, MyReservations       │  │  │
│  │  │  Services: API Client (Axios)                   │  │  │
│  │  │  Context: Auth, UI State                        │  │  │
│  │  │  Components: Header, CourtCard, ReservationForm │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
                        HTTP/REST API
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend Django (Port 8000)                  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  API REST Framework (DRF)                             │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Apps:                                          │  │  │
│  │  │  - auth_app          → Authentification (JWT)   │  │  │
│  │  │  - sites             → Gestion des sites        │  │  │
│  │  │  - courts            → Gestion des terrains    │  │  │
│  │  │  - reservations      → Gestion réservations    │  │  │
│  │  │  - payments          → Paiements Stripe        │  │  │
│  │  │  - core              → Utilitaires, perms      │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Couche Métier:                                │  │  │
│  │  │  - Logique de réservation                      │  │  │
│  │  │  - Vérification disponibilité                  │  │  │
│  │  │  - Gestion des paiements                       │  │  │
│  │  │  - Permissions et droits d'accès               │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Modèles ORM Django:                           │  │  │
│  │  │  - User, Role, Site, Court, Equipment         │  │  │
│  │  │  - Reservation, Payment, Invoice              │  │  │
│  │  │  - BlockedPeriod, OpeningHours                │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
            ↙                    ↓                    ↘
      PostgreSQL          Stripe API            Media Files
      (Données)           (Paiements)           (Images)
```

## Structure des dossiers

```
Python_Project/
├── backend/
│   ├── apps/
│   │   ├── auth_app/          # Authentification et utilisateurs
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── sites/             # Gestion des sites
│   │   ├── courts/            # Gestion des terrains
│   │   ├── reservations/      # Gestion des réservations
│   │   ├── payments/          # Gestion des paiements
│   │   └── core/              # Utilitaires et middleware
│   ├── sportsbooking/         # Configuraton Django principale
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/             # Pages principales
│   │   ├── components/        # Composants réutilisables
│   │   ├── services/          # Services API
│   │   ├── context/           # Context API pour l'état global
│   │   ├── hooks/             # Hooks personnalisés
│   │   ├── styles/            # Styles CSS
│   │   ├── App.js             # Composant racine
│   │   └── index.js           # Point d'entrée
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── Dockerfile
│   ├── tailwind.config.js
│   └── .env.example
├── docs/
│   ├── INSTALLATION.md        # Guide d'installation
│   ├── API.md                 # Documentation API
│   ├── ARCHITECTURE.md        # Ce fichier
│   ├── DATABASE.md            # Schéma base de données
│   └── DEPLOYMENT.md          # Guide de déploiement
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Flux de données

### 1. Authentification

```
User → Login Form → Auth Service → Django Login Endpoint
                        ↓
                  JWT Tokens (access + refresh)
                        ↓
                  Local Storage
                        ↓
                  Header: Authorization: Bearer {token}
```

### 2. Réservation

```
User → Court Selection → Availability Check → Reservation Form
                              ↓
                        API POST /reservations/
                              ↓
                        Django Model Validation
                              ↓
                        Check Overlapping Reservations
                              ↓
                        Create Reservation (PENDING)
                              ↓
                        Redirect to Payment
```

### 3. Paiement

```
User → Payment Form → Stripe Payment Intent
                           ↓
                    Stripe Frontend Element
                           ↓
                      Payment Processing
                           ↓
                    Webhook Notification
                           ↓
                API POST /payments/confirm_payment/
                           ↓
                    Update Reservation Status
```

## Modèle de données

### Relations principales

```
User (1) ──→ (many) Reservation
     ↓
     └─→ Managed Sites

Site (1) ──→ (many) Court
        ──→ (many) OpeningHours

Court (1) ──→ (many) Reservation
      ──→ (many) Equipment (M-N)
      ──→ (many) CourtImage
      ──→ (many) BlockedPeriod

Reservation (1) ──→ (1) Payment
            ──→ (1) Court
            ──→ (1) User

Payment (1) ──→ (1) Invoice
        ──→ (1) Reservation
```

## Sécurité

### Authentification
- JWT avec access token (24h) et refresh token (7 jours)
- Tokens stockés dans le localStorage
- Validation sur chaque requête API

### Autorisation
- Rôles: CLIENT, MANAGER, ADMIN
- Permissions granulaires par endpoint
- Vérification de propriété des ressources

### Protection
- CORS configuré pour les domaines approuvés
- CSRF tokens sur POST/PUT/DELETE
- Chiffrement des mots de passe (bcrypt)
- Validation des entrées

## Performance

### Frontend
- Code splitting
- Lazy loading des images
- Mise en cache des requêtes API
- Minification CSS/JS

### Backend
- API Pagination (20 éléments par défaut)
- Index sur les colonnes fréquemment requêtées
- Sélection optimisée des champs (select_related, prefetch_related)
- Cache des données statiques

## Scalabilité

### Considérations

1. **Base de données**: PostgreSQL peut gérer des milliers de requêtes/s
2. **Backend**: Django gunicorn avec plusieurs workers
3. **Frontend**: Static assets servés par CDN
4. **Paiements**: Stripe gère la scalabilité
5. **Stockage**: Images servies via CDN

### Améliorations futures
- Cache Redis
- Queue asynchrone (Celery)
- Microservices pour les paiements
- Réplication base de données

## Déploiement

Voir [DEPLOYMENT.md](DEPLOYMENT.md)

## Technologies par couche

### Présentation
- React 18
- Tailwind CSS
- Axios
- React Router

### Application
- Django 4.2
- Django REST Framework
- Simple JWT
- Django Filters

### Données
- PostgreSQL / SQLite
- Django ORM

### Services Externes
- Stripe API
- AWS S3 (optionnel pour images)

## Points d'extension

1. **Authentification sociale**: Google, Facebook OAuth
2. **Notifications**: Email, SMS, Push
3. **Chat**: Websocket pour chat en temps réel
4. **Analytics**: Suivi des réservations et revenus
5. **Mobile**: React Native app
6. **Paiement fractionné**: Intégration PayPal
7. **Reviews**: Système d'avis des clients
8. **Loyalty**: Programme de fidélité
