from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class LifeDiary(models.Model):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    author = models.CharField('作者', max_length=50, default="陈错错")
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    
    # 添加点赞关联和属性
    likes = models.ManyToManyField(
        User,
        through='DiaryLike',
        related_name='liked_diaries',
        blank=True
    )
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        """获取日记的绝对URL"""
        return reverse('diary:diary_detail', kwargs={'pk': self.pk})
    
    def get_current_page_url(self, page_number):
        """获取日记所在的分页URL"""
        return f"{reverse('diary:diary_list')}?page={page_number}"
    
    def get_like_count(self):
        """获取点赞数量"""
        return self.diary_likes.count()
    
    def user_has_liked(self, user):
        """检查用户是否已点赞"""
        if not user.is_authenticated:
            return False
        return self.diary_likes.filter(user=user).exists()
    
    class Meta:
        verbose_name = '生活日记'
        verbose_name_plural = '生活日记'
        ordering = ['-created_at']  # 默认按创建时间倒序

class DiaryImage(models.Model):
    diary = models.ForeignKey(
        LifeDiary, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        '图片', 
        upload_to='diary_images/%Y/%m/%d/'
    )
    caption = models.CharField('图片说明', max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.diary.title} 的图片"
    
    def get_absolute_url(self):
        """获取图片的绝对URL"""
        if self.image:
            return self.image.url
        return ""
    
    class Meta:
        verbose_name = '日记图片'
        verbose_name_plural = '日记图片'

class DiaryComment(models.Model):
    diary = models.ForeignKey(
        LifeDiary, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='diary_comments'
    )
    nickname = models.CharField('昵称', max_length=50)
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    def __str__(self):
        return f"{self.nickname}的评论: {self.content[:20]}"
    
    def get_author(self):
        """获取评论作者显示名称"""
        if self.user:
            return self.user.username
        return self.nickname
    
    class Meta:
        verbose_name = '日记评论'
        verbose_name_plural = '日记评论'
        ordering = ['-created_at']  # 按时间倒序显示

class DiaryLike(models.Model):
    """日记点赞模型"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='diary_likes'
    )
    diary = models.ForeignKey(
        LifeDiary, 
        on_delete=models.CASCADE,
        related_name='diary_likes'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'diary')  # 确保用户不能重复点赞同一篇日记
        verbose_name = '日记点赞'
        verbose_name_plural = '日记点赞'
    
    def __str__(self):
        return f"{self.user.username} 点赞了 {self.diary.title}"