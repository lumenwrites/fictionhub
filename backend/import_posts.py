import json
from posts.models import Post
from profiles.models import User
from categories.models import Category
from series.models import Series

with open('posts.json') as data_file:    
    posts = json.load(data_file)

with open('users.json') as data_file:    
    users = json.load(data_file)

to_import = []
for post in posts:
    if not post["fields"]["daily"] and  post["fields"]["author"] != 1:
        to_import.append(post)

category = Category.objects.get(slug="rational")        
for post in to_import:
    body =  "# " + post["fields"]["title"] + "\n" + post["fields"]["body"]
    slug = post["fields"]["slug"]
    published = post["fields"]["published"]    
    author_pk = post["fields"]["author"]
    created_at = post["fields"]["pub_date"]    

    for user in users:
        if user["pk"] == author_pk and user["model"] == "profiles.user":
            author_saved = user
    username = author_saved["fields"]["username"]
    password = author_saved["fields"]["password"]
    try:
        author = User.objects.get(username=username)
    except:
        author = User(username=username, password=password)
        author.save()

    series = None
    if post["fields"]["parent"]:
        # Find parent
        for p in to_import:
            if post["fields"]["parent"] == p["pk"]:
                parent = p
        series_title = parent["fields"]["title"]
        series_slug = parent["fields"]["slug"]
        # Get or create series
        try:
            series = Series.objects.get(slug=series_slug)
        except:
            series = Series(title=series_title, slug=series_slug)
            series.save()
        slug = parent["fields"]["slug"] + "-" + slug
    else:
        # If post has no parent, try getting series created just above,
        # By parent's slug, because Im using it to generate slug for series.
        try:
            series = Series.objects.get(slug=slug)
        except:
            # Check if has children
            for p in to_import:
                if p["fields"]["parent"] == post["pk"]:
                    series = Series(title=post["fields"]["title"], slug=slug)
                    series.save()

    try:
        Post.objects.get(slug=slug)
    except:
        new_post = Post(body=body, author=author, published=True, slug=slug, category=category, series=series, created_at = created_at)
        new_post.save()


