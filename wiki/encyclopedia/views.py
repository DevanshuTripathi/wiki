from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from markdown2 import Markdown

markdowner=Markdown()
class NewTaskForm(forms.Form):
    title = forms.CharField(label ="Enter Title")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add(request):
    if request.method=="POST":
        form= NewTaskForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=request.POST.get('content')
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form":form
            })
    return render(request, "encyclopedia/add.html", {
        "form":NewTaskForm()
    })

def search(request):
    search = request.POST.get('q')
    if search in util.list_entries():
        return markdowner.convert(util.get_entry(search))
