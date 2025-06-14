# Generated by Django 5.2.1 on 2025-06-01 07:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_item_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacantroom',
            name='room_type',
            field=models.CharField(choices=[('Single', 'Single'), ('Double', 'Double'), ('Self-Contained', 'Self-Contained'), ('Bedsitter', 'Bedsitter'), ('Airbnb', 'Airbnb'), ('Duplex', 'Duplex'), ('1 Bedroom', '1 Bedroom'), ('2 Bedroom', '2 Bedroom'), ('3 Bedroom', '3 Bedroom'), ('4 Bedroom', '4 Bedroom')], max_length=20),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('rent', 'Rent Property'), ('commercial', 'Commercial Property'), ('marketplace', 'Marketplace Item'), ('forsale', 'Property For Sale')], max_length=20)),
                ('item_title', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
