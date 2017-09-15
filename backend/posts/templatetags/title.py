# markdownify
from django import template
from markdown import markdown
 
register = template.Library()
 
@register.filter
def title(post):
    body = post.body
    html = markdown(body)
    firstline = html.splitlines()[0]
    title = firstline[:100]
    title = markdown(title) 
    return title

