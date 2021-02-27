from django.urls import path
from .views import PythonView, RealPythonView, HomeView, BenchmarkView, BoardGamesGeekView, ArcheologyView, \
    ToJuzByloView, ComputerWorldView, BushcraftableView

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
    path('bushcraftable/', BushcraftableView.as_view(), name="bushcraftable"),

    ]