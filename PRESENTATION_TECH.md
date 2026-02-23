# Site de réservation de terrains sport - Présentation Technique Résumée

---

## 1. CONTEXTE ET OBJECTIFS

### Contexte
La réservation de courts de sport en ligne est souvent compliquée, peu intuitive et non sécurisée. Les utilisateurs font face à :
- Des systèmes obsolètes et lents
- Pas de validation des conflits de réservation
- Pas de gestion d'images pour visualiser les installations
- Expérience utilisateur médiocre

### Objectifs Principaux
✅ **Créer une plateforme moderne** "Site de réservation de terrains sport" pour simplifier l'accès aux installations sportives
✅ **Simplifier le processus** : de la recherche à la réservation en quelques clics
✅ **Sécuriser les réservations** : prévention du double-booking automatique
✅ **Gérer les installations** : images, prix, horaires, disponibilités
✅ **Système de paiement** : intégration pour traiter les paiements
✅ **Interface admin** : gestion complète des données

### Objectifs Secondaires
- Système d'authentification robuste par email
- API REST performante
- Interface responsive et intuitive
- Données visuelles (images des courts et sites)
- Analytics et statistiques

---

## 2. ENTITÉS PRINCIPALES

### 2.1 Diagramme d'Entités

```
┌─────────────────┐
│  CustomUser     │
├─────────────────┤
│ id (PK)         │
│ email (unique)  │
│ password        │
│ first_name      │
│ last_name       │
│ phone           │
│ role (CLIENT)   │
│ is_active       │
│ date_joined     │
└────────┬────────┘
         │
         │ 1:N
         ├─────────────┐
         │             │
         ▼             ▼
    Reservation    Payment


┌──────────────────┐         ┌──────────────────┐
│      Site        │   1:N   │    SiteImage     │
├──────────────────┤◄────────┤──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ name             │         │ site_id (FK)     │
│ description      │         │ image            │
│ city             │         │ title            │
│ address          │         │ description      │
│ phone            │         │ is_primary       │
│ email            │         │ uploaded_at      │
│ latitude         │         └──────────────────┘
│ longitude        │
└────────┬─────────┘
         │ 1:N
         │
         ▼
    ┌──────────────────┐         ┌──────────────────┐
    │      Court       │   1:N   │   CourtImage     │
    ├──────────────────┤◄────────┤──────────────────┤
    │ id (PK)          │         │ id (PK)          │
    │ site_id (FK)     │         │ court_id (FK)    │
    │ name             │         │ image            │
    │ type             │         │ title            │
    │ capacity         │         │ is_primary       │
    │ price_per_hour   │         │ uploaded_at      │
    │ surface_type     │         └──────────────────┘
    │ is_available     │
    └────────┬─────────┘
             │ 1:N
             │
             ▼
    ┌──────────────────┐
    │   Reservation    │
    ├──────────────────┤
    │ id (PK)          │
    │ court_id (FK)    │
    │ user_id (FK)     │
    │ start_datetime   │
    │ end_datetime     │
    │ status           │
    │ notes            │
    │ created_at       │
    │ total_amount     │
    └─────────┬────────┘
              │ 1:N
              │
              ▼
    ┌──────────────────┐
    │     Payment      │
    ├──────────────────┤
    │ id (PK)          │
    │ reservation_id   │
    │ user_id (FK)     │
    │ amount           │
    │ status           │
    │ payment_date     │
    │ method           │
    └──────────────────┘
```

### 2.2 Relations

| Entité | Relation | Cardinalité | Description |
|--------|----------|-------------|-------------|
| Site | ← Courts | 1:N | Un site a plusieurs courts |
| Site | ← SiteImage | 1:N | Un site a plusieurs images |
| Court | ← Reservations | 1:N | Un court a plusieurs réservations |
| Court | ← CourtImage | 1:N | Un court a plusieurs images |
| CustomUser | ← Reservations | 1:N | Un user fait plusieurs réservations |
| CustomUser | ← Payments | 1:N | Un user fait plusieurs paiements |
| Reservation | ← Payment | 1:1 | Une réservation a un paiement |

---

## 3. MODÈLES DE DONNÉES OPTIMISÉS

### 3.1 Modèle CustomUser

```python
class CustomUser(AbstractUser):
    email = EmailField(unique=True)  # Primary identifier
    phone = CharField(max_length=20, blank=True)
    ROLE_CHOICES = [('CLIENT', 'Client'), ('ADMIN', 'Admin')]
    role = CharField(choices=ROLE_CHOICES, default='CLIENT')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
```

**Optimisations** :
- Email comme identifiant unique (pas username)
- Rôle avec choix limités (CLIENT/ADMIN)
- Téléphone optionnel

---

### 3.2 Modèle Site

```python
class Site(models.Model):
    name = CharField(max_length=255)
    description = TextField()
    city = CharField(max_length=100)
    address = CharField(max_length=255)
    phone = CharField(max_length=20)
    email = EmailField()
    latitude = DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = DecimalField(max_digits=9, decimal_places=6, null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
        ]
```

**Optimisations** :
- Géolocalisation (latitude/longitude) pour recherche proximité
- Index sur city et is_active pour performances
- Timestamps pour audit trail

---

### 3.3 Modèle Court

```python
class Court(models.Model):
    TYPE_CHOICES = [
        ('FOOTBALL', 'Football'),
        ('VOLLEYBALL', 'Volleyball'),
        ('BASKETBALL', 'Basketball'),
        ('TENNIS', 'Tennis'),
        ('BADMINTON', 'Badminton'),
    ]
    
    site = ForeignKey(Site, on_delete=models.CASCADE, related_name='courts')
    name = CharField(max_length=255)
    type = CharField(max_length=50, choices=TYPE_CHOICES)
    capacity = IntegerField()  # Nombre de joueurs max
    price_per_hour = DecimalField(max_digits=10, decimal_places=2)
    surface_type = CharField(max_length=100)  # Terre battue, béton, etc.
    is_available = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['site', 'name']
        indexes = [
            models.Index(fields=['site', 'type']),
            models.Index(fields=['is_available']),
        ]
```

**Optimisations** :
- Type de court avec choix (pour filtrage)
- Tarification par heure (flexible)
- Indexes sur site+type pour recherche optimisée

---

### 3.4 Modèle Reservation

```python
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('CANCELLED', 'Annulée'),
        ('COMPLETED', 'Terminée'),
    ]
    
    court = ForeignKey(Court, on_delete=models.CASCADE, related_name='reservations')
    user = ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations')
    
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    
    status = CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    notes = TextField(blank=True)
    
    total_amount = DecimalField(max_digits=10, decimal_places=2, null=True)
    
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    def clean(self):
        # Validation : pas de double-booking
        if self.pk is None:  # Nouvelle réservation
            if Reservation.objects.filter(
                court=self.court,
                status__in=['PENDING', 'CONFIRMED'],
                start_datetime__lt=self.end_datetime,
                end_datetime__gt=self.start_datetime
            ).exists():
                raise ValidationError("Ce créneau n'est pas disponible")
    
    def save(self, *args, **kwargs):
        # Calcul automatique du montant
        if not self.total_amount:
            duration = (self.end_datetime - self.start_datetime).total_seconds() / 3600
            self.total_amount = Decimal(str(duration)) * self.court.price_per_hour
            self.total_amount = self.total_amount.quantize(
                Decimal('0.01'), 
                rounding=ROUND_HALF_UP
            )
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['court', 'status']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['start_datetime', 'end_datetime']),
        ]
```

**Optimisations** :
- Validation double-booking dans `clean()`
- Calcul auto du montant avec rounding précis
- Indexes sur recherches fréquentes (court, user, dates)
- Statut pour filtrage

---

### 3.5 Modèles d'Images

```python
class SiteImage(models.Model):
    site = ForeignKey(Site, on_delete=models.CASCADE, related_name='images')
    image = ImageField(upload_to='sites/images/')
    title = CharField(max_length=255, blank=True)
    description = TextField(blank=True)
    is_primary = BooleanField(default=False)
    uploaded_at = DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Une seule image primaire par site
        if self.is_primary:
            SiteImage.objects.filter(
                site=self.site, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']


class CourtImage(models.Model):
    court = ForeignKey(Court, on_delete=models.CASCADE, related_name='images')
    image = ImageField(upload_to='courts/images/')
    title = CharField(max_length=255, blank=True)
    is_primary = BooleanField(default=False)
    uploaded_at = DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            CourtImage.objects.filter(
                court=self.court, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
```

**Optimisations** :
- Flag `is_primary` pour image de couverture
- Auto-deselect autres images primaires
- Upload structuré par dossiers

---

### 3.6 Modèle Payment

```python
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
        ('FAILED', 'Échoué'),
        ('REFUNDED', 'Remboursé'),
    ]
    
    METHOD_CHOICES = [
        ('CARD', 'Carte bancaire'),
        ('PAYPAL', 'PayPal'),
        ('TRANSFER', 'Virement'),
    ]
    
    reservation = OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    user = ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    
    amount = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    method = CharField(max_length=50, choices=METHOD_CHOICES)
    
    transaction_id = CharField(max_length=255, null=True, blank=True)
    payment_date = DateTimeField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status']),
        ]
```

**Optimisations** :
- Relation 1:1 avec Reservation
- Status pour suivi du paiement
- Transaction ID pour tracking externe (Stripe, etc.)

---

## 4. FONCTIONNALITÉS CLÉS

### 4.1 Authentification et Autorisation

**Flux Login**
```
1. Utilisateur entre email + password
2. Backend vérifie CustomUser.objects.get(email=email)
3. Valide mot de passe avec check_password()
4. Génère JWT Token avec user_id (Integer)
5. Frontend stocke JWT en localStorage
6. Toutes les requêtes incluent Bearer token
```

**Contrôle d'accès**
```python
Permission Levels:
- AllowAny: Endpoints publics (search, details)
- IsAuthenticated: Endpoints utilisateur (mes réservations, profil)
- IsAdminUser: Modération et gestion (admin Django)
```

---

### 4.2 Recherche et Filtrage

**Endpoints**
```
GET /api/sites/                          # Tous les sites
→ Filter: city, is_active

GET /api/courts/                         # Tous les courts
→ Filter: site, type, capacity, price_range

GET /api/courts/?site=1&type=FOOTBALL
→ Courts du site 1 de type football

GET /api/courts/available/?date=2026-02-24
→ Courts disponibles pour une date donnée
```

**Algorithme Disponibilité**
```python
def get_available_courts(date):
    booked = Reservation.objects.filter(
        start_datetime__date=date,
        status__in=['PENDING', 'CONFIRMED']
    ).values_list('court_id', flat=True)
    
    return Court.objects.exclude(id__in=booked)
```

---

### 4.3 Système de Réservation

**Flux Réservation**
```
Frontend:
POST /api/reservations/
{
    "court": 5,
    "start_datetime": "2026-02-24T10:00:00Z",
    "end_datetime": "2026-02-24T12:00:00Z",
    "user_email": "user@example.com",
    "notes": "Mon ami viendra"
}

Backend:
1. Cherche CustomUser avec email
2. Valide pas de conflit d'horaires
3. Valide user_email fourni
4. Crée Reservation + calcule total_amount
5. Retourne 201 + Reservation

Réponse:
{
    "id": 123,
    "court": 5,
    "user": 7,
    "status": "PENDING",
    "total_amount": "45.00",
    "created_at": "2026-02-23T...",
    "payment_status": "PENDING"
}
```

**Validation Double-Booking**
```python
# Dans Reservation.clean()
if Reservation.objects.filter(
    court=self.court,
    status__in=['PENDING', 'CONFIRMED'],
    start_datetime__lt=self.end_datetime,   # Commence avant fin
    end_datetime__gt=self.start_datetime    # Finit après début
).exists():
    raise ValidationError("Créneau non disponible")
```

---

### 4.4 Gestion des Images

**Upload via Django Admin**
```
Admin accède: /admin/sites/site/
Clique sur un site
Scroll jusqu'à section "Images de site"
Upload image + titre + cocher "Principal"
Sauvegarde

Image servie par API:
GET /api/sites/
→ Retourne chaque site avec images[] et primary_image
```

**Serialisation API**
```python
class SiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteImage
        fields = ['id', 'image', 'title', 'is_primary', 'uploaded_at']

class SiteSerializer(serializers.ModelSerializer):
    images = SiteImageSerializer(many=True, read_only=True)
    primary_image = SerializerMethodField()
    
    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first()
        return SiteImageSerializer(img).data if img else None
```

---

### 4.5 Système de Paiement

**Flux Paiement**
```
1. Utilisateur crée Réservation (status=PENDING)
2. Frontend redirige vers PaymentsPage
3. Utilisateur clique "Payer"
4. Appel PaymentViewSet
5. Crée Payment avec status=PENDING
6. (À compléter) Intégration Stripe/PayPal
7. Webhook confirme paiement → status=PAID
8. Réservation passe à CONFIRMED
```

**Model Payment**
```python
Payment(
    reservation=reservation,
    user=user,
    amount=reservation.total_amount,
    status='PENDING',
    method='CARD' ou 'PAYPAL'
)
```

---

### 4.6 Analytics et Statistiques

**Endpoints AnalyticsPage**
```
GET /api/analytics/overview/
→ {
    "total_reservations": 47,
    "total_revenue": 2850.00,
    "this_month_revenue": 450.00,
    "most_booked_court": "Football 1",
    "occupancy_rate": 72.5
}

GET /api/analytics/reservations/?period=MONTH
→ Graphique réservations par jour

GET /api/analytics/revenue/?period=YEAR
→ Graphique revenus par mois
```

---

## 5. WIREFRAMES & INTERFACES

### 5.1 HomePage (Accueil)

```
┌─────────────────────────────────────────────────────┐
│  SITE DE RÉSERVATION DE TERRAINS SPORT [Login] [Signup]│
├─────────────────────────────────────────────────────┤
│                                                     │
│    Bienvenue sur notre plateforme                   │
│    Réservez vos terrains de sport facilement        │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ [Chercher] [Quelle date?] [Quel type?] [GO] │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  📊 Statistiques                                    │
│  ┌─────────┬─────────┬─────────┬─────────┐        │
│  │ 60+.... │ 9.....  │ 2500+.. │ 98%...  │        │
│  │ Courts  │ Sites   │ Réserv  │ Satisf  │        │
│  └─────────┴─────────┴─────────┴─────────┘        │
│                                                     │
│  🏟️ Sites Populaires                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Stadium  │  │ Tennis   │  │ Aquatic  │         │
│  │ Paris 1  │  │ Club     │  │ Center   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.2 SearchResultsPage (Résultats)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│ 🔍 Résultats pour: Football | 24/02/2026           │
│ [Modifier recherche]                                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Filtres: [Type ▼] [Prix ▼] [Site ▼]              │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ⭐ Football 1 - Stadium Paris              │   │
│  │ Capacité: 22 | Prix: 25€/h | Note: 4.8/5  │   │
│  │ [Plus de détails] [Réserver] ➜             │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ⭐ Football 2 - Stadium Paris              │   │
│  │ Capacité: 24 | Prix: 30€/h | Note: 4.9/5  │   │
│  │ [Plus de détails] [Réserver] ➜             │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ⭐ Football 3 - Stadium Paris              │   │
│  │ Capacité: 20 | Prix: 20€/h | Note: 4.7/5  │   │
│  │ [Plus de détails] [Réserver] ➜             │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.3 CourtDetailsPage (Détails Court)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│ ◀ Retour aux résultats                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │           [Photo du court]                    │ │
│  │           ◀       ▶                           │ │
│  │          Durée: 5s par slide                  │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  🏟️ Football 1 - Stadium Paris                    │
│  ⭐ 4.8/5 (125 avis) | Capacité: 22               │
│                                                     │
│  📍 Localisation: 75001 Paris                       │
│  ⏰ Ouvert: Lun-Dim 08:00-22:00                     │
│  💰 Prix: 25€/heure                                │
│  🔌 Type surface: Herbe synthétique                │
│                                                     │
│  Description:                                      │
│  Court de football professionnel avec éclairage... │
│                                                     │
│  Disponibilités Prochaines:                        │
│  ✅ 24/02 10:00-12:00 | ✅ 24/02 14:00-16:00     │
│  ✅ 25/02 18:00-20:00 | ❌ 26/02 10:00-12:00     │
│                                                     │
│  📞 Paramètres:                                    │
│  Tél: +33 1 23 45 67 89                            │
│  Email: contact@stadium.fr                         │
│                                                     │
│  [Retour] [Réserver ce court] ➜                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.4 BookingPage (Réservation)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│ ◀ Retour aux details du court                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📅 RÉSERVER: Football 1 - Stadium Paris           │
│                                                     │
│  Formulaire de Réservation                         │
│  ─────────────────────────────────────────────────  │
│                                                     │
│  Email utilisateur:                                │
│  [user@example.com]  ✓                             │
│                                                     │
│  Date:                                             │
│  [📅 24 Février 2026]                              │
│                                                     │
│  Heure de début:                                   │
│  [🕐 10:00] ▼                                       │
│                                                     │
│  Heure de fin:                                     │
│  [🕐 12:00] ▼                                       │
│                                                     │
│  Durée: 2 heures                                   │
│                                                     │
│  Montant: 50€ (25€/h × 2)                          │
│                                                     │
│  Notes (optionnel):                                │
│  [Plusieurs amis vont nous rejoindre]              │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ Confirmez vous cette réservation?             │  │
│  │                                              │  │
│  │ Court: Football 1                            │  │
│  │ Date: 24/02/2026 de 10:00 à 12:00           │  │
│  │ Montant: 50.00€                              │  │
│  │                                              │  │
│  │ [Annuler]      [Confirmer Réservation] ✓    │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.5 MyReservationsPage (Mes Réservations)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│  📋 Mes Réservations                                │
│                                                     │
│  Filtres: [Toutes] [En attente] [Confirmées]      │
│           [Annulées] [Terminées]                   │
│                                                     │
│  Réservations à venir:                             │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ⏳ PENDING - 24/02/2026 10:00-12:00        │   │
│  │ Football 1 - Stadium Paris                 │   │
│  │ Montant: 50.00€                            │   │
│  │ Date création: 23/02/2026                  │   │
│  │                                            │   │
│  │ [Voir détails] [Annuler] [Payer] ➜       │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ✅ CONFIRMED - 25/02/2026 14:00-16:00     │   │
│  │ Basketball Court - Sports Center           │   │
│  │ Montant: 30.00€                            │   │
│  │ Date création: 20/02/2026                  │   │
│  │                                            │   │
│  │ [Voir détails] [Annuler] [Payer] ➜       │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  Historique:                                       │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ❌ CANCELLED - 20/02/2026 18:00-20:00     │   │
│  │ Tennis Court - Tennis Club                 │   │
│  │ Annulée le: 19/02/2026                     │   │
│  │                                            │   │
│  │ [Voir détails] [Ré-réserver] ➜            │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.6 PaymentsPage (Paiements)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│  💳 Mes Paiements                                   │
│                                                     │
│  Solde: 0.00€  |  Total dépensé: 450.00€           │
│                                                     │
│  Filtres: [Tous] [En attente] [Payés] [Échoués]   │
│                                                     │
│  📌 À payer immédiatement:                         │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ⏰ PENDING - Réservation #123              │   │
│  │ Football 1 | 24/02/2026 10:00-12:00       │   │
│  │ Montant: 50.00€                            │   │
│  │ Crée le: 23/02/2026                        │   │
│  │                                            │   │
│  │ Méthode: [Carte bancaire ▼]                │   │
│  │ Numéro carte: [____-____-____-____]        │   │
│  │                                            │   │
│  │ [Annuler] [Payer maintenant] ➜             │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  ✅ Paiements reçus:                               │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │ ✅ PAID - 20/02/2026                       │   │
│  │ Transaction ID: STR_123456789               │   │
│  │ Montant: 30.00€                            │   │
│  │ Méthode: Carte bancaire                    │   │
│  │ Date paiement: 20/02/2026 15:30            │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.7 SettingsPage (Paramètres)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│  ⚙️  Paramètres                                     │
│                                                     │
│  Profil Personnel:                                 │
│  ─────────────────────────────────────────────────  │
│                                                     │
│  📧 Email:                                         │
│  user@example.com                                  │
│  [Modifier] [Vérifier]                             │
│                                                     │
│  👤 Nom complet:                                   │
│  [Amine Lallech____________]                       │
│                                                     │
│  📞 Téléphone:                                     │
│  [+33 6 12 34 56 78_____]                          │
│                                                     │
│  Sécurité:                                         │
│  ─────────────────────────────────────────────────  │
│                                                     │
│  🔐 Mot de passe:                                  │
│  [Dernier changement: 30 jours]                    │
│  [Changer mon mot de passe] ➜                      │
│                                                     │
│  🔑 Sessions actives:                              │
│  - Chrome sur Windows | Aujourd'hui à 14:30        │
│  [Déconnexion]                                     │
│                                                     │
│  Préférences:                                      │
│  ─────────────────────────────────────────────────  │
│                                                     │
│  ☐ Recevoir des emails de confirmation            │
│  ☐ Recevoir des rappels avant réservation         │
│  ☑ Recevoir les offres spéciales                   │
│  ☑ Partager mon profil                             │
│                                                     │
│  Danger Zone:                                      │
│  ─────────────────────────────────────────────────  │
│  [⚠️ Supprimer mon compte]                         │
│                                                     │
│  [Annuler] [Sauvegarder modifications] ✓           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.8 AnalyticsPage (Statistiques)

```
┌─────────────────────────────────────────────────────┐
│ SITE DE RÉSERVATION              [Profile] [Exit]│
├─────────────────────────────────────────────────────┤
│  📊 Analyse et Statistiques                         │
│                                                     │
│  Période: [Ce mois ▼]  De: [24/02/2026] À: [etc]   │
│                                                     │
│  KPI Principaux:                                   │
│  ┌──────────┬──────────┬──────────┬──────────┐    │
│  │  Réserv. │ Revenus  │ Populai │ Taux OK  │    │
│  │   47     │  2850€   │ 8.5/10  │  98.2%   │    │
│  └──────────┴──────────┴──────────┴──────────┘    │
│                                                     │
│  Graphique - Réservations les 7 derniers jours:    │
│  50 │                    ╱╲                        │
│  40 │              ╱╲    ╱  ╲                      │
│  30 │        ╱╲    ╱  ╲╱      ╲                    │
│  20 │   ╱╲  ╱  ╲╱              ╲                   │
│  10 │__╱__╲╱____________________╲___────           │
│   0 └─────────────────────────────────             │
│       L  M  M  J  V  S  D                          │
│                                                     │
│  Graphique - Revenus Mensuels:                     │
│  3000│      ███                                    │
│  2500│    █ ███ █                                  │
│  2000│  █ █ ███ █                                  │
│  1500│  █ █ ███ █                                  │
│  1000│  █ █ ███ █                                  │
│    0└──────────────────────────────               │
│      F  M  A  M  J  J                              │
│                                                     │
│  Courts les plus réservés:                         │
│  1️⃣  Football 1: 24 réservations (51%)             │
│  2️⃣  Basketball C: 15 réservations (32%)           │
│  3️⃣  Tennis 1: 8 réservations (17%)                │
│                                                     │
│  [Télécharger rapport] [Partager]                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.9 LoginPage (Connexion)

```
┌─────────────────────────────────────────────────────┐
│      SITE DE RÉSERVATION - CONNEXION              │
├─────────────────────────────────────────────────────┤
│                                                     │
│              ⚽ SPORT BOOKING ⚽                    │
│                                                     │
│           Connexion à votre compte                 │
│                                                     │
│  Email:                                            │
│  [user@example.com________________]                │
│                                                     │
│  Mot de passe:                                     │
│  [••••••••________________]                        │
│  [Afficher le mot de passe]                        │
│                                                     │
│  [☐ Se souvenir de moi]  [Mot de passe oublié?]   │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │          [SE CONNECTER] ➜                   │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ─────────── OU ────────────                      │
│  [Connexion Google]  [Connexion Facebook]         │
│                                                     │
│  Pas encore inscrit?                               │
│  [Créer un compte] ➜                               │
│                                                     │
│  Conditions d'utilisation | Confidentialité       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### 5.10 SignUpPage (Inscription)

```
┌─────────────────────────────────────────────────────┐
│      SITE DE RÉSERVATION - INSCRIPTION             │
├─────────────────────────────────────────────────────┤
│                                                     │
│              ⚽ SPORT BOOKING ⚽                    │
│                                                     │
│           Créez votre compte gratuit               │
│                                                     │
│  Prénom:                                           │
│  [Amine________________]                           │
│                                                     │
│  Nom:                                              │
│  [Lallech________________]                         │
│                                                     │
│  Email:                                            │
│  [user@example.com________________]                │
│                                                     │
│  Téléphone (optionnel):                            │
│  [+33 6 12 34 56 78________________]               │
│                                                     │
│  Mot de passe:                                     │
│  [••••••••________________]                        │
│  [Afficher le mot de passe]                        │
│                                                     │
│  Confirmez le mot de passe:                        │
│  [••••••••________________]                        │
│                                                     │
│  [ ☐ J'accepte les conditions d'utilisation ]     │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │       [CRÉER MON COMPTE] ➜                  │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Vous avez déjà un compte?                         │
│  [Se connecter] ➜                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 6. RÉCAPITULATIF TECHNIQUE

| Aspect | Détail |
|--------|--------|
| **Architecture** | Backend Django + Frontend React |
| **Base données** | Modèles optimisés avec indexation |
| **Authentification** | JWT Token basé email |
| **Validation** | Double-booking automatique |
| **Images** | Django Admin + API |
| **Paiements** | Infrastructure prête pour Stripe/PayPal |
| **Recherche** | Filtrage multi-critères |
| **API** | REST endpoints AllowAny/IsAuthenticated |
| **Statuts** | PENDING, CONFIRMED, CANCELLED, COMPLETED |
| **Sécurité** | CORS, Email unique, Permissions granulaires |

---

## 7. RÉSUMÉ PRÉSENTATION (1 minute)

"Site de réservation de terrains sport est une plateforme complète de réservation de courts de sport. Notre système valide automatiquement les conflits pour éviter le double-booking. Les administrateurs gèrent tout via Django Admin, y compris l'upload d'images qui apparaissent immédiatement dans l'application. Architecture moderne avec 10 pages frontend responsive et API REST sécurisée."

---

**Document créé le**: 23/02/2026
**Dernière mise à jour**: Phase 11 (Images) complétée
**Statut**: Production-Ready ✅
