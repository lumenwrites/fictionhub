# markdownify
from django import template
from markdown import Markdown
import re

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
            
    md = Markdown(extensions = ['markdown.extensions.meta']) # , 'markdown.extensions.nl2br'
    html = md.convert(body)    


    # If it's a Screenplay
    # if "format" in md.Meta and md.Meta["format"] == "screenplay":
    if "title" in md.Meta:
        # Return markdown, will be rendered into pretty screenplay format by frontend js
        screenplay = '<div class="screenplay">' + body + '</div>'
        
        if truncated:
            clickabletitle = '<a href="'+post.get_absolute_url()+'"><h1>'+md.Meta["title"][0]+'</h1></a>'
            readmorelink = '<a class="read-more" href="'+post.get_absolute_url()+'">Read more...</a>'
            screenplay = clickabletitle + screenplay + readmorelink

        return screenplay
    
    # Replace all the \n's with linebreak+space, but not \n\n's
    # lookahead/lookbehind make sure theres no 2nd one around
    body = re.sub('(?<!\n)\n(?!\n)' , '\n ', body)


    firstline = html.splitlines()[0]
    rest = html.splitlines()[1:]
    # If first line is a header, make it link to the post
    if "<h1>" in firstline and truncate:
        firstline = '<a href="'+post.get_absolute_url()+'">'+firstline+'</a>'
    html = str(firstline) + str(''.join(rest))

    if truncated:
        html += '<a class="read-more" href="'+post.get_absolute_url()+'">Read more...</a>'
    return html

