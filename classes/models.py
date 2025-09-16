from django.db import models

class FitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField()
    price_cents = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = (
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
        ('ATTENDED', 'Attended'),
        ('NO_SHOW', 'No Show')
    )
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NO_SHOW')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.fitness_class} - {self.status}"

class Attendance(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    marked_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    marked_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.booking.member} - {self.booking.fitness_class} - {self.present}"