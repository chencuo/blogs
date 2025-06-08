from django.contrib import admin
from .models import Article
from django.utils.text import slugify
import uuid  # 添加uuid库

class ArticleAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('title', 'author', 'pub_date', 'is_published', 'views', 'word_count', 'slug')
    
    # 可过滤的字段
    list_filter = ('is_published', 'pub_date')
    
    # 可搜索的字段
    search_fields = ('title', 'content', 'summary', 'slug')  # 添加slug到搜索
    
    # 表单页的字段分组
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'image', 'is_published')
        }),
        ('内容部分', {
            'fields': ('summary', 'content')
        }),
        ('元数据', {
            'fields': ('pub_date',)  # 只保留 pub_date 字段
        }),
    )
    
    # 自动填充slug字段 - 保留但增加保护
    prepopulated_fields = {'slug': ('title',)}
    
    # 设置日期时间字段的快捷过滤
    date_hierarchy = 'pub_date'
    
    # 只读字段列表
    readonly_fields = ('word_count', 'views')  # 添加只读字段
    
    # 添加保护性逻辑 - 确保始终有有效的slug
    def save_model(self, request, obj, form, change):
        """
        在保存前确保文章有有效的slug
        """
        # 如果slug为空、空白或只包含空格
        if not obj.slug or not obj.slug.strip():
            # 尝试使用标题生成slug
            if obj.title and obj.title.strip():
                base_slug = slugify(obj.title)  # 生成基本slug
            else:
                # 如果标题也无效，则使用基于UUID的slug
                base_slug = f"article-{uuid.uuid4().hex[:8]}"
            
            # 如果生成的slug为空（例如标题全是特殊字符）
            if not base_slug:
                base_slug = f"article-{uuid.uuid4().hex[:8]}"
            
            # 确保slug唯一
            unique_slug = base_slug
            counter = 1
            while Article.objects.filter(slug=unique_slug).exclude(pk=obj.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            obj.slug = unique_slug  # 设置新的有效slug
        
        # 确保作者不为空
        if not obj.author or not obj.author.strip():
            obj.author = "admin"
        
        # 调用父类方法保存对象
        super().save_model(request, obj, form, change)

# 注册Article模型及自定义的Admin类
admin.site.register(Article, ArticleAdmin)