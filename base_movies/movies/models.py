from django.db import models
from django.contrib.auth.models import User

import uuid
# Create your models here.



class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Movie(models.Model):
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE,null=True)
    uuid = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    