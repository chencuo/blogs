from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from articles.models import Article
from diary.models import LifeDiary
from django.core.paginator import Paginator

def search_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    
    # 搜索文章标题
    articles = Article.objects.filter(
        title__icontains=query,
        is_published=True
    ).order_by('-pub_date')[:5]  # 限制5个结果
    
    for article in articles:
        results.append({
            'type': '文章',
            'title': article.title,
            'url': article.get_absolute_url(),
            'date': article.pub_date.strftime("%Y-%m-%d")
        })
    
    # 搜索生活日记标题
    diaries = LifeDiary.objects.filter(
        title__icontains=query
    ).order_by('-created_at')[:5]  # 限制5个结果
    
    # 获取所有日记并按创建时间倒序排列
    all_diaries = LifeDiary.objects.all().order_by('-created_at')
    paginator = Paginator(all_diaries, 1)  # 每页1篇日记
    
    for diary in diaries:
        # 计算该日记在分页中的位置
        diary_index = None
        for i, d in enumerate(all_diaries):
            if d.id == diary.id:
                diary_index = i + 1  # 索引从1开始
                break
        
        # 计算页码 (每个日记都是单独的一页)
        page_number = diary_index if diary_index else 1
        
        # 构建URL
        diary_url = f"{reverse('diary:diary_list')}?page={page_number}"
        
        results.append({
            'type': '生活日记',
            'title': diary.title,
            'url': diary_url,
            'date': diary.created_at.strftime("%Y-%m-%d")
        })
    
    return JsonResponse({'results': results})