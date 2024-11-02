from .models import Product

def selected_category(request):
    return {
        'selected_category': request.session.get('selected_category')
    }

def cart_items(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for id_product, quantity in cart.items():
        try:
            product = Product.objects.get(id=id_product)
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            total += subtotal
        except Product.DoesNotExist:
            continue
    return {
        'cart_items': cart_items,
        'cart_total': total,
    }
