from rest_framework import serializers,validators
from django.contrib.auth.models import User
from Data_Interaction.models import User,CategoryProduct,ListProduct,AdminInformation,BankInformation,CryptoInformation,PersonalTransactionHistory
from rest_framework.validators import ValidationError


from django.core.mail import send_mail
import random
from django.conf import settings 
from .models import User
from rest_framework.response import Response
from rest_framework import status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','email','username','password','Money','Total_recharge_money','Total_amount_deducted','Two_factor_authentication','Password_Level_2']
        extra_kwargs = {
            'password':{'write_only':'true'},
        }

class PersonalTransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=PersonalTransactionHistory 
        fields='__all__'

class PersonalSerializer(serializers.ModelSerializer):
    userlink = PersonalTransactionHistorySerializer(many=True,read_only=True)
    class Meta:
        model= User
        fields=['id','email','username','Money','userlink']
        # extra_kwargs = {
        #     'password':{'write_only':'true'},
        # }

    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # instance.Money = validated_data.get('Money', instance.Money)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        # instance.Money = validated_data.get('Money', instance.Money)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=ListProduct 
        fields='__all__'
        # extra_kwargs = {
        #     'Data_Txt':{'write_only':'true'},
        #     # 'Create_Date':{'write_only':'true'},
        #     # 'Data_Txt':{'write_only':'true'},
        # }

class CategoryProductSerializer(serializers.ModelSerializer):
    Categoryy = ListProductSerializer(many=True,read_only=True)
    class Meta:
        model=CategoryProduct 
        fields='__all__'

class AdminInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminInformation 
        fields='__all__'

class BankInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=BankInformation 
        fields='__all__'

class CryptoInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=CryptoInformation
        fields='__all__'