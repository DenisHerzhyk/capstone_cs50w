from django.db import models

# Create your models here.
class File(models.Model):
    FILE_TYPE_CHOICE = (
        ("extracted", "Extracted"),
        ("attached", "Attached")
    )
    content_type = models.CharField(max_length=50)
    file_format = models.CharField(max_length=20)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICE)
    file_name = models.CharField(max_length=500)
    file_location = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_location
    

class TextInput(models.Model):
    text_content = models.CharField(max_length=5000)

    def __str__(self):
        return "TEXT_CONTENT"