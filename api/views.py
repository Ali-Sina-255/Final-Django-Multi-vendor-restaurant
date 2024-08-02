from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin

from menu.models import Category, FootItem
from vendor.models import Vendor
from accounts.models import User, UserProfile
from marketplace.models import Cart
from .serializers import (
    CategorySerializer,
    FoodItemSerializer,
    UserSerializer,
    UserProfileSerializer,
    VendorSerializer,
    CartSerializer,
)
from .filters import (
    CategoryFilter,
    UserFilterClass,
    FoodItemFilterClass,
    VendorFilterClass,
    CartFilter,
)
from .pagination import DefaultPaginationClass, CartItemPaginationClass


class CartApiViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = CartItemPaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CartFilter
    search_fields = ["food_item"]
    ordering_fields = ["food_item", "updated_at"]


class CategoryApiViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CategoryFilter
    pagination_class = DefaultPaginationClass
    search_fields = ["category_name", "description"]
    ordering_fields = ["category_name", "vendor", "updated_at"]


class FoodItemApiViewSet(ModelViewSet):
    queryset = FootItem.objects.all()
    pagination_class = DefaultPaginationClass
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FoodItemFilterClass

    ordering_fields = ["price", "is_available", "updated_at"]

    def get_serializer_class(self):
        return FoodItemSerializer


class UserApiViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserFilterClass
    pagination_class = DefaultPaginationClass
    ordering_fields = ["role", "updated_at"]
    search_fields = ["role", "first_name", "last_name", "phone_number"]


class UserProfileApiViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=["get"])
    def get_user_profile(self, request, pk=None):
        try:
            user_profile = UserProfile.objects.get(user_id=pk)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)


class VendorApiViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VendorFilterClass

    ordering_fields = ["user", "is_approved", "updated_at"]
    pagination_class = DefaultPaginationClass
