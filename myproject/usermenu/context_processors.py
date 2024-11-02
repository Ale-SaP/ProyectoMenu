from .models import Product

def selected_category(request):
    return {
        'selected_category': request.session.get('selected_category')
    }

from .models import Product
from django.shortcuts import get_object_or_404

def cart_items(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for id_product, quantity in cart.items():
        try:
            product = Product.objects.get(id_product=id_product)
            cart_items.append({
                'product': product,
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            continue
    return {
        'cart_items': cart_items,
    }

def cart_operations(request):
    """
    Context processor to handle cart operations such as adding products to the cart.
    """
    def add_to_cart(id_product, quantity=1):
        cart = request.session.get('cart', {})
        
        if str(id_product) in cart:
            cart[str(id_product)] += quantity
        else:
            cart[str(id_product)] = quantity

        # Save the updated cart to the session and mark it as modified
        request.session['cart'] = cart
        request.session.modified = True

    def remove_from_cart(id_product):
        cart = request.session.get('cart', {})
        
        if str(id_product) in cart:
            del cart[str(id_product)]
            request.session['cart'] = cart
            request.session.modified = True

    return {
        'add_to_cart': add_to_cart,
        'remove_from_cart': remove_from_cart,
    }
