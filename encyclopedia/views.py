from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

from markdown2 import Markdown

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


