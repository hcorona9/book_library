from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Book, Favorite
from .forms import BookForm, ReviewForm, SearchForm


# ---------- BASIC LIST/HOME ----------
def index(request):
    books = Book.objects.all().order_by("title")
    return render(request, "displaybooks.html", {"books": books, "item_list": []})


def displaybooks(request):
    books = Book.objects.all().order_by("title")
    return render(request, "displaybooks.html", {"books": books, "item_list": []})


# ---------- CREATE A BOOK ----------
def postbook(request):
    submitted = request.GET.get("submitted") == "True"
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"{reverse('postbook')}?submitted=True")
    else:
        form = BookForm()
    return render(
        request,
        "postbook.html",
        {"form": form, "submitted": submitted, "item_list": []},
    )


# ---------- BOOK DETAIL + COMMENTS (REVIEWS) ----------
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.order_by("-created_at")
    avg = round(sum(r.rating for r in reviews) / len(reviews), 2) if reviews else 0

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.book = book
            r.save()
            return redirect("book-detail", pk=book.pk)
    else:
        form = ReviewForm()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            book=book
        ).exists()

    return render(
        request,
        "book_detail.html",
        {
            "book": book,
            "reviews": reviews,
            "avg": avg,
            "form": form,
            "is_favorite": is_favorite,
            "item_list": [],
        },
    )



# ---------- SIMPLE SEARCH ----------
def search(request):
    form = SearchForm(request.GET or None)
    books = []
    query = ""

    if form.is_valid():
        query = form.cleaned_data.get("q", "").strip()
        if query:
            books = (
                Book.objects.filter(
                    models.Q(title__icontains=query)
                    | models.Q(author__icontains=query)
                    | models.Q(isbn__icontains=query)
                )
                .order_by("title")
            )

    return render(
        request,
        "search.html",
        {"form": form, "query": query, "books": books, "item_list": []},
    )


# ---------- SHOPPING CART (SESSION-BASED) ----------
def _get_cart(session):
    # cart format: {"book_id": quantity}
    return session.get("cart", {})


def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True


@require_POST
def cart_add(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart = _get_cart(request.session)
    key = str(book.pk)
    cart[key] = cart.get(key, 0) + 1
    _save_cart(request.session, cart)
    return redirect("cart-view")


@require_POST
def cart_remove(request, pk):
    cart = _get_cart(request.session)
    key = str(pk)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            cart.pop(key)
        _save_cart(request.session, cart)
    return redirect("cart-view")


def cart_clear(request):
    _save_cart(request.session, {})
    return redirect("cart-view")


def cart_view(request):
    cart = _get_cart(request.session)
    ids = [int(i) for i in cart.keys()]
    books = Book.objects.filter(id__in=ids)
    items = []
    total_items = 0
    for b in books:
        qty = cart.get(str(b.id), 0)
        total_items += qty
        items.append({"book": b, "qty": qty})
    return render(
        request,
        "cart.html",
        {"items": items, "total_items": total_items, "item_list": []},
    )


# ---------- FAVORITES ----------
@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        book=book,
    )

    if not created:
        favorite.delete()

    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url:
        return redirect(next_url)

    return redirect("book_detail", pk=book.id)


@login_required
def favorites_list(request):
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("book")
        .order_by("-created_at")
    )
    return render(
        request,
        "favorites.html",
        {"favorites": favorites, "item_list": []},
    )


# ---------- REGISTRATION ----------
class Register(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("register-success")

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

mybooks = displaybooks
my_books = displaybooks
