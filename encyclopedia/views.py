from django.shortcuts import render, redirect

from . import util
from random import randint
import markdown2
from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "Title already exist. Try another.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/add.html")

def random(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)

def entry(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        content = "## Page was not found"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title})
    
def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {
            'error': "404 Not Found"
        })
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {
                "message": "Can't save with empty field.", 
                "title": title, 
                "content": content
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {
        'content': content, 'title': title
    })

def search(request):    
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {
        "entry": util.get_entry(q), 
        "q": q,
        "entries": util.list_entries()
    })
