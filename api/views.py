from operator import eq

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'created_at']

    filterset_fields = {
        'price': ['lt', 'gte', 'exact'],
        'created_at': ['lt', 'gte', 'exact', 'date']
    }

    @action(detail=False, methods=['get'])
    def cheapest(self, request):
        article = Item.objects.order_by('price').first()
        if article:
            serializer = ItemSerializer(article)
            return Response(serializer.data)
        return Response({'message': 'No items found'}, status=400)


