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
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name='vehicles')
    car_model=models.CharField(max_length=255)
    car_make=models.CharField(max_length=255)

    def __str__(self):

        return self.car_make


class MechProfile(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='mechprofile')
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


    def __str__(self):

     return self.garage_name


class CarHistory(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='history')
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

#we need to keep track of a cluster a user belongs to
#this is so that we will have a view that returns wines by cluster ID and not by a single user
# this whole process will give us wine suggestions that satisfy two conditions:
# 1. The requesting user has never reviewed those wines.
# 2. The wines have been reviewed positively by users within our cluster,that tend to score wines the sameway we do
class Wine(models.Model):
    name=models.CharField(max_length=200)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES=(
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        )
    mechanicname=models.ForeignKey(User,on_delete=models.CASCADE,related_name='mech')
    pub_date=models.DateTimeField('date published')
    customer_name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='review')
    comment=models.CharField(max_length=200)
    rating=models.IntegerField(choices=RATING_CHOICES)


#our cluster stores a name and a list of users
#we leave the door open for users to belong to more than one cluster by using ManyToManyField
class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
