from django.urls import path

from diary import views

app_name = 'diary'

urlpatterns = [
    path('', views.DiaryListView.as_view(), name='diary_list'),
    path('create/', views.DiaryCreateView.as_view(), name='diary_create'),
    path('<int:pk>/', views.DiaryDetailView.as_view(), name='diary_detail'),
    path('<int:pk>/edit/', views.DiaryUpdateView.as_view(), name='diary_edit'),
    path('<int:pk>/delete/', views.DiaryDeleteView.as_view(), name='diary_delete'),
]
