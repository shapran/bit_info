from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class IndexPageTests(TestCase):

    def setUp(self):
        # Create user
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
            
    def test_home_status_code_redirect(self):
        # Check redirection from homepage
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302, 'Should return status_code 302.'
                         ' Instead returned {}'.format(response.status_code))
 
    def test_client_exist(self):
        # Check status_code for registered user 
        c = Client()
        c.login(username='testuser', password='12345')        
        
        response = c.get('/' )
        self.assertEqual(response.status_code, 200, 'Should return status_code 200.'
                         ' Instead returned {}'.format(response.status_code))

