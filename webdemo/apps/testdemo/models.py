from django.db import models

# Create your models here.


class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=225)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.EmailField()
    def __str__(self):
        return self.name


class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    prince = models.DecimalField(max_digits=5,decimal_places=2)
    publish = models.ForeignKey(to="Publish",related_name='book',related_query_name='book',on_delete=models.CASCADE)
    #book.objects.filter('book__nid') 如果存在related_query_name 只能 publish.objects.get() obj.book
    authors = models.ManyToManyField(to='Author')


