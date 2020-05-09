from django.db import models

# Create your models here.


class Benchmark(models.Model):
    article_title = models.CharField(max_length=256)
    article_date = models.DateField(auto_now=False, auto_now_add=False)
    article_author = models.CharField(max_length=100)
    article_url = models.URLField()
 
    def __str__(self):
        return self.article_title


class Wykop(models.Model):
    article_title = models.CharField(max_length=256)
    article_date = models.DateField(auto_now=False, auto_now_add=False)
    article_author = models.CharField(max_length=100)
    article_url = models.URLField()
    article_image = models.URLField()
 
    def __str__(self):
        return self.article_title



