from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
import uuid
from django.db import models
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL标识', max_length=200, unique=True, blank=True)
    image = models.ImageField('封面图片', upload_to='article_covers/%Y/%m/', blank=True, null=True)
    summary = models.TextField('摘要', max_length=300)
    content = models.TextField('内容')
    author = models.CharField('作者', max_length=100, default='cuo')
    pub_date = models.DateTimeField('发布时间', default=timezone.now)  # 只有pub_date
    views = models.PositiveIntegerField('浏览量', default=0)
    is_published = models.BooleanField('已发布', default=True)


    def save(self, *args, **kwargs):
        # 确保创建时总是有有效的slug
        if not self.slug or self.slug == '':
            # 使用标题生成基本slug
            if self.title:
                base_slug = slugify(self.title) or f"article-{uuid.uuid4().hex[:6]}"
            else:
                base_slug = f"article-{uuid.uuid4().hex[:6]}"
            
            # 确保slug唯一
            counter = 1
            unique_slug = base_slug
            while Article.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = unique_slug
        
        super().save(*args, **kwargs)
    
    # 计算字数
    @property
    def word_count(self):
        return len(self.content)
    
    # 计算阅读时间（300字/分钟）
    @property
    def reading_time(self):
        minutes = max(1, round(self.word_count / 300))
        return f"{minutes}分钟"
    
    # 获取文章绝对URL
    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})
    
    # 增加浏览量
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章列表'
        ordering = ['-pub_date']