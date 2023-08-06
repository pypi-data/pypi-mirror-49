from django.urls import path, include
from rest_framework import routers
from . import views

# pg47 Use Underscores in URL Pattern Names Rather Than Dashes
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author_detail'),

]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(),
         name='my_borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(),
         name='all_borrowed'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(),
         name='my_borrowed'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),
]


urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(),
         name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(),
         name='author_delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(),
         name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(),
         name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(),
         name='book_delete'),
]

router = routers.DefaultRouter()
router.register('api/books', views.BookViewSet)
router.register('api/authors', views.AuthorViewSet)

urlpatterns += [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))

]
