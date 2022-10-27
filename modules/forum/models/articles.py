from telnetlib import theNULL
from urllib import request
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.models import TreeForeignKey
from modules.system.services import ImageDirectory, create_distinct_slug, get_meta_keywords
from django.urls import reverse
from modules.forum.managers import ArticleManager
from modules.system.models import AbstractBaseMeta
from django.template.defaultfilters import striptags, truncatewords_html
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field

class Article(AbstractBaseMeta):
    title = models.CharField(verbose_name='Tiêu đề', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Thể loại')
    short_description = models.TextField(max_length=300, verbose_name='Mô tả ngắn gọn')
    full_description = CKEditor5Field(verbose_name='Mô tả đầy đủ', config_name='extends')
    author = models.ForeignKey(User, verbose_name='Tác giả', on_delete=models.PROTECT, related_name='article_author')
    created_at = models.DateTimeField(verbose_name='Thời gian tạo', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name='Thời gian cập nhật', auto_now=True, db_index=True)
    reason = models.CharField(verbose_name='Lý do cập nhật', blank=True, max_length=100)
    is_fixed = models.BooleanField(verbose_name='Đã sửa ?', default=False, db_index=True)
    is_published = models.BooleanField(verbose_name='Đăng ?', default=True)
    thumbnail = models.ImageField(
        verbose_name='Thumbnail',
        blank=True,
        upload_to=ImageDirectory('images/thumbnails/'),
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))
        ]
    )
    objects = models.Manager()
    custom_manager = ArticleManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-is_fixed', '-created_at')
        verbose_name = 'Bài đăng'
        verbose_name_plural = 'Bài đăng'
        db_table = 'app_articles'

    def __str__(self):
        return self.title

    @property
    def get_thumbnail(self):
        if not self.thumbnail:
            return '/media/images/placeholder.png'
        return self.thumbnail.url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_distinct_slug(self, self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = striptags(truncatewords_html(self.short_description, 300))
        if not self.meta_keywords:
            self.meta_keywords = get_meta_keywords(self.full_description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})

    def get_rating_sum(self):
        return sum([rating.value for rating in self.article_rating.all()])
    
    def get_like_sum(self):
        like = 0
        for rating in self.article_rating.all():
            if rating.value == 1:
                like += 1
        return like

    def get_dislike_sum(self):
        dislike = 0
        for rating in self.article_rating.all():
            if rating.value == -1:
                dislike += 1
        return dislike

    def get_article_author_rating(self, author):
        for rating in self.article_rating.all():
            if rating.author == author:
                return rating.value
        return None

    def get_article_author(self):
        result = []
        for rating in self.article_rating.all():
            result.append(rating.author)
        return result


