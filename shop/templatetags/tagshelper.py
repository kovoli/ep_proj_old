from django import template

register = template.Library()


@register.filter
def get_list(dictionary, key):
    return '&brand='.join(dict(dictionary).get(key))


@register.filter
def slice_name(name):
    return str(name)[:1]
