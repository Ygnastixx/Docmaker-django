from django.http import JsonResponse


def fake_user(request):
    user_id = request.GET.get("id", "1")
    return JsonResponse({
        "id": user_id,
        "username": "Test User",
        "email": "test@example.com",
        "address": {
            "city": "Arcadia",
            "street": "42 Magic Road"
        },
        "roles": ["admin", "editor"]
    })
