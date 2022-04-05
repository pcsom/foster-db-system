# Generated by Django 4.0 on 2021-12-31 01:40

import adminManagement.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='donorEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unset', max_length=300)),
                ('emailAddress', models.EmailField(default='UNSET@UNSET.UNSET', max_length=300)),
                ('mailingAddress', models.CharField(default='Unset', max_length=300)),
                ('itemsDonated', models.TextField(blank=True, null=True)),
                ('dataTableInfo', models.JSONField(default=adminManagement.models.donorEntry.buildDefDict)),
            ],
        ),
        migrations.CreateModel(
            name='volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unset', max_length=300)),
                ('totalHoursWorked', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('dataTableInfo', models.JSONField(default=adminManagement.models.volunteer.buildDefDict)),
            ],
        ),
        migrations.CreateModel(
            name='distributionEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateDistributed', models.DateField(default=datetime.date.today)),
                ('onesies', models.IntegerField(default=0)),
                ('twoPieceOutfits', models.IntegerField(default=0)),
                ('sleepSack', models.IntegerField(default=0)),
                ('cribSheets', models.IntegerField(default=0)),
                ('crib', models.IntegerField(default=0)),
                ('bibs', models.IntegerField(default=0)),
                ('receivingBlankets', models.IntegerField(default=0)),
                ('burpCloths', models.IntegerField(default=0)),
                ('washcloths', models.IntegerField(default=0)),
                ('bottles', models.IntegerField(default=0)),
                ('stroller', models.IntegerField(default=0)),
                ('formula', models.IntegerField(default=0)),
                ('diapers', models.IntegerField(default=0)),
                ('wipes', models.IntegerField(default=0)),
                ('furniture', models.IntegerField(default=0)),
                ('shortSleeveShirts', models.IntegerField(default=0)),
                ('longSleeveShirts', models.IntegerField(default=0)),
                ('shorts', models.IntegerField(default=0)),
                ('longPants', models.IntegerField(default=0)),
                ('pajamas', models.IntegerField(default=0)),
                ('dressClothes', models.IntegerField(default=0)),
                ('dresses', models.IntegerField(default=0)),
                ('winterCoats', models.IntegerField(default=0)),
                ('swimwear', models.IntegerField(default=0)),
                ('shoes', models.IntegerField(default=0)),
                ('toothbrush', models.IntegerField(default=0)),
                ('toothpaste', models.IntegerField(default=0)),
                ('deodorant', models.IntegerField(default=0)),
                ('soap', models.IntegerField(default=0)),
                ('shampoo', models.IntegerField(default=0)),
                ('ethnicHairCairProducts', models.IntegerField(default=0)),
                ('hairAccessories', models.IntegerField(default=0)),
                ('makeUpItems', models.IntegerField(default=0)),
                ('schoolSupplies', models.IntegerField(default=0)),
                ('toys', models.IntegerField(default=0)),
                ('games', models.IntegerField(default=0)),
                ('books', models.IntegerField(default=0)),
                ('bedding', models.IntegerField(default=0)),
                ('weightedBlanket', models.IntegerField(default=0)),
                ('dataTableInfo', models.JSONField(default=adminManagement.models.distributionEntry.buildDefDict)),
                ('forFamily', models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to='auth.user')),
            ],
        ),
    ]
