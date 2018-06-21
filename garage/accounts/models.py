from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from django.shortcuts import reverse
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
import  numpy as np
# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_mechanic = models.BooleanField(default=False)


class CarMake(models.Model):
    make=models.CharField(max_length=255)

    def __str__(self):
        return self.make

class Vehicle(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE,related_name='vehicles')
    number_plate=models.CharField(max_length=100)
    make=models.ForeignKey(CarMake)
    car_model=models.CharField(max_length=255,help_text="ex LandCruiser",blank=True)
    type=models.CharField(max_length=255,help_text="ex Car,Lorry",blank=True)

    fuel_choice=(
        ('Petrol','Petrol'),
        ('Diesel','Diesel'),
    )

    fuel_type=models.CharField(max_length=10,choices=fuel_choice)

    def __str__(self):

        return self.number_plate


class MechProfile(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='mechprofile',null=True)
    image=models.ImageField(blank=True,null=True)
    garage_name=models.CharField(max_length=255)
    desc=models.TextField(max_length=1000,help_text="write a small description about you")
    town=models.CharField(max_length=250,help_text="ex Nairobi,Nakuru,Rongai")
    estate=models.CharField(max_length=250,help_text="ex SouthB,Bahati")

    dental_removal=models.BooleanField(blank=True)
    car_spa=models.BooleanField(blank=True)
    interior_detailing=models.BooleanField(blank=True)
    general_service=models.BooleanField(blank=True)
    # user=models.OneToOneField(User,on_delete=models.CASCADE)


    county_choices=(
        ('N','Nairobi'),
        ('K','Kiambu'),
        ('M','Mombasa'),
        ('Nk','Nakuru'),
    )
    county=models.CharField(max_length=1,choices=county_choices)

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def __str__(self):
     return str(self.name)


class Review(models.Model):
    RATING_CHOICES=(
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        )
    mechprofile=models.ForeignKey(MechProfile)

    pub_date=models.DateTimeField('date published',auto_now_add=True)
    user_name = models.CharField(max_length=100)
    comment=models.CharField(max_length=200)
    rating=models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):

      return  str(self.mechprofile)

#our cluster stores a name and a list of users
#we leave the door open for users to belong to more than one cluster by using ManyToManyField
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])



class Repair(models.Model):
   mechanic=models.ForeignKey(MechProfile)
   vehicle=models.ForeignKey(Vehicle)
   mileage=models.IntegerField()
   date=models.DateTimeField(auto_now_add=True)
   regular_maintenance=models.TextField(help_text="update on regular maintenance",max_length=1000,blank=True)
   replace_part=models.TextField(help_text="part replaced",max_length=500,blank=True)
   repair_type=models.TextField(help_text="type of repair done",max_length=1000,blank=True)



class Price(models.Model):
    price=models.DecimalField(max_digits=10,decimal_places=2)
    date_set=models.DateTimeField(auto_now_add=True)

class Passenger(models.Model):
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    survived = models.BooleanField(blank=True)
    age = models.FloatField()
    ticket_class = models.PositiveSmallIntegerField()
    embarked = models.CharField(max_length=200)


class ClientRepairs(models.Model):
    name=models.CharField(max_length=200)
    created_on=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=200)
    car_model=models.CharField(max_length=200)
    license_plate=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=200)
    # Charges=models.IntegerField
    Issue=models.TextField(max_length=1000)


    def __str__(self):
        return str(self.license_plate)



# class RegularService(models.Model):
#    periodic_choice=(
#        ('E','Engine Oil'),
#        ('O','Oil filter'),
#        ('A','Air Filter'),
#        ('B','Breake'),
#        ('Cl','Clutch'),
#        ('C','Coolant'),
#
#    )
#
#    other_choice=(
#
#        ('B','Wheel Balancing'),
#        ('R','Wheel Rotation'),
#        ('A','Wheel Alignment'),
#    )
#
#    other_service=MultiSelectField(choices=other_choice)
#    periodic_service=MultiSelectField(choices=periodic_choice)



# class Painting(models.Model):
#     painting_choices=(
#         ('U','Undercoat Finishes'),
#         ('B','Base Coat Paints'),
#         ('A','Acyrlic lacquers'),
#         ('C','Clear Coat finishes'),
#         ('F','Full Body Painting'),
#         ('D','Dental Removals'),
#         ('R','Dry Dent removal on bumpers'),
#         ('E','Exhaust pipe welding/repair'),
#         ('W','Water leaks'),
#     )
#
#     painting_issues=MultiSelectField(choices=painting_choices)
#     other=models.TextField(max_length=3000,blank=True,help_text='other')
#
