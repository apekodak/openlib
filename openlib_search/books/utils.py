import requests
from django.urls import reverse

from books.models import FavouriteBook


BASE_SEARCH_API_URL: str = 'http://openlibrary.org/search.json'
BASE_IMAGE_API_URL: str = 'https://covers.openlibrary.org/b/{0}/{1}-{2}.jpg'
BASE_BOOK_API_URL: str = 'https://openlibrary.org/works/{0}.json'
BASE_IMAGE_KEYS: list[str] = [
    'cover_i',
    'isbm',
    'oclc',
    'lccn',
    'olid'
]
BASE_IMAGE_URL = '/static/images/base.jpg'
BASE_IMAGE_SIZE = 'M'

BOOK_KEYS = [
    'title',
    'author_name',
    'key'
] + BASE_IMAGE_KEYS


def prepate_data(source: list, needed_keys: list[str], quantity: int = None, *args, **kwargs) -> dict:
    if quantity:
        source = source[:quantity]

    result: list = []

    for source_dict in source:
        new_dict = {key: source_dict[key] for key in source_dict if key in needed_keys}

        new_dict['author_name'] = new_dict.get('author_name', [''])[0]
        new_dict['key'] = new_dict.get('key', '').split('/')[-1]
        new_dict['url'] = reverse('books:detail', kwargs={'id': new_dict['key']})

        result.append(new_dict)

    return result


def create_search_url(search_text: str, *args, **kwargs):
    return BASE_SEARCH_API_URL + '?q=' + search_text.strip()


def get_image_url(key_name: str, image_id: str, size: str = BASE_IMAGE_SIZE, *args, **kwargs):
    return BASE_IMAGE_API_URL.format(key_name, image_id, size)


def add_image_to_book(book_dict: dict) -> dict:
    book_dict['image'] = BASE_IMAGE_URL

    for image_key in BASE_IMAGE_KEYS:
        if image_id_list := book_dict.get(image_key, None):
            if image_key == 'cover_i':
                image_key = 'id'
                image_id_list = [image_id_list, ]
            book_dict['image'] = get_image_url(key_name=image_key, image_id=image_id_list[0])

            break
    return book_dict


def add_images_to_books(books_list:list[dict]) -> list[dict]:
    return list(map(add_image_to_book, books_list))


def search_books(search_text: str, quantity: int = None, *args, **kwargs) -> list[dict]:
    request_url = create_search_url(search_text)

    '''
        1. First make request using requests.get
        2. Second serialize response using .json() method
        3. Third get all books from data dictionary using 'docs' key
        4. At last prepare data using prepare_data function and quantity
    '''
    books: list[dict] = prepate_data(
        requests.get(request_url).json()['docs'],
        BOOK_KEYS,
        quantity=quantity,
    )

    books = add_images_to_books(books)

    return books


def get_book(book_id: str) -> dict:
    data = requests.get(BASE_BOOK_API_URL.format(book_id)).json()
    try:
        book = FavouriteBook.objects.get(key=data['key'].split('/')[-1])
        data['image'] = book.image
        data['author_name'] = book.author_name
        data['delete_url'] = book.get_delete_url()
    except Exception:
        data = add_image_to_book(data)

    if type(data.get('description', None)) == dict:
        data['description'] = data['description']['value']
    if places_list := data.get('subject_places', None):
        data['subject_places'] = places_list[0]

    data['created'] = data['created']['value']
    return data
