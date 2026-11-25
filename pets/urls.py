from django.urls import path

from pets import views

app_name = 'pets'

urlpatterns = [
    path('', views.PetsListView.as_view(), name='pets_list'),
    path('create/', views.PetCreateView.as_view(), name='pet_create'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='pets_detail'),
    path('<int:pk>/edit/', views.PetUpdateView.as_view(), name='pet_edit'),
    path('<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet_delete'),
]
