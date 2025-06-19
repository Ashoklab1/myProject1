# posts/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Tag, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return ""


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')

    inlines = [PostImageInline]


# Register other models only once
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostImage)
