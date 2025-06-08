from django.contrib import admin
from .models import LifeDiary, DiaryImage

class DiaryImageInline(admin.TabularInline):
    model = DiaryImage
    extra = 1
    fields = ('image', 'caption')

@admin.register(LifeDiary)
class LifeDiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'comment_count')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    inlines = [DiaryImageInline]
    
    # 显示评论数
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = '评论数'

# 单独注册图片模型（可选）
@admin.register(DiaryImage)
class DiaryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'diary_title')
    
    def diary_title(self, obj):
        return obj.diary.title
    diary_title.short_description = '所属日记'