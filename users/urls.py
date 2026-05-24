from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('update/', views.UpdateUserAPIView.as_view(), name='update-user'),
    path('login/', views.LoginUserAPIView.as_view(), name='login'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('delete/', views.DeleteUserAPIView.as_view(), name='delete-user'),
    path('logout/', views.LogoutUserAPIView.as_view(), name='logout'),
]
