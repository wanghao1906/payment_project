from django.db import models


# Create your models here.
class User(models.Model):
    #user_id = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    deposit = models.FloatField()
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Bill(models.Model):
    #Records_Id = models.IntegerField()
    Time = models.DateTimeField()
    Recipient = models.CharField(max_length=45)
    Amount = models.IntegerField()
    Money = models.FloatField()
    secret_key = models.CharField(max_length=45)
    User_Id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User_Id')
    Airline_order = models.CharField(max_length=45)
    State = models.BooleanField()

    def __str__(self):
        return self.Recipient
