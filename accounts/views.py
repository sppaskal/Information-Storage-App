from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import (
    AccountSerializer,
    TypeSerializer
)
from .models import Account


class TestConnection(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Your view logic here
        return Response({"message": "Connection Successful"})

# -------------------------------------------------------------------


class AddAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Deserialize and validate the incoming data
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Added Account",
                    "account": serializer.data
                }
            )
        else:
            return Response(serializer.errors, status=400)

# -------------------------------------------------------------------


class ListAccounts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(
            accounts,
            many=True,
        )
        return Response(serializer.data)

# -------------------------------------------------------------------


class ListAccountsByEmail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, email):
        accounts = Account.objects.filter(email=email)
        serializer = AccountSerializer(
            accounts,
            many=True,
        )
        return Response(serializer.data)

# -------------------------------------------------------------------


class AddType(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Deserialize and validate the incoming data
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Added Type",
                    "account": serializer.data
                }
            )
        else:
            return Response(serializer.errors, status=400)
