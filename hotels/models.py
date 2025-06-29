from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=300,blank=True, null=True)
    star_rating = models.IntegerField(default=3)
    image = CloudinaryField('image',blank=True, null=True) 

    def __str__(self):
        return self.name
    

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    bed_type = models.CharField(max_length=100, blank=True, null=True)
    view_type = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='room_types')

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"

    def available_rooms(self, check_in, check_out):
        # Optional helper for analytics (not restriction)
        booked_count = Reservation.objects.filter(
            room_type=self,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).count()
        return max(self.quantity - booked_count, 0)

    def booked_count(self):
        return self.reservations.count()



class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms',blank=True, null=True)
    room_number = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} ({self.room_type.name})"



class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('unsuccessful', 'Unsuccessful'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='reservations', blank=True, null=True)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.guest_name} - {self.room_type.name}"

    def clean(self):
        if not self.room_type or not self.check_in or not self.check_out:
            raise ValidationError("Room type and dates are required.")
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out must be after check-in.")

        # ❌ Removed overbooking restriction
        # Overbooking is now allowed by design

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images',blank=True, null=True)
    image = CloudinaryField('image',blank=True, null=True) 
    is_main = models.BooleanField(default=False)  # Optional: for main image tagging

    def __str__(self):
        return f"{self.hotel.name} Image"
