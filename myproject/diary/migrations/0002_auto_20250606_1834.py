# Generated by Django 3.2.18 on 2025-06-06 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diarycomment',
            options={'ordering': ['-created_at'], 'verbose_name': '日记评论', 'verbose_name_plural': '日记评论'},
        ),
        migrations.AlterModelOptions(
            name='lifediary',
            options={'ordering': ['-created_at'], 'verbose_name': '生活日记', 'verbose_name_plural': '生活日记'},
        ),
        migrations.AddField(
            model_name='diarycomment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diary_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='diaryimage',
            name='image',
            field=models.ImageField(upload_to='diary_images/%Y/%m/%d/', verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='lifediary',
            name='author',
            field=models.CharField(default='陈错错', max_length=50, verbose_name='作者'),
        ),
        migrations.CreateModel(
            name='DiaryLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('diary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diary_likes', to='diary.lifediary')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diary_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '日记点赞',
                'verbose_name_plural': '日记点赞',
                'unique_together': {('user', 'diary')},
            },
        ),
        migrations.AddField(
            model_name='lifediary',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_diaries', through='diary.DiaryLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
