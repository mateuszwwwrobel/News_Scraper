from django.db import models

portals = (
    ('Benchmark.pl', 'Benchmark.pl'),
    ('Wykop.pl', 'Wykop.pl'),
    ('Tojuzbylo.pl', 'Tojuzbylo.pl'),
    ('Zwiadowca Historii', 'Zwiadowca Historii'),
    ('Computer World', 'Computer World'),
)


class Article(models.Model):
    portal = models.CharField(max_length=100, choices=portals)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=50, default='Author')
    date_created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    def __str__(self):
        return f'{self.portal} - {self.title}'
