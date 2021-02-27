from django.db import models

portals = (
    ('Benchmark.pl', 'Benchmark.pl'),
    ('boardgamesgeek.com', 'boardgamesgeek.com'),
    ('Tojuzbylo.pl', 'Tojuzbylo.pl'),
    ('Zwiadowca Historii', 'Zwiadowca Historii'),
    ('Computer World', 'Computer World'),
    ('InfoWorldPython.com', 'InfoWorldPython.com'),
    ('RealPython.com', 'RealPython.com'),

)


class Article(models.Model):
    portal = models.CharField(max_length=100, choices=portals)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=50, default='Author')
    date_created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    def __str__(self):
        return f'{self.portal} - {self.title}'

    @classmethod
    def check_if_article_already_exist(cls, posts_list, portal) -> None:
        all_articles = Article.objects.filter(portal=portal)
        article_list = []
        [article_list.append(article.url) for article in all_articles]

        for post in posts_list:
            if post[0] in article_list:
                continue
            else:
                cls.save_article(post[1], post[0], portal)

    @classmethod
    def save_article(cls, title, url, portal) -> None:
        if title == '' or url == '':
            pass
        else:
            article = Article(
                portal=portal,
                title=title,
                url=url,
            )
            article.save()
