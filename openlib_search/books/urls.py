from django.urls import path
from books.views import search_page, favourite_page, add_to_favourite_books, delete_favourite, detail_page


app_name = "books"

urlpatterns = [
    path("", search_page, name="search"),
    path("favourite/", favourite_page, name="favourite"),
    path("add-favourite/", add_to_favourite_books, name="add_to_favourite"),
    path("delete-favourite/<str:id>", delete_favourite, name="favourite-delete"),
    path("detail/<str:id>/", detail_page, name="detail")
]
