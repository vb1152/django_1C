from django.test import TestCase, Client
#from django.contrib.auth.models import User
from .models import User

# Create your tests here.
class Desk_app_TestCase(TestCase):
    
    def setUp(self):
        # Create new users
        user = User.objects.create(username="username1")
        user.set_password('1')
        user.save()
        
    # Create your tests here.
    def test_index(self):
        ''' Test for index.html and layout.html'''
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')
        self.assertTemplateUsed('layout.html')

    def test_login(self):
        ''' Test for login rout with username and password'''
        c = Client()
        response = c.login(username='username1', password='1')
        self.assertTrue(response)

    def test_IC_rout(self):
        ''' Test for /IC rout'''
        c = Client()
        c.login(username='username1', password='1')
        response = c.get('/IC')
        self.assertEqual(response.status_code, 200)

        

        
