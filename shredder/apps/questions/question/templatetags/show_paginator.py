from django import template
import cgi, urllib

register = template.Library()

@register.inclusion_tag('paginator.html', takes_context=True)
def show_paginator(context, pages, adjacent_pages=4):
    """render paginator

       adjacent_pages must >= 3
    """
    if adjacent_pages < 3:
        adjacent_pages = 3

    PAGE_RANGE_DISPLAYED = adjacent_pages * 2 + 1
    total_pages = pages.paginator.num_pages
    current_page = pages.number

    if pages.paginator.num_pages <= PAGE_RANGE_DISPLAYED:
        page_numbers = pages.paginator.page_range
    else:
        page_numbers = [n for n in range(current_page - adjacent_pages, current_page + adjacent_pages + 1) if n > 0 and n <= total_pages]
        if len(page_numbers) < PAGE_RANGE_DISPLAYED:
            if page_numbers[0] == 1:
                page_numbers.extend(range(page_numbers[-1]+1, page_numbers[-1] + 1 + PAGE_RANGE_DISPLAYED - len(page_numbers)))
            elif page_numbers[-1] == total_pages:
                page_numbers = range(page_numbers[0] - (PAGE_RANGE_DISPLAYED - len(page_numbers)), page_numbers[0]) + page_numbers
            else:
                pass

        if page_numbers[0] != 1:
            page_numbers[0] = 1
            page_numbers[1] = 0
        if page_numbers[-1] != total_pages:
            page_numbers[-2] = 0
            page_numbers[-1] = total_pages

    # https://bugzilla.redhat.com/show_bug.cgi?id=851054
    # preserve query string while pagination.
    # idea from http://djangosnippets.org/snippets/1139/
    path = context.get("paginator_path_override", context["request"].path)
    qs = context["request"].META.get("QUERY_STRING")
    if not qs:
        qs = ""
    # strip out blank values from query string
    query_dict = dict(cgi.parse_qsl(qs))
    # query_dict = dict(cgi.parse_qsl(qs, keep_blank_values=True))
    if "page" in query_dict: del query_dict["page"]
    qs = urllib.urlencode(query_dict)
    if qs:
        path = "%s?%s&" % (path, qs)
    else:
        path = "%s?" % path

    return {
        'page_numbers': page_numbers,
        'current_page': current_page,
        'pages': pages,
        'path': path,
    }
