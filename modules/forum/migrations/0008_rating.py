# Generated by Django 4.1 on 2022-10-25 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0007_alter_comment_options_alter_comment_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Thời gian đánh giá')),
                ('value', models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')], verbose_name='Rating')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Địa chỉ IP')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_rating', to='forum.article', verbose_name='Bài đăng')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_rating_author', to=settings.AUTH_USER_MODEL, verbose_name='Tác giả')),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Rating',
                'db_table': 'app_ratings',
                'ordering': ('-created_at',),
            },
        ),
    ]
