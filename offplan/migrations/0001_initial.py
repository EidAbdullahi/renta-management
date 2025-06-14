# Generated by Django 5.2.1 on 2025-05-18 15:27

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('client_email', models.EmailField(max_length=254)),
                ('client_phone', models.CharField(max_length=20)),
                ('deposit_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(blank=True, choices=[('Deposit', 'Deposit'), ('Installment', 'Installment')], max_length=50, null=True)),
                ('receipt_number', models.CharField(default='DEFAULT123', max_length=255)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='offplan.clientbooking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('number_of_units', models.PositiveIntegerField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('completion_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expense_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='general_expenses', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='offplan.project')),
            ],
        ),
        migrations.CreateModel(
            name='ConstructionExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(choices=[('materials', 'Materials'), ('labor', 'Labor'), ('equipment', 'Equipment'), ('permits', 'Permits'), ('consultants', 'Consultants'), ('transport', 'Transport'), ('misc', 'Miscellaneous')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date_incurred', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='construction_expenses', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='construction_expenses', to='offplan.project')),
            ],
        ),
        migrations.CreateModel(
            name='Construction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('progress_percentage', models.PositiveIntegerField(default=0)),
                ('current_phase', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='constructions', to=settings.AUTH_USER_MODEL)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='construction', to='offplan.project')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(max_length=50)),
                ('unit_type', models.CharField(max_length=50)),
                ('size_in_sqft', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_sold', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='offplan.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clientbooking',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='offplan.unit'),
        ),
    ]
