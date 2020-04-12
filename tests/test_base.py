from tests.base import FirestoreTest

from firestorm.base import Base


class Model(Base):
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
        """ Delets data by calling `document.delete` """
        model = Model(id='id', value=0)
        result = model.delete()

        # firestore.Client().collection().document('id')
        mock = self.mock().collection().document
        mock.assert_called_with('id')

        # document.set({'value': 0})
        mock = mock().delete
        mock.assert_called_with()
        self.assertIs(result, mock())
