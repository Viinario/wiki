import secrets
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

from markdown2 import Markdown

class NewForm(forms.Form):
    title = forms.CharField(max_length=20)
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def find(request, name):
    page = util.get_entry(name)
    if page is not None:
        return render(request, "encyclopedia/page.html", {
        "entry": Markdown().convert(page),
        "name": name
        })
    else:
      return render(request, "encyclopedia/notFound.html", {
        "name": name
        })

def search(request):
    querry = request.GET.get('q','')
    if(util.get_entry(querry) is not None):
        return find(request, querry)
    else:
        ul = []
        for e in util.list_entries():
            if querry.upper() in e.upper():
                ul.append(e)
    return render(request, "encyclopedia/index.html", {
        "entries": ul,
        "querry": querry
    })

def newPage(request):
    return render(request, "encyclopedia/newPage.html",{
        "form": NewForm()
    })

def savePage(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("find", kwargs={'name': title}))
            else:
                return render(request, "encyclopedia/newPage.html",{
                        "form": form,
                        "warming": True,
                        "page": title
                        })

def edit(request, name):
    page = util.get_entry(name)
    if page is None:
        return  render(request, "encyclopedia/notFound.html", {
        "name": name
        })
    else:
        form = NewForm()
        form.fields["title"].initial = name
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = page
        return render(request, "encyclopedia/edit.html",{
            "form": form,
            "name": name
        })

def saveEditPage(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("find", kwargs={'name': title}))

def random(request):
    pages = util.list_entries()
    name = secrets.choice(pages)
    return HttpResponseRedirect(reverse("find", kwargs={'name':name}))





