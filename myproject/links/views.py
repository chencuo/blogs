from django.views.generic import ListView
from django.db.models import Max, Sum
from django.utils import timezone
from .models import FriendLink, PageView

class FriendLinkListView(ListView):
    model = FriendLink
    template_name = 'links/friendlink_list.html'
    context_object_name = 'friendlinks'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 获取最后更新时间（只显示一个时间）
        last_updated = FriendLink.objects.filter(is_active=True).aggregate(
            latest=Max('updated_at')
        )['latest'] or timezone.now()
        context['last_updated'] = last_updated
        
        # 获取页面访问统计
        page_view = PageView.objects.first()
        if not page_view:
            page_view = PageView.objects.create()
        context['page_views'] = page_view.views
        
        # 获取总点赞数
        total_likes = FriendLink.objects.aggregate(total=Sum('likes'))['total'] or 0
        context['total_likes'] = total_likes
        
        return context
    
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import FriendLink, PageView

@require_POST
def like_link(request, pk):
    try:
        link = FriendLink.objects.get(pk=pk)
        if not request.session.get(f'link_liked_{pk}', False):
            link.likes += 1
            link.save(update_fields=['likes'])
            request.session[f'link_liked_{pk}'] = True
            
            # 返回新的点赞数和总点赞数
            total_likes = FriendLink.objects.aggregate(total=Sum('likes'))['total'] or 0
            
            return JsonResponse({
                'success': True, 
                'likes': link.likes,
                'total_likes': total_likes
            })
        return JsonResponse({'success': False, 'error': '已经点过赞了'})
    except FriendLink.DoesNotExist:
        return JsonResponse({'success': False, 'error': '友链不存在'}, status=404)
    

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@require_POST
@csrf_exempt
def increment_page_views(request):
    """增加页面访问量"""
    page_view = PageView.objects.first()
    if not page_view:
        page_view = PageView.objects.create()
        
    # 使用session防止刷新重复计数
    if not request.session.get('page_viewed', False):
        page_view.increment_views()
        request.session['page_viewed'] = True
        
    return JsonResponse({'page_views': page_view.views})