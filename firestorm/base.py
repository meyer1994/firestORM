import functools
import itertools
from contextlib import contextmanager

from pydantic import BaseModel
from google.cloud import firestore


class Base(object):

    class Model(BaseModel):
        id: str

    def __init__(self, **kwargs):
        self.data = self.Model(**kwargs)

    @classmethod
    def path(cls, *parents):
        """ Returns the path of this collection """
        paths = ((p.__class__.__name__, p.data.id) for p in parents)
        paths = itertools.chain(*paths)
        paths = itertools.chain(paths, [cls.__name__])
        return '/'.join(paths).lower()

    @classmethod
    def collection(cls):
        """ Utility function to return the collection of this model """
        path = cls.path()
        client = firestore.Client()
        collection = client.collection(path)
        return collection

    def save(self):
        """ Saves model to collection """
        collection = self.collection()
        document = collection.document(self.data.id)
        data = self.data.dict()
        data.pop('id')
        return document.set(data)

    def delete(self):
        """ Deletes model from collection """
        collection = self.collection()
        document = collection.document(self.data.id)
        return document.delete()

    @classmethod
    def where(cls, *args, **kwargs):
        """ Performs where operations """
        collection = cls.collection()
        return collection.where(*args, **kwargs)

    @classmethod
    @contextmanager
    def parents(cls, *parents):
        """ Context manager to use sub collections """
        path = cls.path
        cls.path = functools.partial(path, *parents)
        yield cls
        cls.path = path
