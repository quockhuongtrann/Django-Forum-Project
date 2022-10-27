from django.db import models

class AbstractBaseMeta(models.Model):
    meta_title = models.CharField(verbose_name='Meta tiêu đề', max_length=255, blank=True)
    meta_description = models.CharField(verbose_name='Meta mô tả', blank=True, max_length=300)
    meta_keywords = models.CharField(verbose_name='Meta từ khóa', max_length=255, blank=True)

    class Meta:
        abstract = True