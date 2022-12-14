from enum import auto
from django.db import models
from django.forms import DateField
from django.urls import reverse
from datetime import datetime, date  
from django.contrib.auth.models import User


RATINGS = (
    ('E', 'Excellent'),
    ('VG', 'Very Good'),
    ('G', 'Good'),
    ('A', 'Average'),
    ('B', 'Bad'),
    ('VB', 'Very Bad'),
    ('S', 'Stay Away')
)

class ProfilePicture(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo created for {self.user.username}"


class PropertyFeature(models.Model):
    feature = models.CharField(
        max_length=30,
    )
    
    def __str__(self):
        return f"{self.feature}"
    
    class Meta:
        ordering = ['feature']


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1200)
    location = models.CharField(max_length=100)
    property_features = models.ManyToManyField(PropertyFeature)
    price = models.FloatField()
    date_listed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on {self.date_listed}"

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'property_id': self.id})

    class Meta:
        ordering = ['-date_listed']


class Photo(models.Model):
    photo_url = models.CharField(max_length=200)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Photo created for {self.property.title} on {self.date_created}"

    class Meta:
        ordering = ['date_created']


class Availability(models.Model):
    from_date = models.DateField('Available from')
    till_date = models.DateField('Available till')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.from_date} to {self.till_date} for {self.property.title}"

    class Meta:
        ordering = ['from_date']
    
    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'property_id': self.property.id})


class Like(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.user.username} likes {self.property.title}"


class Review(models.Model):
    user_name = models.CharField(max_length=100)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating = models.CharField(
        max_length=2,
        choices = RATINGS,
    )
    review_text = models.TextField(max_length=800)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"By {self.user_name} on {self.date}"

    class Meta:
        ordering = ['-date']


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete = models.CASCADE)
    property = models.ForeignKey(Property, on_delete = models.CASCADE)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user} made reservation on {self.availability} "
    
    class Meta:
        ordering = ['date']