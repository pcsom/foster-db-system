# Generated by Django 4.0 on 2022-08-19 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irequests', '0003_remove_itemsrequest_bedding_remove_itemsrequest_bibs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsrequest',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 20, 17, 22, 132359)),
        ),
    ]
