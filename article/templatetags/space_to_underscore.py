from django import template
register = template.Library()


@register.filter(name='space_to_underscore')
def space_to_underscore(value):
    """ A filter for convert space into underscore"""
    return value.replace(" ","_")
