from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls')),
    path('pets/', include('pets.urls', namespace='pets')),
    path('diary/', include('diary.urls', namespace='diary')),
    path('care/', include('care.urls', namespace='care')),
    path('advice/', include('advice.urls', namespace='advice')),
    path('api/', include('api.urls')),
    path('assistant/', include('assistant.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
