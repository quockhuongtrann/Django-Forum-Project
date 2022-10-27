from django.contrib import admin
from modules.forum.models import Article, Category, Profile, Comment, Rating
from mptt.admin import DraggableMPTTAdmin

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author')
    list_display_links = ('title', 'slug')

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')

    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('title', 'slug', 'parent')}),
        ('Mô tả', {'fields': ('description',)}),
    )

@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'created_at', 'is_published')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('created_at', 'is_fixed', 'author')

    list_editable = ('is_published',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'article')

admin.site.register(Profile)
admin.site.register(Rating)

