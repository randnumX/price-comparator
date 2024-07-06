from django.urls import path
from .views import ScrapeProductView,APIViewExample

ROOT_URLCONF = 'backend.urls'
urlpatterns = [
    # path('example/', APIViewExample.as_view(), name='api_example'),
    path('scrape/', ScrapeProductView.as_view(), name='scrape-product'),
]
