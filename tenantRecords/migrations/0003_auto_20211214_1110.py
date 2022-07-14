# Generated by Django 3.2.6 on 2021-12-14 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenantRecords', '0002_auto_20211209_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='shop',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shops', to='tenantRecords.tenant'),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tenantRecords.basemodel')),
                ('method', models.CharField(blank=True, default='', max_length=500, null=True)),
            ],
            bases=('tenantRecords.basemodel',),
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='tenantRecords.paymentmethod'),
        ),
    ]