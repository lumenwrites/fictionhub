# markdownify
from django import template
from markdown import markdown
 
register = template.Library()
 
@register.filter
def markdownify(body, truncate = False):
    if truncate:
        try:
            text = body.split("<!-- readmore -->")[0].strip()
        except:
            pass
        text = body[:1024]

    html = markdown(body)

    return html

