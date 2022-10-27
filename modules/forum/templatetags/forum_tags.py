from django import template

from modules.forum.models import Article

register = template.Library()


@register.simple_tag
def get_article_author_rating(article, author):
    for rating in article.article_rating.all():
        if rating.author == author:
            return rating.value
    return None