from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class TestConnection(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        msg = "Connection Successful"
        logger.info(msg)
        return Response(
            {"message": msg},
            status=status.HTTP_200_OK
        )
