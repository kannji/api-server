# protected content, can only be accessed when logged in
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse


@login_required()
def user_profile(request, *args, **kwargs):
	return JsonResponse(get_user_object(request.user))


def get_user_object(user):
	
	userJson = {}
	
	# getting user information
	userJson['user_id'] = user.id
	userJson['full_name'] = user.get_full_name()
	userJson['email'] = user.email
	
	return userJson
