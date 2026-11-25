from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('pets', views.PetViewSet, basename='pet')
router.register('diary', views.DiaryEntryViewSet, basename='diary-entry')
router.register('vet-visits', views.VetVisitViewSet, basename='vet-visit')
router.register('care', views.ProcedureViewSet, basename='procedure')
router.register('procedure-logs', views.ProcedureLogViewSet, basename='procedure-log')
router.register('advice', views.AdviceViewSet, basename='advice')
router.register('advice-categories', views.AdviceCategoryViewSet, basename='advice-category')

urlpatterns = [
    path('', views.APIRootView.as_view(), name='api_root'),
    path('auth/register/', views.RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('auth/password-reset/request/', views.PasswordResetRequestAPIView.as_view(), name='api-password-reset-request'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='api-password-reset-confirm'),
]
urlpatterns += router.urls
urlpatterns += [path('users/me/', views.UserViewSet.as_view({'get': 'retrieve'}), name='user-me')]
