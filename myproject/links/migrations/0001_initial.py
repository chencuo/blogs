# Generated by Django 3.2.18 on 2025-06-06 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='网站名称')),
                ('url', models.URLField(verbose_name='网站链接')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='friend_links/logos/', verbose_name='网站Logo')),
                ('logo_url', models.URLField(blank=True, null=True, verbose_name='Logo URL')),
                ('description', models.TextField(verbose_name='网站描述')),
                ('category', models.CharField(default='未分类', max_length=50, verbose_name='分类')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览次数')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='点赞数')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否显示')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['-created_at'],
            },
        ),
    ]
