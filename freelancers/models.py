from django.db import models
from cloudinary.models import CloudinaryField

CATEGORY_CHOICES = [
    ('Plumber', 'Plumber'),
    ('Electrician', 'Electrician'),
    ('Cleaner', 'Cleaner'),
    ('Caretaker', 'Caretaker'),
    ('Handyman', 'Handyman'),
    ('Movers', 'Movers'),
]

class Freelancer(models.Model):
    name = models.CharField(max_length=100)
    photo = CloudinaryField('image')  # Cloudinary image field
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    contact = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    video = CloudinaryField('video', resource_type='video', blank=True, null=True)  # Cloudinary video field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.freelancer.name}"
