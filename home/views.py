from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render


# For now just a basic redirect to the API discovery
def index(request):
    return HttpResponseRedirect(reverse('wanna-see-it'))
