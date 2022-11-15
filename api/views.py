from django.http import HttpResponse

def consume_file(request):
    if request.method == 'POST':
        print(request.FILES['file'])
        return HttpResponse(request.FILES['file'].name)