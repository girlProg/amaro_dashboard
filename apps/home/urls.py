# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    re_path('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/options$', login_required(views.DetailView.as_view()), name='detail'),
    re_path('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/summary$', login_required(views.SummaryView.as_view()), name='summary'),
    re_path('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/profile$', login_required(views.ShopProfileView.as_view()), name='profile'),
    re_path('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/receipt$', login_required(views.ReceiptView.as_view()), name='receipt'),
    re_path('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/tenancy_details$', login_required(views.TenancyDetailsView.as_view()), name='tenancy_details'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
app_name = 'home'
