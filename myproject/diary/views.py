from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import LifeDiary, DiaryImage, DiaryComment, DiaryLike  # 修复导入

def diary_list(request):
    """日记列表视图（带分页）"""
    # 获取所有日记并按创建时间倒序
    diaries = LifeDiary.objects.all().order_by('-created_at')
    
    # 如果没有日记，返回空页面
    if not diaries.exists():
        return render(request, 'diary/diary_list.html', {'diary': None})
    
    # 每页显示1篇日记
    paginator = Paginator(diaries, 1)
    page = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是整数，显示第一页
        page_obj = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        page_obj = paginator.page(paginator.num_pages)
    
    # 获取当前页面的日记（应该只有一篇）
    if page_obj.object_list:
        current_diary = page_obj.object_list[0]
    else:
        # 如果没有日记，显示空页面
        current_diary = None
    
    # 如果有日记，处理相关信息
    if current_diary:
        # 处理图片URL
        for image in current_diary.images.all():
            if image.image:
                # 构建完整的绝对URL
                image.image_url = request.build_absolute_uri(image.image.url)
        
        # 获取该日记的评论
        comments = DiaryComment.objects.filter(diary=current_diary).order_by('-created_at')
        
        # 获取用户点赞状态
        current_diary.user_has_liked = False
        if request.user.is_authenticated:
            current_diary.user_has_liked = DiaryLike.objects.filter(
                user=request.user, 
                diary=current_diary
            ).exists()
        
        # 获取总点赞数
        current_diary.like_count = DiaryLike.objects.filter(diary=current_diary).count()
    else:
        comments = []
    
    context = {
        'page_obj': page_obj,
        'diary': current_diary,
        'comments': comments,
    }
    
    return render(request, 'diary/diary_list.html', context)

@require_POST
def post_comment(request, diary_id):
    """处理评论提交"""
    diary = get_object_or_404(LifeDiary, id=diary_id)
    page = request.GET.get('page', 1)
    
    nickname = request.POST.get('nickname', '')
    content = request.POST.get('content', '')
    
    if not nickname:
        nickname = request.user.username if request.user.is_authenticated else "游客"
    
    if content.strip():
        # 创建评论
        with transaction.atomic():
            DiaryComment.objects.create(
                diary=diary,
                user=request.user if request.user.is_authenticated else None,
                nickname=nickname,
                content=content
            )
    
    # 重定向回当前页面
    return redirect(f"{reverse('diary:diary_list')}?page={page}#comments")

@require_POST
@login_required
def like_diary(request, diary_id):
    """处理点赞功能"""
    diary = get_object_or_404(LifeDiary, id=diary_id)
    
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': '请登录后再点赞'
        }, status=401)
    
    # 使用原子事务确保数据一致性
    with transaction.atomic():
        # 检查是否存在点赞记录
        like, created = DiaryLike.objects.get_or_create(
            user=request.user,
            diary=diary
        )
        
        # 如果已经点赞过，则取消点赞
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        
        # 重新计算点赞数量确保准确性
        like_count = DiaryLike.objects.filter(diary=diary).count()
        
    # 返回JSON响应
    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'like_count': like_count
    })