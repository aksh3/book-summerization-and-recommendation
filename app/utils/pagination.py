def paginate(query, page=1, per_page=10):
    paged = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": paged.items,
        "page": paged.page,
        "per_page": paged.per_page,
        "total": paged.total
    }