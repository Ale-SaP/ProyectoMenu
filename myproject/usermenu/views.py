from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from django.db.models import Q
from django import forms

from usermenu.models import Product, OrgConfig, Category

class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False
    )

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
            products = Product.objects.none()
    else:
        products = Product.objects.none()
        query = ''
    return render(request, 'usermenu/content.html', {
        'rows': products,
        'query': query,
    })
