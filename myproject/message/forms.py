from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'email', 'content']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '输入您的用户名',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '输入您的邮箱',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '在此输入您的留言...'
            }),
        }
        
