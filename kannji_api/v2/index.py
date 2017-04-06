from django.http import HttpResponse


def index(request):
	return HttpResponse("Hello, you are at the Kannji api version 2 index.")
