from django.shortcuts import render

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
