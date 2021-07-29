from django.db import models
from django.db.models import ForeignKey
from django.db.models.aggregates import Count
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField
from django.db.models.base import Model
from django.db.models.expressions import F

class BookQuerySet(models.QuerySet):
    def author_books(self):
        return self.annotate(author_books=Count('author__books'))

    def author_name(self):
        return self.annotate(author_name=F('author__name'))

    def amount(self):
        return self.aggregate(amount=Count('id'))


class BookManager(models.Manager.from_queryset(BookQuerySet)):
    def get_queryset(self):
        return super().get_queryset()

class Author(Model):
    name = CharField(max_length=255)

class Book(Model):
    custom_objects = BookManager()
    name = CharField(max_length=255)
    author = ForeignKey(Author, CASCADE, related_name='books')