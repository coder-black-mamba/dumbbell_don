from django.db import models

class Feedback(models.Model):
    member = models.ForeignKey('users.User', on_delete=models.CASCADE)
    fitness_class = models.ForeignKey('classes.FitnessClass', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.member} - {self.fitness_class} - {self.rating}"
    