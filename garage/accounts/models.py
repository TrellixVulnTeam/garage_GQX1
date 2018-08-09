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

#
# class CarMake(models.Model):
#     make=models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.make


class Make(models.Model):
    make=models.CharField(max_length=255)

    def __str__(self):
        return self.make

class Vehicle(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner')
    vehicle_name=models.CharField(max_length=25,help_text="Enter a name/nickname to distinguish the vehicle",unique=True)
    number_plate=models.CharField(max_length=100)
    #make=models.ForeignKey(Make)
    car_model=models.CharField(max_length=255,help_text="ex LandCruiser",blank=True)
    type=(
        ('Car','Car'),
        ('Lorry','Lorry'),
        ('MotorCycle','MotorCycle'),
        ('ForkLift','ForkLift'),
        ('Bus','Bus'),
        ('Boat','Boat'),
        ('Van','Van'),

    )

    type=models.CharField(max_length=10,choices=type)
    image=models.ImageField(blank=True,null=True,upload_to = 'media/',height_field=None)
    image1=models.ImageField(blank=True,null=True,upload_to = 'media/',height_field=None,help_text="Add photo")
    image2=models.ImageField(blank=True,null=True,upload_to = 'media/',height_field=None,help_text="Add photo")
    ownership=(
        ('Owned','Owned'),
        ('leased','leased'),
        ('Rented','Rented'),

    )

    ownership=models.CharField(max_length=10,choices=ownership,blank=False)
    status=(
        ('Sold','sold'),
        ('Inactive','Inactive'),
        ('Inactive','Inactive'),
        ('Active','Active'),

    )

    status=models.CharField(max_length=10,choices=status)

    def __str__(self):

        return self.vehicle_name


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

   repair_priority=(
        ('High','high'),
        ('medium','medium'),
        ('low','low'),
    )

   #user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
   vehicle=models.ForeignKey(Vehicle)
   date=models.DateTimeField(auto_now_add=True)
   summary=models.TextField(max_length=100,blank=True,help_text="Brief overview of the issue")
   mileage=models.IntegerField()
   image=models.ImageField(blank=True,null=True,help_text='You can upload a photo here')
   description=models.TextField(help_text="update on regular maintenance",max_length=1000,blank=True)
   priority=models.CharField(max_length=10,choices=repair_priority)





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


class Dashboard(models.Model):
    repair=models.ForeignKey(Repair)


class Contact(models.Model):
    group_choice=(
        ('driver','driver'),
        ('mechanic','mechanic'),
    )

    first_name=models.CharField(max_length=20,blank=False)
    last_name=models.CharField(max_length=50,blank=True)
    phone_number=models.IntegerField(blank=False)
    group=models.CharField(max_length=10,choices=group_choice,blank=True)
    image=models.ImageField(blank=True,null=True)
    file=models.FileField(blank=True,null=True)
