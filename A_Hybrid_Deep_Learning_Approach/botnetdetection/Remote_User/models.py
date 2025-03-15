from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    gender= models.CharField(max_length=30)
    address= models.CharField(max_length=30)


class bottleneck_detection(models.Model):

    ID1= models.CharField(max_length=3000)
    Sender_IP= models.CharField(max_length=3000)
    Sender_Port= models.CharField(max_length=3000)
    Target_IP= models.CharField(max_length=3000)
    Target_Port= models.CharField(max_length=3000)
    Transport_Protocol= models.CharField(max_length=3000)
    Duration= models.CharField(max_length=3000)
    AvgDuration= models.CharField(max_length=3000)
    PBS= models.CharField(max_length=3000)
    AvgPBS= models.CharField(max_length=3000)
    TBS= models.CharField(max_length=3000)
    PBR= models.CharField(max_length=3000)
    AvgPBR= models.CharField(max_length=3000)
    TBR= models.CharField(max_length=3000)
    Missed_Bytes= models.CharField(max_length=3000)
    Packets_Sent= models.CharField(max_length=3000)
    Packets_Received= models.CharField(max_length=3000)
    SRPR= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



