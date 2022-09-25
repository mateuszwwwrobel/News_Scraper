from collections import Counter
from random import randint

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import Article, portals, languages
from utils.utils import parse_a_website


BENCHMARK_URL = 'https://www.benchmark.pl/'
BGG_URL = 'https://boardgamegeek.com/blog/1/boardgamegeek-news'
ZWIAD_HISTORII_URL = 'https://www.zwiadowcahistorii.pl/'
TOJUZBYLO_URL = 'https://tojuzbylo.pl/aktualnosci'
COMPUTER_WORLD_WEB_URL = 'https://www.computerworld.pl/'
PYTHON_WEB_URL = 'https://www.infoworld.com/uk/category/python/'
REAL_PYTHON_WEB_URL = 'https://realpython.com/'
LIVESCIENCE_URL = 'https://livescience.com/'


class HomeView(TemplateView):
    template_name = 'homepage.html'


class StatisticsView(View):
    def get(self, request):
        return render(self.request, 'statistics.html')

    def get_all_article_pie_chart_data(self):
        all_articles = list(Article.objects.all().values_list('portal', flat=True))
        articles = Counter(all_articles)

        colors = []
        for color in range(len(articles)):
            color = '#%06x' % randint(0, 0xFFFFFF)
            colors.append(color)

        context = {
            'labels': list(articles.keys()),
            'data': list(articles.values()),
            'colors': colors,
        }

        return JsonResponse(data=context)

    def get_all_article_tab_chart_data(self):
        all_articles = list(Article.objects.all().values_list('portal', flat=True))
        articles = Counter(all_articles)
        sorted_articles = dict(sorted(articles.items(), key=lambda item: item[1], reverse=True))

        colors = []
        for color in range(len(articles)):
            color = '#%06x' % randint(0, 0xFFFFFF)
            colors.append(color)

        context = {
            'labels': list(sorted_articles.keys()),
            'data': list(sorted_articles.values()),
            'colors': colors,
        }

        return JsonResponse(data=context)

    def get_top_en_word_chart_data(self):
        all_titles = list(Article.objects.filter(language='ENG').values_list('title', flat=True))

        top_words = []
        for title in all_titles:
            split_title = title.split(' ')
            for word in split_title:
                if len(word) > 3:
                    top_words.append(word.lower())

        count_top_words = Counter(top_words)
        sorted_words = dict(sorted(count_top_words.items(), key=lambda item: item[1], reverse=True))

        colors = []
        for color in range(10):
            color = '#%06x' % randint(0, 0xFFFFFF)
            colors.append(color)

        context = {
            'labels': list(sorted_words.keys())[:10],
            'data': list(sorted_words.values())[:10],
            'colors': colors,
        }

        return JsonResponse(data=context)

    def get_top_pl_word_chart_data(self):
        all_titles = list(Article.objects.filter(language='PL').values_list('title', flat=True))

        top_words = []
        for title in all_titles:
            split_title = title.split(' ')
            for word in split_title:
                if len(word) > 3:
                    top_words.append(word.lower())

        count_top_words = Counter(top_words)
        sorted_words = dict(sorted(count_top_words.items(), key=lambda item: item[1], reverse=True))

        colors = []
        for color in range(10):
            color = '#%06x' % randint(0, 0xFFFFFF)
            colors.append(color)

        context = {
            'labels': list(sorted_words.keys())[:10],
            'data': list(sorted_words.values())[:10],
            'colors': colors,
        }

        return JsonResponse(data=context)


class BenchmarkView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(BENCHMARK_URL)
        sections = soup.find_all('section')
        section_3 = sections[4]
        section_3_divs = section_3.find_all('div')

        data = []
        for div in section_3_divs[1:2]:
            benchmark_li = div.find_all('li')
            for li in benchmark_li:
                title = (li.find('a').text).split('\t\t\t')[1].split('\n')[0]
                url = f"http://benchmark.pl{li.find('a')['href']}"
                data.append((url, title))

        Article.check_if_article_already_exist(data, 'Benchmark.pl', 'PL')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'benchmark.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'benchmark.html', context)


class BoardGamesGeekView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(BGG_URL)
        posts = soup.find_all("h3", {"class": 'post_title'})

        data = []
        for post in posts:
            title = post.find('a').text
            url = f"https://boardgamegeek.com{post.find('a')['href']}"
            data.append((url, title))

        Article.check_if_article_already_exist(data, 'boardgamesgeek.com', 'ENG')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'bgg.html', context)

        context = {'data': data}

        return render(self.request, 'bgg.html', context,)


class ArcheologyView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(ZWIAD_HISTORII_URL)
        divs_1 = soup.find_all("div", {"class": 'td_module_1 td_module_wrap td-animation-stack'})

        data = []
        for div in divs_1:
            divs_2 = div.find_all('div', {'class': 'td-module-thumb'})
            for element in divs_2:
                title = element.find('a')['title']
                url = element.find('a')['href']
                img = element.find('img')['data-img-url']
                data.append((url, title, img))

        Article.check_if_article_already_exist(data, 'Zwiadowca Historii', 'PL')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'archeology.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'archeology.html', context)


class ToJuzByloView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(TOJUZBYLO_URL)
        tds = soup.find_all('td', {'class': 'col-1 col-first'})

        data = []
        for td in tds:
            title = (td.find('h2', {'class': 'tytul'}).text).split('\n')[1]
            img = td.find('img')['src']
            href = td.find_all('a')[1]['href']
            url = f"https://tojuzbylo.pl/{href}"
            data.append((url, title, img))

        Article.check_if_article_already_exist(data, 'Tojuzbylo.pl', 'PL')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'tojuzbylo.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'tojuzbylo.html', context,)


class ComputerWorldView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(COMPUTER_WORLD_WEB_URL)
        main_div = soup.find('div', {'class': 'left-side'})
        divs = main_div.find_all('div', {'class': 'row-item-icon'})

        data = []
        for div in divs:
            img = div.find('img', {'class': 'img-fluid'})['src']
            url = f"https://www.computerworld.pl{div.find('a')['href']}"
            title = div.find('a')['href'].split(',')[0].split('/')[2].replace('-', ' ')
            data.append((url, title, img))

        Article.check_if_article_already_exist(data, 'Computer World', 'PL')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'computer_world_news.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'computer_world_news.html', context,)


class PythonView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(PYTHON_WEB_URL)
        divs = soup.find_all('div', {'class': 'post-cont'})
        figs = soup.find_all('figure', {'class': 'well-img'})

        data = []
        for div, figure in zip(divs, figs):
            title = div.find('a').text
            url = f"https://www.infoworld.com{div.find('a')['href']}"
            img = figure.find('img')['data-original']
            data.append((url, title, img))

        Article.check_if_article_already_exist(data, 'InfoWorldPython.com', 'ENG')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'python.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'python.html', context)


class RealPythonView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(REAL_PYTHON_WEB_URL)
        posts = soup.find_all('div', {'class': 'card border-0'})

        data = []
        for post in posts:
            a_tags = post.find_all('a')[0]
            title = a_tags.find('img')['alt']
            img = a_tags.find('img')['src']
            url = f"https://realpython.com{a_tags['href']}"
            data.append((url, title, img))

        Article.check_if_article_already_exist(data, 'RealPython.com', 'ENG')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'real_python.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'real_python.html', context)


class LiveScienceView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(LIVESCIENCE_URL)

        posts = soup.find_all('div', {'class': 'listingResult'})
        data = []
        for post in posts[:-3]:
            if post.find('a'):
                url = post.find('a')['href']
                title = post.find('a')['aria-label']
                img = post.find('figure')['data-original']
                data.append((url, title, img))

        Article.check_if_article_already_exist(data, 'livescience.com', 'ENG')

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'livescience.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'livescience.html', context)
