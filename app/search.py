from flask import current_app

def add_to_index(index, model):
    if not current_app.opensearchpy:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.opensearchpy.index(index=index, body=payload, id=model.id, refresh=True)

def remove_from_index(index, model):
    if not current_app.opensearchpy:
        return
    current_app.opensearchpy.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.opensearchpy:
        return [], 0
    search = current_app.opensearchpy.search(
        index=index,
        body={
            'query': {
                'multi_match': {
                    'query': query, 
                    'fields': ['*']
                }
            }
        },
        from_=(page - 1) * per_page,
        size=per_page)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']