from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django import forms

from usermenu.models import Product, OrgConfig, Category

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=50,
        required=False
    )

def categories(request):
    categories = Category.objects.all()
    return render(request, 'usermenu/categories.html', {
        'categories': categories
    })


def content(request, category_id=None):
    if category_id:
        # Store the selected category in the session
        request.session['selected_category'] = category_id
    else:
        # Try to get the category from the session
        category_id = request.session.get('selected_category')

    if category_id:
        # Use the category from the session or parameter
        category = get_object_or_404(Category, id_category=category_id)
    else:
        # Use the default category from OrgConfig
        default_config = get_object_or_404(OrgConfig, id_organization=1)
        if default_config.default_category:
            category = default_config.default_category
            category_id = category.id_category
            request.session['selected_category'] = category_id
        else:
            raise Http404("Default category not set in OrgConfig.")

    # Retrieve products based on the category
    products = Product.objects.filter(productcategory__id_category=category.id_category)

    return render(request, 'usermenu/content.html', {
        'rows': products,
        'category': category
    })

def modal_content(request, id_product):
    try:
        getProduct = get_object_or_404(Product, id_product=id_product)
        getCategories = Category.objects.filter(productcategory__id_product=id_product)
        getCategoryNames = getCategories.values_list('name', flat=True)

        return render(request, 'usermenu/modal_content.html', {
            'product': getProduct,
            'categories': getCategoryNames
        })

    except Exception as e:
        print(f"Error: {e}")
        raise Http404("Invalid product or category")

def shopping_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for id_product, quantity in cart.items():
        product = get_object_or_404(Product, id_product=id_product)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'usermenu/shopping_cart.html', {
        'rows': cart_items,
        'subtotal': total,
    })

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['q']
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(productcategory__id_category__name__icontains=query)
            ).distinct()
        else:
            return content(request)
    else:
        products = Product.objects.none()
        query = ''
    return render(request, 'usermenu/content.html', {
        'rows': products,
        'query': query,
    })

def add_to_cart(request, id_product):
    """
    Add a specified quantity of a product to the shopping cart.
    """
    product = get_object_or_404(Product, id_product=id_product)
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('unit_numbers', 1))
    if id_product in cart:
        cart[str(id_product)] += quantity
    else:
        cart[str(id_product)] = quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(shopping_cart)

def view_cart(request):
    """
    Display the contents of the shopping cart.
    """


def remove_from_cart(request, id_product):
    """
    Remove a product from the shopping cart.
    """
    cart = request.session.get('cart', {})
    
    if id_product in cart:
        del cart[id_product]
        request.session['cart'] = cart