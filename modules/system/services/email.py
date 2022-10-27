from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from modules.system.services.utils import account_activation_token

def send_account_activation_email(email):
    user = User.objects.get(email=email)
    current_site = Site.objects.get_current().domain
    subject = 'Kích hoạt tài khoản trên TQK Forum'
    message = render_to_string('modules/system/authentication/email/activate_account_mail.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    return user.email_user(subject, message)