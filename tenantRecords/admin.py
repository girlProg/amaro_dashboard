from django.contrib import admin
from tenantRecords import models
from reversion.admin import VersionAdmin

#admin.site.register(models.Shop)
admin.site.register(models.Payment)
# admin.site.register(models.Tenant)
admin.site.register(models.Charges)
admin.site.register(models.Invoice)
admin.site.register(models.LetterType)

class PaymentsInline(admin.StackedInline):
    model = models.Payment
    extra = 1

    search_fields = ['depositor', 'shop', 'amount',]


class InvoiceInline(admin.StackedInline):
    model = models.Invoice
    extra = 1

class LetterInline(admin.StackedInline):
    model = models.Letter
    extra = 1

class ShopAdmin(VersionAdmin):
    fieldsets = [
        (None,{'fields': ['suitenumber', 'number', 'tenant', ('tenancystartdate', 'tenancyenddate','tenancyduration'),
                          ('businessname', 'lineofbusiness'), 'squarefeet', 'totaltobepaid','vat', 'servicecharge', 'floor', 'rate', 'discount', 'balancebroughtforward',
                          'chargespercentages', ('haspaidvat','haspaidrent', 'haspaidlegalfees', 'haspaidservicecharge') ,'notes']
        })
        ,
    ]
    inlines = [InvoiceInline, PaymentsInline]
    #list_display = ('number', 'tenant')


class TenantAdmin(VersionAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'phonenumber', 'email', 'houseaddress']})
        ,
    ]
    inlines = [LetterInline,]

admin.site.register(models.Shop, ShopAdmin)
admin.site.register(models.Tenant, TenantAdmin)
admin.site.register(models.Vendor)
admin.site.register(models.SCExpense)

