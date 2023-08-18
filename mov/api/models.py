from django.db import models

# Create your models here.
class UserDetails(models.Model):
    UserID=models.AutoField(primary_key=True)
    Username=models.CharField(max_length=100)
    date_added = models.DateField(auto_now = True)
    email_id =models.EmailField(unique=True)
    password=models.TextField()

    def __str__(self):
        return self.Username
    

class MovieDetails(models.Model):
    MovieID=models.AutoField(primary_key=True)
    Moviename=models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    Movietype=models.CharField(max_length=100)
    Movieprice=models.IntegerField(default=100)

    def __str__(self):
        return self.Moviename

class MovieBooking(models.Model):
    BookingID = models.AutoField(primary_key=True)
    MovieID=models.IntegerField()
    Movieprice=models.IntegerField(default=100)
    date_added = models.DateField(auto_now_add=True)
    Quantity=models.IntegerField(default=1)
    UserID=models.IntegerField(default=1)

    def __str__(self):
        return self.MovieBooking