from datetime import datetime
from django.db import models


class Services(models.Model):
    service_name = models.CharField(verbose_name="услуга", max_length=128, unique=True)
    service_description = models.TextField(verbose_name='текст услуги', blank=True)
    service_id = models.CharField(verbose_name='id текста на странице', max_length=128, blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2,
                                default=0)
    img_1 = models.ImageField(upload_to="services_img", blank=True)
    img_2 = models.ImageField(upload_to="services_img", blank=True)
    img_3 = models.ImageField(upload_to="services_img", blank=True)
    is_active = models.BooleanField(verbose_name='услуга активна',
                                    default=True)
    discount = models.PositiveIntegerField(verbose_name='скидка', default=0)
    finished = models.DateField(verbose_name='окончание скидки', blank=True, default=datetime.now)

    def chained_relation(self):
        return self.masters_set.all()

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name_plural = 'Услуги'

    @property
    def discount_price(self):
        return round((self.price * (100 - self.discount) / 100), 2)


class Masters(models.Model):
    name = models.CharField(verbose_name="мастер", max_length=128, unique=True)
    photo = models.ImageField(upload_to='masters_photo', blank=True)
    greeting = models.TextField(verbose_name='краткое приветствие', blank=True)
    master_specialization = models.CharField(verbose_name='специализация', max_length=256,
                                             blank=True)
    master_services = models.ManyToManyField(Services, blank=True, verbose_name='услуги мастера')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Мастера'


class ActionsNews(models.Model):
    title = models.CharField(verbose_name="заголовок", max_length=128)
    published = models.DateField(verbose_name="опубликовано",
                                 default=datetime.now)
    description = models.TextField(verbose_name="текст новости")
    is_active = models.BooleanField(verbose_name='акция активна',
                                    default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']
        verbose_name_plural = 'Новости'


class Portfolio(models.Model):
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    img_1 = models.ImageField(upload_to="portfolio", blank=True)
    img_2 = models.ImageField(upload_to="portfolio", blank=True)
    img_3 = models.ImageField(upload_to="portfolio", blank=True)
    is_active = models.BooleanField(verbose_name='портфолио активно',
                                    default=True)

    def __str__(self):
        return f'Портфолио услуги {self.service_id}'

    class Meta:
        verbose_name_plural = 'Портфолио'


class Time(models.Model):
    TIME_CHOICE = (
        ('9:00', '9:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:30', '13:30'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
        ('19:00', '19:00')
    )
    time = models.CharField(max_length=32, verbose_name='часы работы', choices=TIME_CHOICE)

    class Meta:
        verbose_name_plural = 'Время'

    def __str__(self):
        return self.time


class WorkDays(models.Model):
    DAY_CHOICE = (
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье')
    )

    days = models.CharField(max_length=1, verbose_name='день недели', choices=DAY_CHOICE)
    time = models.ManyToManyField(Time, verbose_name='время работы')

    class Meta:
        verbose_name_plural = 'Рабочие дни'

    def __str__(self):
        return self.get_days_display()


class Contacts(models.Model):
    client_name = models.CharField(verbose_name="имя клиента", max_length=10)
    phone_number = models.CharField(verbose_name="телефон клиента", max_length=11)
    service_choice = models.ForeignKey(Services, on_delete=models.CASCADE)
    masters_choice = models.ForeignKey(Masters, on_delete=models.CASCADE)
    date_field = models.DateField(verbose_name='дата услуги')
    time_field = models.ForeignKey(Time, on_delete=models.CASCADE, verbose_name='время услуги')

    class Meta:
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.date_field} {self.client_name}'
