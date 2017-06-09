import datetime
import time

from django.utils.timezone import utc

def rank_hot(posts, top=180, consider=1000):
    # top - number of stories to show,
    # consider - number of latest stories to rank
    
    def score(post, gravity=1.2, timebase=120):
        # number_of_comments = len(post.comments.all())
        rating = (post.score + 1)**0.8 # + number_of_comments
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        age = int((now - post.created_at).total_seconds())/60
        # temporary hack to not let score be below zero
        try:
            if float(rating) > 1:
                scr = rating/(age+timebase)**gravity
            else:
                scr = 0
        except:
            scr = 0
        return scr

    latest_posts = posts.order_by('-created_at')#[:consider]
    #comprehension, posts with rating, sorted
    posts_with_rating = [(score(post), post) for post in latest_posts]
    #ranked_posts = sorted(posts_with_rating, reverse = True) - old but worked
    ranked_posts = sorted(latest_posts, key=score, reverse = True)
    #strip away the rating and return only posts
    # return [post for _, post in ranked_posts][:top] - old but worked
    return ranked_posts

def rank_top(stories, timespan = None):
    # if timespan == "day":
    #     day = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('day')
    #     stories = stories.filter(created_at__day = day)        
    # elif timespan == "month":
    #     month = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('month')
    #     stories = stories.filter(created_at__month = month)        
    # elif timespan == "all-time":
    #     year = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('year')
    #     stories = stories.filter(created_at__year = year)                
    
    top_stories = stories.order_by('-score')
    return top_stories



def age(timestamp):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    created_at = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
    
    age_in_minutes = int((now-created_at).total_seconds())/60

    # usage: age(prompt.created_utc)
    return age_in_minutes


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    

    
# def send_email(subject, body, to=['raymestalez@gmail.com']):
#     context = Context({
#         'body':body
#     })    

#     text_content = render_to_string('email/email.txt', context)
#     email = EmailMultiAlternatives(subject, text_content)

#     email.to = to
#     email.send()
