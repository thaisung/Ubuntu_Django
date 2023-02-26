from rest_framework import serializers,validators
from polls.models import CategoryIndustry,ListProductIndustry,ImageProductIndustry


from django.core.mail import send_mail
import random
from django.conf import settings 
from rest_framework.response import Response
from rest_framework import status


class ImageProductIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageProductIndustry
        fields=['Image']

class ListProductIndustrySerializer(serializers.ModelSerializer):
    Product_Industry = ImageProductIndustrySerializer(many=True,read_only=True)
    class Meta:
        model=ListProductIndustry
        fields=['Title','Title_English','Information','Information_English','Domain_Server','Oder_Image','Product_Industry']

class CategoryIndustrySerializer(serializers.ModelSerializer):
    Category_Industry = ListProductIndustrySerializer(many=True,read_only=True)
    class Meta:
        model=CategoryIndustry 
        fields=['Name','Active','Category_Industry']