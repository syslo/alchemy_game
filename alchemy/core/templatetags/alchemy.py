from django import template
from ..models import LogItem


register = template.Library()


@register.inclusion_tag('alchemy/parts/log.html', takes_context=True)
def user_logs(context, limit=10):
    return {
        'logs': context.request.user.logs.order_by('-datetime')[:limit],
    }


@register.inclusion_tag('alchemy/parts/log.html')
def type_logs(type, limit=10):
    return {
        'logs': LogItem.objects.filter(type=type).order_by('-datetime')[:limit],
    }
