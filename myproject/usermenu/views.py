from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django import forms

from usermenu.models import Product, OrgConfig, Category
from usermenu.context_processors import cart_items, cart_operations, selected_category

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=50,
        required=False
    )

def categories(request):
    categories = Category.objects.all()
    return render(request, 'usermenu/categories.html', {
        'categories': categories,
        'selected_category': selected_category(request).get("get_category")()["selected_category"]
    })


def content(request, category_id=None):
    update_selected_category = selected_category(request).get("replace_category")
    if category_id:
        # Store the selected category in the session
        update_selected_category(category_id)
        
    category_id = selected_category(request).get("get_category")()["selected_category"]
    category = get_object_or_404(Category, id_category=category_id)
    products = Product.objects.filter(productcategory__id_category=category.id_category)

    return render(request, 'usermenu/content.html', {
        'rows': products,
        'category': category
    }) 

from django.shortcuts import render, get_object_or_404
from django.http import Http404

def modal_content(request, id_product):
    try:
        
        id_product = int(id_product)
        getProduct = get_object_or_404(Product, id_product=id_product)

        getCategories = Category.objects.filter(productcategory__id_product=id_product)
        getCategoryNames = getCategories.values_list('name', flat=True)
        
        cart_items_call = cart_items(request).get("cart_items", [])
        already_added_quantity = next(
            (item["quantity"] for item in cart_items_call if item["product"] == id_product),
            1
        )
        return render(request, 'usermenu/modal_content.html', {
            'product': getProduct,
            'categories': getCategoryNames,
            'already_added_quantity': already_added_quantity
        })
    except Exception as e:
        print(f"Error: {e}")
        raise Http404("Invalid product or category")


def shopping_cart(request):
    cart_items_call = cart_items(request).get("cart_items")
    final_cart_with_data = []
    total = 0

    for item in cart_items_call:
        product = Product.objects.get(id_product=item['product'])
        quantity = item['quantity']
        subtotal = product.price * quantity
        total += subtotal
        final_cart_with_data.append({
            'product': product.__dict__,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'usermenu/shopping_cart.html', {
        'rows': final_cart_with_data,
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
    Adds a product to the shopping cart using the cart_operations context processor.
    """
    quantity = int(request.POST.get('unit_numbers', 1))
    if (quantity > 100):
        return HttpResponse(status=200)
    if (quantity == 0):
        return redirect('remove_from_cart', id_product=id_product)
    operations = cart_operations(request)
    operations = operations.get("add_to_cart")
    operations(id_product, quantity)
    
    return redirect("shopping_cart")

def remove_from_cart(request, id_product):
    """
    Remove a product from the shopping cart.
    """
    operations = cart_operations(request)
    operations = operations.get("remove_from_cart")
    operations(id_product)
    return redirect("shopping_cart")