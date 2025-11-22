# Template Admin & Document Generation Module

Ce module Django fournit un système complet pour : 
- gérer des **templates DOCX**, 
- configurer des **champs dynamiques**, 
- récupérer des données via des **datasources API**, 
- pré-remplir un formulaire avant génération, 
- générer un **document final DOCX** via `docxtpl`.

Il est pensé pour être **intégrable dans n'importe quel projet Django**,
sans dépendances spécifiques à un métier.

------------------------------------------------------------------------

## 🚀 Fonctionnalités principales

### 1. Gestion des templates DOCX

-   Upload des fichiers DOCX depuis l'admin Django.
-   Association de plusieurs datasources à un même template.
-   Définition d'une liste de champs avec :
    -   type (`text`, `number`, `date`, `choice`, `table`)
    -   source de données
    -   clé JMESPath
    -   options de choix
    -   champs utilisateurs

------------------------------------------------------------------------

### 2. Pré-remplissage automatique (API)

L'API prend un `template_slug` + des paramètres et renvoie un **contexte
auto-rempli**.

Exemple d'appel :

``` json
GET /api/documents/prefill/
{
  "business_code": "invoice",
  "params": { "invoice_id": 24 }
}
```

Réponse :

``` json
{
  "template": "invoice",
  "fields": [
    { "name": "client_name", "label": "Nom du client", "value": "John Doe", "field_type": "text", "is_user_input": false },
    { "name": "items", "label": "Liste d'objets", "value": [ ... ], "field_type": "table", "is_user_input": false }
  ]
}
```

------------------------------------------------------------------------

### 3. Génération du document (API)

L'API reçoit un **contexte final** et renvoie un document `.docx`.

Exemple :

``` json
POST /api/templates/render/
{
  "template": "invoice",
  "context": {
    "client_name": "John Doe",
    "items": [...]
  }
}
```

------------------------------------------------------------------------

## 📂 Structure du module

    templates_admin/
     ├── doc_templates/
     ├── generated_docs/
     ├── migrations/
     ├── services/
     │     ├── datasource_engine.py
     │     ├── data_resolver.py
     │     ├── template_prefill_engine.py
     │     ├── template_resolver.py
     │     └── templating_engine.
     ├── admin.py
     ├── apps.py
     ├── models.py
     ├── serializers.py
     ├── test_api.py
     ├── tests.py
     ├── urls.py
     └── Views.py

------------------------------------------------------------------------

## ⚙️ Installation

1.  Copier le dossier `templates_admin/` dans votre projet Django.
2.  Ajouter dans `settings.py` :

``` python
INSTALLED_APPS += ["templates_admin"]

# Chemins configurables pour l'app templates_admin
TEMPLATES_ADMIN_DOC_TEMPLATES_DIR = BASE_DIR / "templates_admin" / "doc_templates"
TEMPLATES_ADMIN_GENERATED_DOCS_DIR = BASE_DIR / "templates_admin" / "generated_docs"

# Crée les dossiers si absents
os.makedirs(TEMPLATES_ADMIN_DOC_TEMPLATES_DIR, exist_ok=True)
os.makedirs(TEMPLATES_ADMIN_GENERATED_DOCS_DIR, exist_ok=True)
```

3.  Ajouter les URLs :

``` python
    path("api/documents/", include("templates_admin.urls"))
```

4.  Installer les dépendances :

``` bash
    pip install docxtpl jmespath requests
 ```  

------------------------------------------------------------------------

## 🧪 Tests

Exécuter :

    python manage.py test templates_admin

Des tests manuels sont fournis dans le guide utilisateur.

------------------------------------------------------------------------

## 📘 Documentation complémentaire

Un guide utilisateur complet est disponible dans le fichier
`USER_GUIDE.md`.
