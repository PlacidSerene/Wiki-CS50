from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("wiki/<str:title>/edit_page", views.edit_page, name="edit_page"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("random", views.random_page, name="random_page") 
]
