from django.core.management.base import BaseCommand
from articles.models import Article
from django.utils.text import slugify
import uuid

class Command(BaseCommand):
    help = '修复所有缺失或不正确的文章slug'
    
    def handle(self, *args, **options):
        # 查找所有需要修复的文章
        broken_articles = Article.objects.filter(slug__in=['', None]) | \
                          Article.objects.filter(slug__regex=r'[^a-zA-Z0-9_-]')  # 含非法字符
        
        self.stdout.write(f"发现 {broken_articles.count()} 个需要修复的文章")
        
        for article in broken_articles:
            old_slug = article.slug
            
            # 生成新的slug
            if article.title:
                base_slug = slugify(article.title) or f"article-{uuid.uuid4().hex[:6]}"
            else:
                base_slug = f"article-{uuid.uuid4().hex[:6]}"
            
            # 确保slug唯一
            counter = 1
            unique_slug = base_slug
            while Article.objects.filter(slug=unique_slug).exclude(pk=article.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            article.slug = unique_slug
            article.save()
            
            self.stdout.write(f"文章 #{article.id} 已修复: {old_slug or '空'} -> {unique_slug}")
        
        self.stdout.write(self.style.SUCCESS("所有文章slug已成功修复"))