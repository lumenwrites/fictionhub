import json
from posts.models import Post
from profiles.models import User

with open('posts.json') as data_file:    
    posts = json.load(data_file)

with open('users.json') as data_file:    
    users = json.load(data_file)

to_import = []
for post in posts:
    if post["fields"]["published"] and post["fields"]["rational"]:
        to_import.append(post)

for post in to_import:
    body =  "# " + post["fields"]["title"] + "\n" + post["fields"]["body"]
    slug = post["fields"]["slug"]
    published = post["fields"]["published"]    
    author_pk = post["fields"]["author"]

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
    new_post = Post(body=body, author=author, published=published, slug=slug)
    new_post.save()
