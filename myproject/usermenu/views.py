import os
import json
from django.shortcuts import render, HttpResponse, Http404


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def categories(request):
    # Path to the categories.json file
    json_file_path = os.path.join(BASE_DIR, 'mock-data', 'categories.json')
    
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        categories_data = json.load(file)
    
    # Pass the categories data to the template
    return render(request, 'usermenu/categories.html', {'categories': categories_data})

def content(request, category):
    json_file_path = os.path.join(BASE_DIR, 'mock-data/content', f'{category}.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        categories_data = json.load(file)

    return render(request, 'usermenu/content.html', {'rows': categories_data})

def modal_content(request, product_id):
    try:
        category_id, prod_id = product_id.split('-')
        loading_categories = os.path.join(BASE_DIR, 'mock-data', 'categories.json')
        with open(loading_categories, 'r', encoding='utf-8') as file:
            categories_data = json.load(file)

        category_filter = next((item for item in categories_data if str(item['id']) == category_id), None)
        
        if not category_filter:
            raise Http404("Category not found")
        
        category_content_path = os.path.join(BASE_DIR, 'mock-data/content', f'{category_filter["endpoint"]}.json')
        with open(category_content_path, 'r', encoding='utf-8') as content_file:
            category_content = json.load(content_file)
        product_filter = next((item for item in category_content if str(item['id']) == prod_id), None)
        if not product_filter:
            raise Http404("Product not found")
        return render(request, 'usermenu/modal_content.html', {'product': product_filter})

    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        raise Http404("Invalid product or category")