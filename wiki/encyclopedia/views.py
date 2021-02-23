from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
from markdown2 import Markdown
from . import util

class NewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows":"3", "columns":"6"}))

# All entries



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html",{
            "search": True, 
        })
    else:
        return render(request, "encyclopedia/title.html",{
            "content": Markdown().convert(util.get_entry(title)), "title":title
        })
    
    
def search(request):
    if request.method == "GET":
        search_entry = request.GET.get("q").upper()
        if util.get_entry(search_entry) is not None: #able to find result
            return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={"title":search_entry}))
        else:
            # there is no result
            # find the substring!
            match = [] #this list stores the match results
            for entry in util.list_entries():
                if search_entry.lower() in entry.lower():
                    #return to result page
                    match.append(entry)
            
            if len(match) != 0:
                return render(request, "encyclopedia/result.html", {
                    "results": match 
                })
            else:
                return render(request, "encyclopedia/error.html",{
                    "search": True,
                })


def new_page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title not in util.list_entries():
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:title", kwargs={'title': title}))

            else:
                render(request, "encyclopedia/error.html", {
                    "search": False,
                })
    return render(request, "encyclopedia/new_page.html",{
        "form": NewPage()
    })