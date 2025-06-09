from flask import request

def get_pagination_params(default_page=1, default_per_page=10):
    page= request.args.get('page', default=default_page, type=int)
    per_page = request.args.get('per_page', default=default_per_page, type=int)
    return page, per_page

def format_paginated_result(pagination, schema):
    return{
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "items": schema.dump(pagination.items)
    }