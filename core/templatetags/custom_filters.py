from django import template

register = template.Library()


@register.filter
def format_price(value):
    return f"{value:,}"


@register.filter
def multiply(value, arg):
    return value * arg
