from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("books/", views.displaybooks, name="displaybooks"),
    path("books/<int:pk>/", views.book_detail, name="book-detail"),
    path("postbook", views.postbook, name="postbook"),

    # Search
    path("search/", views.search, name="search"),

    # Cart
    path("cart/", views.cart_view, name="cart-view"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart-add"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart-remove"),
    path("cart/clear/", views.cart_clear, name="cart-clear"),
]
