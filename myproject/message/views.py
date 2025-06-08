from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random
from django.utils import timezone
from django.http import JsonResponse

class CommentBoardView(View):
    template_name = 'message/comment_board.html'
    
    def get(self, request):
        form = CommentForm()
        approved_comments = Comment.objects.filter(status='approved').order_by('-pinned', '-created_at')
        comment_count = Comment.objects.filter(status='approved').count()
        
        return render(request, self.template_name, {
            'form': form,
            'comments': approved_comments,
            'comment_count': comment_count + 1,
            'now': timezone.now().strftime("%Y-%m-%d")
        })
    
    def post(self, request):
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            
            # 设置随机设备信息（如第一张图所示）
            devices = ['Android', 'iPhone', 'iPad']
            browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']
            regions = ['北京', '上海', '广东', '江苏', '湖北', '浙江', '四川']
            
            comment.device_info = f"{random.choice(devices)}/{random.choice(browsers)}"
            comment.region = random.choice(regions)
            comment.status = 'pending'
            comment.save()
            
            return render(request, self.template_name, {
                'form': CommentForm(),
                'comments': Comment.objects.filter(status='approved').order_by('-pinned', '-created_at'),
                'comment_count': Comment.objects.filter(status='approved').count() + 1,
                'now': timezone.now().strftime("%Y-%m-%d"),
                'submission_success': True
            })
        
        return render(request, self.template_name, {
            'form': form,
            'comments': Comment.objects.filter(status='approved').order_by('-pinned', '-created_at'),
            'comment_count': Comment.objects.filter(status='approved').count() + 1,
            'now': timezone.now().strftime("%Y-%m-%d")
        })

@method_decorator(csrf_exempt, name='dispatch')
class AdminCommentView(View):
    """处理置顶和回复操作（如第三张图所示）"""
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            action = request.POST.get('action')
            
            if action == 'toggle_pin':
                # 处理置顶操作
                comment.pinned = not comment.pinned
                comment.save()
                return JsonResponse({'success': True, 'pinned': comment.pinned})
                
            elif action == 'add_reply':
                # 处理回复操作
                reply_text = request.POST.get('reply', '')
                comment.reply = reply_text
                comment.save()
                return JsonResponse({'success': True})
                
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': '留言不存在'})
        
        return JsonResponse({'success': False, 'error': '无效的操作'})