from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date
from copy import deepcopy
from django.utils import timezone




class Charges(models.Model):
    legalfeepercentage = models.FloatField(default=0.02)
    servicechargepercentage = models.FloatField(default=0.125)
    vatpercentage = models.FloatField(default=0.05)

    def __unicode__(self):
        return str(self.servicechargepercentage)


class Tenant (models.Model):
    name = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=200)
    houseaddress = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name



class Shop (models.Model):

    number = models.CharField(max_length=4, default=000, primary_key=True)
    tenant = models.ForeignKey(Tenant)
    tenancystartdate = models.DateField('date tenancy starts')
    tenancyenddate = models.DateField('date tenancy ends')
    tenancyduration = models.IntegerField(default=1)
    businessname = models.CharField(max_length=200, default= " ")
    lineofbusiness = models.CharField(blank=True,default="",max_length=200)
    squarefeet = models.FloatField(default=0)
    floor = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    rent = models.FloatField(default=0)
    servicecharge = models.FloatField(default=0)
    legalfees = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    totaltobepaid = models.FloatField(default=0)
    paymentrec = models.FloatField(default=0)
    outstandingpayment = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    chargespercentages = models.ForeignKey(Charges, null=True)
    haspaidrent = models.BooleanField(default=False)
    haspaidvat = models.BooleanField(default=False)
    haspaidlegalfees = models.BooleanField(default=False)
    haspaidservicecharge = models.BooleanField(default=False)
    notes = models.CharField(default= " ", max_length=500, blank=True, null=True)
    key = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    signage = models.ImageField(upload_to='Images/Signage', default="", null=True, blank=True)


    def save(self, *args, **kwargs):


        #RevisionShop(deepcopy(self)).save()
        self.rent = self.squarefeet * self.rate
        self.legalfees = self.rent * self.chargespercentages.legalfeepercentage
        self.vat = self.rent * self.chargespercentages.vatpercentage
        self.servicecharge = self.rent * self.chargespercentages.servicechargepercentage
        self.totaltobepaid = ((self.rent * self.tenancyduration) - self.discount) + self.servicecharge + self.legalfees + self.vat
        self.outstandingpayment = self.totaltobepaid - self.paymentrec
        self.tenancyenddate = add_years(self.tenancystartdate, self.tenancyduration)

        #create a revision
        rs = RevisionShop()
        rs.number = self.number
        rs.tenancystartdate = self.tenancystartdate
        rs.tenancyenddate = self.tenancyenddate
        rs.tenancyduration = self.tenancyduration
        rs.businessname = self.businessname
        rs.lineofbusiness = self.lineofbusiness
        rs.squarefeet = self.squarefeet
        rs.floor = self.floor
        rs.rate = self.rate
        rs.rent = self.rent
        rs.servicecharge = self.servicecharge
        rs.legalfees = self.legalfees
        rs.vat = self.vat
        rs.totaltobepaid = self.totaltobepaid
        rs.paymentrec = self.paymentrec
        rs.outstandingpayment = self.outstandingpayment
        rs.discount = self.discount
        rs.chargespercentages = self.chargespercentages
        rs.haspaidrent = self.haspaidrent
        rs.haspaidvat = self.haspaidvat
        rs.haspaidlegalfees = self.haspaidlegalfees
        rs.haspaidservicecharge = self.haspaidservicecharge
        rs.tenant = deepcopy(self.tenant)

        rs.save()
        super(Shop, self).save(*args, **kwargs) # Call the "real" save() method so self.payments is accessible.

    def __unicode__(self):
        return self.number

class RevisionShop(models.Model):
    revid = models.AutoField(primary_key=True)
    number = models.CharField(max_length=4, default=000)
    tenant = models.ForeignKey(Tenant)
    tenancystartdate = models.DateField('date tenancy starts')
    tenancyenddate = models.DateField('date tenancy ends')
    tenancyduration = models.IntegerField(default=1)
    businessname = models.CharField(max_length=200, default= " ")
    lineofbusiness = models.CharField(blank=True,default="",max_length=200)
    squarefeet = models.FloatField(default=0)
    floor = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    rent = models.FloatField(default=0)
    servicecharge = models.FloatField(default=0)
    legalfees = models.FloatField(default=0)
    vat = models.FloatField(default=0)
    totaltobepaid = models.FloatField(default=0)
    paymentrec = models.FloatField(default=0)
    outstandingpayment = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    chargespercentages = models.ForeignKey(Charges, null=True)
    haspaidrent = models.BooleanField(default=False)
    haspaidvat = models.BooleanField(default=False)
    haspaidlegalfees = models.BooleanField(default=False)
    haspaidservicecharge = models.BooleanField(default=False)
    notes = models.CharField(default= " ", max_length=500, blank=True, null=True)
    key = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    signage = models.ImageField(upload_to='Images/Signage', default="", null=True, blank=True)

    def __unicode__(self):
        return self.number


class Payment (models.Model):
    depositor = models.CharField(max_length=200)
    shop = models.ForeignKey(Shop)
    amount = models.FloatField(default=0)
    paymentdate = models.DateField('date of payment made')
    rent_paid = models.FloatField(default=0)
    servicecharge_paid = models.FloatField(default=0)
    legalfees_paid = models.FloatField(default=0)
    vat_paid = models.FloatField(default=0)
    statementpicture = models.ImageField(upload_to='Images/Statements', default="", null=True, blank=True)
    paymentnote = models.CharField(default= "", max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.depositor

class Invoice(models.Model):
    shop = models.ForeignKey(Shop)
    issuedate = models.DateField(blank=True)
    image = models.ImageField(upload_to='Images/Invoices')

@receiver(post_save, sender=Payment)
def populaterecievedpayments(sender, **kwargs):
    paymentrec=0
    payment = kwargs.get('instance')
    pmts = Payment.objects.filter(shop=payment.shop)

    for payment in pmts:
        paymentrec += payment.amount
    payment.shop.paymentrec = paymentrec
    payment.shop.save()

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))