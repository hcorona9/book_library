# bookMng/admin.py
from django.contrib import admin
from .models import Book, Review, Message

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "isbn")
    search_fields = ("title", "author", "isbn")
    ordering = ("title",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "reviewer_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("reviewer_name", "book__title")
    ordering = ("-created_at",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    search_fields = ("name", "email")
    ordering = ("-created_at",)
