from django.http import HttpResponse

def hello(request):

    a = "hello"

    return HttpResponse("Hello world" + a)
