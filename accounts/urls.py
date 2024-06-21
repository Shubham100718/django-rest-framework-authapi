from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterView, VerifyEmailView, LoginView, LogoutView, ProfileView, FilterView


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('verify-email/<uid>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('filter/', FilterView.as_view(), name='user-filter'),
]

