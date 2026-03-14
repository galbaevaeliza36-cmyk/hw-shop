from rest_framework import serializers
from .models import Category, Product, Review
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ConfirmationCode
from django.contrib.auth import authenticate


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate(self, data):
        if len(data.get("text", "")) < 5:
            raise serializers.ValidationError("Review text must contain at least 5 characters")
        return data


class ProductSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate(self, data):
        if len(data.get("title", "")) < 3:
            raise serializers.ValidationError("Product title must contain at least 3 characters")
        return data


class CategorySerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Category name must contain at least 3 characters")
        return value
    



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()

        ConfirmationCode.objects.create(user=user)

        return user
    

class ConfirmSerializer(serializers.Serializer):

    username = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data["username"])
            confirmation = ConfirmationCode.objects.get(user=user)
        except:
            raise serializers.ValidationError("User or code not found")

        if confirmation.code != data["code"]:
            raise serializers.ValidationError("Invalid confirmation code")

        user.is_active = True
        user.save()
        confirmation.delete()

        return data
    




class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User not confirmed")

        return data