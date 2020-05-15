from django.contrib import admin
from django.urls import path
from .views import home_view, BenchmarkView, WykopView, ArcheologyView

app_name = 'core'

urlpatterns = [
    path('', home_view, name="home-page"),
    path('benchmark-page', BenchmarkView.as_view(), name="benchmark-page"),
    path('wykop-page', WykopView.as_view(), name="wykop-page"),
    path('archeology-page', ArcheologyView.as_view(), name="archeology-page"),

    ]