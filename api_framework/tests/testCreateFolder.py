__author__ = 'Elena'

from api_utils import Calls
from api_utils import Config
from unittest import TestCase
import httplib



class TestClass(TestCase):

    @classmethod
    def setUpClass(cls): #cls - class is class method
        cls.calls = Calls()
        cls.config = Config()

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

    def test_delete_folder_wrong_accept_name(self):
        folder_name = self.calls.gen_random_name()
        resp = self.calls.delete_folder(folder_name, accept= 'application/xml')
        assert resp.http_code == httplib.NOT_ACCEPTABLE

    def test_create_and_delete_100_folders(self):
        folder_name = self.calls.gen_random_name()
        for i in range(100):
            resp = self.calls.create_folder(folder_name + str(i))
            assert resp.http_code == httplib.CREATED
        for i in range(100):
            resp = self.calls.delete_folder(folder_name + str(i))
            assert resp.http_code == httplib.OK


    def test_perms_full(self):
        #Create folder with Full permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Full')
        assert resp.http_code == httplib.OK
        resp = self.calls.create_folder(folder_name, username=self.config.puser, test_path='%s/%s/' %
                                                                                (self.config.test_path, folder_name))
        assert resp.http_code == httplib.CREATED

    def test_perms_viewer(self):
        #Create folder with Viewer permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Viewer')
        assert resp.http_code == httplib.OK
        resp = self.calls.create_folder(folder_name, username=self.config.puser, test_path='%s/%s/' %
                                                                                (self.config.test_path, folder_name))
        assert resp.http_code == httplib.FORBIDDEN

    def test_perms_editor(self):
        #Create folder with Editor permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Editor')
        assert resp.http_code == httplib.OK
        resp = self.calls.create_folder(folder_name, username=self.config.puser, test_path='%s/%s/' %
                                                                                (self.config.test_path, folder_name))
        assert resp.http_code == httplib.CREATED

    def test_perms_none(self):
        #Create folder with None permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='None')
        assert resp.http_code == httplib.OK
        resp = self.calls.create_folder(folder_name, username=self.config.puser, test_path='%s/%s/' %
                                                                                (self.config.test_path, folder_name))
        assert resp.http_code == httplib.FORBIDDEN

    def test_perms_owner(self):
        #Create folder with Owner permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Owner')
        assert resp.http_code == httplib.OK
        resp = self.calls.create_folder(folder_name, username=self.config.puser, test_path='%s/%s/' %
                                                                                (self.config.test_path, folder_name))
        assert resp.http_code == httplib.CREATED

    def test_delete_folder_none(self):
        #Delete folder None permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='None')
        assert resp.http_code == httplib.OK
        resp = self.calls.delete_folder(folder_name, username=self.config.puser)
        assert resp.http_code == httplib.FORBIDDEN

    def test_delete_folder_full(self):
        #Delete folder Full permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Full')
        assert resp.http_code == httplib.OK
        resp = self.calls.delete_folder(folder_name, username=self.config.puser)
        assert resp.http_code == httplib.OK

    def test_delete_folder_viewer(self):
        #Delete folder Viewer permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Viewer')
        assert resp.http_code == httplib.OK
        resp = self.calls.delete_folder(folder_name, username=self.config.puser)
        assert resp.http_code == httplib.FORBIDDEN

    def test_delete_folder_editor(self):
        #Delete folder Editor permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Editor')
        assert resp.http_code == httplib.OK
        resp = self.calls.delete_folder(folder_name, username=self.config.puser)
        assert resp.http_code == httplib.FORBIDDEN

    def test_delete_folder_owner(self):
        #Delete folder Owner permissions
        folder_name = self.calls.gen_random_name()
        self.calls.create_folder(folder_name)
        resp = self.calls.set_perms(folder_name, user=self.config.puser, permission='Owner')
        assert resp.http_code == httplib.OK
        resp = self.calls.delete_folder(folder_name, username=self.config.puser)
        assert resp.http_code == httplib.OK