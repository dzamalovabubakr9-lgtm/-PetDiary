from django.urls import path

from care import views

app_name = 'care'

urlpatterns = [
    path('', views.ProceduresListView.as_view(), name='procedures'),
    path('<int:pk>/', views.ProcedureDetailView.as_view(), name='procedure_detail'),
    path('create/', views.ProcedureCreateView.as_view(), name='procedure_create'),
    path('<int:pk>/edit/', views.ProcedureUpdateView.as_view(), name='procedure_edit'),
    path('<int:pk>/delete/', views.ProcedureDeleteView.as_view(), name='procedure_delete'),
]
