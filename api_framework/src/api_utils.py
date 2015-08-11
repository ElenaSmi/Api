__author__ = 'Elena'
from ConfigParser import SafeConfigParser
import os
import requests
import json
import time
import sys

class Config:
    def __init__(self):
        self.parser = SafeConfigParser()
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            print('No config.ini found under root folder.')
            sys.exit()
        self.domain = self.parser.get('Server', 'domain')
        self.admin_login = self.parser.get('Server', 'admin')
        self.password = self.parser.get('Server', 'password')
        self.test_path = self.parser.get('Server', 'testpath')
        self.puser = self.parser.get('Server', 'puser')


class Response:#response always has header and status code
    def __init__(self):
        self.http_code = 0
        self.json = dict()
        self.headers = dict()


class Calls:
    def __init__(self):
        self.config = Config()
        self.no_json = 'NoJson'

    def create_folder(self, name, domain=None, username=None,password=None, content_type=None,
                  accept=None, method=None, test_path=None):

        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method ='Post'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/fs/'
        url = domain + endpoint + test_path + name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept

        data = dict()
        data['action'] = 'add_folder'

        data = json.dumps(data)# translates from dict to json; loads translate from json to dict

        r = requests.request(
            url = url,
            auth = (username, password),
            headers = headers,
            data = data,
            method = method)

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'Options':
                json_resp = r.content
            else:
                json_resp = self.no_json

        r.json = json_resp
        response = Response()
        response.http_code = r.status_code
        response.json = r.json
        response.headers = r.headers
        return response

    def delete_folder(self, name, domain=None, username=None,password=None, content_type=None,
                  accept=None, method=None, test_path=None):

        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method ='Delete'
        if content_type is None:
            content_type = 'application/json'
        if accept is None:
            accept = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/fs/'
        url = domain + endpoint + test_path + name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept

        r = requests.request(
            url = url,
            auth = (username, password),
            headers = headers,
            method = method
        )

        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'Options':
                json_resp = r.content
            else:
                json_resp = self.no_json

        r.json = json_resp
        response = Response()
        response.http_code = r.status_code
        response.json = r.json
        response.headers = r.headers
        return response

    def set_perms(self, name, permission, user, domain=None, username=None, password=None,
                  content_type=None, accept=None, method=None, test_path=None):
        '''
        curl -u<username>:<password> -H "Content-Type: application/json" "https://istepanko25.qa-egnyte.com/public-api
        /v1/perms/folder/Shared/smoke_test/dynamic_name_143906369545/testname4853666" -d '{"users": ["atest"],
         "permission": "Viewer"}' -X POST

        '''
        if domain is None:
            domain = self.config.domain
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if accept is None:
            accept = 'application/json'
        if content_type is None:
            content_type = 'application/json'
        if test_path is None:
            test_path = self.config.test_path

        endpoint = '/public-api/v1/perms/folder'
        url = domain + endpoint + test_path + name
        headers = dict()
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        data = dict()
        data['permission'] = permission
        data['users'] = list()
        data['users'].append(user)
        data = json.dumps(data)
        # Request method returning server response to r
        r = requests.request(
            url=url,
            auth=(username, password),
            headers=headers,
            data=data,
            method=method
        )

        # Fist: Trying to parse json and convert it to Pythonic dict.
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            # If parsing failed then check, maybe method was 'OPTIONS'
            if method == 'OPTIONS':
                json_resp = r.content
            # And finally return no_json string to json_resp variable
            else:
                json_resp = self.no_json
        # Putting processed r.content into r.json
        r.json = json_resp
        # Creating object of class Response()
        response = Response()
        response.http_code = r.status_code
        response.body = r.json
        response.headers = r.headers
        print('\n' + str(response.http_code))
        return response

    @staticmethod
    def gen_random_name():
        return 'dynamic_name_%s' % str(time.time()).replace('.', '')
