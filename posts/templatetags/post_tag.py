from django import template

from ..models import Post

register = template.Library()


@register.simple_tag()
def get_last_post():
    return Post.objects.filter(draft=False).order_by('-created')[:1]
