from django.core.paginator import Paginator


def get_paging_from_request(request):
	return request.GET.get('paging', "")


def get_page_index_from_request(request):
	paging = get_paging_from_request(request)
	return paging.split(':')[0]


def get_page_size_from_request(request):
	paging = get_paging_from_request(request)
	return paging.split(':')[1]


def get_paginator(query_set, request):
	# get the page size
	page_size = get_page_size_from_request(request)
	
	# prepare the paginator
	return Paginator(query_set, page_size)
