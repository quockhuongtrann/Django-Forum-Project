from django.urls import path, include
from modules.forum.views import ArticleListView, ArticleDetailView, ArticleCreateView
from modules.forum.views import ArticleUpdateView, ArticleDeleteView, ArticleByTagListView
from modules.forum.views import ProfileDetailView, ProfileUpdateView, ArticleSearchView, ProfileFollowingCreateView
from modules.forum.views import CommentCreateView, CommentDeleteView
from modules.forum.views import RatingCreateView
from modules.forum.models import Rating

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('user/', include([
        path('update/', ProfileUpdateView.as_view(), name='profile-update'),
        path('<str:slug>/', ProfileDetailView.as_view(), name='profile'),
        path('<str:slug>/follow/', ProfileFollowingCreateView.as_view(), name='follow-to-user'),
    ])),
    path('articles/', include([
        path('', ArticleListView.as_view(), name='article-list'),
        path('create/', ArticleCreateView.as_view(), name='article-create-view'),
        path('tags/<str:tag>/', ArticleByTagListView.as_view(), name='article-list-by-tags'), 
        path('<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment-create-view'),
        path('<int:pk>/comments/delete/', CommentDeleteView.as_view(), name='comment-delete-view'),
        path('<str:slug>/', ArticleDetailView.as_view(), name='article-detail'),
        path('<str:slug>/update/', ArticleUpdateView.as_view(), name='article-update-view'),
        path('<str:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete-view'),
        path('<int:pk>/like/', RatingCreateView.as_view(value=Rating.LIKE), name='article-rating-like'),
        path('<int:pk>/dislike/', RatingCreateView.as_view(value=Rating.DISLIKE), name='article-rating-dislike'),
    ])),
    path('search/', ArticleSearchView.as_view(), name='search'),
]