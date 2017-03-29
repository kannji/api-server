from django.core.paginator import Paginator

from kannji_api.v1.general_values import DEFAULT_PAGE_INDEX, DEFAULT_PAGE_SIZE


def get_page_index_from_request(request):
    return request.POST.get('page_number', DEFAULT_PAGE_INDEX)


def get_page_size_from_request(request):
    return request.POST.get('page_size', DEFAULT_PAGE_SIZE)


def get_paginator(query_set, request):

    # get the page size
    page_size = get_page_size_from_request(request)

    # prepare the paginator
    return Paginator(query_set, page_size)
