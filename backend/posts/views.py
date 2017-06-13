import re, time
from datetime import datetime, timedelta
from math import floor # to round views

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt


from comments.utils import get_comment_list


from .models import Post
from .forms import PostForm
from core.utils import rank_hot
from tags.models import Tag
from categories.models import Category
from series.models import Series
from comments.models import Comment
from profiles.models import User

from .utils import update_wordcount

class GeneralMixin(object):
    def get_context_data(self, **kwargs):
        context = super(GeneralMixin, self).get_context_data(**kwargs)
        user = request.user
        context['notifications'] = Message.filter(to_user=user,isread=False)

class FilterMixin(object):
    paginate_by = 15
    def get_queryset(self):
        qs = super(FilterMixin, self).get_queryset()

        # Filter by query.
        query = self.request.GET.get('query')
        if query:
            # Search in titles, descriptions, authors, tags
            qs = qs.filter(Q(body__icontains=query) |
                           Q(author__username__icontains=query) |
                           Q(tags__title__icontains=query))                    


        # Filter by category.
        category = self.request.GET.get('category')
        if 'category' in self.kwargs:
            category = self.kwargs['category']
        if category:
            category = Category.objects.get(slug=category)
            qs = qs.filter(category=category)
        else:
            # Exclude categories
            exclude_categories = ['discussion', 'daily-practice', 'on-writing', 'blog']
            qs = qs.exclude(category__slug__in=exclude_categories)
            
        # Filter by tag
        tag = self.request.GET.get('tag')
        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
        if tag:
            tag = Tag.objects.get(slug=tag)
            qs = qs.filter(tags=tag)            
            
        # Sorting
        # (Turns queryset into the list, can't just .filter() later
        sorting = self.request.GET.get('sorting')
        if sorting == 'top':
            qs = qs.order_by('-score')
        elif sorting == 'new':
            qs = qs.order_by('-created_at')
        else:
            qs = rank_hot(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        urlstring = ""

        # All Tags
        tags = Tag.objects.all()
        tags = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')   
        context['tags'] = tags

        # All Categories
        categories = Category.objects.all()        
        context['categories'] = categories
        
        # Solo Tag
        context['tag'] = self.request.GET.get('tag')

        # Category
        category = self.request.GET.get('category')
        category_page = False
        if 'category' in self.kwargs:
            category = self.kwargs['category']
            category_page = True            
        if category:
            category = Category.objects.get(slug=category)
            context['category'] = category.title
            context['category_page'] = category_page

        # Sorting
        sorting = self.request.GET.get('sorting')
        if sorting:
            context['sorting'] = sorting
            
        # Query
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            urlstring += "&query=" + query            

        context['urlstring'] = urlstring

        context['submitform'] = PostForm()
        
        return context
    


class BrowseView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(BrowseView, self).get_queryset()
        # Show only published posts
        # Post doesn't have series, or is the first one in series
        qs = [p for p in qs if (p.published == True and
                                (not p.series or p.series.chapters.all()[0] == p))]

        return qs
    

class ProfileView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(ProfileView, self).get_queryset()
        profile = User.objects.get(username=self.kwargs['username'])
        # Filter author's posts
        qs = [p for p in qs if (p.author==profile)]
        # Show all posts to author, only published to everyone else
        if self.request.user != profile:
            qs = [p for p in qs if (p.published==True)]       
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = User.objects.get(username=self.kwargs['username'])
        context['profile'] = profile

        # Categories user has posted in
        posts = Post.objects.filter(author=profile)
        profile_categories = []
        for post in posts:
            if post.category and post.category not in profile_categories:
                profile_categories.append(post.category)
        context['categories'] = profile_categories

        # Position on the leaderboard
        leaderboard = list(User.objects.all().order_by('-karma')[:25])
        try:
            context['leaderboard_position'] = leaderboard.index(profile) + 1
        except:
            context['leaderboard_position'] = False

        # View Stats
        view_count = 0
        for post in profile.posts.all():
            view_count += post.views
        if view_count > 1000:
            view_count = str(floor(view_count/1000)) + "K"
        context['view_count'] = view_count

        # Calendar
        calendar = []
        saved_days = {}
        if profile.calendar:
            saved_days = eval(profile.calendar)
        today = time.strftime("%Y-%m-%d")
        # String to date
        start = datetime.strptime(today, "%Y-%m-%d")
        # Generate calendar
        for d in range(10):
            # Subtract d days from today
            this_day = start - timedelta(days=d)
            this_day = this_day.strftime("%Y-%m-%d")
            if this_day in saved_days:
                # If there's saved wordcount on this day, add it to calendar
                calendar.append(saved_days[this_day] * 0.001)
            else:
                calendar.append(0)
        context['calendar'] = calendar[::-1]

        # Calculate streak
        streak = 0
        for d in range(100):
            this_day = start - timedelta(days=d)
            this_day = this_day.strftime("%Y-%m-%d")
            if this_day in saved_days:
                # If I wrote 100+ words - increment the streak
                if saved_days[this_day] > 100:
                    streak += 1
                else:
                    # Once the day is missed - the streak is over
                    break
        context['streak'] = streak

        return context


    
    

class SubscriptionsView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(SubscriptionsView, self).get_queryset()
        # Filter by subscriptions
        subscribed_to = self.request.user.subscribed_to.all()
        qs = [p for p in qs if (p.author in subscribed_to and p.published)]
        return qs
        
    

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'    
    template_name = "posts/post-detail.html"


    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['submitform'] = PostForm()
        categories = Category.objects.all()        
        context['categories'] = categories

        post = self.object
        # Comments
        top_lvl_comments =Comment.objects.filter(post=post, parent = None)
        ranked_comments = top_lvl_comments.order_by('score', '-created_at')
        nested_comments = list(get_comment_list(ranked_comments, rankby="hot"))
        context['comments'] = nested_comments

        # Prev/next chapters
        if post.series:
            chapters = post.series.chapters.filter(published=True)
            this_index = 0
            prev_chapter = 0
            next_chapter = 0                
            if post.series:
                for index, chapter in enumerate(chapters):
                    if post == chapter:
                        this_index = index
            if this_index > 0:
                prev_chapter = chapters[this_index - 1]
            if this_index + 1 < len(chapters) and chapters[this_index + 1].published:
                next_chapter = chapters[this_index + 1]
                
            context['chapters'] = chapters
            context['prev_chapter'] = prev_chapter
            context['next_chapter'] = next_chapter        

        # Increment view counter
        if self.request.user != post.author:
            post.views +=1
            post.save()

        return context
    
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.score += 1 # self upvote
            post.save()

            # request.user.upvoted.add(post)

            # Add tags
            tags = request.POST.get('tags')
            if tags:
                tags = tags.split(",")
                for tag in tags:
                    title = tag.strip()
                    slug = slugify(title)
                    # Get tag by slug. Create tag if it doesn't exist.
                    try: 
                        tag = Tag.objects.get(slug=slug)
                    except:
                        tag = Tag.objects.create(title=tag)
                    post.tags.add(tag)

            # Add category
            category = request.POST.get('post_category')
            if category:
                category = Category.objects.get(slug=category)
                post.category = category

            # Add series
            series = request.GET.get('series')
            if series == "new":
                # If I'm being sent from a post that doesn't have series
                # (by clicking "Add Chapter")
                # I create series
                first_chapter = Post.objects.get(slug=request.GET.get('post'))
                series_title = first_chapter.body.splitlines()[0][:100]
                series = Series(slug = first_chapter.slug, title = series_title)
                series.save()
                # Add the original post to it
                first_chapter.series = series
                first_chapter.save()
                # Add the post I've just created to it
                post.series = series
            elif series:
                series = Series.objects.get(pk=series)
                post.series = series

            post.save()

            wordcount = len(re.findall(r'\w+', post.body))
            update_wordcount(wordcount, post.author)
            # post.hubs.add(*form.cleaned_data['tags'])
            # hubs = post.hubs.all()
            
            return HttpResponseRedirect('/post/'+post.slug+'/edit')

    else:
        form = PostForm()
        categories =  Category.objects.all()

        today = time.strftime("%Y-%m-%d")
        if today in request.user.calendar:
            wordcount = eval(request.user.calendar)[today]
        else:
            wordcount = 0
        
        return render(request, 'posts/edit.html', {
            'form':form,
            'wordcount':wordcount,            
            'categories': categories
        })


def post_edit(request, slug):
    post = Post.objects.get(slug=slug)
    prev_wordcount = len(re.findall(r'\w+', post.body))            
    # throw him out if he's not an author
    if request.user != post.author and not request.user.is_staff:
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()                

            # Replace tags
            tags = request.POST.get('tags')
            post.tags.set([])
            if tags:
                tags = tags.split(",")
                for tag in tags:
                    title = tag.strip()
                    slug = slugify(title)
                    # Get tag by slug. Create tag if it doesn't exist.
                    try: 
                        tag = Tag.objects.get(slug=slug)
                    except:
                        tag = Tag.objects.create(title=tag)
                    post.tags.add(tag)

            # Set category
            category = request.POST.get('post_category')
            if category:
                category = Category.objects.get(slug=category)
                post.category = category
            post.save()

            wordcount = len(re.findall(r'\w+', post.body)) - prev_wordcount
            update_wordcount(wordcount, post.author)

            return HttpResponseRedirect('/post/'+post.slug+'/edit')
    else:
        form = PostForm(instance=post)
        post_tags = [tag.title for tag in post.tags.all()]
        post_tags = ",".join(post_tags)

        today = time.strftime("%Y-%m-%d")
        if today in request.user.calendar:
            wordcount = eval(request.user.calendar)[today]
        else:
            wordcount = 0
            
        return render(request, 'posts/edit.html', {
            'post':post,
            'form':form,
            'post_tags':post_tags,
            'wordcount':wordcount,        
            'categories': Category.objects.all(),
        })
    

def post_delete(request, slug):
    post = Post.objects.get(slug=slug)

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.delete()
    return HttpResponseRedirect('/') 
    

# Voting
def upvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.save()
    post.author.karma += 1
    post.author.save()
    user = request.user
    user.upvoted.add(post)
    user.save()
    return HttpResponse()

def unupvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score -= 1
    post.save()
    post.author.karma -= 1
    post.author.save()
    user = request.user
    user.upvoted.remove(post)
    user.save()
    return HttpResponse()

    



def post_publish(request, slug):
    post = Post.objects.get(slug=slug)

    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.published = True
    post.save()
    
    return HttpResponseRedirect('/post/'+post.slug+'/edit')

def post_unpublish(request, slug):
    post = Post.objects.get(slug=slug)

    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.published = False
    post.save()
    
    return HttpResponseRedirect('/post/'+post.slug+'/edit')
