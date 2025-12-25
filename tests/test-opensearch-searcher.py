from opensearchpy import OpenSearch

# Simple HTTP connection (No SSL, No Auth)
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,
    use_ssl=False,     
    verify_certs=False,
    http_auth=None      
)

try:
    # Check connection
    info = client.info()
    print(f"SUCCESS! Connected to OpenSearch {info['version']['number']}")
    print(f"Node Name: {info['name']}")

    #search it
    search_body = {"query": {"match": {"text": "final" }}}
    search = client.search(index='my_index', body=search_body)
    print(search)

except Exception as e:
    print(f"Error: {e}")