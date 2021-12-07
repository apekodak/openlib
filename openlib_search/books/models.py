from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class FavouriteBook(models.Model):
    user = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='name', unique=True)
    image = models.CharField(max_length=200, null=True)
    author_name = models.CharField(max_length=200, null=True, blank=True)
    key = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'id': self.key})

    def get_delete_url(self):
        return reverse('books:favourite-delete', kwargs={'id': self.key})
