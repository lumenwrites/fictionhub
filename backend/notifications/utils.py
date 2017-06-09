def email_notification(message):
    from_username = message.from_user.username
    to_user = message.to_user
    topic = from_username + message.body
    body = from_username  + message.body + "unsubscribe"
    message.email_sent = True
    message.save()
