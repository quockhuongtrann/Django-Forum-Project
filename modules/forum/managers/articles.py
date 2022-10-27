from django.db import models


class ArticleManager(models.Manager):

    def all_published(self):
        return self.get_queryset().filter(is_published=True)

    def detail(self):
        return self.get_queryset().filter(is_published=True)\
            .select_related('category', 'author', 'author__profile')