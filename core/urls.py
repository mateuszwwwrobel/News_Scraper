from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from .views import home_view, BenchmarkView, WykopView, ArcheologyView, ToJuzByloView, SpidersWebView
=======
from .views import home_view, BenchmarkView, WykopView, ArcheologyView, ToJuzByloView
>>>>>>> ecd98a128097ac970d13ced896362b128c402aaa

app_name = 'core'

urlpatterns = [
    path('', home_view, name="home-page"),
    path('benchmark-page', BenchmarkView.as_view(), name="benchmark-page"),
    path('wykop-page', WykopView.as_view(), name="wykop-page"),
    path('archeology-page', ArcheologyView.as_view(), name="archeology-page"),
    path('tojuzbylo-page', ToJuzByloView.as_view(), name="tojuzbylo-page"),
<<<<<<< HEAD
    path('spidersweb-page', SpidersWebView.as_view(), name="spidersweb-page"),

=======
>>>>>>> ecd98a128097ac970d13ced896362b128c402aaa
    ]