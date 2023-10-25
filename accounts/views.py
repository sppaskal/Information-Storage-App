from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .helpers.account_helper import AccountHelper
from .helpers.type_helper import TypeHelper
from .serializers import (
    AccountSerializer,
    AccountUpdateSerializer,
    TypeSerializer,
    TypeUpdateSerializer
)


class TestConnection(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {"message": "Connection Successful"},
            status=status.HTTP_200_OK
        )

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
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# -------------------------------------------------------------------


class UpdateAccount(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = AccountUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        account_id = self.kwargs.get('id')
        return AccountHelper.get_account_qs_by_id(account_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Updated Account",
                "type": serializer.data
            },
            status=status.HTTP_200_OK
        )

# -------------------------------------------------------------------


class ListAccounts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = AccountHelper.get_all_accounts()
        serializer = AccountSerializer(
            accounts,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

# -------------------------------------------------------------------


class ListAccountsByEmail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, email):
        accounts = AccountHelper.get_account_qs_by_email(email)
        serializer = AccountSerializer(
            accounts,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

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
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# -------------------------------------------------------------------


class UpdateType(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TypeUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        type_id = self.kwargs.get('id')
        return TypeHelper.get_type_qs_by_id(type_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Updated Type",
                "type": serializer.data
            },
            status=status.HTTP_200_OK
        )

# -------------------------------------------------------------------


class ListTypes(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        types = TypeHelper.get_all_types()
        serializer = TypeSerializer(
            types,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
