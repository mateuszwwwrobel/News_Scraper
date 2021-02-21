from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, TemplateView
from .models import Article, portals
from bs4 import BeautifulSoup
import requests
import itertools


BENCHMARK_URL = 'https://www.benchmark.pl/'
WYKOP_URL = 'https://www.wykop.pl/'
ARCHEOLOGY_VIEW = 'https://www.zwiadowcahistorii.pl/'
TOJUZBYLO_VIEW = 'https://tojuzbylo.pl/aktualnosci'
COMPUTER_WORLD_WEB_VIEW ='https://www.computerworld.pl/'


class HomeView(TemplateView):
    template_name = 'homepage.html'


class BenchmarkView(View):
    def get(self, *args, **kwargs):

        benchmark_url = BENCHMARK_URL
        benchmark_response = requests.get(benchmark_url)
        benchmark_data = benchmark_response.text
        benchmark_soup = BeautifulSoup(benchmark_data, 'html.parser')
        benchmark_ready_soup = benchmark_soup.find_all('section')

        # SECTION 3 - NEWS:
        benchmark_final_elements_s3 = []

        section_3 = benchmark_ready_soup[3]
        section_3_divs = section_3.find_all('div')

        for post in section_3_divs[1:2]:
            # Scraping information
            benchmark_li = post.find_all('li')
            for element in benchmark_li:
                benchmark_title = element.find('a').text
                benchmark_href = element.find('a')['href']
                benchmark_url_maker = "http://benchmark.pl{}"
                benchmark_link = (benchmark_url_maker.format(benchmark_href))

                benchmark_final_elements_s3.append((benchmark_link, benchmark_title))

        # Creating Article
        check_if_article_already_exist(benchmark_final_elements_s3, portals[0][0])

        if len(benchmark_final_elements_s3) == 0:
            return render(
                self.request,
                'benchmark.html',
                {'benchmark_final_elements_s3': [('#', 'No data to view. Contact with administrator.')]}
            )

        context = {
            'benchmark_final_elements_s3': benchmark_final_elements_s3,
        }

        return render(self.request, 'benchmark.html', context)


class WykopView(View):
    def get(self, *args, **kwargs):
        wykop_url = WYKOP_URL
        wykop_response = requests.get(wykop_url)
        wykop_data = wykop_response.text
        wykop_soup = BeautifulSoup(wykop_data, 'html.parser')

        # SOUP with url and title:
        first_part_of_soup = wykop_soup.find_all("a", {"rel": 'noopener'})

        # <a> tag with href and title.
        shorter_first_part_of_soup = list(itertools.islice(first_part_of_soup, 1, None, 3))
        ready_first_part_of_soup = list(shorter_first_part_of_soup[3:])
        print(ready_first_part_of_soup)

        wykop_final_elements = []

        for items in ready_first_part_of_soup:
            wykop_link = items['href']
            wykop_title = items['title']

            wykop_final_elements.append((wykop_link, wykop_title))

        # Creating Article
        check_if_article_already_exist(wykop_final_elements, portals[1][1])

        if len(wykop_final_elements) == 0:
            return render(
                self.request,
                'wykop.html',
                {'wykop_final_elements': [('#', 'No data to view. Contact with administrator.')]}
            )

        context = {
            'wykop_final_elements': wykop_final_elements,
        }

        return render(self.request, 'wykop.html', context,)


class ArcheologyView(View):
    def get(self, *args, **kwargs):
        archeo_url = ARCHEOLOGY_VIEW
        archeo_response = requests.get(archeo_url)
        archeo_data = archeo_response.text
        archeo_soup = BeautifulSoup(archeo_data, 'html.parser')

        #SOUP with url and title and img:
        first_part_of_soup = archeo_soup.find_all("div", {"class": 'td_module_1 td_module_wrap td-animation-stack'})

        archeo_final_elements = []

        for item in first_part_of_soup:
            archeo_stuff = item.find_all('div', {'class': 'td-module-thumb'})
            for element in archeo_stuff:
                archeo_title = element.find('a')['title']
                archeo_link = element.find('a')['href']
                archeo_image = element.find('img')['data-img-url']
                archeo_final_elements.append((archeo_link, archeo_title, archeo_image))

        # Creating Article
        check_if_article_already_exist(archeo_final_elements, portals[3][1])

        if len(archeo_final_elements) == 0:
            return render(
                self.request,
                'wykop.html',
                {'archeo_final_elements': [('#', 'No data to view. Contact with administrator.')]}
            )

        context = {
            'archeo_final_elements': archeo_final_elements,
        }

        return render(self.request, 'archeology.html', context,)


class ToJuzByloView(View):
    def get(self, *args, **kwargs):
        tojuzbylo_url = TOJUZBYLO_VIEW
        tojuzbylo_response = requests.get(tojuzbylo_url)
        tojuzbylo_data = tojuzbylo_response.text
        tojuzbylo_soup = BeautifulSoup(tojuzbylo_data, 'html.parser')

        #SOUP:
        first_part_of_soup = tojuzbylo_soup.find_all('td', {'class': 'col-1 col-first'})


        tojuzbylo_final_elements = []

        for element in first_part_of_soup:
            tojuzbylo_title = element.find('h2', {'class': 'tytul'}).text
            tojuzbylo_href_and_image = element.find_all('div', {'class': 'picture'})


            for item in tojuzbylo_href_and_image:
                tojuzbylo_image = element.find('img')['src']
                tojuzbylo_href_body = element.find_all('a')[1]['href']
                tojuzbylo_href = f"https://tojuzbylo.pl/{tojuzbylo_href_body}"

                tojuzbylo_final_elements.append((tojuzbylo_href, tojuzbylo_title, tojuzbylo_image))

        # Creating Article
        check_if_article_already_exist(tojuzbylo_final_elements, portals[2][1])

        if len(tojuzbylo_final_elements) == 0:
            return render(
                self.request,
                'wykop.html',
                {'tojuzbylo_final_elements': [('#', 'No data to view. Contact with administrator.')]}
            )

        context = {
            'tojuzbylo_final_elements': tojuzbylo_final_elements,
        }

        return render(self.request, 'tojuzbylo.html', context,)


class ComputerWorldView(View):
    def get(self, *args, **kwargs):
        try:
            computer_world_url = COMPUTER_WORLD_WEB_VIEW
            computer_world_response = requests.get(computer_world_url)
            computer_world_data = computer_world_response.text
            computer_world_soup = BeautifulSoup(computer_world_data, 'html.parser')
            
            #SOUP:
            main_computer_world_soup = computer_world_soup.find('div', {'class': 'left-side'})
            ingredient_one = main_computer_world_soup.find_all('div', {'class': 'row-item-icon'})    

            computer_world_final_elements = []

            for element in ingredient_one:
                computer_world_image = element.find('img', {'class': 'img-fluid'})['src']
                computer_world_href_1 = element.find('a')['href']
                computer_world_href = f"https://www.computerworld.pl{computer_world_href_1}"
                computer_world_title = element.find('a')['href'].split(',')[0].split('/')[2].replace('-', (' '))

                computer_world_final_elements.append((computer_world_href, computer_world_title, computer_world_image))

            # Creating Article
            check_if_article_already_exist(computer_world_final_elements, portals[4][1])

            if len(computer_world_final_elements) == 0:
                return render(
                    self.request,
                    'wykop.html',
                    {'computer_world_final_elements': [('#', 'No data to view. Contact with administrator.')]}
                )
            
            context = {
                'computer_world_final_elements': computer_world_final_elements,
            }
            
            
            return render(self.request, 'computer_world_news.html', context,)

        except ObjectDoesNotExist:
            messages.warning(self.request, "Something is wrong.")
            return redirect("/")


def check_if_article_already_exist(posts_list, portal) -> None:
    all_articles = Article.objects.filter(portal=portal)
    article_list = []
    [article_list.append(article.url) for article in all_articles]

    for post in posts_list:
        if post[0] in article_list:
            continue
        else:
            create_article(post[1], post[0], portal)


def create_article(title, url, portal) -> None:
    if title == '' or url == '':
        pass
    else:
        article = Article(
            portal=portal,
            title=title,
            url=url,
        )
        article.save()


    # soup.find_all(lambda tag: tag.name == 'p' and 'et' in tag.text)
