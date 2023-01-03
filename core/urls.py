from django.urls import path
from .views import (
    PythonView,
    RealPythonView,
    HomeView,
    BenchmarkView,
    BoardGamesGeekView,
    ArcheologyView,
    ToJuzByloView,
    ComputerWorldView,
    LiveScienceView,
    StatisticsView,
    LowcyGierView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('benchmark/', BenchmarkView.as_view(), name="benchmark"),
    path('bgg/', BoardGamesGeekView.as_view(), name="bgg"),
    path('archeology/', ArcheologyView.as_view(), name="archeology"),
    path('tojuzbylo/', ToJuzByloView.as_view(), name="tojuzbylo"),
    path('computerworld/', ComputerWorldView.as_view(), name="computer-world"),
    path('python/', PythonView.as_view(), name="python"),
    path('real-python/', RealPythonView.as_view(), name="real-python"),
    path('livescience/', LiveScienceView.as_view(), name="livescience"),
    path('lowcy-gier/', LowcyGierView.as_view(), name="lowcygier"),
    path('statistics/', StatisticsView.as_view(), name="statistics"),

    path('chart-1/', StatisticsView.get_all_article_pie_chart_data, name='chart-1'),
    path('chart-2/', StatisticsView.get_all_article_tab_chart_data, name='chart-2'),
    path('chart-3/', StatisticsView.get_top_en_word_chart_data, name='chart-3'),
    path('chart-4/', StatisticsView.get_top_pl_word_chart_data, name='chart-4'),

    ]