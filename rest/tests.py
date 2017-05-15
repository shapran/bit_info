from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient
from rest.views import SymbolViewSet
from rest.models import Symbol
import json

class QuestionViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()

        # Create test data in Symbol table
        self.symbol = Symbol.objects.create(name='Test Coin', symbol='TESTCOIN')
        self.symbol.save()

    def tearDown(self):
        self.client.logout()

    def _require_login(self):
        self.client.login(username='testuser', password='testing')

    def test_test_user_authenticated(self):
        self.assertEqual(self.user.is_authenticated(), True,
                         'Expected test user to be authenticated but he is not!')

    def test_SymbolViewSet_not_authenticated(self):
        response = self.client.get('/api/v1/symbols/')
        self.assertEqual(response.status_code, 403,
                         'Expected Response Code 403, received {0} instead.'.format(response.status_code))

    def test_SymbolViewSet_authenticated(self):
        self._require_login()
        response = self.client.get('/api/v1/symbols/')
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_SymbolViewSet_results(self):
        self._require_login()
        response = self.client.get('/api/v1/symbols/')

        content = json.loads(response.content.decode())
        self.assertIn("results", content)

    def test_SymbolViewSet_results_contains(self):
        self._require_login()
        response = self.client.get('/api/v1/symbols/')

        content = json.loads(response.content.decode())
        self.assertIn({'name': 'Test Coin', 'symbol':'TESTCOIN', 'coins': []}, content['results'])