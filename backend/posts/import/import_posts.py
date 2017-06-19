import json
from posts.models import Post
from profiles.models import User
from categories.models import Category
from series.models import Series

with open('posts.json') as data_file:    
    all_posts = json.load(data_file)

with open('users.json') as data_file:    
    all_users = json.load(data_file)

posts = []
for post in all_posts:
    if not post["fields"]["daily"]:
        posts.append(post)

users = []
for user in all_users:
    if user["model"] == "profiles.user":
        users.append(user)
        
category = Category.objects.get(slug="rational")        
for post in posts:
    # Get post data
    body =  "# " + post["fields"]["title"] + "\n" + post["fields"]["body"]
    slug = post["fields"]["slug"]
    published = post["fields"]["published"]
    views = post["fields"]["views"]
    score= post["fields"]["score"]            
    created_at = post["fields"]["pub_date"]    
    author_pk = post["fields"]["author"]

    # Find author by pk
    for user in users:
        if user["pk"] == author_pk:
            author_saved = user
    # Get author data
    username = author_saved["fields"]["username"]
    password = author_saved["fields"]["password"]
    karma = author_saved["fields"]["karma"]
    # Get or create author
    try:
        author = User.objects.get(username=username)
    except:
        author = User(username=username, password=password, karma=karma)
        author.save()


    series = None
    # Create a series for the chapter, with slug/title of a parent
    if post["fields"]["post_type"] == "chapter":
        # Find parent
        for p in posts:
            if p["pk"] == post["fields"]["parent"]:
                parent = p
        # Modify slug to parent-slug-chapter-slug.
        slug = parent["fields"]["slug"] + "-" + slug

        # Create series for a parent
        series_title = parent["fields"]["title"]
        series_slug = parent["fields"]["slug"]

        # Get or create series
        try:
            series = Series.objects.get(slug=series_slug)
        except:
            series = Series(title=series_title, slug=series_slug)
            series.save()
    # If the story is a parent, find series with matching slug and add it to it.
    try:
        series = Series.objects.get(slug=slug)
    except:
        pass

    try:
        # Check if post already exists
        post = Post.objects.get(slug=slug)
        # On a second run, making sure to add series to parent posts
        post.series = series
        post.save()
    except:
        # Create post if it doesnt exist yet
        new_post = Post(body=body,
                        slug=slug,
                        views=views,
                        score=score,                        
                        author=author,
                        published=True,
                        category=category,
                        series=series,
                        created_at = created_at)
        new_post.save()


