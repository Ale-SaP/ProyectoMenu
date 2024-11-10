from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q
from django import forms
from django.utils import timezone
from usermenu.models import Product, Category, PaymentMethod, Client, Order, Detail, Receipt, PaymentStatus
from usermenu.context_processors import cart_items, cart_operations, selected_category
import uuid

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=50,
        required=False
    )

class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500',
            'placeholder': 'Your Name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500',
            'placeholder': 'Your Email',
        })
    )
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500',
        })
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


def modal_content(request, id_product):
    print(request.session.get("cart"))
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

def checkout(request):
    cart_items_call = cart_items(request).get("cart_items", [])
    final_cart_with_data = []
    total = 0

    for item in cart_items_call:
        product = Product.objects.get(id_product=item['product'])
        quantity = item['quantity']
        subtotal = product.price * quantity
        total += subtotal
        final_cart_with_data.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create client
            client = Client.objects.create(
                name=form.cleaned_data['name'],
                creation_date=timezone.now(),
            )

            # Create order
            order = Order.objects.create(
                uuid=uuid.uuid4(),
                order_date=timezone.now().date(),
                creation_date=timezone.now(),
                id_client=client,
            )

            # Create order details
            for item in final_cart_with_data:
                Detail.objects.create(
                    quantity=item['quantity'],
                    creation_date=timezone.now(),
                    id_order=order,
                    id_product=item['product'],
                )

            # Fetch or create the PaymentStatus
            payment_status, created = PaymentStatus.objects.get_or_create(
                status_name='PENDING',
                defaults={'creation_date': timezone.now()}
            )

            # Create receipt
            receipt = Receipt.objects.create(
                uuid=uuid.uuid4(),
                receipt_date=timezone.now().date(),
                creation_date=timezone.now(),
                id_order=order,
                id_payment_method=form.cleaned_data['payment_method'],
                id_payment_status=payment_status,
            )

            # Clear cart and redirect
            request.session['cart'] = []
            return redirect('order_confirmation', order_id=order.id_order)
        else:
            # Return form with errors
            return render(request, 'usermenu/checkout.html', {
                'rows': final_cart_with_data,
                'total': total,
                'form': form,
            })
    else:
        form = CheckoutForm()

    return render(request, 'usermenu/checkout.html', {
        'rows': final_cart_with_data,
        'total': total,
        'form': form,
    })

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id_order=order_id)
    order_details = Detail.objects.filter(id_order=order)
    order_items = []
    total = 0
    for detail in order_details:
        product = detail.id_product
        quantity = detail.quantity
        subtotal = product.price * quantity
        total += subtotal
        order_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'usermenu/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'total': total,
    })
