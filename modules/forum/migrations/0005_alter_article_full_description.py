# Generated by Django 4.1 on 2022-10-20 08:30

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_article_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='full_description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Mô tả đầy đủ'),
        ),
    ]