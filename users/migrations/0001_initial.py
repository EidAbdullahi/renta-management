# Generated by Django 5.1.7 on 2025-04-04 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('position', models.CharField(max_length=50)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gender', models.CharField(max_length=6)),
                ('emergency_contact', models.CharField(max_length=15)),
                ('upload_id', models.FileField(upload_to='employee_ids/')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_rented', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('property_address', models.CharField(max_length=255)),
                ('move_in_date', models.DateField()),
                ('rent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_document', models.FileField(blank=True, null=True, upload_to='tenant_documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receipt', models.FileField(blank=True, null=True, upload_to='receipts/')),
                ('payment_method', models.CharField(choices=[('M-Pesa', 'M-Pesa'), ('Bank', 'Bank Transfer'), ('Cash', 'Cash')], max_length=10)),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Overdue', 'Overdue')], default='Pending', max_length=10)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tenant')),
            ],
        ),
    ]
