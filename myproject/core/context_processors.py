from links.models import FriendLink, PageView
from message.models import Comment
from django.db.models import Count, Max, Sum, Q
from django.utils import timezone
from django.contrib.auth.models import User, Group
from articles.models import Article
from admin_interface.models import Theme
from datetime import datetime, timedelta
from diary.models import LifeDiary  # 导入生活日记模型


def backend_stats(request):
    """提供网站统计数据 - 全部公开给所有用户"""
    stats = {}
    
    try:
        # 1. 友情链接统计 - 全部公开
        links_total = FriendLink.objects.count()
        links_last_updated = FriendLink.objects.aggregate(
            latest=Max('updated_at')
        )['latest'] or timezone.now()
        
        # 获取页面浏览量
        page_view = PageView.objects.first()
        links_views = page_view.views if page_view else 0
        links_likes = FriendLink.objects.aggregate(total=Sum('likes'))['total'] or 0
        
        stats.update({
            'links_total': links_total,
            'links_views': links_views,
            'links_likes': links_likes,
            'links_last_updated': links_last_updated
        })
    except Exception as e:
        # 错误处理
        print(f"友情链接统计数据错误: {str(e)}")
        stats.update({
            'links_total': 0,
            'links_views': 0,
            'links_likes': 0,
            'links_last_updated': timezone.now()
        })
    
    try:
        # 2. 留言板统计 - 全部公开
        comment_stats = Comment.objects.aggregate(
            total=Count('id'),
            approved=Count('id', filter=Q(status='approved')),
            pending=Count('id', filter=Q(status='pending')),
            rejected=Count('id', filter=Q(status='rejected'))
        )
        
        stats.update({
            'comments_total': comment_stats.get('total', 0),
            'comments_approved': comment_stats.get('approved', 0),
            'comments_pending': comment_stats.get('pending', 0),
            'comments_rejected': comment_stats.get('rejected', 0)
        })
    except Exception as e:
        print(f"留言板统计数据错误: {str(e)}")
        stats.update({
            'comments_total': 0,
            'comments_approved': 0,
            'comments_pending': 0,
            'comments_rejected': 0
        })
    
    try:
        # 3. 用户统计 - 全部公开
        stats['users_total'] = User.objects.count()
        stats['groups_total'] = Group.objects.count()
        
        # 计算过去30天新用户数量
        thirty_days_ago = timezone.now() - timedelta(days=30)
        stats['users_new'] = User.objects.filter(
            date_joined__gte=thirty_days_ago
        ).count()
    except Exception as e:
        print(f"用户统计数据错误: {str(e)}")
        stats['users_total'] = 0
        stats['groups_total'] = 0
        stats['users_new'] = 0
    
    try:
        # 4. 主题统计 - 全部公开
        stats['themes_total'] = Theme.objects.count()
    except Exception as e:
        print(f"主题统计数据错误: {str(e)}")
        stats['themes_total'] = 0
    
    try:
        # 5. 文章统计 - 全部公开
        stats['articles_total'] = Article.objects.count()
        stats['articles_published'] = Article.objects.filter(
            is_published=True
        ).count()
        stats['articles_draft'] = Article.objects.filter(
            is_published=False
        ).count()
        stats['articles_views'] = Article.objects.aggregate(
            total=Sum('views')
        )['total'] or 0
    except Exception as e:
        print(f"文章统计数据错误: {str(e)}")
        stats['articles_total'] = 0
        stats['articles_published'] = 0
        stats['articles_draft'] = 0
        stats['articles_views'] = 0
    
    try:
        # 6. 生活日记统计 - 全部公开
        diaries_total = LifeDiary.objects.count()
        
        # 本月新增日记数
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        diaries_monthly = LifeDiary.objects.filter(
            created_at__gte=first_day_of_month
        ).count()
        
        # 作者数量
        diaries_authors = LifeDiary.objects.values('author').distinct().count()
        
        stats.update({
            'diaries_total': diaries_total,
            'diaries_monthly': diaries_monthly,
            'diaries_authors': diaries_authors
        })
    except Exception as e:
        print(f"生活日记统计数据错误: {str(e)}")
        stats.update({
            'diaries_total': 0,
            'diaries_monthly': 0,
            'diaries_authors': 0
        })
    
    # 7. 添加URL信息 - 全部公开
    try:
        stats['articles_url'] = "/articles/"
        stats['friendlinks_url'] = "/links/"
        stats['comments_url'] = "/message/comment_board/"
        stats['diaries_url'] = "/diary/"
        stats['users_url'] = "/admin/auth/user/"  # 如果需要可改为前台用户列表页
    except:
        stats.update({
            'articles_url': "#",
            'friendlinks_url': "#",
            'comments_url': "#",
            'diaries_url': "#",
            'users_url': "#"
        })
    
    # 返回完整的统计数据字典
    return stats