from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
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
    
    
def search(request):
    all_entries = util.list_entries()
    if request.method == "GET":
        search_entry = request.GET.get("q").upper()
        if util.get_entry(search_entry) is not None: #able to find result
            return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title":search_entry}))
        else:
            print(search_entry) 
            # there is no result
            # find the substring!
            match = [] #this string is to store the match results
            for entry in all_entries:
                if search_entry.lower() in entry.lower():
                    #return to result page
                    match.append(entry)
            return render(request, "encyclopedia/result.html", {
                "results": match
            })
            

