from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, TemplateView
from .models import Article, portals
from utils.utils import parse_a_website


BENCHMARK_URL = 'https://www.benchmark.pl/'
BGG_URL = 'https://boardgamegeek.com/blog/1/boardgamegeek-news'
ZWIAD_HISTORII_URL = 'https://www.zwiadowcahistorii.pl/'
TOJUZBYLO_URL = 'https://tojuzbylo.pl/aktualnosci'
COMPUTER_WORLD_WEB_URL = 'https://www.computerworld.pl/'
PYTHON_WEB_URL = 'https://www.infoworld.com/uk/category/python/'
REAL_PYTHON_WEB_URL = 'https://realpython.com/'
BUSHCRAFTABLE_URL = 'https://bushcraftable.com/'

class HomeView(TemplateView):
    template_name = 'homepage.html'


class BenchmarkView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(BENCHMARK_URL)

        # Getting data from soup
        data = []

        sections = soup.find_all('section')
        section_3 = sections[3]
        section_3_divs = section_3.find_all('div')

        for div in section_3_divs[1:2]:
            benchmark_li = div.find_all('li')
            for li in benchmark_li:
                title = li.find('a').text
                href = li.find('a')['href']
                url = f"http://benchmark.pl{href}"

                data.append((url, title))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[0][0])

        # Check if data not empty
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

        # Getting data from soup
        data = []
        posts = soup.find_all("h3", {"class": 'post_title'})

        for post in posts:
            bgg_post_title = post.find('a').text
            bgg_post_link = post.find('a')['href']
            data.append((bgg_post_link, bgg_post_title))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[1][1])

        # Check if data not empty
        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'bgg.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'bgg.html', context,)


class ArcheologyView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(ZWIAD_HISTORII_URL)

        # Getting data from soup
        data = []
        divs_1 = soup.find_all("div", {"class": 'td_module_1 td_module_wrap td-animation-stack'})

        for div in divs_1:
            divs_2 = div.find_all('div', {'class': 'td-module-thumb'})
            for element in divs_2:
                title = element.find('a')['title']
                url = element.find('a')['href']
                img = element.find('img')['data-img-url']
                data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[3][1])

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

        # Getting data from soup
        data = []
        tds = soup.find_all('td', {'class': 'col-1 col-first'})

        for td in tds:
            title = td.find('h2', {'class': 'tytul'}).text
            img = td.find('img')['src']
            href = td.find_all('a')[1]['href']
            url = f"https://tojuzbylo.pl/{href}"
            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[2][1])

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

        # Getting data from soup
        data = []
        main_div = soup.find('div', {'class': 'left-side'})
        divs = main_div.find_all('div', {'class': 'row-item-icon'})

        for div in divs:
            img = div.find('img', {'class': 'img-fluid'})['src']
            href = div.find('a')['href']
            url = f"https://www.computerworld.pl{href}"
            title = div.find('a')['href'].split(',')[0].split('/')[2].replace('-', ' ')

            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[4][1])

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

        # Getting data from soup
        data = []
        divs = soup.find_all('div', {'class': 'post-cont'})
        figs = soup.find_all('figure', {'class': 'well-img'})

        for div, figure in zip(divs, figs):
            href = div.find('a')['href']
            title = div.find('a').text
            url = f'https://www.infoworld.com{href}'
            img = figure.find('img')['data-original']

            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[5][1])

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

        # Getting data from soup
        data = []

        posts = soup.find_all('div', {'class': 'card border-0'})

        for post in posts:
            a_tags = post.find_all('a')[0]
            title = a_tags.find('img')['alt']
            img = a_tags.find('img')['src']
            url = a_tags['href']
            data.append((url, title, img))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[6][1])

        if len(data) == 0:
            context = {'data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'real_python.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'real_python.html', context)



# soup.find_all(lambda tag: tag.name == 'p' and 'et' in tag.text)

# TODO: Widok statystyk. Obliczenie ilości artykułów i piechart na widoku statystycznym,

# TODO: Uporządkowanie navbaru. Footera? Frontend.

# TODO: Settingsy porownac do django projektu KWL/Inforshare i pozmieniać.