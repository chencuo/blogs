from django.contrib import admin
from .models import FriendLink

class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'url', 'category', 'description', 'is_active')
        }),
        ('图片设置', {
            'fields': ('logo', 'logo_url'),
            'classes': ('collapse',)
        }),
        ('统计数据', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
        ('日期信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """为分类字段提供选项排序"""
        if db_field.name == 'category':
            # 设置分类选项的顺序
            CATEGORY_CHOICES = [
                ('tech', '技术博客'),
                ('gaming', '游戏社区'),
                ('friends', '亲朋好友'),
                ('other', '其他'),
            ]
            kwargs['choices'] = CATEGORY_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)

admin.site.register(FriendLink, FriendLinkAdmin)