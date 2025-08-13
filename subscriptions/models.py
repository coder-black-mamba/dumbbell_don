from django.db import models

# Create your models here.
class Subscription(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    )
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    plan = models.ForeignKey('plans.MembershipPlan', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    auto_renew = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.username} - {self.plan.name} - {self.status} - {self.auto_renew}"
