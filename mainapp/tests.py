import datetime

from django.forms import CharField
from django.test import TestCase
from django.test.client import Client

from mainapp.forms import ContactForm
from mainapp.models import Masters, Services, Portfolio, ActionsNews, Contacts, Time


class MainappTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Services.objects.create(service_name='стрижка мужская', service_description='Lorem Ipsum', price=2000,
                                               discount=20, img_1='test.img')
        self.master = Masters.objects.create(name='Ivanova', greeting='lorem ipsum sit amen', master_specialization='lorem',
                                        is_active=True)
        ActionsNews.objects.create(title='news title', description='text of news')
        Portfolio.objects.create(service_id=self.service, img_1='test.img')
        self.client_time = Time.objects.create(time='10:00')
        Contacts.objects.create(client_name="Семен", phone_number='8914700533', date_field=str(datetime.date.today()),
                                time_field=self.client_time, masters_choice=self.master, service_choice=self.service)

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_valid_form(self):
        form_data = {
            'client_name': 'Иван',
            'phone_number': '89147000011',
            'masters_choice': self.master.name,
            'service_choice': self.service.service_name,
            'date_field': datetime.date.today() + datetime.timedelta(days=1),
            'time_field': self.client_time.time
        }
        response = self.client.post('/contacts/', form_data)
        self.assertEqual(response.status_code, 200)


