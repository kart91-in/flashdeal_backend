from django.contrib.auth.models import User
from django.db import models
from core.models import BaseModel

image_dir_path = 'images/%Y/%m/%d'
video_dir_path = 'videos/%Y/%m/%d'

class Image(BaseModel):

    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    image = models.ImageField(upload_to=image_dir_path)


class Video(BaseModel):

    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    video = models.FileField(upload_to=video_dir_path)
