from django.urls import path
from modules.system.views import RegisterView, UserLoginView, ChangePasswordView, ConfirmResetPasswordView
from modules.system.views import ForgotPasswordView, ActivateAccountView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('set-new-password/<uidb64>/<token>/', ConfirmResetPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]