# Generated by Django 4.1 on 2022-10-19 14:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import modules.system.services.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_article_meta_description_article_meta_keywords_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL người dùng')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Tiểu sử')),
                ('avatar', models.ImageField(blank=True, upload_to=modules.system.services.utils.ImageDirectory('images/avatars/'), validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))], verbose_name='Ảnh đại diện')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Ngày sinh')),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='forum.profile', verbose_name='Đang theo dõi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
            options={
                'verbose_name': 'Hồ sơ',
                'verbose_name_plural': 'Hồ sơ',
                'db_table': 'app_profiles',
                'ordering': ('user',),
            },
        ),
    ]
