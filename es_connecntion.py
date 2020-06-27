from elasticsearch_dsl import connections, Search

connections.create_connection(
    alias="default", hosts=["http://127.0.0.1:10200"], timeout=60, http_compress=True
)
