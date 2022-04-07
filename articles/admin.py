from django.contrib import admin
from .models import Article, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'slug', 'last_update', 'created_at']
    search_fields = ['title', 'content']
    # list_display_links = ['title']
    fields = ['author', 'title', 'image', 'slug', 'content', 'tags', 'time', 'last_update', 'created_at']
    readonly_fields = ['last_update', 'created_at']
    list_filter = ['created_at']
    prepopulated_fields = ({'slug': ('title', )})
    filter_horizontal = ('tags', )
    # list_editable = ['title']
    save_on_top = True


admin.site.register(Article, ArticleAdmin)

