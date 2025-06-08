from django.db import models
from django.urls import reverse

# 定义分类选项
CATEGORY_CHOICES = [
    ('tech', '技术博客'),
    ('gaming', '游戏社区'),
    ('friends', '亲朋好友'),
    ('other', '其他'),
]

class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=100)
    url = models.URLField('网站链接')
    logo = models.ImageField('网站Logo', upload_to='friend_links/logos/', blank=True, null=True)
    logo_url = models.URLField('Logo URL', blank=True, null=True)
    description = models.TextField('网站描述')
    
    # 添加分类字段并设置选项
    category = models.CharField(
        '分类', 
        max_length=20, 
        choices=CATEGORY_CHOICES,
        default='tech'
    )
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    views = models.PositiveIntegerField('浏览次数', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    is_active = models.BooleanField('是否显示', default=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_logo(self):
        """获取Logo URL，优先使用本地上传的图片"""
        if self.logo:
            return self.logo.url
        return self.logo_url
    
    def get_category_display(self):
        """获取分类的显示名称"""
        for choice in CATEGORY_CHOICES:
            if choice[0] == self.category:
                return choice[1]
        return '其他'
    
    def get_category_class(self):
        """获取分类对应的CSS类"""
        category_classes = {
            'tech': 'tech',
            'gaming': 'gaming',
            'friends': 'friends',
            'other': 'other',
        }
        return category_classes.get(self.category, 'other')
    
    def increment_views(self):
        """增加浏览次数"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def increment_likes(self):
        """增加点赞数"""
        self.likes += 1
        self.save(update_fields=['likes'])

from django.db import models

class PageView(models.Model):
    """记录友情链接页面的访问量"""
    views = models.PositiveIntegerField('访问量', default=0)
    last_updated = models.DateTimeField('最后更新时间', auto_now=True)

    class Meta:
        verbose_name = '页面访问统计'
        verbose_name_plural = '页面访问统计'
        
    def increment_views(self):
        """增加访问量"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def __str__(self):
        return f"访问量: {self.views}"