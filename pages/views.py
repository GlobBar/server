from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def police(request):
    template = loader.get_template('pages/privacy_policy.html')
    context = {
        'data': '',
    }
    return HttpResponse(template.render(context, request))

def terms(request):
    template = loader.get_template('pages/terms_and_conditions.html')
    context = {
        'data': '',
    }
    return HttpResponse(template.render(context, request))
