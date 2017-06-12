import time

def update_wordcount(wordcount, author):
    today = time.strftime("%Y-%m-%d")
    calendar={}
    if author.calendar:
        calendar = eval(author.calendar)
    if calendar[today]:
        calendar[today] += wordcount
    else:
        calendar[today] = wordcount                
    author.calendar = repr(calendar)
    author.save()
                    
