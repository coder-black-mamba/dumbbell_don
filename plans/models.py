from django.db import models

# Create your models here.
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_days = models.IntegerField()
    price_cents = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    