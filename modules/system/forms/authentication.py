from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from forum_project import settings

class RegisterForm(UserCreationForm):

    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": 'Tên đăng nhập'})
        self.fields['email'].widget.attrs.update({"placeholder": 'Email'})
        self.fields['first_name'].widget.attrs.update({"placeholder": 'Tên'})
        self.fields['last_name'].widget.attrs.update({"placeholder": 'Họ'})
        self.fields['password1'].widget.attrs.update({"placeholder": 'Mật khẩu'})
        self.fields['password2'].widget.attrs.update({"placeholder": 'Nhập lại mật khẩu'})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
    
    def check_unique_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email phải là duy nhất')
        return email

class LoginForm(AuthenticationForm):
    
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Tên đăng nhập'
        self.fields['password'].widget.attrs['placeholder'] = 'Mật khẩu'
        self.fields['username'].label = 'Tên đăng nhập'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class ChangePasswordForm(SetPasswordForm):

    # recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
    #                            private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class ForgotPasswordForm(PasswordResetForm):

    # recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
    #                            private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class SetNewPasswordForm(SetPasswordForm):

    # recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
    #                            private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')
                               
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })