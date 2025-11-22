## Guide étape-par-étape — Générer un document (exemple complet)

> **But de l’exemple** : générer une fiche profil utilisateur (template `profiles`) à partir d’une API factice (`/mock/user`) grâce à l’app `templates_admin`.

### Prérequis

* Python 3.10+
* Projet Django avec `manage.py`
* Virtualenv recommandé
* Modules Python : `django`, `djangorestframework`, `requests`, `jmespath`, `docxtpl`
  Install :

```bash
pip install Django djangorestframework requests jmespath docxtpl
```

---

### Résumé de l’exemple

* template slug : `profiles`
* business code : `user_profile`
* datasource mock : `http://127.0.0.1:8000/mock/user?id=55`
* champs : `full_name`, `email`, `address.city`, `roles`
* fichier DOCX : `profiles.docx` (avec `{{ full_name }}`, etc.)

---

### 1) Copier l’app `templates_admin/`

Copie le dossier `templates_admin/` dans la racine du projet (même niveau que `manage.py`).

---

### 2) `settings.py`

Ajouter dans `INSTALLED_APPS` :

```py
INSTALLED_APPS += [
  "rest_framework",  # si pas encore dans la liste
  "templates_admin",
  "mock_api",  # facultatif si tu utilises l'API factice
]
```

Ajouter (modifiable pour chaque projet) :

```py
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_ADMIN_DOC_TEMPLATES_DIR = str(BASE_DIR / "templates_admin" / "doc_templates")
TEMPLATES_ADMIN_GENERATED_DOCS_DIR = str(BASE_DIR / "templates_admin" / "generated_docs")

import os
os.makedirs(TEMPLATES_ADMIN_DOC_TEMPLATES_DIR, exist_ok=True)
os.makedirs(TEMPLATES_ADMIN_GENERATED_DOCS_DIR, exist_ok=True)


MEDIA_ROOT = str(BASE_DIR / "media") # à ajouter si ...
MEDIA_URL = "/media/" # ... pas encore là
```

---

### 3) Migrations & superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### 4) (Optionnel) API factice `mock_api`

`mock_api/views.py` :

```py
from django.http import JsonResponse

def fake_user(request):
    user_id = request.GET.get("id", "55")
    return JsonResponse({
        "id": user_id,
        "full_name": "Alice Doe",
        "email": "alice@example.com",
        "address": { "city": "Paris", "zip": "75000" },
        "roles": ["admin", "editor"]
    })
```

`mock_api/urls.py` :

```py
from django.urls import path
from .views import fake_user
urlpatterns = [ path("user", fake_user) ]
```

Dans `project/urls.py` :

```py
path("mock/", include("mock_api.urls")),
```

---

### 5) Préparer le template DOCX

Crée `profiles.docx` (Word) contenant :

```
Nom : {{ full_name }}
Email : {{ email }}
Ville : {{ address.city }}
Rôles :
{% for r in roles %}- {{ r }}{% endfor %}
```

Place le fichier dans `templates_admin/doc_templates/` OU upload via admin si le FileField `upload_to` est configuré pour écrire dans ce dossier.

---

### 6) Créer la Datasource (admin)

* name: `MockUserAPI`
* api_endpoint: `http://127.0.0.1:8000/mock/user`

---

### 7) Créer TemplateDocument (admin)

* name: `Profiles`
* slug: `profiles`
* template_filename / file: `profiles.docx`

---

### 8) Créer TemplateField (admin) — exemples

1. `full_name` — datasource_key `full_name`, type `text`
2. `email` — datasource_key `email`, type `text`
3. `address_city` — datasource_key `address.city`, type `text`
4. `roles` — datasource_key `roles`, type `choice` or `table`, `is_multiple=True`

> `datasource_key` doit être une expression JMESPath valide (`address.city`, `roles`, etc.).

Vous trouvez plus de détails sur [la documentation de JMESPath](https://jmespath.org). 

---

### 9) Créer DocumentType (admin)

* code: `user_profile`
* template: `Profiles`
* is_active: True

---

### 10) Tester le pré-remplissage

Lancer le serveur :

```bash
python manage.py runserver
```

Test via Python `requests` :

```py
import requests
params = {"business_code":"user_profile", "id":"55"}
r = requests.get("http://127.0.0.1:8000/api/documents/prefill/", params=params)
print(r.json())
```

On attend : JSON contenant `fields` pré-remplis.

---

### 11) Générer le document (render)

Exemple POST (frontend enverra le contexte confirmé) :

```py
import requests
payload = {
  "business_code": "user_profile",
  "context": {
    "full_name": "Alice Doe",
    "email": "alice@example.com",
    "address": {"city": "Paris", "zip": "75000"},
    "roles": ["admin","editor"]
  }
}
r = requests.post("http://127.0.0.1:8000/api/documents/render/", json=payload)
print(r.status_code, r.json())
```

Si réponse contient `download_url` : récupérer le fichier :

```py
dl = requests.get("http://127.0.0.1:8000" + r.json()["download_url"])
open("profile_output.docx","wb").write(dl.content)
```

---

### 12) Dépannage rapide

* `null` dans champs : vérifier `datasource_key` (JMESPath).
* path doublé : vérifie `upload_to` et `TEMPLATES_ADMIN_DOC_TEMPLATES_DIR`, utiliser `template_upload_path()` de `models.py`.
* Les champs `table` ne s'affichent pas : cocher `is_multiple` dans la page d'admin. 

---

### 13) Script de test complet minimal

```py
import requests

base = "http://127.0.0.1:8000/api/documents"
r1 = requests.get(f"{base}/prefill/", params={"business_code":"user_profile", "id":"55"})
print("PREFILL:", r1.json())

payload = {"business_code":"user_profile", "context": { "full_name":"Alice Doe", "email":"alice@example.com", "address":{"city":"Paris","zip":"75000"},"roles":["admin"] } }
r2 = requests.post(f"{base}/render/", json=payload)
print("RENDER:", r2.json())
```

---

### 14) Notes pour production

* utiliser stockage externe (S3) pour templates et documents générés
* ajouter réessais & logs pour appels API externes
* sécuriser accès aux endpoints (auth/permissions)

