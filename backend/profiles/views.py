from furl import furl

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from notifications.models import Message
from .models import User, Subscriber
from .forms import RegistrationForm, UserForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
 
    nextpage = request.GET.get('next', '/')

    # Initialize the form either fresh or with the appropriate POST data as the instance
    auth_form = AuthenticationForm(None, request.POST or None)
    
    if auth_form.is_valid():
        auth_login(request, auth_form.get_user())
        return HttpResponseRedirect(nextpage)
    
    else:
        # for errors
        return render(request, 'profiles/login.html', {
            'loginform': auth_form,
        })
    
# Only sign up
def join(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
 
    nextpage = request.GET.get('next', '/')

    auth_form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                            None,
                                            form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.save()

            # log user in after signig up
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return HttpResponseRedirect("/")
        else:
            # for errors
            return render(request, 'profiles/login.html', {
                'joinform': form,
            })

    else:
        return render(request, 'profiles/login.html', {
            'joinform': auth_form,
        })



# Email subscribe
def email_subscribe(request):
    if request.method == 'POST':    
        email = request.POST.get('email')
        ref = request.GET.get('ref')
        redirect_to = request.GET.get('next')
        # Add ?notification=subscribed to show the success alert and close the box
        # Use furl to magically add it to anything, even if I already have a get query
        redirect_to =  furl(redirect_to).add({'notification':'subscribed'}).url
        email_subscriber, created = Subscriber.objects.get_or_create(email=email,ref=ref)
        email_subscriber.save()
        return HttpResponseRedirect(redirect_to)


def subscribe(request, username):
    profile = User.objects.get(username=username)
    if not request.user.is_anonymous():
        user = request.user
        user.subscribed_to.add(profile)
        user.save()
        # Notification
        message = Message(from_user=user,
                          to_user=profile,
                          body="subscribed to your stories!")
        message.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/login/')    

def unsubscribe(request, username):
    userprofile = User.objects.get(username=username)    
    user = request.user
    user.subscribed_to.remove(userprofile)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    

def leaderboard(request):
    users = User.objects.all().order_by('-karma')[:25]
    return render(request, 'profiles/leaderboard.html',{
        'users':users
    })




@login_required
def settings(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings/')            
    else:
        form = UserForm(instance=request.user)
    
    return render(request, "profiles/settings.html", {
        'form': form
    })

@login_required
def update_paypal_email(request):
    if request.method == 'POST':
        user = request.user
        user.paypal_email = request.POST.get('paypal_email')
        user.save()
    return HttpResponseRedirect('/income/')            
    

@login_required
def income(request):
    balance = request.user.balance
    return render(request, "profiles/income.html", {
        'balance': balance
    })

@login_required
def update_password(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/preferences/')                        
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "profiles/prefs.html", {
        'form': form,
        # 'message': "Error, try again.",
        'title': "Change Password"                        
    })


