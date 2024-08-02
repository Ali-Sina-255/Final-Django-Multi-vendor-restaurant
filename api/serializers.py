from menu.models import Category, FootItem
from rest_framework import serializers
from accounts.models import User, UserProfile
from vendor.models import Vendor
from marketplace.models import Cart
from django.db.models import Sum, F
import logging


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "user",
            "user_profile",
            "vendor_name",
            "vendor_slug",
            "vendor_licenses",
            "is_approved",
            "update_om",
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "vendor",
            "category_name",
            "slug",
            "description",
            "created_at",
            "updated_at",
        ]


class FoodItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = FootItem
        fields = [
            "vendor",
            "category",
            "food_title",
            "description",
            "price",
            "image",
            "is_available",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        vendor = validated_data.get("vendor")  # Get the vendor from the FoodItem
        category_data["vendor"] = vendor  # Set the vendor for the Category
        category, created = Category.objects.get_or_create(**category_data)
        food_item = FootItem.objects.create(category=category, **validated_data)
        return food_item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


logger = logging.getLogger(__name__)


class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    vendor = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    food_item = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    total_food_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "user",
            "vendor_id",
            "category_id",
            "vendor",
            "category",
            "food_item",
            "quantity",
            "updated_at",
            "total_food_items",
            "total_price",
        ]

    def get_vendor(self, obj):
        return (
            obj.food_item.vendor.vendor_name
            if obj.food_item and obj.food_item.vendor
            else None
        )

    def get_category(self, obj):
        return (
            obj.food_item.category.category_name
            if obj.food_item and obj.food_item.category
            else None
        )

    def get_food_item(self, obj):
        return obj.food_item.food_title if obj.food_item else None

    def get_total_food_items(self, obj):
        total_food_items = Cart.objects.filter(user=obj.user).aggregate(
            total_items=Sum("quantity")
        )["total_items"]
        return total_food_items

    def get_total_price(self, obj):
        total_price = Cart.objects.filter(user=obj.user).aggregate(
            total_price=Sum(F("quantity") * F("food_item__price"))
        )["total_price"]
        return total_price

    def create(self, validated_data):
        user = self.context["request"].user
        vendor = validated_data.pop("vendor_id")
        category = validated_data.pop("category_id")
        quantity = validated_data.get("quantity")

        logger.debug(f"Vendor ID: {vendor.id}, Category ID: {category.id}")

        # Ensure the category belongs to the vendor
        if not Category.objects.filter(id=category.id, vendor=vendor).exists():
            logger.error(
                f"Category ID {category.id} does not belong to Vendor ID {vendor.id}"
            )
            raise serializers.ValidationError(
                "The selected category does not belong to the specified vendor."
            )

        # Assuming FoodItem has foreign keys to Vendor and Category
        food_item = FootItem.objects.filter(vendor=vendor, category=category).first()
        if not food_item:
            logger.error(
                f"No food item found for vendor ID {vendor.id} and category ID {category.id}"
            )
            raise serializers.ValidationError(
                "No food item found for the given vendor and category."
            )

        cart_item, created = Cart.objects.update_or_create(
            user=user, food_item=food_item, defaults={"quantity": quantity}
        )
        return cart_item

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["vendor_id"] = instance.food_item.vendor.id
        representation["category_id"] = instance.food_item.category.id
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        vendor_id = data.get("vendor_id")
        category_id = data.get("category_id")

        # Validate that the category belongs to the vendor
        if not Category.objects.filter(id=category_id, vendor_id=vendor_id).exists():
            raise serializers.ValidationError(
                "The selected category does not belong to the specified vendor."
            )

        return internal_value
