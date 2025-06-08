# message/admin.py
from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    # 定义在后台列表中显示的字段
    list_display = ('username', 'email', 'device_type', 'region', 'status', 'created_at', 'pinned')
    
    # 添加状态筛选器
    list_filter = ('status', 'pinned', 'created_at')
    
    # 添加搜索字段
    search_fields = ('username', 'email', 'content')
    
    # 允许在列表页快速编辑状态和置顶
    list_editable = ('status', 'pinned')
    
    # 分页
    list_per_page = 20
    
    # 动作（批量审核）
    actions = ['approve_comments', 'reject_comments', 'unpin_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(status='approved')
    approve_comments.short_description = "审核通过所选留言"
    
    def reject_comments(self, request, queryset):
        queryset.update(status='rejected')
    reject_comments.short_description = "拒绝所选留言"
    
    def unpin_comments(self, request, queryset):
        queryset.update(pinned=False)
    unpin_comments.short_description = "取消置顶所选留言"

# 注册模型到Admin
admin.site.register(Comment, CommentAdmin)