from django import template
register = template.Library()


@register.inclusion_tag('netvis/load_js.html', takes_context=True)
def load_netvis_js(context):
    values = {}
    return values