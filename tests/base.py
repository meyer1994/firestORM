from unittest import TestCase, mock


class Object(object):
    pass


class FirestoreTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """ Starts mocks for `firestore.Client` """
        super(FirestoreTest, cls).setUpClass()
        patcher = mock.patch('google.cloud.firestore.Client')
        cls.mock = patcher.start()

    @classmethod
    def tearDownClass(cls):
        """ Stops mocks for `firestore.Client` """
        super(FirestoreTest, cls).tearDownClass()
        cls.mock.stop()
