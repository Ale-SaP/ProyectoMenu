# context_processors.py

def selected_category(request):
    return {
        'selected_category': request.session.get('selected_category')
    }
