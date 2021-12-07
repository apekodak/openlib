from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from books.forms import FavouriteBookForm
from books.models import FavouriteBook
from books.utils import search_books, get_book


def search_page(request):
    books: list = []
    message: str = ''
    if searchQuery := request.GET.get('q'):
        books: list[dict] = search_books(searchQuery)

        if len(books) == 0:
            message = 'No books was found.'

    return render(request, 'books/index.html', {
        'books': books,
        'message': message
    })


@login_required(login_url='../users/login')
def favourite_page(request):
    message: str = ''
    queryset = request.user.books.all()
    if len(queryset) == 0:
        message = 'You don`t have favourite books yet'
    return render(request, 'books/favourite.html', {'books': queryset, 'message': message})


@login_required(login_url='../users/login')
def add_to_favourite_books(request):
    if request.method == 'POST':
        data = dict(request.POST)
        data['user'] = request.user
        form = FavouriteBookForm(data)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect(reverse('books:favourite'))

    return redirect(reverse('books:search'))


def detail_page(request, id):
    book = get_book(id)
    if image_url := request.GET.get('img'):
        book['image'] = image_url
    return render(request, 'books/detail.html', {
        'book': book
    })


@login_required(login_url='../users/login')
def delete_favourite(request, id):
    try:
        FavouriteBook.objects.get(user=request.user, key=id).delete()
    except FavouriteBook.DoesNotExist:
        pass

    return redirect('books:favourite')
