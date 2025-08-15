from django.core.paginator import Paginator, EmptyPage
from django.http import Http404

import math

def make_pagination_range(page_range, qty_pages, current_page):
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)
    start_range_offset = 0

    if start_range < 0:
        start_range_offset = abs(start_range)
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': start_range > 0,
        'last_page_out_of_range': stop_range < total_pages,
    }

def make_pagination(request, quetyset, per_page, qty_pages=4):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(quetyset, per_page)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        raise Http404()

    pagination = make_pagination_range(
        paginator.page_range,
        qty_pages,
        page_number
    )

    return page_obj, pagination