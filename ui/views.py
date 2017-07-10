"""
Views for ui app
"""
import csv

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ui.apis import fetch_times


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
            return Response(data=fetch_times())
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
