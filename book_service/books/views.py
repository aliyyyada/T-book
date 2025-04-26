from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm
from .scrapers import searchWiki, searchOpenlibrary
from .models import Book
import django

def index(request):
    form = SearchForm(request.GET or None)
    books = []
    if form.is_valid():
        q = form.cleaned_data['query']
        raw = searchWiki(q) + searchOpenlibrary(q)

        for item in raw:
            book, created = Book.objects.get_or_create(
                external_id = item['external_id'],
                defaults={
                    'title': item.get('title', ''),
                    'author': item.get('author', ''),
                    'year': item.get('year'),
                    'genre': item.get('genre', ''),
                    'summary': item.get('summary', ''),
                }
            )
            books.append(book)

    fav_ids = request.session.get('favorites', [])
    context = {
        'form': form,
        'books': books,
        'favorites': fav_ids,
    }

    return render(request, 'books/index.html', context)

def add_favorite(request, pk):
    fav = request.session.get('favorites', [])
    if pk not in fav:
        fav.append(pk)
        request.session['favorites']=fav
    return redirect('books:index')

def remove_favorite(request, pk):
    fav = request.session.get('favorites', [])
    if pk in fav:
        fav.remove(pk)
        request.session['favorites'] = fav
    return redirect('books:favorites')

def favorites(request):
    fav = request.session.get('favorites', [])
    books = Book.objects.filter(pk__in=fav)
    return render(request, 'books/favorites.html', {'books': books})
