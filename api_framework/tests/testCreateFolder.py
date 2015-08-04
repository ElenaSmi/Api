__author__ = 'Elena'

from api_utils import Calls
from unittest import TestCase
import httplib

class TestClass(TestCase):

    @classmethod
    def setUpClass(cls): #cls - class is class method
        cls.calls = Calls()

    def test_create_folder_positive(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder)
        assert resp.http_code == httplib.CREATED

    def test_create_folder_incorrect_credentials(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder, password='asds')
        assert resp.http_code == httplib.UNAUTHORIZED
        assert resp.json['inputErrors']['credentials'][0]['code'] == 'INVALID_CREDENTIALS'
        assert resp.json['inputErrors']['credentials'][0]['msg'] == 'This request is unauthenticated. Please provide' \
                                                                    ' credentials and try again.'

    def test_delete_folder_positive(self):
        folder = self.calls.gen_random_name()
        self.calls.create_folder(folder)
        resp = self.calls.delete_folder(folder)
        assert resp.http_code == httplib.OK

    def test_create_folder_incorrect_path(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder, test_path='/Share/smoke_test/')
        assert resp.http_code == httplib.CONFLICT
        assert resp.json['errorMessage'] == 'The path /Share/smoke_test/%s is invalid' % folder

    def test_create_dupe_folder(self):
        folder = self.calls.gen_random_name()
        self.calls.create_folder(folder)
        resp = self.calls.create_folder(folder)
        assert resp.http_code == httplib.CONFLICT
        assert resp.json['errorMessage'] == 'Folder already exists at this location'

    def test_create_10_folders_positive(self):
        for i in range(10):
            folder = self.calls.gen_random_name()
            resp = self.calls.create_folder(folder)
            assert resp.http_code == httplib.CREATED

    def test_create_folder_incorrect_username(self):
        folder = self.calls.gen_random_name()
        resp = self.calls.create_folder(folder, username='admi')
        assert resp.http_code == httplib.UNAUTHORIZED
        assert resp.json['inputErrors']['credentials'][0]['code'] == 'INVALID_CREDENTIALS'
        assert resp.json['inputErrors']['credentials'][0]['msg'] == 'This request is unauthenticated. Please provide' \
                                                              ' credentials and try again.'



