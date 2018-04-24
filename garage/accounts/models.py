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

class Vehicle(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE,related_name='vehicles')
    car_model=models.CharField(max_length=255)
    car_make=models.CharField(max_length=255)

    def __str__(self):

        return self.car_make


class MechProfile(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='mechprofile',null=True)
    profile_photo=models.ImageField(upload_to = 'img/',)
    garage_name=models.CharField(max_length=255)
    desc=models.TextField(max_length=1000,help_text="write a small description about you")

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


class CarHistory(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='history')
    service_date= models.DateTimeField(null=True)
    mechanic_name=models.CharField(max_length=20)
    service_choice=(
        ('P','PanelBeating'),
        ('W','ElectricalWiring'),
        ('E','Engine'),
        ('Pa','Painting'),
        ('G','GeneralMaintenance'),
    )
    service=MultiSelectField(choices=service_choice,max_length=5,max_choices=5)
    garage_location=models.CharField(max_length=255,help_text='location where car has been serviced')
    New_Car_Part=models.CharField(max_length=255,help_text='New car part replaced')
    Part_Cost=models.IntegerField(help_text='price of car part')
    location=models.CharField(max_length=20)
    repair_done=models.TextField(max_length=1000,help_text='small description of repair done')
    service_cost=models.IntegerField(help_text='total cost of repair')
    # mechanic_phoneno=RegexValidator(phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))




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


#our cluster stores a name and a list of users
#we leave the door open for users to belong to more than one cluster by using ManyToManyField
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
