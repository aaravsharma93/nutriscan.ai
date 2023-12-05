from django.db import models
import uuid
from uuid import uuid4


class AudioList(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    song_name     = models.CharField(max_length=50)
    duration      = models.IntegerField()
    uploaded_time = models.DateField(auto_now_add=True)
    file_path     = models.FileField(upload_to="music", max_length=100)

    def __str__(self):
        return self.song_name