from datetime import datetime

from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView

from mainapp.forms import ContactForm
from django.shortcuts import render
from mainapp.models import Masters, Services, ActionsNews, Portfolio, Contacts, Time


class MainView(TemplateView):

    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Masters.objects.filter(is_active=True)
        context['service'] = Services.objects.filter(is_active=True)
        context['news'] = ActionsNews.objects.filter(is_active=True).order_by('-published')[:3]
        context['title'] = 'Главная'
        return context


class PortfolioView(TemplateView):

    template_name = 'mainapp/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = Portfolio.objects.filter(service_id__is_active=True)
        context['title'] = "Портфолио"
        return context


class ServicesView(TemplateView):

    template_name = 'mainapp/price.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Наши услуги"
        context['service'] = Services.objects.filter(is_active=True)
        return context


class NewsView(ListView):

    model = ActionsNews
    paginate_by = 5
    queryset = ActionsNews.objects.filter(is_active=True).order_by('-published')
    extra_context = {'title': 'Новости и акции'}


class ContactsView(CreateView):

    template_name = 'mainapp/contacts.html'
    form_class = ContactForm
    success_url = 'contacts'
    sent = False
    service_choice, masters_choice, date_field, time_field, msg = None, None, None, None, None

    def form_valid(self, form):
        self.sent = True
        self.service_choice = form.cleaned_data['service_choice']
        self.masters_choice = form.cleaned_data['masters_choice']
        self.date_field = form.cleaned_data['date_field']
        self.time_field = form.cleaned_data['time_field']
        super(ContactsView, self).form_valid(form)
        return render(self.request, self.template_name, self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Контакты"
        context['sent'] = self.sent
        context['masters_choice'] = self.masters_choice
        context['service_choice'] = self.service_choice
        context['date_field'] = self.date_field
        context['time_field'] = self.time_field
        return context


def load_masters(request):
    service_id = request.GET.get('service_choice')
    masters = Masters.objects.filter(master_services__id=service_id).order_by('name')
    return render(request, 'mainapp/masters_dropdown_list_options.html', {'masters': masters})


def load_time(request):
    date = request.GET.get('date')
    master = request.GET.get('master')
    rec_date = date
    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.weekday()
    time_set = Time.objects.filter(workdays__days=date)
    time_busy = []
    if master and rec_date:
        query = Contacts.objects.filter(masters_choice_id=int(master), date_field=rec_date)
        for item in query:
            time_busy.append(str(item.time_field))
    return render(request, 'mainapp/time_choice_list.html', {'time_set': time_set, 'time_busy': time_busy})


def valid_fields(request):
    name = request.GET.get('client_name')
    phone = request.GET.get('phone_number')
    response = {
        'valid_name': name,
        'valid_phone': phone
    }
    return JsonResponse(response)
