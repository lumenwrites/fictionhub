# markdownify
from django import template
from markdown import markdown
 
register = template.Library()
 
@register.filter
def markdownify(post, truncate = False):
    body = post.body
    truncated = False
    if truncate:
        if "<!-- more -->" in body:
            text = body.split("<!-- more -->")[0].strip()
        else:
            text = body[:380]
        if len(text) < len(body):
            body = text
            truncated = True

    body = body.replace('\n\n','<br/>')
    body = body.replace('\n',' ')    
    html = markdown(body)
    firstline = html.splitlines()[0]
    rest = html.splitlines()[1:]
    # If first line is a header, make it link to the post
    if "<h1>" in firstline and truncate:
        firstline = '<a href="'+post.get_absolute_url()+'">'+firstline+'</a>'
    html = str(firstline) + str(''.join(rest))

    if truncated:
        html += '<a class="read-more" href="'+post.get_absolute_url()+'">Read more...</a>'
    return html

