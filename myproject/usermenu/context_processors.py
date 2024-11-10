from .models import Product, OrgConfig

def selected_category(request):
    def get_category_with_fallback():
        category = request.session.get('selected_category')
        
        if (not category):
        # Use the default category from OrgConfig
            default_config = get_object_or_404(OrgConfig, id_organization=1)
            if default_config.contenido_inicial:
                category = default_config.contenido_inicial
                category_id = category
                request.session['selected_category'] = category_id
                
        return {
            'selected_category': category
        }
        
    def replace_category(category_id):
        request.session['selected_category'] = category_id
        request.session.modified = True
    
    return {
        'get_category': get_category_with_fallback,
        'replace_category': replace_category,
    }

from .models import Product
from django.shortcuts import get_object_or_404

def cart_items(request):
    cart = request.session.get('cart', {})
    cart_items_list = []

    # Ensure cart is a dictionary
    if not isinstance(cart, dict):
        cart = {}
        request.session['cart'] = cart

    for id_product, quantity in cart.items():
        try:
            product = Product.objects.get(id_product=id_product)
            cart_items_list.append({
                'product': product.id_product,
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            continue

    return {
        'cart_items': cart_items_list,
    }

def cart_operations(request):
    """
    Context processor to handle cart operations such as adding products to the cart.
    """
    def add_to_cart(id_product, quantity=1):
        cart = request.session.get('cart', {})
        
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
