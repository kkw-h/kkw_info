from elasticsearch7 import Elasticsearch, exceptions
import hashlib, os

es = Elasticsearch(hosts=os.getenv("ES_HOST"))


def duplicates(name, id):
    try:
        es_id = hashlib.md5(id.encode(encoding='UTF-8')).hexdigest()
        es.get(id=es_id, index=name)
        return True
    except exceptions.NotFoundError:
        return False


def save(name, id, content):
    es_id = hashlib.md5(id.encode(encoding='UTF-8')).hexdigest()
    es.index(index=name, body=content, id=es_id)
    return True
