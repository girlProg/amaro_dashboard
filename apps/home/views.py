# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from tenantRecords import models as tenant_models
from django.db.models import Sum
from datetime import date, timedelta, datetime
from calendar import monthrange
import pendulum
from django.views import generic
from tenantRecords.models import Shop, Payment


@login_required(login_url="/login/")
def index(request):

    today = date.today()
    pendulum_today = pendulum.now()

    last_day_of_month = monthrange(today.year, today.month)[1]

    this_month = [pendulum_today.start_of('month') , pendulum_today.end_of('month')]

    last_month = [today.replace(month=today.month-1, day=1) , today.replace(month=today.month-1, day=monthrange(today.year, today.month-1)[1])]

    # this_week = [today - timedelta(days=7), today.strftime("%Y-%m-%d")]
    this_week = [pendulum_today.start_of('week'), pendulum_today.end_of('week')]
    last_week = [(today - timedelta(days=14)), (today - timedelta(days=7))]
    this_year = [today.replace(day=1).replace(month=1) , today.replace(day=31).replace(month=12)]

    context = {'segment': 'index',
               'is_upper_mgt': True if request.user.get_username() in [''] else False,
               'shops' : tenant_models.Shop.objects.all(),
               'payments': tenant_models.Payment.objects.all().order_by('-paymentdate')[:30],
               'years_payments': tenant_models.Payment.objects.filter(paymentdate__range=this_year).aggregate(Sum('amount'))['amount__sum'],
               'weeks_payments': tenant_models.Payment.objects.filter(paymentdate__range=this_week).aggregate(Sum('amount'))['amount__sum'],
               'previous_weeks_payments': tenant_models.Payment.objects.filter(paymentdate__range=last_week).aggregate(Sum('amount'))['amount__sum'],
               'sc_expenses_month': tenant_models.SCExpense.objects.filter(date__range=this_month).aggregate(Sum('amount'))['amount__sum'],
               'sc_expenses_last_month': tenant_models.SCExpense.objects.filter(date__range=last_month).aggregate(Sum('amount'))['amount__sum'],
               'sc_expenses_week': tenant_models.SCExpense.objects.filter(date__range=this_week).aggregate(Sum('amount'))['amount__sum'],
               'percent': 50,
               }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class DetailView(generic.DetailView):
    model = Shop
    template_name = 'home/invoice.html'


class SummaryView(generic.DetailView):
    model = Shop
    template_name = 'home/invoice.html'


class ShopProfileView(generic.DetailView):
    model = Shop
    template_name = 'home/Profile.html'


class ReceiptView(generic.DetailView):
    model = Payment
    template_name = 'home/invoice.html'


class TenancyDetailsView(generic.DetailView):
    model = Shop
    template_name = 'home/tenancy_details.html'
