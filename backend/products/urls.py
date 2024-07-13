from django.urls import path
from .views import ScrapeProductView, HistoricalDataView

ROOT_URLCONF = 'backend_f.urls'
urlpatterns = [
    path('scrape/', ScrapeProductView.as_view(), name='scrape-product'),
    path('trackedItem/', HistoricalDataView.as_view(), name='tracked-items')
]


