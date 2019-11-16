from django import template
register = template.Library()

@register.filter
def pic_name(value):
    path = value
    name = path.split("/")[-1]
    return name
