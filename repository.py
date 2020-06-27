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

from elasticsearch_dsl import connections, Search
from elasticsearch_dsl import Q, SF
from es_connecntion import *


class Corpus(Document):
    """
    Base class for Question and Answer containing the common fields.
    """

    corpus_id = Keyword()
    page_sentence = Join(relations={"page": "sentence"})


class Sentence(Corpus):

    origin = Text(analyzer="whitespace")
    token = Text(analyzer="whitespace")
    tag = Text(analyzer="whitespace")
    pos = Text(analyzer="whitespace")
    lemma = Text(analyzer="whitespace")


class Page(Corpus):
    title = Text()
