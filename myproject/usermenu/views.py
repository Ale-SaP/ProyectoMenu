import os
import json
from django.shortcuts import render, HttpResponse, Http404


from usermenu.models import Product, OrgConfigs, Category

def categories(request):
    categories = Category.objects.all()
    return render(request, 'usermenu/categories.html', {'categories': categories})

def content(request, category):
    products = Product.objects.filter(productcategory__id_category=category)

    return render(request, 'usermenu/content.html', {'rows': products})

def modal_content(request, product_id):
    try:
        category_id, prod_id = product_id.split('-')
        
        getProduct = Product.objects.get(product_id = prod_id)
        
        if not getProduct:
            raise Http404("Category not found")
        
        return render(request, 'usermenu/modal_content.html', {'product': getProduct})

    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        raise Http404("Invalid product or category")