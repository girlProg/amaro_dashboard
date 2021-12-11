# Generated by Django 3.1.3 on 2020-12-04 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legalfeepercentage', models.FloatField(default=0.02)),
                ('servicechargepercentage', models.FloatField(default=0.2)),
                ('vatpercentage', models.FloatField(default=0.05)),
            ],
        ),
        migrations.CreateModel(
            name='LetterType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phonenumber', models.CharField(max_length=200)),
                ('email', models.CharField(default='', max_length=200)),
                ('houseaddress', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('number', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('suitenumber', models.CharField(default='0', max_length=100)),
                ('cnumber', models.CharField(blank=True, default='000', max_length=100, null=True)),
                ('tenancystartdate', models.DateField(verbose_name='date tenancy starts')),
                ('tenancyenddate', models.DateField(verbose_name='date tenancy ends')),
                ('tenancyduration', models.IntegerField(default=1)),
                ('businessname', models.CharField(default=' ', max_length=200)),
                ('lineofbusiness', models.CharField(blank=True, default='', max_length=200)),
                ('squarefeet', models.FloatField(default=0)),
                ('floor', models.FloatField(default=0)),
                ('rate', models.FloatField(default=0)),
                ('rent', models.FloatField(default=0)),
                ('servicecharge', models.FloatField(default=0)),
                ('legalfees', models.FloatField(default=0)),
                ('vat', models.FloatField(default=0)),
                ('totaltobepaid', models.FloatField(default=0)),
                ('paymentrec', models.FloatField(default=0)),
                ('outstandingpayment', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('haspaidrent', models.BooleanField(default=False)),
                ('haspaidvat', models.BooleanField(default=False)),
                ('haspaidlegalfees', models.BooleanField(default=False)),
                ('haspaidservicecharge', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, default=' ', max_length=500, null=True)),
                ('key', models.BooleanField(default=False)),
                ('ac', models.BooleanField(default=False)),
                ('signed', models.BooleanField(default=False)),
                ('signage', models.ImageField(blank=True, default='', null=True, upload_to='Images/Signage')),
                ('balancebroughtforward', models.FloatField(default=0)),
                ('discountedrent', models.FloatField(default=0)),
                ('rentrec', models.FloatField(default=0)),
                ('zakahrec', models.FloatField(default=0)),
                ('servicechargerec', models.FloatField(default=0)),
                ('legalrec', models.FloatField(default=0)),
                ('vatrec', models.FloatField(default=0)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('chargespercentages', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenantRecords.charges')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenantRecords.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depositor', models.CharField(max_length=200)),
                ('amount', models.FloatField(default=0)),
                ('paymentdate', models.DateField(verbose_name='date of payment made')),
                ('statementpicture', models.ImageField(blank=True, default='', null=True, upload_to='Images/Statements')),
                ('paymentnote', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('partSC', models.FloatField(blank=True, default=0)),
                ('partrent', models.FloatField(blank=True, default=0)),
                ('partvat', models.FloatField(blank=True, default=0)),
                ('partzakah', models.FloatField(blank=True, default=0)),
                ('partlegal', models.FloatField(blank=True, default=0)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='tenantRecords.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letterImage', models.ImageField(blank=True, default='', null=True, upload_to='Images/Correspondence/')),
                ('datesent', models.DateField(null=True, verbose_name='date letter was sent')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='letter', to='tenantRecords.shop')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='letter', to='tenantRecords.tenant')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letter', to='tenantRecords.lettertype')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuedate', models.DateField(blank=True)),
                ('image', models.ImageField(upload_to='Images/Invoices')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenantRecords.shop')),
            ],
        ),
    ]
