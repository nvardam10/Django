from django.db import models

# Create your models here.
class User_Details(models.Model):
    UserID=models.AutoField(primary_key=True)
    Username=models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)
    email_id =models.EmailField(unique=True)
    password=models.TextField()
    phone= models.CharField(max_length=12, unique=True)


    def __str__(self):
        return self.Username
    

class Movie_Details(models.Model):
    MovieID=models.AutoField(primary_key=True)
    Moviename=models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now = True)
    Movietype=models.CharField(max_length=100)
    Movieprice=models.IntegerField()

    def __str__(self):
        return self.Moviename


class Movie_Booking(models.Model):
    BookingID = models.AutoField(primary_key=True)
    # TODO - add foreign key here
    MovieID = models.ForeignKey(Movie_Details, on_delete=models.CASCADE)
    Movieprice=models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now=True)
    Quantity=models.PositiveIntegerField()
    # TODO - add foreign key here
    UserID = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False,editable=False)

    def __str__(self):
        return self.MovieBooking