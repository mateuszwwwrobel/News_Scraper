from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from .models import Benchmark, Wykop
from bs4 import BeautifulSoup
import requests
import itertools

# Create your views here.

BENCHMARK_URL = 'https://www.benchmark.pl/'
WYKOP_URL = 'https://www.wykop.pl/'
ARCHEOLOGY_VIEW = 'https://www.zwiadowcahistorii.pl/'
TOJUZBYLO_VIEW = 'https://tojuzbylo.pl/aktualnosci'
SPIDERS_WEB_VIEW ='https://www.spidersweb.pl/kategoria/glowna'


def home_view(request):
    return render(request, "homepage.html")


class BenchmarkView(View):
    def get(self, *args, **kwargs):
        try:
            benchmark_url = BENCHMARK_URL
            benchmark_response = requests.get(benchmark_url)
            benchmark_data = benchmark_response.text
            benchmark_soup = BeautifulSoup(benchmark_data, 'html.parser')
            benchmark_url_maker = "http://benchmark.pl{}"

            benchmark_final_elements_s1 = []
            

            benchmark_ready_soup = benchmark_soup.find_all('section')
            
            #Section 1 and 2 deleted - useless

            #SECTION 3 - NEWS: 
            benchmark_final_elements_s3 = []

            section_3 = benchmark_ready_soup[3]
            section_3_divs = section_3.find_all('div')
            

            for post in section_3_divs:
                benchmark_li = post.find_all('li')
                for element in benchmark_li:
                    benchmark_title = element.find('a').text
                    benchmark_href = element.find('a')['href']
                    benchmark_link = (benchmark_url_maker.format(benchmark_href))


                    #Modify url to be title of an article:
                    #benchmark_title = benchmark_title.split('/')[2].split('.html')[0]
                    #x = benchmark_title.replace('-',' ')
                    #benchmark_title = x.capitalize()

                    benchmark_final_elements_s3.append((benchmark_link, benchmark_title))

            
            del benchmark_final_elements_s3[12:]
            

            context = {
                'benchmark_final_elements_s3': benchmark_final_elements_s3,
            }

            return render(self.request, 'benchmark.html', context)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")
    



class WykopView(View):
    def get(self, *args, **kwargs):
        try:
            wykop_url = WYKOP_URL
            wykop_response = requests.get(wykop_url)
            wykop_data = wykop_response.text
            wykop_soup = BeautifulSoup(wykop_data, 'html.parser')
            
            #SOUP with url and title:
            first_part_of_soup = wykop_soup.find_all("a", {"rel": 'noopener'})
            
            #<a> tag with href and title.
            shorter_first_part_of_soup = list(itertools.islice(first_part_of_soup,1,None,3))
            ready_first_part_of_soup = list(shorter_first_part_of_soup[3:])
            
            wykop_final_elements = []

            for items in ready_first_part_of_soup:
                wykop_link = items['href']
                wykop_title = items['title']

                wykop_final_elements.append((wykop_link, wykop_title,))
            

            context = {
                'wykop_final_elements': wykop_final_elements,
            }
            
            
            return render(self.request, 'wykop.html', context,)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")




class ArcheologyView(View):
    def get(self, *args, **kwargs):
        try:
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
                    
                    


                    archeo_final_elements.append((archeo_title, archeo_link, archeo_image)) 
            

            context = {
                'archeo_final_elements': archeo_final_elements,
            }
            
            
            return render(self.request, 'archeology.html', context,)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")




class ToJuzByloView(View):
    def get(self, *args, **kwargs):
        try:
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



                    tojuzbylo_final_elements.append((tojuzbylo_title, tojuzbylo_image, tojuzbylo_href)) 

            context = {
                'tojuzbylo_final_elements': tojuzbylo_final_elements,
            }
            
            
            return render(self.request, 'tojuzbylo.html', context,)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")



class SpidersWebView(View):
    def get(self, *args, **kwargs):
        try:
            spiders_url = SPIDERS_WEB_VIEW
            spiders_response = requests.get(spiders_url)
            spiders_data = spiders_response.text
            spiders_soup = BeautifulSoup(spiders_data, 'html.parser')
            
            #SOUP:
            first_part_of_soup = spiders_soup.find_all('article', {'class': 'article'})
            
            
            spiders_final_elements = []

            for element in first_part_of_soup:
                spiders_title = element.find('span',{'class': 'postlink-inner'}).text
                spiders_image = element.find('img', {'class': 'b-lazy'})['data-src']
                spiders_href_1 = element.find_all('h1', {'class': 'title font25-size'})
                for item in spiders_href_1:
                    spiders_href = item.find('a')['href']
                

                    spiders_final_elements.append((spiders_title, spiders_image, spiders_href)) 

            
            context = {
                'spiders_final_elements': spiders_final_elements,
            }
            
            
            return render(self.request, 'spider_news.html', context,)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/") 