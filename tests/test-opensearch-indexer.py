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

    # Test Indexing
    response = client.index(
        index='my_index',
        body={'text': 'Final working test'},
        id=1,
        refresh=True
    )

    response = client.index(
        index='my_index',
        body={'text': 'Countdown final'},
        id=2,
        refresh=True
    )
    print("Document added successfully:", response['result'])

except Exception as e:
    print(f"Error: {e}")