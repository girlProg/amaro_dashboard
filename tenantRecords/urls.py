from tenantRecords import views
from django.conf.urls import  url
from core import settings
from django.conf.urls.static import static
from django.urls import re_path, path
from django.contrib.auth.decorators import login_required, permission_required

app_name="tenantRecords"

urlpatterns = [
    url('^logout', views.LogoutView.as_view(), name='logout'),
    url('^login', views.LoginView.as_view(), name='login'),
    url('^suites', login_required(views.SuitesAccView.as_view()), name='suitesAcc'),
    url('^suites/([0-9]{4})/$', login_required(views.SuitesAccView.as_view()), name='suitesAcc'),
    url('^rentalyears', login_required(views.RentalYearsView.as_view()), name='rentalyears'),
    url('^pendingsc', login_required(views.PendingSCView.as_view()), name='pendingsc'),
    url('^addresses', login_required(views.AddressesView.as_view()), name='addresses'),
    url('^zeropaid', login_required(views.ZeroPaidView.as_view()), name='zeropaid'),
    url('^totalreceived', login_required(views.TotalReceivedView.as_view()), name='totalreceived'),
    url('^finbreakdown', login_required(views.FinBreakdownView.as_view()), name='finbreakdown'),
    url('^contactdetails', login_required(views.ContactDetailsView.as_view()), name='contactdetails'),
    url('^savepayments', login_required(views.savepayments), name='savepayments'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/$', login_required(views.PrintableDetailView.as_view()), name='detail_printable'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/detail$', login_required(views.DetailView.as_view()), name='detail'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/offer', login_required(views.OfferView.as_view()), name='offer'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/reminder', login_required(views.ReminderView.as_view()), name='reminder'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/statements/$', login_required(views.StatementsView.as_view()), name='statements'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/letters/$', login_required(views.LetterView.as_view()), name='letters'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/revisions/$', login_required(views.RevisionsView.as_view()), name='revisions'),
    url('^(?P<pk>\d+[A-Z]?.?[0-9]*?[a-z]*?)/revisions/(?P<rpk>\d+[A-Z]?)/$', login_required(views.RevisionView.as_view()), name='revision'),
    url('', login_required(views.DirectoryView.as_view()), name='directory'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)