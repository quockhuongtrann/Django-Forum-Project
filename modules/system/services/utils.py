import time
from pathlib import Path
from uuid import uuid4
from django.template.defaultfilters import slugify
from django.utils.deconstruct import deconstructible
import collections
import io
import re
from django.utils.html import strip_tags
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from django.core.files.storage import FileSystemStorage
from forum_project import settings
from urllib.parse import urljoin

@deconstructible
class ImageDirectory(object):
    def __init__(self, save_path):
        self.path = save_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]

        if instance and hasattr(instance, 'slug'):
            filename = f'img-{instance.slug}.{ext}'
        else:
            filename = f'img-{uuid4().hex}.{ext}'
        path = Path(self.path, time.strftime('%Y/%m/%d'), filename)
        return path

def create_distinct_slug(instance, slug):
    model = instance.__class__
    distinct_slug = slugify(slug)
    while model.objects.filter(slug=distinct_slug).exists():
        distinct_slug = f'{distinct_slug}-{uuid4().hex[:8]}'
    return distinct_slug


def get_meta_keywords(description):
    count_min = 7
    count_length = 7
    collection = collections.Counter()
    content = io.StringIO(description)
    keywords = []
    for line in content.readlines():
        collection.update(re.findall(r"[\w']+", strip_tags(line).lower()))
    
    for word, count in collection.most_common():
        if len(word) > (count_length - 1) and count > (count_min - 1):
            keywords.append(word)
    return ', '.join(map(str, keywords))

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.is_active) + six.text_type(user.pk) + six.text_type(timestamp)

account_activation_token = TokenGenerator()

class CkeditorCustomStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, 'uploads/images/')
    base_url = urljoin(settings.MEDIA_URL, 'uploads/images/')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip