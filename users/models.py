from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    property_address = models.CharField(max_length=255)
    move_in_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    property_address = models.CharField(max_length=255)
    move_in_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='tenant_photos/', blank=True, null=True)
    id_document = models.FileField(upload_to='tenant_documents/', blank=True, null=True)

    

    def __str__(self):
        return self.name

   
