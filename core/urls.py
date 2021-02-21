from django.urls import path
from .views import HomeView, BenchmarkView, WykopView, ArcheologyView, ToJuzByloView, ComputerWorldView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('benchmark', BenchmarkView.as_view(), name="benchmark"),
    path('wykop', WykopView.as_view(), name="wykop"),
    path('archeology', ArcheologyView.as_view(), name="archeology"),
    path('tojuzbylo', ToJuzByloView.as_view(), name="tojuzbylo"),
    path('computerworld', ComputerWorldView.as_view(), name="computer-world"),

    ]