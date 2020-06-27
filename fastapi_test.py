<<<<<<< HEAD
import os, json
=======

import os ,json
>>>>>>> d113409810a9634d308c8867bcb3c9861c4d389d

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

<<<<<<< HEAD
from repository import Corpus, Sentence, Page
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections

app = FastAPI()

MAPPING = {
    "udn": "udn_old_sentence",
    "cna": "cna_old_sentence",
    "coca": "coca_sentence",
    "now": "now",
}


class pipline_dict(BaseModel):
    parser: str
    Tok: int
=======

app = FastAPI()

class pipline_dict(BaseModel):
    Tok: int 
>>>>>>> d113409810a9634d308c8867bcb3c9861c4d389d
    Pos: int
    Tag: int
    Ner: int
    Dep: int

<<<<<<< HEAD

class sentence_dict(BaseModel):
    origin: str


class content_list(BaseModel):
    sentence: sentence_dict


class input_json(BaseModel):
    id: str
    title: str = "This is input"
    content: List[content_list]
    pipline: pipline_dict
    metadata: dict = {}


def save_document(datas):

    # try:
    #     with open(datas) as f:
    #         datas = json.load(f)
    # except:
    #     return None

    inserts_data = []
    data = datas
    page = Page(title=data["title"], corpus_id=data["id"], metadata=data["metadata"],)
    page.page_sentence = {"name": "page"}
    page.meta.index = data["metadata"]["index"]
    page.meta.id = data["id"]

    # print(page.to_dict(True))

    # %%
    # res = bulk(connections.get_connection(), [page.to_dict(True)])
    inserts_data.append(page.to_dict(True))
    # %%
    sentences = []
    # for idx, (origin, parsed) in enumerate(zip(data["origin"], data["content"])):
    for idx, c in enumerate(data["content"]):
        c = c["sentence"]
        origin, parsed = c["origin"], c
        #  = item
        sentence = Sentence(
            origin=origin,
            token=" ".join(parsed["Tok"]),
            token_insensitive=" ".join(parsed["Tok"]).lower(),
            tag=" ".join(parsed["Tag"].values()),
            pos=" ".join(parsed["Pos"].values()),
            # lemma=parsed["lemma"],
        )
        sentence.location = idx
        sentence.dependency = parsed["Dep"]
        sentence.name_entity = parsed["Ner"]
        sentence.page_sentence = {"name": "sentence", "parent": data["id"]}
        sentence.meta.index = data["metadata"]["index"]
        sentence.meta.routing = data["id"]
        sentence.meta.id = f'{data["id"]}-{idx}'

        inserts_data.append(sentence.to_dict(True))
        # inserts_data.append(sentence.to_dict(True))

    # for i in inserts_data:
    #     i.save()
    # %%
    #     if len(inserts_data) >= 2000:
    #         res = bulk(connections.get_connection(), inserts_data)
    #         inserts_data = []

    # if len(inserts_data) > 0:
    print(len(inserts_data))
    print(inserts_data)
    res = bulk(connections.get_connection(), inserts_data)
    # inserts_data = []
=======
    
class sentence_dict(BaseModel):
    origin: str

class content_list(BaseModel):
    sentence: sentence_dict
        
class input_json(BaseModel):
  id: int
  title: str = "This is input"
  content: List[content_list]
  pipline: pipline_dict
  metadata: dict={}
>>>>>>> d113409810a9634d308c8867bcb3c9861c4d389d


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/")
async def run(item: input_json):
    paragraph = item.content[0].sentence.origin
<<<<<<< HEAD
    #     pipline = item.pipline.dict()
    with open("./data/input/testing.json", "w") as f:
        json.dump(item.dict(), f)
    #     with open("./data/input/testing.json", 'w') as f:
    #         json.dump(pipline, f)
    #     os.system(
    #         "PYTHONPATH='.' luigi --module start Entry --input-path testing.json --input-pipline {} --input-paragraph {} --local-scheduler".format(
    #             "'" + json.dumps(pipline) + "'", "'" + paragraph + "'"
    #         )
    #     )
    os.system(
        "PYTHONPATH='.' luigi --module start Entry --input-path testing.json --local-scheduler"
    )

    with open("./data/output/testing.json", "r") as f:
        return_json = json.load(f)

    # for i in return_json["content"]:
    # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    save_document(return_json)
    #     return {"hello": "world"}
=======
    pipline = item.pipline.dict()
    
    os.system("PYTHONPATH='.' luigi --module start Entry --input-path testing.json --input-pipline {} --input-paragraph {} --local-scheduler".format('\''+json.dumps(pipline)+'\'', '\''+paragraph+'\''))
    with open('./data/output/testing.json', 'r') as f:
        return_json = json.load(f)
        
>>>>>>> d113409810a9634d308c8867bcb3c9861c4d389d
    return return_json
