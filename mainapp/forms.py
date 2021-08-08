from datetime import datetime, timedelta

from django import forms
from django.core.validators import RegexValidator

from mainapp.models import Contacts, Services, Masters, WorkDays, Time


class DateInput(forms.DateInput):
    input_type = 'date'


class ContactForm(forms.ModelForm):
    class Meta:
        class DateInput(forms.DateInput):
            input_type = 'date'

        model = Contacts
        fields = ['client_name', 'phone_number', 'service_choice', 'masters_choice',
                  'date_field', 'time_field']

        widgets = {
            'date_field': DateInput(),
        }

        labels = {
            'date_field': 'Выберите дату',
            'masters_choice': 'Выберите мастера'
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['client_name'] = forms.CharField(validators=[RegexValidator(regex='^[а-яА-Я]{2,'
                        '10}', message='Имя должно быть от 2-х до 10-ти символов кирилицы')],
                                                     label='Ваше имя')
        self.fields['phone_number'] = forms.CharField(validators=[RegexValidator(regex='^89[0-9]{'
            '9}', message='Вводить тел. номер нужно без пробелов, скобок и дефисов в виде '
            '89ХХХХХХХХХ')], min_length=11, max_length=11, label='Ваш контактный тел.',
            widget=forms.TextInput(attrs={'placeholder': '89XXXXXXXXX'}))
        self.fields['time_field'] = forms.ModelChoiceField(queryset=WorkDays.objects.none(),
                                                to_field_name=None, label='Выберите время')

        self.fields['service_choice'] = forms.ModelChoiceField(queryset=Services.objects.filter(
            is_active=True), to_field_name=None, label='Выберите услугу')

        self.fields['masters_choice'].queryset = Masters.objects.none()

        if 'service_choice' in self.data:
            try:
                service_id = int(self.data.get('service_choice'))
                self.fields['masters_choice'].queryset = Masters.objects.filter(master_services__id=service_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'date_field' in self.data:
            try:
                date_field = self.data.get('date_field')
                date_field = datetime.strptime(date_field, '%Y-%m-%d')
                date = date_field.weekday()
                self.fields['time_field'].queryset = Time.objects.filter(workdays__days=date)
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        date_field = cleaned_data['date_field']
        time_field = cleaned_data['time_field']
        date_field = datetime.strptime(str(date_field), '%Y-%m-%d')
        res = date_field - datetime.now()
        delta = timedelta(days=14)
        if date_field.date() < datetime.now().date():
            raise forms.ValidationError({'date_field': 'Выбранная вами дата не может быть раньше текущей'})
        if res > delta:
            raise forms.ValidationError({'date_field': 'Эллектронная запись доступна только в пределах двух недель. Для более поздней записи свяжитесь с нами по телефону.'})
        if date_field.date() == datetime.now().date():
            if str(time_field) < datetime.now().strftime('%H:%M'):
                raise forms.ValidationError({'time_field': 'Час на которой вы планируете записаться уже прошел. Пожалуйста выберите час записи больше текущего.'})



