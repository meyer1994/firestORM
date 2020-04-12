from pydantic import BaseModel
from google.cloud import firestore


class Base(BaseModel):
    id: str

    def collection(self):
        """ Utility function to return the collection of this model """
        cls = self.__class__.__name__.lower()
        client = firestore.Client()
        collection = client.collection(cls)
        return collection

    def save(self):
        """ Saves model to collection """
        collection = self.collection()
        document = collection.document(self.id)
        data = self.dict()
        data.pop('id')
        return document.set(data)

    def delete(self):
        """ Deletes model from collection """
        collection = self.collection()
        document = collection.document(self.id)
        return document.delete()
