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

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

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


