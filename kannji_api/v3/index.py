from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

def index(request):
    return HttpResponse("Hello, you are at the Kannji api version 3 index.")

# protected content, can only be accessed when logged in
@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)