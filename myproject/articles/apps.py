from django.apps import AppConfig

class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
    
    # 添加verbose_name以在Admin中显示友好的名称
    verbose_name = '文章管理'