from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from modules.system.services import create_distinct_slug, get_meta_keywords
from modules.system.models import AbstractBaseMeta
from django.template.defaultfilters import striptags, truncatewords_html

class Category(MPTTModel, AbstractBaseMeta):
    title = models.CharField(max_length=255, verbose_name='Tên thể loại')
    slug = models.SlugField(max_length=255, verbose_name='URL thể loại', blank=True)
    description = models.TextField(verbose_name='Mô tả', max_length=300, blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Thể loại cha'
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Thể loại'
        verbose_name_plural = 'Thể loại'
        db_table = 'app_categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_distinct_slug(self, self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = striptags(truncatewords_html(self.description, 300))
        if not self.meta_keywords:
            self.meta_keywords = get_meta_keywords(self.description)
        super().save(*args, **kwargs)