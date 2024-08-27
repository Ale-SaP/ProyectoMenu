import os
import json
from django.shortcuts import render


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
