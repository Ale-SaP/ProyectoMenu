import os
import json
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404


from usermenu.models import Product, OrgConfig, Category

def categories(request):
    categories = Category.objects.all()
    return render(request, 'usermenu/categories.html', {'categories': categories})

def content(request, category):
    products = Product.objects.filter(productcategory__id_category=category)

    return render(request, 'usermenu/content.html', {'rows': products})

def modal_content(request, product_id):
    try:
        getProduct = get_object_or_404(Product, id_product=product_id)
        getCategories = Category.objects.filter(productcategory__id_product=product_id)
        getCategoryNames = getCategories.values_list('name', flat=True)

        return render(request, 'usermenu/modal_content.html', {
            'product': getProduct,
            'categories': getCategoryNames
        })
    
    except Product.DoesNotExist:
        raise Http404("Product not found")
    except Category.DoesNotExist:
        raise Http404("Category not found")
    except Exception as e:
        print(f"Error: {e}")
        raise Http404("Invalid product or category")

def shopping_cart(request):
    return render(request, 'usermenu/shopping_cart.html')