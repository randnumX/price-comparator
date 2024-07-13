import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from products.mongo_client import get_max_data, update_max_param_data, get_data_from_tracker, add_data_to_tracker
from .scraper.shopping_scrapper import ShoppingScraper
import traceback

class ScrapeProductView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            body_data = json.loads(request.body.decode('utf-8'))
            search_term = body_data.get("data")["name"]
            search_type = body_data.get("data")["type"]

            if not search_term:
                return JsonResponse({"error": "SearchTerm is required in the request body"},
                                    status=status.HTTP_400_BAD_REQUEST)

            if search_type == 'shopping':
                shopping_scraper = ShoppingScraper()
                amazon_results = shopping_scraper.scrape_amazon(search_term)
                flipkart_results = shopping_scraper.scrape_flipkart(search_term)
                max_data = get_max_data()
                combined_results = [{**result, "id": i + 1} for i, result in enumerate(amazon_results + flipkart_results, start=max_data)]
                update_max_param_data(len(combined_results))
                return JsonResponse(combined_results, status=status.HTTP_200_OK, safe=False)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format in request body"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoricalDataView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            all_data_from_db = {'response' : get_data_from_tracker()}
            return JsonResponse(all_data_from_db,status=status.HTTP_200_OK)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format in request body"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request, *args, **kwargs):
        body_data = json.loads(request.body.decode('utf-8'))
        print(body_data)

        if not body_data:
            return JsonResponse({"error": "SearchTerm is required in the request body"},
                                status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": "SearchTerm is required in the request body"},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self,request, *args, **kwargs):
        try:
            body_data = json.loads(request.body.decode('utf-8'))
            if not body_data:
                return JsonResponse({"error": "SearchTerm is required in the request body"},
                                    status=status.HTTP_400_BAD_REQUEST)
            dataresponse = add_data_to_tracker(body_data)
            return JsonResponse(dataresponse, status=status.HTTP_200_OK)

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format in request body"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": "errore--"+str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class APIViewExample(APIView):
    def get(self, request, *args, **kwargs):
        # Any additional logic here
        return render(request, 'rest_framework/api.html')



