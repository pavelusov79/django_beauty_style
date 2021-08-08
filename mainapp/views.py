from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

from mainapp.forms import ContactForm
from django.shortcuts import render
from mainapp.models import Masters, Services, ActionsNews, Portfolio, WorkDays, Contacts, Time


def main(request):
    title = 'Главная'
    masters = Masters.objects.filter(is_active=True)
    service = Services.objects.filter(is_active=True)
    news = ActionsNews.objects.filter(is_active=True).order_by('-published')[:3]
    context = {
        'title': title,
        'masters': masters,
        'service': service,
        'news': news
    }
    return render(request, 'mainapp/index.html', context)


def portfolio(request):
    title = "Портфолио"
    portfolio = Portfolio.objects.filter(service_id__is_active=True)
    context = {
        'title': title,
        'portfolio': portfolio
    }
    return render(request, 'mainapp/portfolio.html', context)


def contacts(request):
    title = "Контакты"
    sent = False
    service_choice, masters_choice, date_field, time_field, msg = None, None, None, None, None
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            service_choice = contact_form.cleaned_data['service_choice']
            time_field = contact_form.cleaned_data['time_field']
            print('time_field from contacts = ', time_field)
            date_field = contact_form.cleaned_data['date_field']
            masters_choice = contact_form.cleaned_data['masters_choice']
            contact_form.save()
            sent = True
    else:
        contact_form = ContactForm()

    context = {
        'title': title,
        'form': contact_form,
        'sent': sent,
        'masters_choice': masters_choice,
        'time_field': time_field,
        'date_field': date_field,
        'service_choice': service_choice,
    }
    return render(request, 'mainapp/contacts.html', context)


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
    print('time_busy = ', time_busy)
    return render(request, 'mainapp/time_choice_list.html', {'time_set': time_set, 'time_busy': time_busy})


def valid_fields(request):
    name = request.GET.get('client_name')
    phone = request.GET.get('phone_number')
    response = {
        'valid_name': name,
        'valid_phone': phone
    }
    return JsonResponse(response)


def services(request):
    title = "Наши услуги"
    service = Services.objects.filter(is_active=True)

    context = {
        'title': title,
        'service': service
    }
    return render(request, 'mainapp/price.html', context)


def news(request):
    title = "Новости и акции"
    news = ActionsNews.objects.filter(is_active=True).order_by('-published')
    page = request.GET.get('page')
    paginator = Paginator(news, 5)
    try:
        news_paginator = paginator.page(page)
    except PageNotAnInteger:
        news_paginator = paginator.page(1)
    except EmptyPage:
        news_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': title,
        'news': news_paginator
    }
    return render(request, 'mainapp/news.html', context)
