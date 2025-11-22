# Guide Utilisateur --- Module Template Admin

Ce guide explique comment utiliser ce module dans un projet Django
existant.

------------------------------------------------------------------------

# 1. Configuration initiale

## 1.1 Installer le module

Copiez `templates_admin/` dans votre projet puis ajoutez :

``` python
INSTALLED_APPS += ["templates_admin"]
```

Configurez ensuite les dossiers :

``` python
# Chemins configurables pour l'app templates_admin
TEMPLATES_ADMIN_DOC_TEMPLATES_DIR = BASE_DIR / "templates_admin" / "doc_templates"
TEMPLATES_ADMIN_GENERATED_DOCS_DIR = BASE_DIR / "templates_admin" / "generated_docs"

# Crée les dossiers si absents
os.makedirs(TEMPLATES_ADMIN_DOC_TEMPLATES_DIR, exist_ok=True)
os.makedirs(TEMPLATES_ADMIN_GENERATED_DOCS_DIR, exist_ok=True)
```

Créez les dossiers (si nécessaire) :

    mkdir -p templates_admin/doc_templates
    mkdir -p templates_admin/generated_docs

------------------------------------------------------------------------

# 2. Configuration via l'admin Django

## 2.1 Datasources

Créez une datasource : 
- URL d'une API 
- jeton d'authentification éventuel (si l'API en a besoin) 
- description

## 2.2 Template DOCX

Dans l'admin → *Templates* : 
1. Créez un template 
2. Uploadez un fichier `.docx` 
3. Sélectionnez les datasources à utiliser

## 2.3 Champs du template

Chaque champ représente : 
- ce qui remplira le contexte passé à`docxtpl` 
- ce que verra l'utilisateur dans le formulaire

Paramètres : 
- `name`: identifiant utilisé dans le template DOCX (`{{ client.name }}`) 
- `field_type`: text, number, date, choice, table 
- `datasource`: API utilisée 
- `datasource_key`: chemin JMESPath dans la réponse JSON 
- `is_user_input`: si l'utilisateur doit le remplir à la main

------------------------------------------------------------------------

# 3. Workflow complet

## Étape 1 --- La page métier appelle l'API de pré-remplissage


Paramètre de l'API :
- `business_code` : nom de la logique métier enregistré dans l'admin
- D'autres paramètres nécessaires datasources

Exemple :

``` json
GET /api/documents/prefill/?business_code=profile&id=5
```

L'API : 
- appelle les datasources 
- applique les clés JMESPath 
- renvoie les champs pré-remplis

## Étape 2 --- L'utilisateur vérifie les données

Il peut modifier : 
- les champs *user_input* 
- rien d'autre (readonly conseillé pour les autres)

## Étape 3 --- Le frontend envoie le contexte final

``` json
POST /api/documents/render/
{
  "template": "invoice",
  "context": {
    "client_name": "John Doe",
    "items": [...]
  }
}
```

L'API : 
- construit un contexte complet 
- génère un fichier DOCX 
- renvoie une URL pour le télécharger

------------------------------------------------------------------------

# 4. Exemple de payload complet

## Pré-remplissage (GET /prefill)

Paramètres:

  - `?business_code=profiles`
  - `&username=alice`

Réponse :

``` json
{
  "template": "profiles",
  "fields": [
    { "name": "full_name", "value": "Alice Doe", "field_type": "text" },
    { "name": "roles", "value": ["admin", "editor"], "field_type": "choice" },
    { "name": "address", "value": { "city": "Paris" }, "field_type": "table" }
  ]
}
```

## Génération (POST /render)

``` json
{
  "template": "profiles",
  "context": {
    "full_name": "Alice Doe",
    "roles": ["admin", "editor"],
    "address": { "city": "Paris", "zip": "75000" }
  }
}
```

------------------------------------------------------------------------

# 5. Tests manuels

## 5.1 Tester le pré-remplissage

``` python
import requests


params = {
        "business_code": "profiles"
        "context": json.dumps({"id": 4}),    
    }
    
resp = requests.get(
    "http://localhost:8000/api/documents/prefill/", 
    params=params
)

print(resp.json())
```

## 5.2 Tester la génération

``` python
import requests

resp = requests.post(
    "http://localhost:8000/api/documents/render/",
    json={
        "template": "profiles",
        "context": {
            "full_name": "Alice Doe",
            "roles": ["admin"],
            "address": {"city": "Paris"}
        }
    }
)
open("output.docx", "wb").write(resp.content)
```

------------------------------------------------------------------------

# 6. Ce qui manque / à venir

- Formulaire dynamique prérempli grâce à l'API de préremplissage
- Validation avancée des champs
- Support Excel / PDF
- Interface graphique pour visualiser les templates
- Plugin CLI pour test local d'un template

------------------------------------------------------------------------

Si vous souhaitez étendre les fonctionnalités, le module est conçu pour
être modulaire et facilement modifiable.
