from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from access.models import AccessRule
from access.permissions import HasAccessPermission
from access.serializers import AccessRuleSerializer
from users.authentication import JWTAuthentication


class ProductsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasAccessPermission]
    business_element = 'products'

    def get(self, request):
        return Response(
            data=[{'id': 1, 'name': 'Iphone'}, {'id': 2, 'name': 'Macbook'}],
            status=status.HTTP_200_OK
        )

    def post(self, request):
        return Response(
            data={'id': 3, 'name': request.data.get('name')},
            status=status.HTTP_201_CREATED
        )


class OrdersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasAccessPermission]
    business_element = 'orders'

    def get(self, request):
        return Response(
            data=[{'id': 1, 'title': 'Order #1'}, {'id': 2, 'title': 'Order #2'}],
            status=status.HTTP_200_OK
        )

    def post(self, request):
        return Response(
            data={'id': 3, 'title': request.data.get('title')},
            status=status.HTTP_201_CREATED
        )


class AccessRuleViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasAccessPermission]
    serializer_class = AccessRuleSerializer
    queryset = AccessRule.objects.select_related('role', 'business_element')
    business_element = 'access_rules'
