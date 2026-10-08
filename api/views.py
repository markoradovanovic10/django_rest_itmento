from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

@api_view(['GET'])
def test_enpoint(request):

    article = Item(name='Sample Item')
    serializer = ItemSerializer(article)
    return Response(serializer.data)
