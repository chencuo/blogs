from django.shortcuts import render
from articles.models import Article
from message.models import Comment  # 确保从message应用导入
import random
import json
from django.utils.safestring import mark_safe
from django.conf import settings

def home(request):
    # 1. 获取已通过的评论（确保按您的模型结构获取）
    comments = Comment.objects.filter(status='approved').order_by('-created_at')[:15]
    
    # 准备数据给瀑布流显示（只需要内容和用户名）
    comments_data = [
        {
            "author": comment.username if comment.username else "匿名",
            "content": comment.content
        } 
        for comment in comments
    ]
    
    # 2. 获取随机文章（确保您的文章模型正确）
    if Article.objects.exists():
        all_articles = Article.objects.filter(is_published=True)  # 确保使用正确的过滤字段
        random_articles = random.sample(list(all_articles), min(5, all_articles.count()))
    else:
        random_articles = [
            {"title": "示例文章1", "summary": "这是一个示例文章摘要，用于演示效果"},
            {"title": "示例文章2", "summary": "这是第二个示例文章摘要，用于演示效果"},
            {"title": "示例文章3", "summary": "这是第三个示例文章摘要，用于演示效果"}
        ]
    
    # 3. 传递给模板的上下文
    context = {
        'comments_data': mark_safe(json.dumps(comments_data)),  # 安全传递JSON
        'articles': random_articles,
        'profile_tags': [
            "动漫萌妹爱好者",
            "分享与热心帮助",
            "云计算的小大佬",
            "贪玩而好吃懒做",
            "积极向上乐天派",
            "脚踏实地行动派",
            "团队小组发动机",
            "壮汉人狠话不多"
        ],
        'comments_json_path': settings.STATIC_URL + 'data/comments.json'  # JSON文件路径
    }
    
    return render(request, 'home/home.html', context)