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

class HomeView(TemplateView):
    template_name = 'homepage.html'


class BenchmarkView(View):
    def get(self, *args, **kwargs):
        benchmark_soup = parse_a_website(BENCHMARK_URL)

        # Getting data from soup
        benchmark_data = []

        sections = benchmark_soup.find_all('section')
        section_3 = sections[3]
        section_3_divs = section_3.find_all('div')

        for post in section_3_divs[1:2]:
            benchmark_li = post.find_all('li')
            for element in benchmark_li:
                benchmark_title = element.find('a').text
                benchmark_href = element.find('a')['href']
                benchmark_url = f"http://benchmark.pl{benchmark_href}"

                benchmark_data.append((benchmark_url, benchmark_title))

        # Creating Article
        Article.check_if_article_already_exist(benchmark_data, portals[0][0])

        # Check if data not empty
        if len(benchmark_data) == 0:
            context = {'benchmark_data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'benchmark.html', context)

        context = {
            'benchmark_data': benchmark_data,
        }
        return render(self.request, 'benchmark.html', context)


class BoardGamesGeekView(View):
    def get(self, *args, **kwargs):
        bgg_soup = parse_a_website(BGG_URL)

        # Getting data from soup
        bgg_data = []
        posts = bgg_soup.find_all("h3", {"class": 'post_title'})

        for items in posts:
            bgg_post_title = items.find('a').text
            bgg_post_link = items.find('a')['href']
            bgg_data.append((bgg_post_link, bgg_post_title))

        # Creating Article
        Article.check_if_article_already_exist(bgg_data, portals[1][1])

        # Check if data not empty
        if len(bgg_data) == 0:
            context = {'bgg_data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'bgg.html', context)

        context = {
            'bgg_data': bgg_data,
        }
        return render(self.request, 'bgg.html', context,)


class ArcheologyView(View):
    def get(self, *args, **kwargs):
        zwiad_historii_soup = parse_a_website(ZWIAD_HISTORII_URL)

        # Getting data from soup
        zwiad_historii_data = []
        data = zwiad_historii_soup.find_all("div", {"class": 'td_module_1 td_module_wrap td-animation-stack'})

        for item in data:
            archeo_stuff = item.find_all('div', {'class': 'td-module-thumb'})
            for element in archeo_stuff:
                archeo_title = element.find('a')['title']
                archeo_link = element.find('a')['href']
                archeo_image = element.find('img')['data-img-url']
                zwiad_historii_data.append((archeo_link, archeo_title, archeo_image))

        # Creating Article
        Article.check_if_article_already_exist(zwiad_historii_data, portals[3][1])

        if len(zwiad_historii_data) == 0:
            context = {'zwiad_historii_data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'archeology.html', context)

        context = {
            'zwiad_historii_data': zwiad_historii_data,
        }
        return render(self.request, 'archeology.html', context)


class ToJuzByloView(View):
    def get(self, *args, **kwargs):
        tojuzbylo_soup = parse_a_website(TOJUZBYLO_URL)

        # Getting data from soup
        tojuzbylo_data = []
        first_part_of_soup = tojuzbylo_soup.find_all('td', {'class': 'col-1 col-first'})

        for element in first_part_of_soup:
            tojuzbylo_title = element.find('h2', {'class': 'tytul'}).text
            tojuzbylo_image = element.find('img')['src']
            tojuzbylo_href_body = element.find_all('a')[1]['href']
            tojuzbylo_href = f"https://tojuzbylo.pl/{tojuzbylo_href_body}"
            tojuzbylo_data.append((tojuzbylo_href, tojuzbylo_title, tojuzbylo_image))

        # Creating Article
        Article.check_if_article_already_exist(tojuzbylo_data, portals[2][1])

        if len(tojuzbylo_data) == 0:
            context = {'tojuzbylo_data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'tojuzbylo.html', context)

        context = {
            'tojuzbylo_data': tojuzbylo_data,
        }
        return render(self.request, 'tojuzbylo.html', context,)


class ComputerWorldView(View):
    def get(self, *args, **kwargs):
        computer_world_soup = parse_a_website(COMPUTER_WORLD_WEB_URL)

        # Getting data from soup
        computer_world_data = []
        main_computer_world_soup = computer_world_soup.find('div', {'class': 'left-side'})
        ingredient_one = main_computer_world_soup.find_all('div', {'class': 'row-item-icon'})

        for element in ingredient_one:
            computer_world_image = element.find('img', {'class': 'img-fluid'})['src']
            computer_world_href_1 = element.find('a')['href']
            computer_world_url = f"https://www.computerworld.pl{computer_world_href_1}"
            computer_world_title = element.find('a')['href'].split(',')[0].split('/')[2].replace('-', (' '))

            computer_world_data.append((computer_world_url, computer_world_title, computer_world_image))

        # Creating Article
        Article.check_if_article_already_exist(computer_world_data, portals[4][1])

        if len(computer_world_data) == 0:
            context = {'computer_world_data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'computer_world_news.html', context)

        context = {
            'computer_world_data': computer_world_data,
        }
        return render(self.request, 'computer_world_news.html', context,)


class PythonView(View):
    def get(self, *args, **kwargs):
        python_soup = parse_a_website(PYTHON_WEB_URL)

        # Getting data from soup
        python_data = []
        python_divs = python_soup.find_all('div', {'class': 'post-cont'})
        python_figs = python_soup.find_all('figure', {'class': 'well-img'})

        for div, figure in zip(python_divs, python_figs):
            python_href = div.find('a')['href']
            python_title = div.find('a').text
            python_url = f'https://www.infoworld.com{python_href}'
            python_image = figure.find('img')['data-original']

            python_data.append((python_url, python_title, python_image))

        # Creating Article
        Article.check_if_article_already_exist(python_data, portals[5][1])

        if len(python_data) == 0:
            context = {'python_data': [('#', 'No data to view. Contact with administrator.')]}
            return render(self.request, 'computer_world_news.html', context)

        context = {
            'python_data': python_data,
        }
        return render(self.request, 'python.html', context)


class RealPythonView(View):
    def get(self, *args, **kwargs):
        soup = parse_a_website(REAL_PYTHON_WEB_URL)

        # Getting data from soup
        data = []

        posts = soup.find_all('div', {'class': 'card border-0'})
        print(posts)

        # data.append((url, title, image))

        # Creating Article
        Article.check_if_article_already_exist(data, portals[6][1])

        # if len(data) == 0:
        #     context = {'data': [('#', 'No data to view. Contact with administrator.')]}
        #     return render(self.request, 'computer_world_news.html', context)

        context = {
            'data': data,
        }
        return render(self.request, 'real_python.html', context)


# soup.find_all(lambda tag: tag.name == 'p' and 'et' in tag.text)


# TODO: new pages: jakas z board games? bushcraftowa moze? jakas Pythonowa? IT? Wykop wylatuje na produkcje.

# TODO: Widok statystyk. Obliczenie ilości artykułów i piechart na widoku statystycznym,

# TODO: Uporządkowanie navbaru. Footera? Frontend.

# TODO: Settingsy porownac do django projektu KWL/Inforshare i pozmieniać.