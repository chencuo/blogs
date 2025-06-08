from django.db import models
from django.utils import timezone
import uuid
import hashlib

class Comment(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已退回'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField('用户名', max_length=50)
    email = models.EmailField('邮箱')
    content = models.TextField('留言内容')
    device_info = models.CharField('设备信息', max_length=100, default="Android/Chrome")

    @property
    def device_type(self):
        """返回设备类型部分"""
        return self.device_info.split('/')[0] if '/' in self.device_info else self.device_info
        
    @property
    def browser_type(self):
        """返回浏览器类型部分"""
        parts = self.device_info.split('/')
        return parts[1] if len(parts) > 1 else ""
    
        # 给后台显示设备类型用
    def device_type_display(self):
        return self.device_type
    device_type_display.short_description = '设备'
    
    region = models.CharField('地区', max_length=50, default="湖北")
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    pinned = models.BooleanField('置顶', default=False)
    reply = models.TextField('管理员回复', blank=True, null=True)
    
    class Meta:
        ordering = ['-pinned', '-created_at']
        verbose_name = '留言'
        verbose_name_plural = '留言'
        
    def __str__(self):
        return f"{self.username}: {self.content[:20]}..."
    
    @property
    def avatar_color(self):
        """根据用户名生成十六进制颜色代码"""
        hash = hashlib.md5(self.username.encode()).hexdigest()
        return f"#{hash[:6]}"
    
    @property
    def avatar_text(self):
        if self.username:
            return self.username[0].upper()
        return "?"
    
    @property
    def is_admin(self):
        return self.username.lower() == "admin"