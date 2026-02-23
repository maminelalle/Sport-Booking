# 📚 Documentation API REST - SportBooking

## Vue d'ensemble

L'API REST de SportBooking est construite avec Django REST Framework et utilise l'authentification JWT.

## Base URL

- Développement: `http://localhost:8000/api`
- Production: À définir lors du déploiement

## Documentation Interactive

- Swagger UI: `{base_url}/docs/`
- ReDoc: `{base_url}/redoc/`

## Authentification

Tous les endpoints sauf ceux marqués `[PUBLIC]` requièrent un token JWT.

### Obtenir un token

```
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Utiliser le token

Ajouter l'en-tête `Authorization` à toutes les requêtes:

```
Authorization: Bearer {access_token}
```

### Rafraîchir le token

```
POST /auth/refresh_token/
Content-Type: application/json

{
  "refresh": "refresh_token_value"
}
```

## Endpoints Principaux

### Authentification

#### Inscription
```
POST /auth/register/ [PUBLIC]
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+33123456789",
  "password": "securepassword",
  "password_confirm": "securepassword",
  "role": 1,
  "gdpr_consent": true
}
```

#### Connexion
```
POST /auth/login/ [PUBLIC]
{
  "email": "user@example.com",
  "password": "password"
}
```

#### Profil
```
GET /auth/me/
GET /auth/users/{id}/
PUT /auth/users/{id}/ (vous-même)
```

### Sites

#### Lister les sites
```
GET /sites/
Filtres: city, is_active
Recherche: name, city, address
```

#### Détails d'un site
```
GET /sites/{id}/
```

#### Créer un site [MANAGER/ADMIN]
```
POST /sites/
{
  "name": "Centre Sportif Paris",
  "address": "123 Rue de Paris",
  "city": "Paris",
  "postal_code": "75001",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "description": "...",
  "manager": 1,
  "is_active": true
}
```

#### Horaires d'ouverture
```
GET /sites/{id}/opening_hours/
POST /sites/{id}/set_opening_hours/
[
  {
    "day_of_week": 0,
    "open_time": "08:00:00",
    "close_time": "22:00:00"
  },
  ...
]
```

### Terrains

#### Lister les terrains [PUBLIC]
```
GET /courts/courts/
Filtres: sport_type, site, is_active
Recherche: name, description, site__name
```

#### Détails d'un terrain [PUBLIC]
```
GET /courts/courts/{id}/
```

#### Créer un terrain [MANAGER/ADMIN]
```
POST /courts/courts/
{
  "name": "Terrain 1",
  "description": "...",
  "sport_type": "TENNIS",
  "site": 1,
  "price_per_hour": 25.00,
  "capacity": 2,
  "is_active": true,
  "equipments": [1, 2, 3]
}
```

#### Vérifier la disponibilité
```
GET /courts/courts/{id}/availability/?start=2024-01-15T10:00:00&end=2024-01-15T11:00:00
```

#### Équipements [PUBLIC]
```
GET /courts/equipments/
```

### Réservations

#### Créer une réservation
```
POST /reservations/
{
  "court": 1,
  "start_datetime": "2024-01-15T10:00:00Z",
  "end_datetime": "2024-01-15T11:00:00Z",
  "notes": "..."
}
```

#### Mes réservations
```
GET /reservations/my_reservations/
```

#### Détails d'une réservation
```
GET /reservations/{id}/
```

#### Vérifier la disponibilité (avant réservation)
```
POST /reservations/check_availability/
{
  "court_id": 1,
  "start": "2024-01-15T10:00:00Z",
  "end": "2024-01-15T11:00:00Z"
}
```

#### Annuler une réservation
```
POST /reservations/{id}/cancel/
{
  "reason": "Raison de l'annulation (optionnel)"
}
```

### Paiements

#### Lister les paiements
```
GET /payments/payments/
```

#### Créer un Payment Intent
```
POST /payments/payments/create_payment_intent/
{
  "reservation_id": 1
}

Response:
{
  "payment_intent_id": "pi_xxxx",
  "client_secret": "pi_xxxx_secret",
  "amount": 25.00,
  "currency": "EUR"
}
```

#### Confirmer un paiement
```
POST /payments/payments/confirm_payment/
{
  "payment_intent_id": "pi_xxxx"
}
```

#### Rembourser un paiement
```
POST /payments/payments/{id}/refund/
```

#### Liste des factures
```
GET /payments/invoices/
```

## Codes de statut HTTP

| Code | Signification |
|------|---------------|
| 200 | OK - Requête réussie |
| 201 | Created - Ressource créée |
| 204 | No Content - Succès sans contenu |
| 400 | Bad Request - Erreur de requête |
| 401 | Unauthorized - Authentification requise |
| 403 | Forbidden - Accès refusé |
| 404 | Not Found - Ressource non trouvée |
| 429 | Too Many Requests - Trop de requêtes |
| 500 | Server Error - Erreur serveur |

## Format des erreurs

```json
{
  "detail": "Message d'erreur détaillé",
  "errors": {
    "field_name": ["Message d'erreur"]
  }
}
```

## Pagination

```
GET /endpoint/?page=1&page_size=20
```

## Filtrage

```
GET /endpoint/?field=value&field2=value2
```

## Recherche

```
GET /endpoint/?search=keyword
```

## Tri

```
GET /endpoint/?ordering=field_name
GET /endpoint/?ordering=-field_name (décroissant)
```

## Limites de taux (Rate Limiting)

À définir selon la configuration de déploiement

## Exemples cURL

### Créer une réservation

```bash
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "court": 1,
    "start_datetime": "2024-01-15T10:00:00Z",
    "end_datetime": "2024-01-15T11:00:00Z"
  }'
```

### Récupérer mes réservations

```bash
curl -X GET http://localhost:8000/api/reservations/my_reservations/ \
  -H "Authorization: Bearer your_token"
```

## Webhooks Stripe

Les webhooks Stripe sont traités automatiquement:

- `payment_intent.succeeded` - Paiement approuvé
- `payment_intent.payment_failed` - Paiement échoué

Endpoint: `POST /payments/stripe-webhook/`

## Changements API (Versioning)

L'API utilise le versioning implicite. Les changements majeurs seront communiqués.

## Support

Pour toute question sur l'API, consultez:
- La documentation interactive: `/api/docs/`
- Les issues GitHub
