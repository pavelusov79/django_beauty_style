import datetime

from django.test import TestCase
from django.test.client import Client

import mainapp.forms
from mainapp.models import Masters, Services, Portfolio, ActionsNews, Contacts, Time


class MainappTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Services.objects.create(service_name='стрижка мужская',
                                               service_description='Lorem Ipsum',
                                               price=2000,
                                               discount=20,
                                               img_1='okras.png',
                                               img_2='okras1.png',
                                               img_3='okras2.png'
                                               )
        self.master = Masters.objects.create(name='Ivanova',
                                             greeting='lorem ipsum sit amen',
                                             master_specialization='lorem',
                                             is_active=True
                                             )
        ActionsNews.objects.create(title='news title', description='text of news')
        Portfolio.objects.create(service_id=self.service, img_1='okras.png', img_2='okras1.png', img_3='okras2.png')
        self.client_time = Time.objects.create(time='10:00')
        Contacts.objects.create(client_name="Семен",
                                phone_number='8914700533',
                                date_field=str(datetime.date.today()),
                                time_field=self.client_time,
                                masters_choice=self.master,
                                service_choice=self.service
                                )

    def test_main_app_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_validate_name(self):
        response = self.client.post('/contacts/', data={'client_name': 'Ivan'})
        self.assertFormError(response, 'form', 'client_name', errors='Имя должно быть от 2-х до 10-ти символов '
                                                                     'кирилицы')

    def test_validate_phone(self):
        response = self.client.post('/contacts/', data={'phone_number': '79140003322'})
        self.assertFormError(response, 'form', 'phone_number',
                             errors='Вводить тел. номер нужно без пробелов, скобок и дефисов в виде 89ХХХХХХХХХ')

    def test_validate_past_date(self):
        response = self.client.post('/contacts/',
                                    data={'date_field': datetime.date.today() - datetime.timedelta(days=1)})
        self.assertFormError(response, 'form', 'date_field', errors='Выбранная вами дата не может быть раньше текущей')

    def test_validate_future_exceed_date(self):
        response = self.client.post('/contacts/',
                                    data={'date_field': datetime.date.today() + datetime.timedelta(days=15)})
        self.assertFormError(response, 'form', 'date_field', errors='Эллектронная запись доступна только в пределах '
                                                                    'двух недель. Для более поздней записи свяжитесь '
                                                                    'с нами по телефону.')




