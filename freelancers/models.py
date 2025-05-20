from django.db import models
from cloudinary.models import CloudinaryField  # Make sure this import is included

CATEGORY_CHOICES = [
    ('Plumber', 'Plumber'),
    ('Electrician', 'Electrician'),
    ('Cleaner', 'Cleaner'),
    ('Caretaker', 'Caretaker'),
    ('Handyman', 'Handyman'),
    ('Movers', 'Movers'),  # Capitalized for consistency
]

class Freelancer(models.Model):
    name = models.CharField(max_length=100)
    photo = CloudinaryField('image', null=True, blank=True)  # Replaces ImageField
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    video = CloudinaryField('video', null=True, blank=True)  # Replaces FileField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
