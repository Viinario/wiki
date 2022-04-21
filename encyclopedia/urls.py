from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.find, name="find"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage")
]
