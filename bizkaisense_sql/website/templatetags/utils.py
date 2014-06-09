from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    s = arg.split(':')
    return value.replace(s[0], s[1])
