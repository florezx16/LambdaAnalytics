from django.urls import path
from . import views

webScraping_patterns = ([
    path(route='index_scraping_view/',view=views.index_scraping_view,name='index_scraping_view'),
    path(route='search/',view=views.search,name='search'),
    path(route='get_etl/',view=views.get_etl,name='get_etl')
],'web_scraping')