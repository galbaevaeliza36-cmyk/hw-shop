from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategoryListSerializer, CategoryDetailSerializer, ProductListSerializer, ProductDetailSerializer, ReviewListSerializer, ReviewDetailSerializer, ProductWithReviewsSerializer, ProductWithReviewsSerializer, ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer, RegisterSerializer, ConfirmUserSerializer, LoginSerializer
from .models import Category, Product, Review, UserConfirmation
from django.db.models import Avg
from django.db.models import Count
from django.db import transaction
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import random
from django.contrib.auth import authenticate

# Create your views here.
from rest_framework.views import APIView

class CategoriesListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(products_count=Count("product"))
        data = CategoryListSerializer(categories, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        name = request.data.get('name')
        with transaction.atomic():
            category = Category.objects.create(name=name)

        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)
    



class CategoriesDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response({'error': 'category not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        data = CategoryDetailSerializer(category).data
        return Response(data=data)

    def put(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response({'error': 'category not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = request.data.get('name')
        category.save()

        return Response(data=CategoryDetailSerializer(category).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        category = self.get_object(id)
        if not category:
            return Response({'error': 'category not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class ProductsListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductListSerializer(products, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_name = serializer.validated_data.get('category_name')

        category, _ = Category.objects.get_or_create(name=category_name)

        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                category=category
            )

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)



class ProductsDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'category not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(ProductDetailSerializer(product).data)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'category not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')

        category_name = request.data.get('category_name')
        category, _ = Category.objects.get_or_create(name=category_name)
        product.category = category

        product.save()

        return Response(ProductDetailSerializer(product).data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'category not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ReviewsListAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewListSerializer(reviews, many=True).data
        return Response(data)

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        stars = request.data.get('stars')
        text = request.data.get('text')
        product_name = request.data.get('product_name')

        product, _ = Product.objects.get_or_create(title=product_name)

        with transaction.atomic():
            review = Review.objects.create(
                stars=stars,
                text=text,
                product=product
            )

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)