# home/templatetags/color_tags.py

from django import template

register = template.Library()

COLORS = [
    '#ff79c6', # 图片中的粉红色
    '#8be9fd', # 淡蓝色
    '#50fa7b', # 亮绿色
    '#bd93f9', # 紫色
    '#ffb86c', # 橙色
    '#44d5bd', # 绿松石色
    '#ff5555'  # 红色
]

@register.filter(name='color_by_index')
def color_by_index(index):
    return COLORS[index % len(COLORS)]