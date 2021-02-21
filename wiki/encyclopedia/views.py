from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/title.html",{
            "content": markdowner.convert(util.get_entry(title)), "title":title
        })

