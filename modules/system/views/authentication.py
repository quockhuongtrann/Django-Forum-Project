from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from modules.system.forms import RegisterForm, LoginForm, ChangePasswordForm
from modules.system.forms import ForgotPasswordForm, SetNewPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from modules.system.services import send_account_activation_email

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from django.contrib.auth.models import User

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from modules.system.services import account_activation_token
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'modules/system/authentication/register.html'
    success_message = 'Bạn đã đăng ký thành công. Xác nhận email của bạn, có thể nằm trong mail SPAM.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đăng ký'
        return context

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_account_activation_email(user.email)
        return super().form_valid(form)

class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginForm
    template_name = 'modules/system/authentication/login.html'
    next_page = 'home'
    success_message = 'Bạn đã đăng nhập thành công. Chào mừng bạn đến với forum.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đăng nhập'
        return context

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'modules/system/authentication/change_password.html'
    success_message = 'Mật khẩu của bạn đã thay đổi thành công.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Đổi mật khẩu'
        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug': self.request.user.profile.slug})

class ForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = ForgotPasswordForm
    template_name = 'modules/system/authentication/forgot_password.html'
    success_url = reverse_lazy('home')
    success_message = 'Truy cập email của bạn để xem hướng dẫn khôi phục mật khẩu'
    subject_template_name = 'modules/system/authentication/email/subject_forgot_password_mail.html'
    email_template_name = 'modules/system/authentication/email/forgot_password_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Quên mật khẩu'
        return context

class ConfirmResetPasswordView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = SetNewPasswordForm
    template_name = 'modules/system/authentication/set_new_password.html'
    success_url = reverse_lazy('home')
    success_message = 'Bạn đã khôi phục mật khẩu thành công, bây giờ bạn có thể đăng nhập bằng mật khẩu mới.'

    def get_context_data(self, **kwargs):                                                               
        context = super().get_context_data(**kwargs)                                                    
        context['title'] = 'Khôi phục mật khẩu'                                                    
        return context

class ActivateAccountView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Tài khoản của bạn đã được xác minh thành công.')
            return redirect('home')
        else:
            messages.warning(request, 'Link để kích hoạt tài khoản của bạn đã hết hạn hoặc không hoạt động.')
            return redirect('home')