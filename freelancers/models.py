from django.db import models

CATEGORY_CHOICES = [
    ('Plumber', 'Plumber'),
    ('Electrician', 'Electrician'),
    ('Cleaner', 'Cleaner'),
    ('Caretaker', 'Caretaker'),
    ('Handyman', 'Handyman'),
    ('movers', 'movers'),

]

class Freelancer(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='freelancers/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
