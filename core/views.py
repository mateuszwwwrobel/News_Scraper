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
            benchmark_url_maker = "http://benchmark.pl{}"

            benchmark_final_elements_s1 = []
            benchmark_final_elements_s2 = []

            benchmark_ready_soup = benchmark_soup.find_all('section')
            

            #SECTION 1 - MAIN TOPICS
            section_1 = benchmark_ready_soup[1]
            section_1_divs = section_1.find_all('div')
            

            for post in section_1_divs:
                benchmark_href = post.find('a')['href']
                benchmark_title = post.find('a')['href']
                benchmark_link = (benchmark_url_maker.format(benchmark_href))
                
                benchmark_final_elements_s1.append((benchmark_link, benchmark_title))

            
            del benchmark_final_elements_s1[8:12]
            del benchmark_final_elements_s1[1:7]
            
            print(benchmark_final_elements_s1)


            #SECTION 2 - MAIN TOPICS:
            section_2 = benchmark_ready_soup[2]
            section_2_divs = section_2.find_all('div')
            

            for post in section_2_divs:
                benchmark_href = post.find('a')['href']
                benchmark_title = post.find('a')['href']
                benchmark_link = (benchmark_url_maker.format(benchmark_href))
                
                benchmark_final_elements_s2.append((benchmark_link, benchmark_title))

            
            del benchmark_final_elements_s2[8:12]
            del benchmark_final_elements_s2[1:7]
            
            print(benchmark_final_elements_s2)

            #SECTION 3 - NEWS: 

            #NEWSY LISTA POWINNA BYC PROSTA





            context = {
                'benchmark_final_elements_s1': benchmark_final_elements_s1,
                'benchmark_final_elements_s2': benchmark_final_elements_s2,
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


