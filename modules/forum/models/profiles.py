from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from modules.system.services.utils import ImageDirectory, create_distinct_slug
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Người dùng', on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL người dùng', max_length=255, blank=True, unique=True)
    bio = models.TextField(max_length=500, verbose_name='Tiểu sử', blank=True)
    avatar = models.ImageField(
        verbose_name='Ảnh đại diện',
        blank=True,
        upload_to=ImageDirectory('images/avatars/'),
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))
        ]
    )
    birthday = models.DateField(verbose_name='Ngày sinh', blank=True, null=True)
    following = models.ManyToManyField('self', verbose_name='Đang theo dõi', related_name='followers', symmetrical=False, blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Hồ sơ'
        verbose_name_plural = 'Hồ sơ'
        db_table = 'app_profiles'

    @property
    def get_avatar(self):
        if not self.avatar:
            return f'https://ui-avatars.com/api/?size=128&background=random&name={self.user.username}'
        return self.avatar.url
    
    @property
    def get_age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)

    def get_absolute_url(self):    
        return reverse('profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_distinct_slug(self, self.user.username)
        if self.slug:
            self.slug = self.slug.lower()    
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()