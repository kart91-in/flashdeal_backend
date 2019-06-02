from django.contrib.auth.models import User
from django.db import models
from core.models import BaseModel

image_dir_path = 'images/%Y/%m/%d'
video_dir_path = 'videos/%Y/%m/%d'

class Image(BaseModel):

    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=image_dir_path)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.image and not self.name:
            self.name = self.image.name
        super().save(force_insert, force_update, using, update_fields)


class Video(BaseModel):

    name = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to=video_dir_path)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.video and not self.name:
            self.name = self.video.name
        super().save(force_insert, force_update, using, update_fields)