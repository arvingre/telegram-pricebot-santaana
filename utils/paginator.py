def paginate_products(records, page, page_size=5):
    start = (page - 1) * page_size
    end = start + page_size
    return records[start:end]
