from django import template
from ..models import Category, Comment

register =template.Library()

@register.simple_tag
def all_categories():
    return Category.objects.all()

