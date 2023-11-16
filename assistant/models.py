from django.db import models
import os
from datetime import datetime

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        timestamp = str(int(datetime.now().timestamp() * 1000))
        filename = '{}.{}'.format(timestamp, ext)
        return os.path.join(path, filename)

    return wrapper

class UploadModel(models.Model):
    file = models.FileField("Attachment", upload_to=path_and_rename("uploaded_files"), help_text='browse a file')