# Flask Student Registration App

Mini-projet Flask pour l'inscription des étudiants avec Supabase.

## Structure du projet

```
flask_app/
├── app.py              # Application Flask principal
├── requirements.txt    # Dépendances Python
├── .env               # Variables d'environnement (Supabase)
├── .gitignore         # Fichiers à ignorer par Git
├── templates/
│   └── index.html     # Template HTML du formulaire
└── static/
    ├── style.css      # Styles CSS minimal (design japonais)
    ├── script.js      # Logique JavaScript côté client
    └── logo.png       # Votre logo (optionnel)
```

## Personnalisation

### Ajouter votre logo

1. Placez votre logo en image (PNG, JPG, SVG, etc.) dans le dossier `static/`
2. Nommez-le `logo.png` (ou modifiez le nom dans `templates/index.html` ligne 14)
3. Le logo s'affichera automatiquement en haut du formulaire
4. Taille recommandée : 100x100 pixels maximum

### Couleurs

Le design utilise une palette de couleurs japonaise minimaliste :
- **Rouge** : `#c41e3a` (couleur principale)
- **Blanc** : `#ffffff` (fond)
- **Noir** : `#1a1a1a` (texte)
- **Gris léger** : `#f5f5f5`, `#fafafa` (accents)

## Installation

1. **Créer un environnement virtuel Python :**
   ```bash
   python -m venv venv
   ```

2. **Activer l'environnement virtuel :**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Le fichier `.env` contient déjà vos identifiants Supabase. Aucune configuration supplémentaire nécessaire.

## Lancer l'application

```bash
python app.py
```

L'application sera accessible à `http://127.0.0.1:5000`

## Fonctionnalités

- ✅ Formulaire d'inscription avec validation
- ✅ Champs obligatoires : Prénom, Nom, Email
- ✅ Champs optionnels : Téléphone, Date de naissance
- ✅ Vérification de l'unicité de l'email
- ✅ Connexion à Supabase
- ✅ Génération automatique du code étudiant
- ✅ Design minimal et responsive
- ✅ Gradient d'arrière-plan moderne

## API Endpoints

### GET `/`
Retourne la page d'inscription avec l'année académique actuelle.

### POST `/api/register`
Enregistre un nouvel étudiant.

**Request body:**
```json
{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "phone_number": "+33612345678",
    "birth_date": "1990-01-15"
}
```

**Response (success):**
```json
{
    "success": true,
    "message": "Inscription réussie! Code étudiant: ABC123",
    "student_code": "ABC123"
}
```

**Response (error):**
```json
{
    "success": false,
    "error": "L'email 'jean.dupont@example.com' est déjà enregistré"
}
```

## Commandes utiles

- Installer une nouvelle dépendance: `pip install package_name && pip freeze > requirements.txt`
- Générer les requirements: `pip freeze > requirements.txt`
