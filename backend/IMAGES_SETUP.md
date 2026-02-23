# Installation des Images pour Sites et Terrains

## ✅ Modifications Effectuées

### 1. Model SiteImage Créé
- Fichier: `apps/sites/models.py`
- Champs:
  - `image`: ImageField pour les images du site
  - `title`: Titre optionnel de l'image
  - `description`: Description optionnelle
  - `is_primary`: Flag pour l'image principale
  - `uploaded_at`: Timestamp automatique

### 2. Model CourtImage Existant
- Fichier: `apps/courts/models.py`
- Déjà configuré avec les mêmes fonctionnalités pour les terrains

### 3. Django Admin - Configuration

#### Sites avec Images
- URL Admin: `/admin/sites/site/`
- Nouvelle interface "Inlines" pour télécharger/gérer plusieurs images par site
- Chaque site peut avoir une image primaire (et plusieurs secondaires)

#### Terrains avec Images
- URL Admin: `/admin/courts/court/`
- Inlines pour gérer les images de chaque terrain
- Gestion des images primaires et secondaires

#### Gestion Directe des Images
- URL Sites: `/admin/sites/siteimage/`
- URL Terrains: `/admin/courts/courtimage/`
- Filtrage par is_primary, date d'upload, site/terrain

### 4. Migrations Appliquées
- Migration créée: `sites/migrations/0003_...`
- Table `SiteImage` créée dans la base de données
- Toutes les migrations appliquées ✅

### 5. Sérialiseurs API Mis à Jour
- `apps/sites/serializers.py`:
  - Nouvel SiteImageSerializer
  - SiteSerializer inclut images + primary_image
  - SiteListSerializer inclut primary_image
  
- `apps/courts/serializers.py`:
  - Déjà configuré avec CourtImageSerializer
  - CourtListSerializer retourne la main_image

## 🚀 Utilisation dans Django Admin

### Pour ajouter des images à un site:
1. Allez sur `/admin/sites/site/`
2. Cliquez sur un site existant
3. Descendez jusqu'à la section "Images de site"
4. Cliquez sur "Ajouter une image"
5. Téléchargez l'image, ajoutez un titre/description
6. Cochez "Image primaire" pour la photo principale (optionnel)
7. Cliquez "Enregistrer"

### Pour ajouter des images à un terrain:
1. Allez sur `/admin/courts/court/`
2. Cliquez sur un terrain existant
3. Descendez jusqu'à la section "Imagesdu terrain"
4. Téléchargez comme décrit ci-dessus

## 📱 API Endpoints avec Images

### Sites avec Images:
```
GET /api/sites/
Retourne: id, name, city, description, images[], primary_image
```

### Terrains avec Images:
```
GET /api/courts/
Retourne: id, name, sport_type, price_per_hour, images[], main_image
```

## ✨ Fonctionnalités

✅ Plusieurs images par site/terrain
✅ Image principale (primary/main_image)
✅ Gestion complète dans Django Admin
✅ URLs des images retournées dans l'API
✅ Stockage des images: `/media/sites/images/` et `/media/courts/images/`

## 📝 Notes

- Les images sont upload automatiquement dans le dossier media
- Assurez-vous que `/media/` est bien configuré dans settings.py pour servir les images
- L'image primaire doit être définie manuellement dans l'Admin
- Possible d'ajouter plusieurs images à la fois dans l'interface inline
