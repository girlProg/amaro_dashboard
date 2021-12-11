from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import  Tenant, Shop, Payment
from django.views import generic
from django.views.generic import View
from django.http import *
# from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from reversion.models import Version
from reversion import revisions as reversion
from django.db.models.query import QuerySet
from django.views.generic.list import ListView


class BaseView(generic.ListView):
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.order_by('number')


class SuitesAccView( BaseView):
    template_name = 'tenantRecords/suitesAcc.html'
    contx = {}

    # def querysetandcontexd(self):
    #     pathlist = self.request.path.split('/')
    #     if(len(pathlist) > 3):
    #         year = self.request.path.split('/')[3]
    #         return Shop.objects.order_by('number').filter(tenancystartdate__year = year)
    #     else:
    #         return Shop.objects.order_by('number').filter(number__regex = r'[0-9][0-9][0-9]?')
    #
    # def get_context_data(self, **kwargs):
    #     return {'shops': self.querysetandcontexd(), 'payments': Payment.objects.all()}

    def get_queryset(self):
        """Return the shops within the requested year."""
        pathlist = self.request.path.split('/')
        if(len(pathlist) > 3):
            year = self.request.path.split('/')[3]
            if year:
                nextyear = str((int(year)+1)) if year else '2010'
                #return Shop.objects.order_by('number').filter(tenancystartdate__year = year)
                allshops = Shop.objects.order_by('number')
                return allshops.filter(tenancystartdate__year = year)


            # rentyearshops = allshops.filter(tenancystartdate__month = '07', tenancystartdate__year = year)
            # rentyearshops1 = allshops.filter(tenancystartdate__month = '08', tenancystartdate__year = year)
            # rentyearshops2 = allshops.filter(tenancystartdate__month = '09', tenancystartdate__year = year)
            # rentyearshops3 = allshops.filter(tenancystartdate__month = '10', tenancystartdate__year = year)
            # rentyearshops4 = allshops.filter(tenancystartdate__month = '11', tenancystartdate__year = year)
            # rentyearshops5 = allshops.filter(tenancystartdate__month = '12', tenancystartdate__year = year)
            # rentyearshops7 = allshops.filter(tenancystartdate__month = '02', tenancystartdate__year = nextyear)
            # rentyearshops6 = allshops.filter(tenancystartdate__month = '01', tenancystartdate__year = nextyear)
            # rentyearshops8 = allshops.filter(tenancystartdate__month = '03', tenancystartdate__year = nextyear)
            # rentyearshops9 = allshops.filter(tenancystartdate__month = '04', tenancystartdate__year = nextyear)
            # rentyearshops10 = allshops.filter(tenancystartdate__month = '05', tenancystartdate__year = nextyear)
            # rentyearshops11 = allshops.filter(tenancystartdate__month = '06', tenancystartdate__year = nextyear)
            # return rentyearshops | rentyearshops1 | rentyearshops2 | rentyearshops3| rentyearshops5 | rentyearshops4 | rentyearshops6 | rentyearshops7 | rentyearshops8 |rentyearshops9 | rentyearshops10 | rentyearshops11
        else:
            return Shop.objects.order_by('number').filter(number__regex = r'[0-9][0-9][0-9]?')



class AddressesView( BaseView):
    template_name = 'tenantRecords/addresses.html'

class RentalYearsView( BaseView):
    template_name = 'tenantRecords/rentalyears.html'

class ZeroPaidView( BaseView):
    template_name = 'tenantRecords/zeroreceived.html'

class TotalReceivedView( BaseView):
    template_name = 'tenantRecords/totalpaidreport.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Shop.objects.exclude(pk="011").\
            exclude(pk="107").order_by('number')

class FinBreakdownView(ListView):

    tmpshop = {}
    totalrent = 0
    model = Shop
    template_name = 'tenantRecords/finbreakdown.html'

    def get_context_data(self, **kwargs):
        self.tmpshop = Shop.objects.order_by('number').filter(number__regex = r'[0-9][0-9][0-9]?')
        for shop in self.tmpshop:
            if shop.discountedrent:
                if shop.paymentrec < shop.discountedrent:
                    shop.outrent = shop.discountedrent - shop.paymentrec
                    shop.outsc = shop.servicecharge
                elif shop.paymentrec < (shop.discountedrent + shop.servicecharge):
                    shop.outsc  = (shop.discountedrent + shop.servicecharge) - shop.paymentrec
                    shop.outrent = 0
            else:
                if shop.paymentrec < shop.rent:
                    shop.outrent = shop.rent - shop.paymentrec
                    shop.outsc = shop.servicecharge
                elif shop.paymentrec < (shop.rent + shop.servicecharge):
                    shop.outsc  = (shop.rent + shop.servicecharge) - shop.paymentrec
                    shop.outrent = 0
        context = super(FinBreakdownView, self).get_context_data(**kwargs)
        context['shops'] = self.tmpshop
        return context

class PendingSCView( BaseView):
    template_name = 'tenantRecords/pendingsc.html'

class ContactDetailsView( BaseView):
    template_name = 'tenantRecords/contactdetails.html'
    def get_queryset(self):
        return Shop.objects.order_by('tenancystartdate')

class DetailView(generic.DetailView):
    model = Shop
    #slug_field = 'number'
    template_name = 'tenantRecords/detail.html'


class OfferView(generic.DetailView):
    model = Shop
    #slug_field = 'number'
    template_name = 'tenantRecords/offerletter.html'

class ReminderView(generic.DetailView):
    model = Shop
    #slug_field = 'number'
    template_name = 'tenantRecords/reminder.html'


class PrintableDetailView(generic.DetailView):
    model = Shop
    template_name = 'tenantRecords/detail_printable.html'


class DirectoryView(BaseView):
    template_name = 'tenantRecords/directory.html'

    def get_queryset(self):
        """Return the last five published questions."""
        return Shop.objects.order_by('-number')[:5]


class StatementsView(generic.DetailView):
    template_name = 'tenantRecords/statements.html'
    model = Shop

class LetterView(generic.DetailView):
    template_name = 'tenantRecords/letters.html'
    model = Shop

class RevisionsView(generic.ListView):
    context_object_name = 'versions'
    template_name = 'tenantRecords/revisions.html'
    model = Shop

    def get_queryset(self):
        return Shop.objects.get(number=self.kwargs['pk'])


class RevisionView(generic.DetailView):
    context_object_name = 'shop'
    template_name = 'tenantRecords/revision.html'
    model = Shop

    def get_queryset(self):
        shopno, verpk = self.kwargs['pk'], self.kwargs['rpk']
        #fg = reversion.get_for_object(Shop.objects.get(number=shopno))
        #return fg[int(verpk)-1].object
        return Shop.objects.filter(number=shopno)

def savepayments(request):
    for payment in Payment.objects.all():
        payment.save()

class LogoutView(generic.View):

    def get(self, request):
        logout(request)
        return render(request, 'tenantRecords/logout.html')

class LoginView(View):

    def get(self, request):
        context = RequestContext(request)
        return render(request, 'tenantRecords/login.html')

    def post(self,request, *args, **kwargs):
        # Like before, obtain the context for the user's request.
        context = RequestContext(request)

        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':
            # Gather the username and password provided by the user.
            # This information is obtained from the login form.
            username = request.POST['username']
            password = request.POST['password']

            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)

            # If we have a User object, the details are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    return HttpResponseRedirect('/records/')
                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Your Amaro account is disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                print( "Invalid login details: {0}, {1}".format(username, password))
                return HttpResponse("Invalid login details supplied.")

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
        else:
            # No context variables to pass to the template system, hence the
            # blank dictionary object...
            return render(request, 'tenantRecords/login.html', {}, context)