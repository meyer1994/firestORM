from pydantic import BaseModel

from tests.base import FirestoreTest

from firestorm.base import Base


class Model(Base):
    class Model(BaseModel):
        id: str
        value: int


class Child(Base):
    class Model(BaseModel):
        id: str
        value: int


class TestBase(FirestoreTest):
    def test_collection(self):
        """ Gets the collection by calling `client.collection` """
        model = Model(id='id', value=0)
        result = model.collection()

        # firestore.Client()
        self.mock.assert_called_with()

        # client.collection('model')
        mock = self.mock().collection
        mock.assert_called_with('model')
        self.assertIs(result, mock())

    def test_save(self):
        """ Saves the data by calling `document.set` """
        model = Model(id='id', value=0)
        result = model.save()

        # firestore.Client().collection().document('id')
        mock = self.mock().collection().document
        mock.assert_called_with('id')

        # document.set({'value': 0})
        mock = mock().set
        mock.assert_called_with({'value': 0})
        self.assertIs(result, mock())

    def test_delete(self):
        """ Deletes data by calling `document.delete` """
        model = Model(id='id', value=0)
        result = model.delete()

        # firestore.Client().collection().document('id')
        mock = self.mock().collection().document
        mock.assert_called_with('id')

        # document.delete({'value': 0})
        mock = mock().delete
        mock.assert_called_with()
        self.assertIs(result, mock())

    def test_path(self):
        """ Returns path for subcollections """
        child = Child(id='id', value=0)
        model = Model(id='id', value=0)

        path = child.path(model)
        self.assertEqual(path, 'model/id/child')

    def test_parents(self):
        """ Tests contextmanager for parents """
        grand = Child(id='1', value=0)
        model = Model(id='2', value=0)
        child = Child(id='3', value=0)

        with Child.parents(grand, model, child):
            c = Child(id='id', value=0)
            path = c.path()

        self.assertEqual(path, 'child/1/model/2/child/3/child')

    def test_subcollection(self):
        """ Performs operations in subcollections """
        child = Child(id='id', value=0)
        model = Model(id='id', value=0)

        with child.parents(model):
            result = child.save()

        # firestore.Client().collection('model/id/child')
        mock = self.mock().collection
        mock.assert_called_with('model/id/child')
        # firestore.Client().collection().document('id')
        mock = mock().document
        mock.assert_called_with('id')

        # document.set({'value': 0})
        mock = mock().set
        mock.assert_called_with({'value': 0})
        self.assertIs(result, mock())

        with child.parents(model):
            result = child.delete()

        # firestore.Client().collection('model/id/child')
        mock = self.mock().collection
        mock.assert_called_with('model/id/child')
        # firestore.Client().collection().document('id')
        mock = mock().document
        mock.assert_called_with('id')

        # document.delete({'value': 0})
        mock = mock().delete
        mock.assert_called_with()
        self.assertIs(result, mock())
