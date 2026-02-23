# 💾 Base de données - SportBooking

## Diagramme Entité-Relation

```
┌─────────────┐
│    Role     │
├─────────────┤
│ id (PK)     │
│ name        │
│ description │
└─────────────┘
      ↑
      │ 1
      │
      │ many
┌──────────────────────┐
│    CustomUser        │
├──────────────────────┤
│ id (PK)              │
│ email (UNIQUE)       │
│ first_name           │
│ last_name            │
│ phone                │
│ password             │
│ role_id (FK)         │─────┊
│ is_active            │     │
│ created_at           │     │
│ updated_at           │     │
│ gdpr_consent         │     │
└──────────────────────┘     │
      ↑                       │
      │1                      │
      │ many                  │
      │ │                     │
      │ └──────────┐          │
      │            ↓          │
      │      ┌──────────────────────┐
      │      │       Site           │
      │      ├──────────────────────┤
      │      │ id (PK)              │
      │      │ name                 │
      │      │ description          │
      │      │ address              │
      │      │ city                 │
      │      │ postal_code          │
      │      │ latitude             │
      │      │ longitude            │
      │      │ manager_id (FK) ─────┘
      │      │ is_active            │
      │      │ created_at           │
      │      │ updated_at           │
      │      └──────────────────────┘
      │            ↑
      │            │1
      │            │ many
      │      ┌──────────────────┐
      │      │  OpeningHours    │
      │      ├──────────────────┤
      │      │ id (PK)          │
      │      │ site_id (FK)     │
      │      │ day_of_week      │
      │      │ open_time        │
      │      │ close_time       │
      │      └──────────────────┘
      │
      │1
      │ many
┌──────────────────────────┐
│       Court              │
├──────────────────────────┤
│ id (PK)                  │
│ name                     │
│ description              │
│ sport_type               │
│ site_id (FK)             │
│ price_per_hour           │
│ capacity                 │
│ is_active                │
│ created_at               │
│ updated_at               │
└──────────────────────────┘
      ↑ 1
      │ many
      │
      ├────────────────────────────────────┐
      │                                    │
┌─────────────────┐          ┌──────────────────────┐
│  CourtImage     │          │  BlockedPeriod       │
├─────────────────┤          ├──────────────────────┤
│ id (PK)         │          │ id (PK)              │
│ court_id (FK)   │          │ court_id (FK)        │
│ image           │          │ start_datetime       │
│ title           │          │ end_datetime         │
│ is_primary      │          │ reason               │
│ uploaded_at     │          │ created_at           │
└─────────────────┘          └──────────────────────┘
      
┌─────────────────────┐
│    Equipment        │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ description         │
│ icon                │
└─────────────────────┘
      ↑
      │ many-to-many
      │
      └─────────────┐
                    │
              ┌─────────────────────┐
              │ Court_Equipment     │
              ├─────────────────────┤
              │ court_id (FK)       │
              │ equipment_id (FK)   │
              │ (Many-to-Many)      │
              └─────────────────────┘

┌──────────────────────────┐
│    Reservation           │
├──────────────────────────┤
│ id (PK)                  │
│ user_id (FK) ────────────┼─────→ CustomUser
│ court_id (FK) ───────────┼─────→ Court
│ start_datetime           │
│ end_datetime             │
│ price_per_hour (snapshot)│
│ total_amount             │
│ status                   │
│ notes                    │
│ created_at               │
│ updated_at               │
│ cancelled_at             │
└──────────────────────────┘
      ↑ 1
      │ 1
      │
      │
┌──────────────────────┐
│     Payment          │
├──────────────────────┤
│ id (PK)              │
│ reservation_id (FK)  │
│ amount               │
│ currency             │
│ method               │
│ status               │
│ transaction_ref      │
│ stripe_intent_id     │
│ stripe_charge_id     │
│ paypal_trans_id      │
│ metadata (JSON)      │
│ created_at           │
│ updated_at           │
│ paid_at              │
└──────────────────────┘
      ↑ 1
      │ 1
      │
      │
┌──────────────────────┐
│     Invoice          │
├──────────────────────┤
│ id (PK)              │
│ payment_id (FK)      │
│ invoice_number       │
│ pdf_file             │
│ created_at           │
│ updated_at           │
└──────────────────────┘
```

## Structure des tables

### Role
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| name | VARCHAR(20) | UNIQUE | CLIENT/MANAGER/ADMIN |
| description | TEXT | | Description du rôle |

### CustomUser
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| username | VARCHAR(150) | UNIQUE | Nom d'utilisateur |
| email | VARCHAR(254) | UNIQUE | Email unique |
| first_name | VARCHAR(150) | | Prénom |
| last_name | VARCHAR(150) | | Nom |
| phone | VARCHAR(20) | | Téléphone |
| password | VARCHAR(255) | | Hash du mot de passe |
| role_id | INT | FK(Role) | Rôle de l'utilisateur |
| is_active | BOOLEAN | DEFAULT TRUE | Utilisateur actif |
| created_at | DATETIME | DEFAULT NOW | Date création |
| updated_at | DATETIME | DEFAULT NOW | Date modification |
| gdpr_consent | BOOLEAN | DEFAULT FALSE | Consentement RGPD |
| is_superuser | BOOLEAN | DEFAULT FALSE | Admin Django |

### Site
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| name | VARCHAR(255) | | Nom du site |
| description | TEXT | | Description |
| address | VARCHAR(500) | | Adresse |
| city | VARCHAR(100) | | Ville |
| postal_code | VARCHAR(10) | | Code postal |
| latitude | DECIMAL(9,6) | | Latitude GPS |
| longitude | DECIMAL(9,6) | | Longitude GPS |
| manager_id | INT | FK(User) | Gestionnaire |
| is_active | BOOLEAN | DEFAULT TRUE | Site actif |
| created_at | DATETIME | DEFAULT NOW | Date création |
| updated_at | DATETIME | DEFAULT NOW | Date modification |

Indexes: city, manager_id, is_active

### OpeningHours
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| site_id | INT | FK(Site) | Site concerné |
| day_of_week | INT | 0-6 | Lundi-Dimanche |
| open_time | TIME | | Heure ouverture |
| close_time | TIME | | Heure fermeture |

Unique: (site_id, day_of_week)

### Court
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| name | VARCHAR(255) | | Nom du terrain |
| description | TEXT | | Description |
| sport_type | VARCHAR(50) | | Type de sport |
| site_id | INT | FK(Site) | Site d'appartenance |
| price_per_hour | DECIMAL(10,2) | | Prix/heure |
| capacity | INT | DEFAULT 2 | Capacité |
| is_active | BOOLEAN | DEFAULT TRUE | Terrain actif |
| created_at | DATETIME | DEFAULT NOW | Date création |
| updated_at | DATETIME | DEFAULT NOW | Date modification |

Indexes: site_id, sport_type, is_active

### CourtImage
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| court_id | INT | FK(Court) | Terrain |
| image | VARCHAR | | Path image |
| title | VARCHAR(255) | | Titre image |
| is_primary | BOOLEAN | DEFAULT FALSE | Image principale |
| uploaded_at | DATETIME | DEFAULT NOW | Date upload |

### Equipment
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| name | VARCHAR(100) | UNIQUE | Nom équipement |
| description | TEXT | | Description |
| icon | VARCHAR(50) | | Icône |

### BlockedPeriod
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| court_id | INT | FK(Court) | Terrain |
| start_datetime | DATETIME | | Début blocage |
| end_datetime | DATETIME | | Fin blocage |
| reason | VARCHAR(255) | | Raison |
| created_at | DATETIME | DEFAULT NOW | Date création |

Indexes: (court_id, start_datetime)

### Reservation
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| user_id | INT | FK(User) | Client |
| court_id | INT | FK(Court) | Terrain |
| start_datetime | DATETIME | | Début réservation |
| end_datetime | DATETIME | | Fin réservation |
| price_per_hour | DECIMAL(10,2) | | Prix/h (snapshot) |
| total_amount | DECIMAL(10,2) | | Total montant |
| status | VARCHAR(20) | | PENDING/CONFIRMED/CANCELLED |
| notes | TEXT | | Notes |
| created_at | DATETIME | DEFAULT NOW | Date création |
| updated_at | DATETIME | DEFAULT NOW | Date modification |
| cancelled_at | DATETIME | NULL | Date annulation |

Indexes: user_id, court_id, start_datetime, status

Unique constraint empêchant les chevauchements

### Payment
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| reservation_id | INT | FK(Reservation) | Réservation |
| amount | DECIMAL(10,2) | | Montant |
| currency | VARCHAR(3) | DEFAULT EUR | Devise |
| method | VARCHAR(20) | | Méthode paiement |
| status | VARCHAR(20) | | PENDING/SUCCESS/FAILED/REFUNDED |
| stripe_payment_intent_id | VARCHAR(255) | UNIQUE | ID Stripe |
| stripe_charge_id | VARCHAR(255) | | ID charge Stripe |
| paypal_transaction_id | VARCHAR(255) | | ID transaction PayPal |
| transaction_reference | VARCHAR(255) | | Référence générique |
| metadata | JSON | | Données additionnelles |
| created_at | DATETIME | DEFAULT NOW | Date création |
| updated_at | DATETIME | DEFAULT NOW | Date modification |
| paid_at | DATETIME | NULL | Date paiement |

### Invoice
| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| id | INT | PK | Identifiant unique |
| payment_id | INT | FK(Payment) | Paiement |
| invoice_number | VARCHAR(50) | UNIQUE | Numéro facture |
| pdf_file | VARCHAR | | Chemin PDF |
| created_at | DATETIME | DEFAULT NOW | Date création |
| updated_at | DATETIME | DEFAULT NOW | Date modification |

## Migrations Django

### Créer une migration

```bash
python manage.py makemigrations
```

### Appliquer les migrations

```bash
python manage.py migrate
```

### Voir l'état des migrations

```bash
python manage.py showmigrations
```

## Requêtes courantes

### Terrains libres à une date donnée

```python
from django.db.models import Q
from apps.courts.models import Court
from apps.reservations.models import Reservation
from datetime import datetime

start = datetime(2024, 1, 15, 10, 0)
end = datetime(2024, 1, 15, 11, 0)

available_courts = Court.objects.filter(
    is_active=True
).exclude(
    Q(reservations__start_datetime__lt=end) &
    Q(reservations__end_datetime__gt=start) &
    Q(reservations__status__in=['CONFIRMED', 'PENDING'])
)
```

### Revenus d'un site

```python
from apps.payments.models import Payment
from apps.reservations.models import Reservation

site_id = 1

revenue = Payment.objects.filter(
    reservation__court__site_id=site_id,
    status='SUCCESS'
).aggregate(Sum('amount'))

print(revenue['amount__sum'])
```

### Taux d'occupation

```python
total = Reservation.objects.filter(
    court__site_id=site_id
).count()

confirmed = Reservation.objects.filter(
    court__site_id=site_id,
    status='CONFIRMED'
).count()

occupancy = (confirmed / total * 100) if total > 0 else 0
```
