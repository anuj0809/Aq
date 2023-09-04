from django.db import models

# Create your models here.
class audio(models.Model):
    audio_name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to="audio/")
    audio_size = models.IntegerField(null=True)
    audio_extension = models.CharField(max_length=50,null=True)
    audio_upload_date = models.DateTimeField(null=True)
    audio_length = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.audio_name