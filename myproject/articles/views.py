from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'articles'
    paginate_by = 8  # 每页8篇文章
    
    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-pub_date')

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = get_object_or_404(Article, slug=slug, is_published=True)
        obj.increment_views()  # 每次浏览增加浏览量
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加相邻文章
        article = self.object
        context['previous_article'] = Article.objects.filter(
            pub_date__lt=article.pub_date, 
            is_published=True
        ).order_by('-pub_date').first()
        context['next_article'] = Article.objects.filter(
            pub_date__gt=article.pub_date,
            is_published=True
        ).order_by('pub_date').first()
        return context