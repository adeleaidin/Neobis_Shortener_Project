from django.shortcuts import render, redirect
from .models import Url
from django.http import HttpResponse
from .shortner import shortner

def index(request):
    return render(request, 'base/index.html')



# website validation check
import requests
def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False



from django.http import HttpResponseBadRequest

def create(request):
    if request.method == 'POST':
        link = request.POST.get('link')

        # Check if the URL is valid
        if not is_valid_url(link):
            return HttpResponseBadRequest('Invalid URL')  # Return error response if URL is invalid

        # Check if the URL already exists in the database
        existing_url = Url.objects.filter(link=link).first()
        if existing_url:
            return HttpResponse(existing_url.short_url)

        a = shortner().issue_token()
        new_url = Url(link=link, short_url=a)
        new_url.save()
        return HttpResponse(a)
    return HttpResponseBadRequest('Invalid request method')  # Return error response if method is not POST

def go(request, pk):
    try:
        url_details = Url.objects.get(short_url=pk)
        return redirect(url_details.link)
    except Url.DoesNotExist:
        return HttpResponse('URL not found', status=404)




