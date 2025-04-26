from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('add/<int:pk>/', views.add_favorite, name='add_favorite'),
    path('remove/<int:pk>/', views.remove_favorite, name='remove_favorite'),
]
