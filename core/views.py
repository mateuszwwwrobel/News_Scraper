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

def home_view(request):
    return render(request, "homepage.html")


class BenchmarkView(View):
    def get(self, *args, **kwargs):
        try:
            benchmark_url = BENCHMARK_URL
            benchmark_response = requests.get(benchmark_url)
            benchmark_data = benchmark_response.text
            benchmark_soup = BeautifulSoup(benchmark_data, 'html.parser')
            #print(soup)

            benchmark_find_all_headlines = benchmark_soup.find_all('div',{'class': 'bbh-big-slider-mode-container' })

            for post in benchmark_find_all_headlines:
                article_title = post.find('div', {'class': 'bbh-primary'})
                print(article_title)


            context = {
                'article_title': article_title
                #'article_date': article_date
                #'article_url': article_url
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
            
            #First part of the SOUP with image and title:
            first_part_of_soup = wykop_soup.find_all("a", {"rel": 'noopener'})
            
            #<a> tag with <img> tag which include image link and article title.
            shorter_first_part_of_soup = list(itertools.islice(first_part_of_soup,0,None,3))
            ready_first_part_of_soup = list(shorter_first_part_of_soup[3:])
            
            wykop_final_elements = []

            for items in ready_first_part_of_soup:
                wykop_title = items.find("img").get('alt')
                wykop_image = items.find('img').get('data-original')
                
                wykop_final_elements.append((wykop_title, wykop_image,))


            #Second part of the SOUP with image and title:
            second_part_of_the_soup = wykop_soup.find_all('div', {'class': 'media-content'})

            full_wykop_final_elements2 = []

            for items in second_part_of_the_soup:
                wykop_url = items.find('a').get('href')
                

                full_wykop_final_elements2.append(wykop_url,)

                wykop_final_elements2 = list(full_wykop_final_elements2[4:])
            
            
            del full_wykop_final_elements2[10]
            
            
            context = {
                'wykop_final_elements': wykop_final_elements,
                'wykop_final_elements2': wykop_final_elements2,
            }

            
            return render(self.request, 'wykop.html', context,)

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("/")