from .models import CategoryIndustry,ListProductIndustry,ImageProductIndustry
import rest_framework.status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import CategoryIndustrySerializer,ListProductIndustrySerializer,ImageProductIndustrySerializer

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage

from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework import  permissions



from rest_framework.decorators import api_view,permission_classes

from django.core.mail import send_mail
import random
from django.conf import settings 
from rest_framework import status


from django.http import HttpResponse
import requests
import time

import datetime
from django.db import models
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import ModelViewSet

from django.contrib.postgres.search import SearchVector



@api_view(['GET'])
def List_Product(request):
    data = CategoryIndustrySerializer(CategoryIndustry.objects.all(),many=True).data
    message = data
    return Response(message,status=status.HTTP_200_OK)
    
@api_view(['GET'])
def List_Product_Home(request):
    data = CategoryIndustrySerializer(CategoryIndustry.objects.all(),many=True).data

    data_home = []
    for i in data:
        if i['Category_Industry'] != []:
            data_home.append(i['Category_Industry'][0])


    message = data_home
    return Response(message,status=status.HTTP_200_OK)

@api_view(['GET'])
def Search_ListProduct(request):
    search = request.query_params.get('search')
    data_search = ListProductIndustry.objects.annotate(search=SearchVector('Title','Title_English','Information','Information_English','Domain_Server'),).filter(search=search)
    data = ListProductIndustrySerializer(data_search,many=True).data

    message = data
    return Response(message,status=status.HTTP_200_OK)



