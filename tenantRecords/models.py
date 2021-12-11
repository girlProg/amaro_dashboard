from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from datetime import date
from copy import deepcopy
from django.utils import timezone




class Charges(models.Model):
    legalfeepercentage = models.FloatField(default=0.02)
    servicechargepercentage = models.FloatField(default=0.2)
    vatpercentage = models.FloatField(default=0.05)

    def __str__(self):
        return str('SC:'+ str(self.servicechargepercentage * 100) +
                   ' Legal:' + str(self.legalfeepercentage * 100) +
                   ' VAT:' + str(self.vatpercentage * 100)
        )


class Tenant (models.Model):
    name = models.CharField(max_length=200)
    phonenumber = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default='')
    houseaddress = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name



class Shop (models.Model):
    #id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100, primary_key=True)
    suitenumber = models.CharField(max_length=100, default='0')
    cnumber = models.CharField(max_length=100, default='000', blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
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
    chargespercentages = models.ForeignKey(Charges, null=True, on_delete=models.CASCADE)
    haspaidrent = models.BooleanField(default=False)
    haspaidvat = models.BooleanField(default=False)
    haspaidlegalfees = models.BooleanField(default=False)
    haspaidservicecharge = models.BooleanField(default=False)
    notes = models.CharField(default= " ", max_length=500, blank=True, null=True)
    key = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    signage = models.ImageField(upload_to='Images/Signage', default="", null=True, blank=True)
    balancebroughtforward = models.FloatField(default=0)
    discountedrent = models.FloatField(default=0)
    rentrec = models.FloatField(default=0)
    zakahrec = models.FloatField(default=0)
    servicechargerec = models.FloatField(default=0)
    legalrec = models.FloatField(default=0)
    vatrec = models.FloatField(default=0)
    # percentpaid = models.FloatField(default=0)

    deleted= models.BooleanField(default=False,editable=False)

    def watchedfields(self):
        return ['number', 'tenant_id', 'tenancystartdate', 'tenancyenddate','tenancyduration',
              'businessname', 'lineofbusiness', 'squarefeet', 'floor', 'rate', 'discount',
              'chargespercentages_id', 'haspaidvat', 'haspaidlegalfees', 'haspaidservicecharge'
                ]
        #return [a for a in dir(self) if not a.startswith('__')]

    def save(self, *args, **kwargs):

        self.rent = self.squarefeet * self.rate

        #percentage discount
        if self.discount > 0 and self.discount < 100:
            self.discount = (self.discount/100)*self.rent
        self.discountedrent = self.rent - self.discount
        self.cnumber = self.cnumber.split(' ')[0]
        self.cnumber += ' ' + str(timezone.now().day) + str(timezone.now().month)+ str(timezone.now().minute)+ str(timezone.now().second)
        self.legalfees = self.rent * self.chargespercentages.legalfeepercentage
        if self.discountedrent:
            self.vat = self.discountedrent * self.chargespercentages.vatpercentage
            self.legalfees = self.discountedrent * self.chargespercentages.legalfeepercentage
            # self.percentpaid = (self.discountedrent - self.paymentrec) * 100
        else:
            self.vat = self.rent * self.chargespercentages.vatpercentage
            self.legalfees = self.rent * self.chargespercentages.legalfeepercentage
            # self.percentpaid = (self.rent - self.paymentrec) * 100


        self.servicecharge = (self.squarefeet * 35000) * self.chargespercentages.servicechargepercentage
        # self.servicecharge = self.rent * self.chargespercentages.servicechargepercentage
        if self.number.split('.')[0] in ['001', '002','406B', '001.1718', '002.1718', '302B','109A','007C', '208','208A','208B', '011', '207', '403', '105', '307']:
            self.servicecharge = (self.squarefeet * 35000) * self.chargespercentages.servicechargepercentage
        self.totaltobepaid = ((self.rent * self.tenancyduration) - self.discount) + \
                             self.servicecharge + self.legalfees + self.vat + self.balancebroughtforward
        self.outstandingpayment = self.totaltobepaid - self.paymentrec
        self.tenancyenddate = add_years(self.tenancystartdate, self.tenancyduration)



        #drs code
        '''if self.pk is None:
            self.pk = self.cnumber
            return super(self.__class__,self).save(*args,**kwargs)
        if self.__class__.objects.filter(pk=self.pk):
            old_instance=self.__class__.objects.get(pk=self.pk)
            result=super(self.__class__,self).save(*args,**kwargs)
            for field in self.watchedfields():
                if  self.__dict__[field] != old_instance.__dict__[field]:#detect changes in any of the watched  fields
                    old_instance.pk = None
                    old_instance.deleted =True
                    old_instance.save()
                    break
            return result'''

        super(self.__class__,self).save(*args,**kwargs)


    def __str__(self):
        return self.number + '-' + self.businessname


class Payment (models.Model):
    depositor = models.CharField(max_length=200)
    shop = models.ForeignKey(Shop, related_name='payment', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    paymentdate = models.DateField('date of payment made')
    statementpicture = models.ImageField(upload_to='Images/Statements', default="", null=True, blank=True)
    paymentnote = models.CharField(default= "", max_length=500, blank=True, null=True)
    partSC = models.FloatField(default=0, blank=True)
    partrent = models.FloatField(default=0, blank=True)
    partvat = models.FloatField(default=0, blank=True)
    partzakah = models.FloatField(default=0, blank=True)
    partlegal = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.depositor

    def save(self, *args, **kwargs):
        sc, vat, legal, zakah, paidin, rentafterz, total = 0, 0, 0, 0, 0, 0, 0
        verified = False
        payment = self
        shop = self.shop
        rent = shop.rent if shop.discountedrent != 0 else shop.discountedrent

        '''100% RENT PAID IN FULL'''
        if self.amount == self.shop.totaltobepaid:
            self.partzakah = shop.rent * 0.1 if shop.discountedrent != 0 else shop.discountedrent * 0.1
            self.partlegal = shop.legalfees if shop.legalfees != 0 else 0
            self.partrent = rent - zakah
            total = self.partrent + self.partvat + self.partlegal + self.partSC + self.partzakah
            if total == self.amount:
                verified = True

        else:
            if shop.paymentrec <= (rent + shop.vat):
                vat = paidin * 0.05
                zakah = paidin * 0.1
                rentafterz = rent - zakah - vat
                total = rentafterz + vat + zakah

                if total == paidin:
                    verified = True
            else:
                '''IF NEW SHOP, pay legal fees'''
                if shop.paymentrec <= (rent + shop.vat)  :
                    pass

                if shop.legalfees > 0 :

                    pass

        # if self.shop.discountedrent:
        #
        #     if self.shop.outstandingpayment == self.amount:
        #         self.partrent = self.shop.discountedrent
        #         self.partSC = self.shop.servicecharge
        #         self.partvat = self.shop.vat
        #         self.partzakah = self.shop.discountedrent * 0.1
        #     else:
        #         #unsure of this else branch
        #         if self.amount == self.shop.discountedrent:
        #             pass
        # else:
        #     self.partrent = self.shop.rent
        #     pass

        super(self.__class__, self).save(*args, **kwargs)

class Invoice(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    issuedate = models.DateField(blank=True)
    image = models.ImageField(upload_to='Images/Invoices')

@receiver(post_save, sender=Payment)
def populaterecievedpayments(sender, **kwargs):
    paymentrec, vatrec, rentrec , screc, zakahrec= 0, 0, 0 , 0 , 0
    payment = kwargs.get('instance')
    pmts = Payment.objects.filter(shop=payment.shop)

    for payment in pmts:
        paymentrec += payment.amount
        rentrec += payment.partrent
        screc += payment.partSC
        zakahrec += payment.partzakah
        vatrec += payment.partvat
    payment.shop.paymentrec = paymentrec
    payment.shop.rentrec = rentrec
    payment.shop.servicechargerec = screc
    payment.shop.zakahrec = zakahrec
    payment.shop.vatrec = vatrec
    payment.shop.save()


# @receiver(post_save, sender=Payment)
def calculatetransfers(sender, **kwargs):
    sc, vat, legal, zakah, paidin, rentafterz, total = 0, 0, 0, 0, 0, 0, 0
    verified = False
    payment = kwargs.get('instance')
    shop = payment.shop
    rent = shop.rent if shop.discountedrent != 0 else shop.discountedrent


    pmts = Payment.objects.filter(shop=payment.shop)

    for payment in pmts:
        paymentrec += payment.amount
        rentrec += payment.partrent
        screc += payment.partSC
        zakahrec += payment.partzakah
        vatrec += payment.partvat
    payment.shop.paymentrec = paymentrec
    payment.shop.rentrec = rentrec
    payment.shop.servicechargerec = screc
    payment.shop.zakahrec = zakahrec
    payment.shop.vatrec = vatrec
    payment.shop.save()

@receiver(post_delete, sender=Payment)
def populaterecievedpaymentss(sender, **kwargs):
    populaterecievedpayments(sender,**kwargs)


# @receiver(post_delete, sender=Payment)
# def populaterecievedpayments(sender, **kwargs):
#     paymentrec=0
#     payment = kwargs.get('instance', {})
#     pmts = Payment.objects.filter(shop=payment.shop)
#
#     for payment in pmts:
#         paymentrec += payment.amount
#     payment.shop.paymentrec = paymentrec
#     payment.shop.save()

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


class LetterType (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Letter (models.Model):
    shop = models.ForeignKey(Shop, null=True, blank=True, related_name='letter', on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, null=True, blank=True, related_name='letter', on_delete=models.CASCADE)
    letterImage = models.ImageField(upload_to='Images/Correspondence/', default="", null=True, blank=True)
    type = models.ForeignKey(LetterType, related_name='letter', on_delete=models.CASCADE)
    datesent = models.DateField('date letter was sent', null=True)


class Vendor (models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(default= "", max_length=500, blank=True, null=True)
    bank_name = models.CharField(default= "", max_length=500, blank=True, null=True)
    account_number = models.CharField(default= "", max_length=500, blank=True, null=True)
    account_name = models.CharField(default= "", max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class SCExpense (models.Model):
    shop = models.ForeignKey(Shop, null=True, blank=True, related_name='sc_expense', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, related_name='sc_expense', on_delete=models.CASCADE)
    date = models.DateField('Expense Date', null=True)
    amount = models.DecimalField(default= 0, decimal_places=2, blank=True, null=True, max_digits=30)
    description = models.CharField(default= "", max_length=500, blank=True, null=True)
    status = models.CharField(choices=(('paid', 'paid'), ('unpaid', 'unpaid')), default= "", max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.date)
