from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy 

from modules.forum.models import Article


class Rating(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES_TYPE = ((LIKE, gettext_lazy('Like')), (DISLIKE, gettext_lazy('Dislike')))

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Bài đăng', related_name='article_rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=gettext_lazy('Tác giả'), related_name='article_rating_author', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=gettext_lazy('Thời gian đánh giá'), auto_now_add=True, db_index=True)
    value = models.SmallIntegerField(verbose_name=gettext_lazy('Rating'), choices=VOTES_TYPE)
    ip_address = models.GenericIPAddressField(verbose_name=gettext_lazy('Địa chỉ IP'), blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = gettext_lazy('Rating')
        verbose_name_plural = gettext_lazy('Rating')
        db_table = 'app_ratings'

    def __str__(self):
        if self.author:
            return f'{self.author} đánh giá {self.get_value_display()} cho {self.article.title}'
        return f'Khách: {self.ip_address} đánh giá {self.get_value_display()} cho {self.article.title}'