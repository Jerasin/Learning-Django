from django.views.generic import ListView , DetailView
from django.core import paginator
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from django.urls import reverse
from django.http import HttpResponseRedirect
from slugify import slugify
from .forms import BookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
# Create your views here.

def index(request):
    categories = Category.objects.all()
    books = Book.objects.filter(published=True)
    print('categories' , categories)
    categoried_id = request.GET.get('categoryid')
    if categoried_id:
        books = books.filter(category_id=categoried_id)
        

    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'book/index.html', {
        'categories': categories,
        'books': books,
        'categoried_id': categoried_id,
    })


def detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book/detail.html', {
        'book': book,
    })


def book_add(request):
    # form
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.name)
            book.published = True
            book.save()
            form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('book:index', kwargs={}))
        messages.error(request, 'Save Failed')
    return render(request, 'book/add.html', {
        'form': form,
    })


# views เขียนได้ 2 แบบ
# 1.แบบ CBV
# 2.แบบ FBV


class BookListView(ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.filter(published=True)

    def get_context_data(self, *args, **kwargs):
        cd = super(BookListView, self). get_context_data(*args, **kwargs)
        cd.update({
            'categories': Category.objects.all(),
        })

        return cd

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/detail.html'
    slug_url_kwarg = 'slug'


def cart_add(request,slug):
    # query ข้อมูลที่ Model ที่ชื่อ Book โดย where จาก slug
    book = get_object_or_404(Book,slug=slug)
    
    # ดึงค่า seesion จาก key = 'cart_items' ถ้าไม่มีค่าให้ส่งเป็น [] แทน
    cart_items = request.session.get('cart_items') or []
    
    # update item
    duplicated = False
    for item in cart_items:
        if item.get('slug') == book.slug:
            item['qty'] = int(item.get('qty') or '1') + 1
            duplicated = True

    # insert new item
    if not duplicated:
        cart_items.append({
            'id': book.id,
            'slug': book.slug,
            'code': book.code,
            'name': book.name,
            'price': book.price,
            'qty': 1,
        })

    request.session['cart_items'] = cart_items

    # ไปเรียก function cart_list อิ้ง path จาก urls.py
    return HttpResponseRedirect(reverse('book:cart_list', kwargs={}))

def cart_list(request):
    # เอาค่า session มาเก็บไว้ที่ตัวแปร cart_items ถ้าไม่มีค่าให้ใส่เป็น []
    cart_items = request.session.get('cart_items') or []
    total_qty = 0

    # วนลูปบวกจำนวน qty
    for item in cart_items:
        total_qty = total_qty + int(item.get('qty'))

    # สร้าง session cart_qty และเก็บค่า total_qty
    request.session['cart_qty'] = total_qty
    return render(request , 'book/cart.html' , {
        'cart_items': cart_items,
    })

def edit_qty(request):
    reqQty = request.POST.get("qty")
    reqSlug = request.POST.get("slug")
    print(reqQty , reqSlug )
    cart_items = request.session['cart_items'] or []
    for index in range(len(cart_items)):
        print(cart_items[index]['slug'])
        print(reqSlug)
        if cart_items[index]['slug'] == reqSlug:
            print("Test")
            cart_items[index]['qty'] = reqQty
            break
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('book:cart_list' , kwargs={} ))


def cart_delete(request , slug):
    cart_items = request.session.get('cart_items') or []
    for index in range(len(cart_items)):
        if cart_items[index]['slug'] == slug:
            del cart_items[index]
            break
    
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('book:cart_list' , kwargs={} ))


def cart_delete_all(request):
    cart_items = request.session.get('cart_items') or []
    if cart_items:
        del cart_items
    request.session['cart_items'] =  []
    return HttpResponseRedirect(reverse('book:cart_list'))

def cart_checkout(self):
    subject = 'Test Email'
    body = '''
            <p>This is a test mail message</p>
    '''
    email = EmailMessage(subject=subject , body=body , from_email='test@gmail.com' ,to=[''])
    email.content_subtype = 'html'
    email.send()

    return HttpResponseRedirect(reverse('book:index' , kwargs={} ))
