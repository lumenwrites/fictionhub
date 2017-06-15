from django.shortcuts import render
from django.http import HttpResponseRedirect

from profiles.models import User
from .models import Series
from .forms import SeriesForm


def series_update(request, slug):
    series = Series.objects.get(slug=slug)
    # throw him out if he's not an author
    if request.user != series.chapters.all()[0].author:
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        form = SeriesForm(request.POST, instance=series)
        if form.is_valid():
            series = form.save(commit=False)
            series.save()                

    prev_url = request.GET.get('next', '/')
    return HttpResponseRedirect(prev_url)



def series_purchase(request, slug, username):
    # Grab data from POST request sent by paypal
    # slug = request.POST.get('item_name')
    # username = request.POST.get('username')
    series = Series.objects.get(slug=slug)
    user = User.objects.get(username=username)
    # Add to user's purchased series
    user.purchased_series.add(series)
    user.save()

    # Update author's balance
    first_paid_chapter = series.chapters.all()[series.free_chapters]
    author = first_paid_chapter.author
    # Increment authors balance (minus $1 which goes to me)
    author.balance += series.price - 1
    author.save()

    # Redirect to first paid chapter
    return HttpResponseRedirect(first_paid_chapter.get_absolute_url())
