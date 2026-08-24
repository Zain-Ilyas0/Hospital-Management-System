from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    cnic = models.CharField(max_length=15)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Patient(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    patient_name = models.CharField(max_length=100)
    
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=30)
    patient_problem = models.CharField(max_length=100)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="patients"
    )