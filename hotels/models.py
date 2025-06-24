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
    image = CloudinaryField('image') 

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

    amenities = models.ManyToManyField(Amenity, blank=True, related_name='room_types')

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"






class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} ({self.room_type.name})"



class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reservations')
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.guest_name} at {self.room}"

    def clean(self):
        if not self.room or not self.check_in or not self.check_out:
            raise ValidationError("Room and both check-in/check-out dates are required.")

        if self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")

        overlapping = Reservation.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This room is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)




class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image') 
    is_main = models.BooleanField(default=False)  # Optional: for main image tagging

    def __str__(self):
        return f"{self.hotel.name} Image"
