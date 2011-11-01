"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.db.utils import IntegrityError

from django.test import TestCase
from django.test.client import Client
from authz.models import Authorizer
from models import Resource

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class AuthzTest(TestCase):
    fixtures = ['test.json']
    def test_get(self):
        c = Client()
        response = c.get('/authorize/')
        self.assertEqual(response.status_code, 405)
    def test_bogus(self):
        c = Client()
        response = c.get('/bogus/')
        self.assertEqual(response.status_code, 404)
    def test_empty_post(self):
        c = Client()
        response = c.post('/authorize/')
        self.assertEqual(response.status_code, 404)
    def test_post(self):
        c = Client()
        params = {'subject':'user','nonce':'nonce','content':'resource1','signature':'signature'}
        response = c.post('/authorize/', params)
        self.assertEqual(response.status_code, 200)
    def test_post_minus(self):
        c = Client()
        params = {'subject':'subject','nonce':'nonce','content':'content'}
        response = c.post('/authorize/', params)
        self.assertEqual(response.status_code, 404)
    def test_post_authz(self):
        c = Client()
        params = {'subject':'bogus','nonce':'nonce','content':'resource1','signature':'signature'}
        response = c.post('/authorize/', params)
        self.assertEqual(response.status_code, 403)
    def test_duplicate_resource(self):
        r = Resource()
        r.name = 'resource1'
        with self.assertRaises(IntegrityError) as e:
            print "Testing for exception..."
            r.save()
    def test_duplicate_authz(self):
        a = Authorizer()
        a.name = 'user'
        with self.assertRaises(IntegrityError) as e:
            print "Testing for exception..."
            a.save()
    def test_upload(self):
        c = Client()
        f = open('upload.txt')
        params = {'subject':'bogus','file':f}
        response = c.post('/upload/',params)
        self.assertEqual(response.status_code, 200)
    def test_post_register_new(self):
        c = Client()
        params = {'subject':'newUser','cert':'This is my cert data'}
        response = c.post('/register/', params)
        self.assertEqual(response.status_code, 200)
    def test_post_register_duplicate(self):
        c = Client()
        params = {'subject':'user','cert':'This is my cert data'}
        response = c.post('/register/', params)
        self.assertEqual(response.status_code, 403)
