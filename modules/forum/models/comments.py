from django.contrib.auth.models import User
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from modules.forum.models import Article


class Comment(MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Bài đăng', related_name='comments', related_query_name='comment')
    author = models.ForeignKey(User, verbose_name='Tác giả', on_delete=models.CASCADE, related_name='comments_author')
    content = models.TextField(verbose_name='Nội dung', max_length=1500)
    created_at = models.DateTimeField(verbose_name='Ngày đăng', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name='Ngày chỉnh sửa', auto_now=True, db_index=True)
    is_published = models.BooleanField(verbose_name='Đăng?', default=True)
    is_fixed = models.BooleanField(verbose_name='Đã sửa?', default=False)

    parent = TreeForeignKey('self', verbose_name='Bình luận cha', null=True, blank=True, db_index=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-created_at',)

    class Meta:
        ordering = ('-is_fixed', '-created_at')
        verbose_name = 'Bình luận'
        verbose_name_plural = 'Bình luận'
        db_table = 'app_comments'

    def __str__(self):
        return f'{self.author} bình luận về bài đăng: {self.article.title}'