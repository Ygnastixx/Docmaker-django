from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/documents/', include("templates_admin.urls")),
    path("mock/", include("mock_api.urls")),  # mock api pour test
]
