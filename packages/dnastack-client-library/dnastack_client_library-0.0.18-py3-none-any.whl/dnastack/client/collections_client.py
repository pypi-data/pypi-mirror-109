import requests as req


def list_collections(collections_url):
    return req.get(collections_url).json()


def list_tables(collections_url, collection_name):
    collection_tables_url = f"{collections_url}/{collection_name}/data-connect/tables"
    return req.get(collection_tables_url).json()


def query(collections_url, collection_name, query):
    collection_query_url = f"{collections_url}/{collection_name}/data-connect/search"
    return req.post(collection_query_url, json={"query": query}).json()
