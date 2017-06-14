from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from posts.models import Post
from notifications.models import Message
from .models import Comment
from .forms import CommentForm

def comment_submit(request, post_slug=""):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            if post_slug:
                post = Post.objects.get(slug=post_slug)
                comment.post = post
            comment.save()

            # Notification
            body = "replied to your [post]("+comment.post.get_absolute_url()+")<br/>"\
                   + comment.body
            message = Message(from_user=comment.author,
                              to_user=comment.post.author,
                              body=body)
            message.save()
            
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            # If error
            prev_url = request.GET.get('next', '/')
            return HttpResponseRedirect(prev_url)
    else:
        # If not post
        prev_url = request.GET.get('next', '/')
        return HttpResponseRedirect(prev_url)



def reply_submit(request, post_slug, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(slug=post_slug)            
            comment.parent = Comment.objects.get(id=comment_id)
            comment.save()

            # comment_url = request.GET.get('next', '/')+"#id-"+str(comment.id)
            return HttpResponseRedirect(comment.post.get_absolute_url())
        else:
            comment_url = request.GET.get('next', '/')
            return HttpResponseRedirect(comment_url)
    return HttpResponseRedirect('/error')                    


# Voting
def comment_upvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score += 1
    comment.save()
    comment.author.karma += 1
    comment.author.save()
    user = request.user
    user.comments_upvoted.add(comment)
    user.save()
    return HttpResponse()

def comment_unupvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score -= 1
    comment.save()
    comment.author.karma = 1
    comment.author.save()
    user = request.user
    user.comments_upvoted.remove(comment)
    user.save()
    return HttpResponse()



def comment_edit(request, post_slug, comment_id):
    comment = Comment.objects.get(id = comment_id)
    nextpage = request.GET.get('next', '/')

    if request.method == 'POST':
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return HttpResponseRedirect("/post/"+post_slug+"/")
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comments/edit.html', {
        'comment':comment,
        'post_slug':post_slug,        
        'form':form,
        'nextpage':nextpage
    })
    
    # throw him out if he's not an author
    if request.user != comment.author:
        return HttpResponseRedirect('/')        
    return HttpResponseRedirect('/') # to video list


def comment_delete(request, post_slug, comment_id):
    comment = Comment.objects.get(id = comment_id)

    # throw him out if he's not an author
    if request.user != comment.author:
        return HttpResponseRedirect('/')        

    comment.delete()
    
    return HttpResponseRedirect("/post/"+post_slug+"/")


