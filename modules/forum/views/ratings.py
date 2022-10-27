from django.views import View
from modules.forum.models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from modules.system.services import get_client_ip
from django.contrib.auth.mixins import LoginRequiredMixin

class RatingCreateView(LoginRequiredMixin, View):
    value = None
    change = ''
    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, pk):
        if self.is_ajax():
            current_user = request.user
            article = Article.objects.get(pk=pk)
            if current_user.is_authenticated:
                try:
                    rating = article.article_rating.get(author=current_user)
                    if rating.value is not self.value:
                        rating.value = self.value
                        rating.save(update_fields=['value'])
                        if rating.value == 1:
                            self.change = 'You Liked'
                        else:
                            self.change = 'You Disliked'
                    else:
                        rating.delete()
                        self.change = 'No rating'
                except ObjectDoesNotExist:
                    article.article_rating.create(author=current_user, value=self.value)
                    if self.value == 1:
                            self.change = 'You Liked'
                    elif self.value == -1:
                        self.change = 'You Disliked'
                    else:
                        self.change = 'No rating'
                return JsonResponse({
                    'get_rating_sum': article.get_rating_sum(),
                    'get_like_sum': article.get_like_sum(),
                    'get_dislike_sum': article.get_dislike_sum(), 
                    'status': self.change
                }, status=200)
            # else:
            #     try:
            #         rating = article.article_rating.get(ip_address=ip_address)
            #         if rating.value is not self.value:
            #             rating.value = self.value
            #             rating.save(update_fields=['value'])
            #         else:
            #             rating.delete()
            #     except ObjectDoesNotExist:
            #         article.article_rating.create(ip_address=ip_address, value=self.value)
            #     return JsonResponse({
            #         'get_rating_sum': article.get_rating_sum(),
            #         'get_like_sum': article.get_like_sum(),
            #         'get_dislike_sum': article.get_dislike_sum()
            #     }, status=200)