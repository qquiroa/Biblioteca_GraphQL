from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=30)
    birth_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    year = models.IntegerField()
    existence = models.IntegerField()
    author = models.ManyToManyField(Author)
    
    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField()
    quantity = models.IntegerField()
    user_client = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    done_date = models.DateField(null=True)