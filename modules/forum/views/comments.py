from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView
from modules.forum.forms import CommentCreateForm
from modules.forum.models import Comment, Article
from modules.system.services.mixins import AuthorRequiredMixin
from django.urls import reverse_lazy

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    to_model = Article

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)

    def form_valid(self, form):
        if self.is_ajax():
            comment = form.save(commit=False)
            comment.article_id = self.to_model.objects.get(pk=self.kwargs['pk']).pk
            comment.author = self.request.user
            try:
                comment.parent_id = self.model.objects.get(pk=form.cleaned_data['parent']).pk
            except ObjectDoesNotExist:
                comment.parent_id = None
            comment.save()
            return JsonResponse({
                'comment_is_child': comment.is_child_node(),
                'comment_id': comment.id,
                'comment_author': comment.author.username,
                'comment_parent_id': comment.parent_id,
                'comment_created_at': comment.created_at.strftime('%Y-%b-%d %H:%M:%S'),
                'comment_avatar': comment.author.profile.get_avatar,
                'comment_content': comment.content,
                'comment_get_absolute_url': comment.author.profile.get_absolute_url(),
            }, status=200)

    def handle_no_permission(self):
        return JsonResponse({'error': 'Yêu cầu đăng nhập'}, status=400)

class CommentDeleteView(DeleteView):
    model = Comment
    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def delete(self, request, *args, **kwargs):
        if self.is_ajax():
            self.get_object().delete()
            payload = {'delete': 'ok'}
            return JsonResponse(payload)

    def get_success_url(self):
        return reverse_lazy('article-detail', kwargs={'slug': self.object.article.slug})