from django.http import HttpResponse

def index(request):
    with open('laba2app/web_client/index.html', 'rb') as indexView:
        return HttpResponse(indexView, content_type='text/html')