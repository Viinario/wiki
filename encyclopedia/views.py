from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def notFound(request, name):
    return render(request, "encyclopedia/notFound.html", {
        "name": name.capitalize()
    })
