"""
Views for ui app
"""
import csv

import requests
from django.urls.base import reverse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ui.apis import get_mbta_stations_boards


class DepartureBoardFeed(APIView):
    """
    Class based view for getting the data for the departure board,
    No authentication is required
    """

    def get(self, request):
        """
        Handles GET requests
        """

        try:
            return Response(data=get_mbta_stations_boards())
        except requests.exceptions.HTTPError:
            return Response(
                data={'error': 'mbta_backend_error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except csv.Error:
            return Response(
                data={'error': 'mbta_data_error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Index(TemplateView):
    """Index"""
    template_name = "station.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_source_url'] = reverse('departure_board_feed')
        return context
