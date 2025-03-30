from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class AssignedHouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"House {self.house_number} -> {self.user.name}"
