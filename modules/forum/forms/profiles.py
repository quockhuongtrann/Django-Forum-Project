from django import forms
from django.contrib.auth.models import User
from modules.forum.models import Profile
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from forum_project import settings

class ProfileUpdateForm(forms.ModelForm):

    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=settings.RECAPTCHA_PUBLIC_KEY,
                               private_key=settings.RECAPTCHA_PRIVATE_KEY, label='Captcha')
                               
    class Meta:
        model = Profile
        fields = ('slug', 'bio', 'avatar', 'birthday')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    # def check_unique_email(self):
    #     email = self.cleaned_data.get('email')
    #     username = self.cleaned_data.get('username')
    #     if email and User.objects.filter(email=email).exclude(username=username).exists():
    #         raise forms.ValidationError('Địa chỉ email phải là duy nhất')
    #     return email