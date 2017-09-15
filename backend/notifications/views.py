from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Message
from profiles.models import User
# from .utils import send_email

def inbox(request, notificationtype="all"):
    user = request.user
    if user.has_unread_notifications():
        # Show unread messages
        messages = Message.objects.filter(to_user=user,
                                          isread=False).order_by('-created_at')
        for message in messages:
            message.isread = True
            message.save()
    else:
        # Show all messages        
        messages = Message.objects.filter(to_user=user).order_by('-created_at')
        

    
    return render(request, 'notifications/inbox.html', {
        'messages':messages[:25]
    })

