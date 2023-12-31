from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .helpers.account_helper import AccountHelper
from .helpers.type_helper import TypeHelper
from .serializers import (
    AccountSerializer,
    AccountUpdateSerializer,
    TypeSerializer,
    TypeUpdateSerializer
)
import logging

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------


class TestConnection(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        msg = "Connection Successful"
        logger.info(msg)
        return Response(
            {"message": msg},
            status=status.HTTP_200_OK
        )

# -------------------------------------------------------------------------------


class Test(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Enter test code here
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class AddAccount(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
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
                logger.error(str(serializer.errors))
                return Response(
                    {"error": str(serializer.errors)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class UpdateAccount(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = AccountUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        account_id = self.kwargs.get('id')
        return AccountHelper.get_account_qs_by_id(account_id)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "message": "Updated Account",
                    "account": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class DeleteAccount(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = AccountSerializer
    lookup_field = 'id'

    def get_queryset(self):
        account_id = self.kwargs.get('id')
        return AccountHelper.get_account_qs_by_id(account_id)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            account_email = instance.email
            self.perform_destroy(instance)
            return Response(
                {
                    "message": "Deleted Account: " + str(account_email),
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class ListAccounts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            accounts = AccountHelper.select_related_fields(
                    AccountHelper.get_all_accounts()
                )
            serializer = AccountSerializer(
                accounts,
                many=True,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class ListAccountsByEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, email):
        try:
            accounts = AccountHelper.select_related_fields(
                    AccountHelper.get_account_qs_by_email(
                        email)
                )
            serializer = AccountSerializer(
                accounts,
                many=True,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class AddType(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = TypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Added Type",
                        "type": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.error(str(serializer.errors))
                return Response(
                    {"error": str(serializer.errors)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class UpdateType(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TypeUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        type_id = self.kwargs.get('id')
        return TypeHelper.get_type_qs_by_id(type_id)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "message": "Updated Type",
                    "type": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class DeleteType(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TypeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        type_id = self.kwargs.get('id')
        return TypeHelper.get_type_qs_by_id(type_id)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            type_name = instance.name
            self.perform_destroy(instance)
            return Response(
                {
                    "message": "Deleted Type: " + str(type_name)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# -------------------------------------------------------------------------------


class ListTypes(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            types = TypeHelper.get_all_types()
            serializer = TypeSerializer(
                types,
                many=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
