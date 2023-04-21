from django.db import models
import uuid
import os


def teams_image_file_path(instance, filename):
    """ Generate file path for new image """
    # get file extension
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    # This ensures that the path is created according to
    # the operating system that we are running on
    return os.path.join('uploads', 'img', filename)


class Team(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=teams_image_file_path)
    facebook_link = models.URLField(max_length=100)
    twitter_link = models.URLField(max_length=100)
    linked_in_link = models.URLField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        In admin panel will be shown the first name instead
        of the Team object reference
        """
        return self.first_name
