from django.contrib import admin
from .models import Video, Comment, Like, Subscription
from django.utils.html import mark_safe

def thumbnail_preview(self, obj):
    if obj.thumbnail:
        return mark_safe(f'<img src="{obj.thumbnail.url}" width="90" style="border-radius: 8px;" />')
    return "Сүрөт жок"
thumbnail_preview.short_description = "Миниатюра"

# list_display'ге кошуу:
list_display = ('title', 'thumbnail_preview', 'uploaded_by', 'views', 'created_at')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'views', 'created_at', 'updated_at')
    list_display_links = ('title',)                    # Аталышына басуу менен деталга өтүү
    search_fields = ('title', 'description', 'uploaded_by__username')
    list_filter = ('created_at', 'uploaded_by')
    readonly_fields = ('created_at', 'updated_at', 'views')
    ordering = ('-created_at',)
    list_per_page = 20

    fieldsets = (
        ('Негизги маалымат', {
            'fields': ('title', 'description', 'video_file', 'thumbnail')
        }),
        ('Автор жана статистика', {
            'fields': ('uploaded_by', 'views')
        }),
        ('Убакыт', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)                   # Убакыт талааларын жыйыштырып коюу
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'text_short', 'created_at')
    list_display_links = ('video',)
    search_fields = ('text', 'user__username', 'video__title')
    list_filter = ('created_at', 'user')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 30

    def text_short(self, obj):
        """Комментарийдин алгачкы 50 символун гана көрсөтүү"""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_short.short_description = "Комментарий"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'created_at')
    search_fields = ('user__username', 'video__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 30


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'channel', 'created_at')
    search_fields = ('subscriber__username', 'channel__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 30