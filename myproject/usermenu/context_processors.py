from .models import Product

def selected_category(request):
    return {
        'selected_category': request.session.get('selected_category')
    }

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
