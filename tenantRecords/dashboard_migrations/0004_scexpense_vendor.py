# Generated by Django 3.2.6 on 2021-12-07 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps_tenantRecords', '0003_remove_scexpense_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='scexpense',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sc_expense', to='apps_tenantRecords.vendor'),
        ),
    ]
