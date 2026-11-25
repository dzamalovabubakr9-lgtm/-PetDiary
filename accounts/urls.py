from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginViewCustom.as_view(), name='login'),
    path('logout/', views.LogoutViewCustom.as_view(), name='logout'),
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.PasswordResetViewCustom.as_view(), name='reset_password'),
    path('reset-password/done/', views.PasswordResetDoneViewCustom.as_view(), name='reset_password_done'),
    path('reset-password/confirm/<uidb64>/<token>/', views.PasswordResetConfirmViewCustom.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.PasswordResetCompleteViewCustom.as_view(), name='reset_password_complete'),
]
