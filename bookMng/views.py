from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import MainMenu
from .forms import BookForm, ReviewForm, SearchForm
from django.http import HttpResponseRedirect
from .models import Book
from .forms import RatingForm
from .models import Rating
from django import forms

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.db import models





# Create your views here.
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  })


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  })

def displaybooks(request):
    # annotate each Book with its average rating and rating count
    books = Book.objects.all().annotate(
        avg_rating=Avg('rating__value'),
        rating_count=Count('rating')
    )
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })




class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

def book_detail(request, pk):
    book = get_object_or_404(Book.objects.annotate(
        avg_rating=Avg('rating__value'),
        rating_count=Count('rating')
    ), pk=pk)

    reviews = book.reviews.order_by("-created_at")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('register')
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            r = form.save(commit=False)
            r.book = book
            if request.user.is_authenticated:
                r.reviewer_name = request.user.username
            r.save()
            # Refresh book object to update avg_rating and rating_count
            book = get_object_or_404(Book.objects.annotate(
                avg_rating=Avg('rating__value'),
                rating_count=Count('rating')
            ), pk=pk)
            reviews = book.reviews.order_by("-created_at")
            form = ReviewForm(user=request.user)
            return render(request, "bookMng/book_detail.html", {
                "book": book,
                "reviews": reviews,
                "avg_rating": book.avg_rating,
                "rating_count": book.rating_count,
                "form": form,
                "item_list": []
            })
    else:
        form = ReviewForm(user=request.user)
        if request.user.is_authenticated:
            form.fields['reviewer_name'].widget = forms.HiddenInput()

    return render(request, "bookMng/book_detail.html", {
        "book": book,
        "reviews": reviews,
        "avg_rating": book.avg_rating,
        "rating_count": book.rating_count,
        "form": form,
        "item_list": []
    })

def mybooks(request):
    # If user is not authenticated, don't query or process books — template
    # will show a login prompt. This avoids errors when accessing file URLs.
    if not request.user.is_authenticated:
        return render(request,
                      'bookMng/mybooks.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'books': Book.objects.none()
                      })

    books = Book.objects.filter(username=request.user)
    for b in books:
        # defensive: some Book instances may not have an uploaded file
        try:
            b.pic_path = b.picture.url[14:]
        except Exception:
            b.pic_path = ''

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()

    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  })


def about(request):
    """Simple About Us page."""
    return render(request, 'bookMng/about.html', {
        'item_list': MainMenu.objects.all()
    })


def person_profile(request, slug):
    """Render a simple person profile page based on slug.

    Currently this uses a small in-memory map for content. For a
    production app you would store people in the database.
    """
    people = {
        'hector-corona': {
            'name': 'Hector Corona',
            'title': 'Software Developer',
            'bio': 'Hector is a student at Cal State LA full-time.',
            'photo': 'uploads/penguin6.jpg'
        }
    }
    # Add more people by adding new slug keys here. Example:
    people['kevin-luo'] = {
        'name': 'Kevin Luo',
        'title': 'Data Scientist',
        'bio': 'Kevin enjoys visualizing data and building analytics tools.',
        'photo': 'uploads/penguin5.jpg'
    }
    people['esmeralda-amado'] = {
        'name': 'Esmeralda Amado',
        'title': 'Software Developer',
        'bio': 'Esmeralda is a student and developer working on web applications.',
        'photo': 'uploads/penguin4.jpg'
    }
    people['evelyn-muneton'] = {
        'name': 'Evelyn Muneton',
        'title': 'Software Developer',
        'bio': 'Evelyn likes to develop and code in her spare time.',
        'photo': 'uploads/penguin3.jpg'
    }
    people['raquel-alvarado'] = {
        'name': 'Raquel Alvarado',
        'title': 'Software Developer',
        'bio': 'Raquel has a passion for complex data structures.',
        'photo': 'uploads/penguin2.jpg'
    }
    #people['brian-gonzales'] = {
    #    'name': 'Brian Gonzales',
    #    'title': '???',
    #    'bio': '???',
    #    'photo': 'uploads/brian.jpg'
    #}

    person = people.get(slug)
    if not person:
        # simple 404
        from django.http import Http404
        raise Http404('Person not found')

    return render(request, 'bookMng/person.html', {
        'item_list': MainMenu.objects.all(),
        'person': person
    })

@login_required
def book_rating(request, book_id):
    book = Book.objects.get(id=book_id)
    # Prevent users from rating their own book
    if book.username and book.username == request.user:
        messages.error(request, "You cannot rate your own book.")
        return redirect('displaybooks')
    submitted = False

    # Check if the user has rated this book before
    existing_rating = Rating.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.book = book
            rating.user = request.user
            rating.save()
            # use messages and redirect back to the display page so users see the updated average
            messages.success(request, 'Your rating has been saved.')
            return redirect('displaybooks')
    else:
        form = RatingForm(instance=existing_rating)

    return render(request, 'bookMng/book_rating.html', {
        'book': book,
        'form': form,
        'submitted': submitted,
        'item_list': MainMenu.objects.all()
    })

#-------------------------------------- ADDED -------------------------------------------------------#

# ---------- SHOPPING CART (SESSION-BASED) ----------
def _get_cart(session):
    cart = session.get("cart", {})
    # cart format: {"book_id": quantity}
    return cart

def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True

@require_POST
def cart_add(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart = _get_cart(request.session)
    key = str(book.pk)
    # allow adding multiple copies via POST 'quantity' (defaults to 1)
    try:
        qty = int(request.POST.get('quantity', 1))
    except Exception:
        qty = 1
    if qty < 1:
        qty = 1
    cart[key] = cart.get(key, 0) + qty
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
    total_price = 0
    for b in books:
        qty = cart.get(str(b.id), 0)
        total_items += qty
        subtotal = b.price * qty
        total_price += subtotal
        items.append({"book": b, "qty": qty, "subtotal": subtotal})
    return render(request, "bookMng/cart.html", {
        "items": items, "total_items": total_items, "total_price": total_price, "item_list": []
    })

# ---------- SIMPLE SEARCH ----------
def search(request):
    form = SearchForm(request.GET or None)
    books = []
    query = ""
    if form.is_valid():
        query = form.cleaned_data.get("q", "").strip()
        if query:
            books = Book.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(web__icontains=query)
            ).order_by("name")
    return render(request, "bookMng/search.html", {
        "form": form, "query": query, "books": books, "item_list": []
    })