#%%
from elasticsearch import Elasticsearch
from datetime import datetime
from elasticsearch_dsl import (
    Document,
    Date,
    Nested,
    Boolean,
    analyzer,
    InnerDoc,
    Completion,
    Keyword,
    Text,
    DenseVector,
    Keyword,
    Long,
    Join,
)

import gzip
from pathlib import Path
from elasticsearch.helpers import bulk

from elasticsearch_dsl import Search
from elasticsearch_dsl import Q, SF, A

import re
import json

from rich import print
from repository import Corpus, Sentence, Page


#%%
def query_ngram(
    ngram=None, index=["now"], case=False, page_from=0, page_to=10, fields=None
):
    index = ",".join(index)
    if case:
        q = Q("match_phrase", token={"query": ngram})
    else:
        q = Q("match_phrase", token_insensitive={"query": ngram})

    rand_q = Q("function_score", functions=[SF("random_score")])
    b = Sentence().search(index=index).query(q & rand_q)
    b = b.source(fields)

    res = b[page_from:page_to].execute()
    res = res.to_dict()["hits"]["hits"]

    return res


#%%
def query_document(id_=None, index="now", fields=None):
    # index = ",".join(index)
    page = Page().get(id_, index=index)
    # sentence = Sentence().get(child_id, index=index)
    # page = Page().get(sentence.meta.routing, index=index)
    q = Q("has_parent", parent_type="page", query={"ids": {"values": [id_]}},)

    res = Sentence.search(index="now").query(q).sort("location")
    res = res.source(fields)

    return_value = {}
    return_value["title"] = page.to_dict(True)
    return_value["content"] = list(map(lambda x: x.to_dict(True), res.scan()))
    # for i in res.scan():
    #     return_value["content"].append(i.to_dict(True))

    print(len(return_value["content"]))
    return return_value


# %%
