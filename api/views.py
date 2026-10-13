from django.db.migrations import serializer
from rest_framework.response import Response
from .models import Item, Profile
from .serializers import ItemSerializer, RegisterSerializer, ProfileSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsProfileOwnerOrReadOnly
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
    @method_decorator(cache_page(60*15))
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60*60))
    @method_decorator(vary_on_headers('Authorization'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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

        cache_key = "item:cheapest"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        article = Item.objects.order_by('price').first()
        if article:
            serializer = ItemSerializer(article)
            cache.set(cache_key, serializer.data, timeout=60)
            return Response(serializer.data)
        return Response({'message': 'No items found'}, status=400)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
         serializer = RegisterSerializer(data=request.data)
         if serializer.is_valid():
             user = serializer.save()
             tokens = serializer.get_tokens(user)
             return Response({
                 'message': 'User registered successfully',
                 'data': serializer.data,
                 'tokens': tokens
             }, status=201)
         return Response(serializer.errors, status=400)


