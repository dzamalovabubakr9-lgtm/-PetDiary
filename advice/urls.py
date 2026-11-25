from django.urls import path

from advice import views

app_name = 'advice'

urlpatterns = [
    path('', views.AdviceListView.as_view(), name='advice_list'),
    path('<int:pk>/', views.AdviceDetailView.as_view(), name='advice_detail'),
]
