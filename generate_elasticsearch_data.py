import mimesis
from typing import Dict, List
import uuid
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
#
# doc = {
#     'author': 'pabloc',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.utcnow(),
# }
#
# resp = es.index(index="test-index", id=1, document=doc)
# print(resp['result'])
#
# resp = es.get(index="test-index", id=1)
# print(resp['_source'])
#
# es.indices.refresh(index="test-index")
#
# resp = es.search(index="test-index", query={"match_all": {}})
# print("Got %d Hits:" % resp['hits']['total']['value'])
# for hit in resp['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


def generate_fake_document(count: int = 100) -> List[Dict]:
    from mimesis.enums import Gender
    from mimesis.locales import Locale
    from mimesis.schema import Field, Schema

    _ = Field(locale=Locale.EN)
    schema = Schema(schema=lambda: {
        "pk": _("increment"),
        "uuid": _("uuid"),
        "name": _("text.word"),
        "version": _("version", pre_release=True),
        "timestamp": _("timestamp", posix=False, start=2020, end=2021),
        "owner": {
            "email": _("person.email", key=str.lower),
            "token": _("token_hex"),
            "creator": _("full_name"),
        },
        # "battery": f'\n\t{{level = \"{_("float_number", start=0, end=1, precision=2)}\";\n}}'
        # ,
        "is_new": False

    }).create(iterations=count)
    return schema
    # schema.create(iterations=3)
    # Since v5.6.0 you can do the same thing using multiplication:
    # schema * 3
    # for s in schema.iterator(count):
    #     print(s)
    document = {}


def _insert_to_es(documents: List):
    for doc in documents:
        es.index(index="random_users", document=doc)

    print(f"Done inserting {len(documents)} documents")


if __name__ == '__main__':
    p = generate_fake_document()
    _insert_to_es(p)
