from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from modules.forum.forms.comments import CommentCreateForm
from modules.forum.models import Article
from modules.forum.forms import ArticleCreateForm, ArticleUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from modules.system.services import AuthorRequiredMixin
from taggit.models import Tag
import random
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class ArticleListView(ListView):
    model = Article
    template_name = 'modules/forum/articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 3
    queryset = Article.custom_manager.all_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Trang chủ'
        return context

class ArticleByTagListView(ListView):
    model = Article
    template_name = 'modules/forum/articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 3
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        queryset = Article.objects.all().filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Bài viết có tag: {self.tag.name}'
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'modules/forum/articles/article_detail.html'
    context_object_name = 'article'
    queryset = Article.custom_manager.detail()
    
    def get_similar_articles(self, article):
        article_tags_ids = article.tags.values_list('id', flat=True)
        similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(related_tags=Count('tags')).order_by('-related_tags')
        similar_articles_list = [similar for similar in similar_articles.all()]
        random.shuffle(similar_articles_list)
        return similar_articles_list[0:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['similar_articles'] = self.get_similar_articles(self.object)
        context['form'] = CommentCreateForm
        return context

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'modules/forum/articles/article_create.html'
    form_class = ArticleCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Thêm một bài đăng vào forum'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Article
    template_name = 'modules/forum/articles/article_update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm
    login_url = 'home'
    success_message = 'Bạn đã cập nhật thành công bài đăng'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Cập nhật bài đăng: {self.object.title}'
        return context

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('article-list')
    context_object_name = 'article'
    template_name = 'modules/forum/articles/article_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Xóa bài đăng: {self.object.title}'
        return context

class ArticleSearchView(ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 3
    allow_empty = True
    template_name = 'modules/forum/articles/article_list.html'

    def get_queryset(self):
        query = self.request.GET.get('search_keyword')
        search_vector = SearchVector('full_description', weight='B') + SearchVector('title', weight='A')
        search_query = SearchQuery(query)
        return (
            self.model.objects.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.3)
                .order_by('-rank')
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Kết quả tìm kiếm'
        context['search_keyword'] = f"search_keyword={self.request.GET.get('value')}&"
        return context