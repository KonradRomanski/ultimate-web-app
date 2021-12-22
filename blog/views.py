from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
    
# def index(request):
    # return render("{% static 'index.html' %}" )

def my_view(request):
    return render(request, 'index.html', {'foo': 'bar'}, content_type='application/xhtml+xml')