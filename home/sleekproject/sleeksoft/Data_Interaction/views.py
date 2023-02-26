from .models import User,CategoryProduct,ListProduct,AdminInformation,PersonalTransactionHistory,BankInformation,CryptoInformation
import rest_framework.status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer,ListProductSerializer,CategoryProductSerializer,AdminInformationSerializer,BankInformationSerializer,CryptoInformationSerializer,PersonalTransactionHistorySerializer,PersonalSerializer

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage

from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework import  permissions


from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated   
from django_filters.rest_framework import DjangoFilterBackend
# from emails import *

from django.core.mail import send_mail
import random
from django.conf import settings 
from .models import User
from rest_framework import status

from knox.models import AuthToken
from knox.settings import CONSTANTS

import uuid
from django.http import HttpResponse
import requests
import time

import datetime
from django.db import models
from django.utils import timezone
# Create your views here.

# class UserViewSet(viewsets.ViewSet,generics.CreateAPIView):
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = UserSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['email']
#     parser_classes = [MultiPartParser, ]

#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.IsAuthenticated()]
#         if self.action == 'retrieve':
#             return [permissions.IsAuthenticated()]
#         if self.action == 'update':
#             return [permissions.IsAuthenticated()]
#         if self.action == 'partial_update':
#             return [permissions.IsAuthenticated()]
#         return [permissions.AllowAny()]

# ---Du lieu vao la JSON--
@api_view(['POST'])
def create_user(request):
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']
    captchav2 = request.data['captchav2']
    url = "https://www.google.com/recaptcha/api/siteverify"
    data ={"response":captchav2,"secret":"6LfaruMjAAAAAPFwSCuW4-Yda-D-CN8JqZWq6M9O"}
    
    data_user_email = User.objects.filter(email=email)
    data_user_email_serializer = UserSerializer(data_user_email,many=True)

    data_user_username = User.objects.filter(username=username)
    data_user_username_serializer = UserSerializer(data_user_username,many=True)

        
    if email != None and username != None and password != None:

        if email.split() != [] and username.split() != [] and password.split() != []:

            if list(email).count(' ') == 0 and list(username).count(' ') == 0 and list(password).count(' ') == 0:

                if data_user_username_serializer.data == []:
                    
                    response = requests.request("POST", url, data=data)
                    human = response.json()['success']
                    if human == True:

                        if len(data_user_email_serializer.data) < 2:
                            User.objects.create(email=email,username=username,password=password,is_active=True)
                            data_user = User.objects.get(email=email,username=username,is_active=True)
                            pw = data_user.password
                            data_user.set_password(pw)
                            data_user.save()
                            message = {'Create account ':'Account successfully created !'}
                            return Response(message,status=status.HTTP_200_OK)
                        else:
                            message = {'Error message': 'Email của bạn đã lập tối đa 2 tài khoản !','Error message English':'Your email has a maximum of 2 accounts !'}
                            return Response(message, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        message = {'Error message': 'Hệ thống cho rằng bạn là 1 robot, nên không thể xác thực !','Error message English':'The system thinks you are a robot,so it can not authenticate!'}
                        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    message = {'Error message': 'Tên người dùng đã tồn tại, nhập tên khác !','Error message English':'Account username already exists, please enter another account username !'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {'Error message': 'Thông tin đăng kí phải là 1 dãy kí tự viết liền !','Error message English':'Registration information must be a single string of characters !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'Error message': 'Thông tin đăng kí không được để trống !','Error message English':'Registration information cannot be left blank !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {'Error message': 'Thông tin đăng kí không được để trống !','Error message English':'Registration information cannot be left blank !'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def statistical_server_user(request):
    url = "https://api.ipgeolocation.io/timezone"
    params = {"apiKey":"fc2cf66cbf09419e96dd8eab6230d1c1","tz":"Asia/Ho_Chi_Minh"}
    response = requests.request("GET", url, params=params)
    date = response.json()['date']
    time = date.split('-')
    time_today = date
    time_month = time[0] +'-'+ time[1]
    if int(str(time[1]).strip('0')) == 1 or int(str(time[1]).strip('0')) == 3 or int(str(time[1]).strip('0')) == 5 or int(str(time[1]).strip('0')) == 7 or int(str(time[1]).strip('0')) == 8 or int(str(time[1]).strip('0')) == 10 or int(str(time[1]).strip('0')) == 12:
        time_month_range = [time_month+'-01',time_month+'-31']
    if int(str(time[1]).strip('0')) == 4 or int(str(time[1]).strip('0')) == 6 or int(str(time[1]).strip('0')) == 9 or int(str(time[1]).strip('0')) == 11: 
        time_month_range = [time_month+'-01',time_month+'-30']
    if int(str(time[1]).strip('0')) == 2:
        time_month_range = [time_month+'-01',time_month+'-28']
    time_year = time[0] 
    time_last_year = int(time[0]) - 1

    # phần thống kê đăng kí
    user_time_today = UserSerializer(User.objects.filter(date_joined__date=time_today),many=True)
    user_time_month = UserSerializer(User.objects.filter(date_joined__date__range=time_month_range),many=True) 
    user_time_year = UserSerializer(User.objects.filter(date_joined__year=time_year),many=True) 
    user_time_last_year = UserSerializer(User.objects.filter(date_joined__year=time_last_year),many=True)
    user_server = UserSerializer(User.objects.all(),many=True)

    h1=''
    for index, i in enumerate(user_time_today.data, start=1):
        h1 = h1 + str(index) +'.'+ i['username'] + '\r\n'
    h2=''
    for index, i in enumerate(user_time_month.data, start=1):
        h2 = h2 + str(index) +'.'+ i['username'] + '\r\n'
    h3=''
    for index, i in enumerate(user_time_year.data, start=1):
        h3 = h3 + str(index) +'.'+ i['username'] + '\r\n'
    h4=''
    for index, i in enumerate(user_time_last_year.data, start=1):
        h4 = h4 + str(index) +'.'+ i['username'] + '\r\n'
    h5=''
    for index, i in enumerate(user_server.data, start=1):
        h5 = h5 + str(index) +'.'+ i['username'] + '\r\n'

    #phần thống kê đăng nhập
    user_time_today_lg = UserSerializer(User.objects.filter(last_login__date=time_today),many=True)
    user_time_month_lg = UserSerializer(User.objects.filter(last_login__date__range=time_month_range),many=True) 
    user_time_year_lg = UserSerializer(User.objects.filter(last_login__year=time_year),many=True) 
    user_time_last_year_lg = UserSerializer(User.objects.filter(last_login__year=time_last_year),many=True)
    # user_server = UserSerializer(User.objects.all(),many=True)

    h1lg=''
    for index, i in enumerate(user_time_today_lg.data, start=1):
        h1lg = h1lg + str(index) +'.'+ i['username'] + '\r\n'
    h2lg=''
    for index, i in enumerate(user_time_month_lg.data, start=1):
        h2lg = h2lg + str(index) +'.'+ i['username'] + '\r\n'
    h3lg=''
    for index, i in enumerate(user_time_year_lg.data, start=1):
        h3lg = h3lg + str(index) +'.'+ i['username'] + '\r\n'
    h4lg=''
    for index, i in enumerate(user_time_last_year_lg.data, start=1):
        h4lg = h4lg + str(index) +'.'+ i['username'] + '\r\n'
    # h5lg=''
    # for i in user_server.data:
    #     h5 = h5 + i['username'] + '\r\n'

    message1 = [
               {'time':time_today,'quantity':len(user_time_today.data),'user':h1},
               {'time':time_month,'quantity':len(user_time_month.data),'user':h2},
               {'time':time_year,'quantity':len(user_time_year.data),'user':h3},
               {'time':time_last_year,'quantity':len(user_time_last_year.data),'user':h4},
               {'time':'All','quantity':len(user_server.data),'user':h5}
               ]

    message2 = [
               {'time':time_today,'quantity':len(user_time_today_lg.data),'user':h1lg},
               {'time':time_month,'quantity':len(user_time_month_lg.data),'user':h2lg},
               {'time':time_year,'quantity':len(user_time_year_lg.data),'user':h3lg},
               {'time':time_last_year,'quantity':len(user_time_last_year_lg.data),'user':h4lg},
               ]

    message = [message1,message2]

    return Response(message,status=status.HTTP_200_OK)

@api_view(['GET'])
def statistical_server_money(request):
    url = "https://api.ipgeolocation.io/timezone"
    params = {"apiKey":"fc2cf66cbf09419e96dd8eab6230d1c1","tz":"Asia/Ho_Chi_Minh"}
    response = requests.request("GET", url, params=params)
    date = response.json()['date']
    time = date.split('-')
    time_today = date
    time_month = time[0] +'-'+ time[1]
    if int(str(time[1]).strip('0')) == 1 or int(str(time[1]).strip('0')) == 3 or int(str(time[1]).strip('0')) == 5 or int(str(time[1]).strip('0')) == 7 or int(str(time[1]).strip('0')) == 8 or int(str(time[1]).strip('0')) == 10 or int(str(time[1]).strip('0')) == 12:
        time_month_range = [time_month+'-01',time_month+'-31']
    if int(str(time[1]).strip('0')) == 4 or int(str(time[1]).strip('0')) == 6 or int(str(time[1]).strip('0')) == 9 or int(str(time[1]).strip('0')) == 11: 
        time_month_range = [time_month+'-01',time_month+'-30']
    if int(str(time[1]).strip('0')) == 2:
        time_month_range = [time_month+'-01',time_month+'-28']
    time_year = time[0] 
    time_last_year = int(time[0]) - 1

    # phần thống kê nạp tiền
    user_time_today = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__date=time_today,Status='Successful_Money'),many=True)
    user_time_month = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__date__range=time_month_range,Status='Successful_Money'),many=True) 
    user_time_year = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__year=time_year,Status='Successful_Money'),many=True) 
    user_time_last_year = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__year=time_last_year,Status='Successful_Money'),many=True)
    user_server = UserSerializer(User.objects.all().order_by('-Total_recharge_money'),many=True)

    h1=''
    all_money1 = 0
    for index, i in enumerate(user_time_today.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link'])).data
        h1 = h1 + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money1 = all_money1 + int(str(i['Payment_Amount']).strip('+'))
    h2=''
    all_money2 = 0
    for index, i in enumerate(user_time_month.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link'])).data
        h2 = h2 + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money2 = all_money2 + int(str(i['Payment_Amount']).strip('+'))
    h3=''
    all_money3 = 0
    for index, i in enumerate(user_time_year.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link'])).data
        h3 = h3 + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money3 = all_money3 + int(str(i['Payment_Amount']).strip('+'))
    h4=''
    all_money4 = 0
    for index, i in enumerate(user_time_last_year.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link']),many=True).data
        h4 = h4 + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money4 = all_money4 + int(str(i['Payment_Amount']).strip('+'))
    h5=''
    all_money5 = 0
    for index, i in enumerate(user_server.data, start=1):
        h5 = h5 + str(index)+'.'+i['username']+' : '+'+'+str(i['Total_recharge_money']) + '\r\n'
        all_money5 = all_money5 + int(i['Total_recharge_money'])

    message1 = [
               {'time':time_today,'quantity':'+'+str(all_money1),'user':h1},
               {'time':time_month,'quantity':'+'+str(all_money2),'user':h2},
               {'time':time_year,'quantity':'+'+str(all_money3),'user':h3},
               {'time':time_last_year,'quantity':'+'+str(all_money4),'user':h4},
               {'time':'All','quantity':'+'+str(all_money5),'user':h5}
               ]

    # phần thống kê trừ tiền
    user_time_today_tt = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__date=time_today,Status='Successful_Data'),many=True)
    user_time_month_tt = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__date__range=time_month_range,Status='Successful_Data'),many=True) 
    user_time_year_tt = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__year=time_year,Status='Successful_Data'),many=True) 
    user_time_last_year_tt = PersonalTransactionHistorySerializer(PersonalTransactionHistory.objects.filter(Transaction_Time__year=time_last_year,Status='Successful_Data'),many=True)
    user_server_tt = UserSerializer(User.objects.all().order_by('-Total_amount_deducted'),many=True)

    h1tt=''
    all_money1tt = 0
    for index, i in enumerate(user_time_today_tt.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link'])).data
        h1tt = h1tt + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n' 
        all_money1tt = all_money1tt + int(str(i['Payment_Amount']).strip('-'))
    h2tt=''
    all_money2tt = 0
    for index, i in enumerate(user_time_month_tt.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link'])).data
        h2tt = h2tt + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money2tt = all_money2tt + int(str(i['Payment_Amount']).strip('-'))
    h3tt=''
    all_money3tt = 0
    for index, i in enumerate(user_time_year_tt.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link'])).data
        h3tt = h3tt + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money3tt = all_money3tt + int(str(i['Payment_Amount']).strip('-'))
    h4tt=''
    all_money4tt = 0
    for index, i in enumerate(user_time_last_year_tt.data, start=1):
        us=UserSerializer(User.objects.get(pk=i['User_Link']),many=True).data
        h4tt = h4tt + str(index)+'.'+us['username']+' : '+i['Payment_Amount'] + '\r\n'
        all_money4tt = all_money4tt + int(str(i['Payment_Amount']).strip('-'))
    h5tt=''
    all_money5tt = 0
    for index, i in enumerate(user_server_tt.data, start=1):
        h5tt = h5tt + str(index)+'.'+i['username']+' : '+'-'+str(i['Total_amount_deducted']) + '\r\n'
        all_money5tt = all_money5tt + int(i['Total_amount_deducted'])

    message2 = [
               {'time':time_today,'quantity':'-'+str(all_money1tt),'user':h1tt},
               {'time':time_month,'quantity':'-'+str(all_money2tt),'user':h2tt},
               {'time':time_year,'quantity':'-'+str(all_money3tt),'user':h3tt},
               {'time':time_last_year,'quantity':'-'+str(all_money4tt),'user':h4tt},
               {'time':'All','quantity':'-'+str(all_money5tt),'user':h5tt}
               ]

    message = [message1,message2]

    return Response(message,status=status.HTTP_200_OK)

# ---Du lieu vao la JSON--
@api_view(['POST'])
def login_api(request):
    try:
        username = request.data['username']
        password = request.data['password']
        captchav2 = request.data['captchav2']
        url = "https://www.google.com/recaptcha/api/siteverify"
        data ={"response":captchav2,"secret":"6LfaruMjAAAAAPFwSCuW4-Yda-D-CN8JqZWq6M9O"}
        data_user = User.objects.get(username=username,is_active=True)
        data_user_json = UserSerializer(data_user).data
        email = data_user_json['email']

        if  username != None and password != None:

            if  username.split() != [] and password.split() != []:

                if  list(username).count(' ') == 0 and list(password).count(' ') == 0:

                    response = requests.request("POST", url, data=data)
                    human = response.json()['success']
                    if human == True:
                        try:
                            if data_user_json['Two_factor_authentication'] == 'OFF':
                                serializer = AuthTokenSerializer(data=request.data)
                                serializer.is_valid(raise_exception=True)
                                user = serializer.validated_data['user']
                                __,token = AuthToken.objects.create(user)

                                user.last_login = timezone.now()
                                user.save(update_fields=['last_login'])

                                message = {'Login information':'Logged in successfully !','id':user.id,'email':user.email,'username':user.username,'Money':user.Money,'token':token,'Two_factor_authentication':user.Two_factor_authentication}
                                return Response(message,status=status.HTTP_200_OK)
                            if data_user_json['Two_factor_authentication'] == 'ON':
                                try:
                                    subject = 'Please use this level 2 password to proceed with your account login !'
                                    otp = random.randint(100000,999999)
                                    message = 'Password Level 2 of '+"'"+ str(username) +"'"+' account is ' + str(otp)
                                    email_from = settings.EMAIL_HOST
                                    send_mail(subject, message, email_from, [email])

                                    data_user.Password_Level_2 = otp
                                    data_user.save()
                                    message = {'Login information':'Two factor authentication','Password Level 2 information': 'Password Level 2 sent successfully!','username':username,'password':password}
                                    return Response(message, status=status.HTTP_201_CREATED)
                                except:
                                    message = {'Error message': 'Server error !'}
                                    return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        except:
                            message = {'Error message': 'Thông tin đăng nhập không hợp lệ !','Error message English':'Invalid login information !'}
                            return Response(message, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        message = {'Error message': 'Hệ thống cho rằng bạn là 1 robot, nên không thể xác thực !','Error message English':'The system thinks you are a robot, so cannot authenticate !'}
                        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                        message = {'Error message': 'Thông tin đăng nhập phải là 1 dãy kí tự viết liền !','Error message English':'Login information must be a sequence of characters !'}
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {'Error message': 'Thông tin đăng nhập không được để trống !','Error message English':'Login information cannot be blank !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'Error message': 'Thông tin đăng nhập không được để trống !','Error message English':'Login information cannot be blank !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Thông tin đăng nhập không chính xác !','Error message English':'Login information is incorrect !'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# ---Du lieu vao la JSON--
@api_view(['POST'])
def login_Two_factor_authentication(request):
    # try:
        username = request.data['username']
        password = request.data['password']
        Password_Level_2 = request.data['Password_Level_2']
        data_user = User.objects.get(username=username,is_active=True)
        data_user_json = UserSerializer(data_user).data

        if  username != None and password != None:

            if  username.split() != [] and password.split() != []:

                if  list(username).count(' ') == 0 and list(password).count(' ') == 0:
                    # try:
                    if int(data_user_json['Password_Level_2']) == int(Password_Level_2):
                        serializer = AuthTokenSerializer(data={'username':username,'password':password})
                        serializer.is_valid(raise_exception=True)
                        user = serializer.validated_data['user']
                        __,token = AuthToken.objects.create(user)

                        user.last_login = timezone.now()
                        user.save(update_fields=['last_login'])

                        message = {'Login information':'Logged in successfully !','id':user.id,'email':user.email,'username':user.username,'Money':user.Money,'token':token,'Two_factor_authentication':user.Two_factor_authentication}
                        return Response(message,status=status.HTTP_200_OK)
                    else:
                        message = {'Error message': 'Mật khẩu cấp 2 không chính xác !','Error message English':'Level 2 password is incorrect !'}
                        return Response(message, status=status.HTTP_400_BAD_REQUEST) 

                    # except:
                    #     message = {'Error message': 'Thông tin đăng nhập không hợp lệ !','Error message English':'Invalid login information !'}
                    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)
                else:
                        message = {'Error message': 'Thông tin đăng nhập phải là 1 dãy kí tự viết liền !','Error message English':'Login information must be a sequence of characters !'}
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {'Error message': 'Thông tin đăng nhập không được để trống !','Error message English':'Login information cannot be blank !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'Error message': 'Thông tin đăng nhập không được để trống !','Error message English':'Login information cannot be blank !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    # except:
    #     message = {'Error message': 'Thông tin đăng nhập không chính xác !','Error message English':'Login information is incorrect !'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def ON_OFF_2_factor_authentication(request):
    try:
        id_user = request.data["id"]
        token = request.data["token"]
        ON_OFF = request.data["ON_OFF"]
        data_user = User.objects.get(id=id_user,is_active=True)
        data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])

        if int(data_token.user_id) == int(data_user.id):
            data_user.Two_factor_authentication = ON_OFF
            data_user.save(update_fields=['Two_factor_authentication'])
            message = {'2-factor authentication information':'2-factor authentication saved successfully !','ON_OFF':ON_OFF}
            return Response(message,status=status.HTTP_200_OK)
        else:
            message = {'Error message': 'This account is Invalid !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Invalid data !'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def keep_login(request):
    try:
        id_user = request.data["id"]
        token = request.data["token"]
        data_user = User.objects.get(id=id_user,is_active=True)
        data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])

        if int(data_token.user_id) == int(data_user.id):
            data_user.last_login = timezone.now()
            data_user.save(update_fields=['last_login'])
            message = {'Login information':'Logged in successfully !',"data_user":{"id":data_user.id,"email":data_user.email,"username":data_user.username,"Money":data_user.Money,"token":token,"Two_factor_authentication":data_user.Two_factor_authentication}}
            return Response(message,status=status.HTTP_200_OK)
        else:
            message = {'Error message': 'This account is Invalid !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Invalid data !'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)        

# ---Du lieu vao la JSON--
@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def change_password(request):
    username = request.data['username']
    password = request.data['password']
    token = request.data['token']
    new_password = request.data['new_password']
    confirm_new_password = request.data['confirm_new_password']
    data_user = User.objects.get(username=username,is_active=True)
    data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])

    captchav2 = request.data['captchav2']
    url = "https://www.google.com/recaptcha/api/siteverify"
    data ={"response":captchav2,"secret":"6LfaruMjAAAAAPFwSCuW4-Yda-D-CN8JqZWq6M9O"}

    if  username != None and password != None and new_password != None and confirm_new_password != None :
        if username.split() != [] and password.split() != [] and new_password.split() != [] and confirm_new_password.split() != []:
            if int(data_token.user_id) == int(data_user.id):
                serializer = AuthTokenSerializer(data={'username':username,'password':password})
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                if str(user.username)==username:
                    if str(new_password) == str(confirm_new_password):
                        response = requests.request("POST", url, data=data)
                        human = response.json()['success']
                        if human == True:
                            try:
                                # data_user.password = password
                                data_user.set_password(new_password)
                                data_user.save()
                            except:
                                message = {'Error message English': 'Invalid credentials !','Error message': 'Thông tin xác thực không hợp lệ !'}
                                return Response(message, status=status.HTTP_400_BAD_REQUEST)
                            message = {"Username":data_user.username,"Update information":"Đổi mật khẩu thành công !","Update information English":"Change password successfully !"}
                            return Response(message,status=status.HTTP_200_OK)
                        else:
                            message = {'Error message': 'Hệ thống cho rằng bạn là 1 robot, nên không thể xác thực !','Error message English':'The system thinks you are a robot, so cannot authenticate !'}
                            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        message = {'Error message English': 'Confirm the new password is not correct !','Error message': 'Xác nhận mật khẩu mới không chính xác !'}
                        return Response(message, status=status.HTTP_400_BAD_REQUEST)
                else:
                    message = {'Error message English': 'Invalid credentials !','Error message': 'Thông tin xác thực không hợp lệ !'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                message = {'Error message English': 'Invalid credentials !','Error message': 'Thông tin xác thực không hợp lệ !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'Error message': 'Thông tin xác thực không được để trống !','Error message English':'Credentials cannot be blank !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {'Error message': 'Thông tin xác thực không được để trống !','Error message English':'Credentials cannot be blank !'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# ---Du lieu vao la JSON--
@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def change_money(request):
    try:
        username = request.data['username']
        token = request.data['token']
        Money= request.data['Money']

        data_user = User.objects.get(username=username,is_active=True)
        data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])

        old_amount = data_user.Money
        if int(data_token.user_id) == int(data_user.id):
            data_user.Money = int(data_user.Money) + int(Money)
            data_user.save()
            message = {"Username":data_user.username,
                       "Update information":"The amount in the account has been added " +  str(Money),
                       "Old amount": old_amount,
                       "New amount": data_user.Money}
            return Response(message,status=status.HTTP_200_OK)
        else:
            message = {'Error message': 'This account is Invalid !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Invalid data provided !'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

# ---Du lieu vao la JSON--
@api_view(['POST'])
def loc_usernam_vs_mail(request):
    try:
        email = request.data["email"]
        all_data_user = User.objects.filter(email=email,is_active=True)
        all_data_user_serializer=UserSerializer(all_data_user,many=True)
        if all_data_user_serializer.data == []:
            message = {'Error message': 'Invalid email !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(all_data_user_serializer.data,safe=False)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---Du lieu vao la JSON--
@api_view(['PATCH'])
def gui_OTP_den_user(request):
    try:
        email = request.data['email']
        username = request.data['username']
        data_user = User.objects.get(email=email,username=username,is_active=True)

        subject = 'Please use the OTP code below to reset your account password !'
        otp = random.randint(100000,999999)
        message = 'OTP code of '+"'"+ str(username) +"'"+' account is ' + str(otp)
        email_from = settings.EMAIL_HOST
        send_mail(subject, message, email_from, [email])

        data_user.OTP = otp
        data_user.save()
        message = {'OTP information': 'OTP sent successfully!'}
        return Response(message, status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---Du lieu vao la JSON--
@api_view(['POST'])
def so_sanh_OTP(request):
    try:
        email = request.data["email"]
        username = request.data["username"]
        OTP = request.data["OTP"]
        data_user = User.objects.get(email=email,username=username,is_active=True)
        if int(OTP) == int(data_user.OTP):
            message = {'OTP information': 'OTP authentication successful !'}
            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {'OTP information': 'Incorrect OTP code !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---Du lieu vao la JSON--
@api_view(['PATCH'])
def reset_password(request):
    try:
        email = request.data['email']
        username = request.data['username']
        OTP = request.data['OTP']
        password = request.data['password']
        data_user = User.objects.get(email=email,username=username,is_active=True)
        # Check if otp is valid
        if int(OTP) == int(data_user.OTP):
            if password != None and password != '':
                data_user.OTP = random.randint(100000,999999)
                data_user.set_password(password)
                data_user.save() # Here user otp will also be changed on save automatically 
                message = {"Username":data_user.username,"Update information":"Change password successfully !"}
                return Response(message,status=status.HTTP_200_OK)
            else:
                message = {'Error message': 'Password cant be empty'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'Error message': 'Incorrect OTP code !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ---Du lieu vao la JSON--
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def send_recharge_data(request):
    try:
        Payment_Amount = request.data['Payment_Amount']
        if Payment_Amount != 0 and Payment_Amount != None and Payment_Amount != "":
            Code_Orders = request.data['Code_Orders']
            CODENH = ''
            if Code_Orders[0:3] == 'VCB':
                CODENH = 'VIETCOMBANK'
            if Code_Orders[0:3] == 'VTB':
                CODENH = 'VIETINBANK'
            if Code_Orders[0:3] == 'ACB':
                CODENH = 'ACB'

            # Api_key ngân hàng
            apk = BankInformation.objects.get(Short_Name=CODENH,Active=True).Api_Key

            #thoi gian cung ngay
            url = "https://api.ipgeolocation.io/timezone"
            params = {"apiKey":"fc2cf66cbf09419e96dd8eab6230d1c1","tz":"Asia/Ho_Chi_Minh"}
            response = requests.request("GET", url, params=params)
            date = response.json()['date']
            date_time = response.json()['date_time']

            Payment_Amount = request.data['Payment_Amount']
            Payment_Amount1 = 'thai'
            username = request.data['username']
            data_user = User.objects.get(username=username,is_active=True)

            # tra cuu lich su giao dich va doi chieu
            thoi_gian = 0
            while True:
                url = "https://oauth.casso.vn/v2/transactions"
                params = {"fromDate":date,"sort":"DESC"}
                headers = {"Authorization":"Apikey "+ str(apk)}
                response = requests.request("GET", url, params=params,headers=headers)
                records = response.json()['data']['records']

                for m in records:
                    noi_dung_CK = m['description'].split()[2].split("-")[0]
                    so_tien_nap = m['amount']
                    if str(Code_Orders) == str(noi_dung_CK) and int(Payment_Amount) == int(so_tien_nap):
                        Payment_Amount1 = int(so_tien_nap)
                        Old_amount = data_user.Money
                        data_user.Money = int(data_user.Money) + int(so_tien_nap)
                        data_user.Total_recharge_money = int(data_user.Total_recharge_money) + int(so_tien_nap)
                        New_amount = data_user.Money
                        data_user.save()
                        PersonalTransactionHistory.objects.create(Content='Recharge',Code_Orders=Code_Orders,Transaction_Time=str(date_time)+' (+7)',Payment_Amount='+'+str(Payment_Amount),Status='Successful_Money',User_Link=data_user)
                        
                time.sleep(5)
                thoi_gian = thoi_gian + 5
                if Payment_Amount == Payment_Amount1 or thoi_gian == 300:
                    break

            if Payment_Amount == Payment_Amount1:
                message = {"Recharge information":"Recharge successful !","Recharge data":{"username":data_user.username,"Old amount":Old_amount,"Amount deposited":Payment_Amount,"New amount":New_amount,"Code orders":Code_Orders}}
                return Response(message,status=status.HTTP_200_OK)
            else:
                message = {'Error message': 'Recharge failed !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            message = {"data":records}
            return Response(message,status=status.HTTP_200_OK)
        else:
                message = {'Error message': 'Số tiền không thể là 0 hoặc để trống !','Error message English': 'Amount cannot be zero or blank !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

    except:
        message = {'Error message': 'Server error !'}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class PersonalTransactionHistoryViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = PersonalTransactionHistory.objects.filter(Active=True)
    serializer_class = PersonalTransactionHistorySerializer

class PersonalViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = PersonalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']
    parser_classes = [MultiPartParser, ]
    def get_queryset(self,*args,**kwargs):
        username = self.request.query_params.get("username")
        queryset = User.objects.filter(username=username,is_active=True)
        serializer_class = UserSerializer
        return queryset



class ListProductViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    queryset = ListProduct.objects.filter(Active=True)
    serializer_class = ListProductSerializer

    parser_classes = [MultiPartParser, ]


class CategoryProductViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = CategoryProduct.objects.filter(Active=True)
    serializer_class = CategoryProductSerializer

    parser_classes = [MultiPartParser, ]


# Danh sách sản phẩm Trang chủ
@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def product_home_page(request):
    try:
        list_category = CategoryProduct.objects.all()
        list_category_serializer = CategoryProductSerializer(list_category,many=True)
        data_list_category = list_category_serializer.data
        for i in data_list_category:
            for j in i['Categoryy']:
                Quantity_Data_Txt=[]
                for k in j['Data_Txt'].split('\r\n'):
                    if k != None and k != '':
                        Quantity_Data_Txt.append(k)
                j['Quantity'] = len(Quantity_Data_Txt)
                j.pop("Data_Txt")

        message = data_list_category
        return Response(message,status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API tra cứu danh mục
@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def check_list_category(request):
    try:
        list_category = CategoryProduct.objects.all()
        list_category_serializer = CategoryProductSerializer(list_category,many=True)
        data_list_category = list_category_serializer.data
        for i in data_list_category:
            del i['Categoryy'],i['Avatar'],i['Create_Date'],i['Up_Date'],i['Active']
        message = data_list_category
        return Response(message,status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API tra cứu danh sách chi tiết các sản phẩm
@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def check_list_product(request):
    try:
        id_category = request.query_params.get('id_category')
        list_product = ListProduct.objects.filter(Category=id_category,Active=True)
        list_product_serializer = ListProductSerializer(list_product,many=True)
        data_list_product = list_product_serializer.data
        for i in data_list_product:
            Quantity_Data_Txt=[]
            for k in i['Data_Txt'].split('\r\n'):
                if k != None and k != '':
                    Quantity_Data_Txt.append(k)
            i['Quantity'] = len(Quantity_Data_Txt)
            i.pop("Data_Txt")
            del i['Category'],i['Nation'],i['Create_Date'],i['Up_Date'],i['Active'],i['Information']
        message = data_list_product
        return Response(message,status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API tra cứu chi tiết 1 sản phẩm
@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def check_list_product_one(request):
    try:
        id_category = request.query_params.get('id_category')
        id_product = request.query_params.get('id_product')
        list_product = ListProduct.objects.filter(Category=id_category,pk=id_product,Active=True)
        list_product_serializer = ListProductSerializer(list_product,many=True)
        data_list_product = list_product_serializer.data
        for i in data_list_product:
            Quantity_Data_Txt=[]
            for k in i['Data_Txt'].split('\r\n'):
                if k != None and k != '':
                    Quantity_Data_Txt.append(k)
            i['Quantity'] = len(Quantity_Data_Txt)
            i.pop("Data_Txt")
            del i['Category'],i['Nation'],i['Create_Date'],i['Up_Date'],i['Active'],i['Information']
        message = data_list_product[0]
        return Response(message,status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API tra cứu số dư user
@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def check_money_user(request):
    try:
        user_username = request.query_params.get('username')
        user_token = request.query_params.get('token')
        user_data = UserSerializer(User.objects.get(username=user_username,is_active=True))
        data = user_data.data
        del data['id'],data['email'],data['Total_recharge_money'],data['Total_amount_deducted']
        message = data
        return Response(message,status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminInformationViewSet(viewsets.ViewSet,generics.ListAPIView):
    queryset = AdminInformation.objects.filter(Active=True)
    serializer_class = AdminInformationSerializer

    parser_classes = [MultiPartParser, ]

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def bank_infor(request):
    try:
        data_bank_infor = BankInformation.objects.filter(Active=True)
        data_bank_infor_serializer = BankInformationSerializer(data_bank_infor,many=True)
        message = data_bank_infor_serializer.data
        return Response(message,status=status.HTTP_200_OK)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def crypto_infor(request):
    # try:
        data_crypto_infor = CryptoInformation.objects.filter(Active=True)
        data_crypto_infor_serializer = CryptoInformationSerializer(data_crypto_infor,many=True)
        message = data_crypto_infor_serializer.data
        return Response(message,status=status.HTTP_200_OK)
    # except:
    #     message = {'Error message': 'Server error !'}
    #     return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
# @permission_classes((IsAuthenticated, ))
def mua_hang(request):
    try:
        # url = "https://api.ipgeolocation.io/timezone"
        # params = {"apiKey":"fc2cf66cbf09419e96dd8eab6230d1c1","tz":"Asia/Ho_Chi_Minh"}
        # response = requests.request("GET", url, params=params)
        # date = response.json()['date_time']

        product_name_buy = request.query_params.get("product_name_buy")
        quantity_buy = request.query_params.get("quantity_buy")
        user_buy = request.query_params.get("user_buy")
        token = request.query_params.get("token")

        data_user = User.objects.get(username=user_buy)
        data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
        data_product = ListProduct.objects.get(Name=product_name_buy)
        
        dulieu_mathang_all = data_product.Data_Txt.split('\r\n')
        dulieu_mathang = []
        for k in dulieu_mathang_all:
            if k != None and k != "":
                dulieu_mathang.append(k)

        soluong_mathang = len(dulieu_mathang)
        dulieu_khachhangmua = dulieu_mathang[:int(quantity_buy)]
        # return Response(dulieu_khachhangmua)
        update_dulieu_mathang = dulieu_mathang[int(quantity_buy):]
        update_dulieu_mathang_txt = ''
        update_dulieu_khachhangmua_txt = ''
        for i in update_dulieu_mathang:
            update_dulieu_mathang_txt = update_dulieu_mathang_txt + i + '\r\n'

        for j in dulieu_khachhangmua:
            update_dulieu_khachhangmua_txt = update_dulieu_khachhangmua_txt + j + '\r\n'


        if int(data_token.user_id) == int(data_user.id):

            if int(quantity_buy) != None and int(quantity_buy) > 0 and int(quantity_buy) <= int(soluong_mathang):
                into_money = int(quantity_buy) * int(data_product.Price)
                if int(into_money) < int(data_user.Money):
                    data_user.Money = int(data_user.Money) - int(into_money)
                    data_user.save()
                    data_product.Data_Txt = update_dulieu_mathang_txt
                    data_product.save()

                    #luu lịch sử giao dịch: PersonalTransactionHistory
                    CodeOrders = uuid.uuid4().hex
                    PaymentAmount = "-" + str(into_money)
                    BuyData = update_dulieu_khachhangmua_txt
                    UserLink = data_user
                    PersonalTransactionHistory.objects.create(Content=product_name_buy,Code_Orders=CodeOrders,Payment_Amount=PaymentAmount,Buy_Data=BuyData,Status='Successful_Data',User_Link=UserLink)
                    data_user.Total_amount_deducted = int(data_user.Total_amount_deducted)+int(into_money)
                    data_user.save()

                    message = {'Purchase information': 'Successfully purchase !','Order details':{'Account':user_buy,'Product name buy':product_name_buy,'Code orders':CodeOrders,'Quantity buy':quantity_buy,'Transaction amount':PaymentAmount,'Data':dulieu_khachhangmua}}
                    return Response(message, status=status.HTTP_200_OK) 
                else:
                    message = {'Error message':'Số tiền thanh toán hiện tại là không đủ !','Error message English': 'The current payment amount is not enough !'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST) 
            else:
                message = {'Error message':'Số lượng mua không hợp lệ !','Error message English': 'Invalid purchase quantity !'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            # return Response('Valid account!')
        else:
            message = {'Error message':'Tài khoản này không hợp lệ !','Error message English': 'This account is Invalid !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message':'Lỗi máy chủ !','Error message English': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def transaction_history_user(request):
    # try:
        username = request.data["username"]
        token = request.data["token"]
        pagehistory = request.data["pagehistory"]
        seachcode = request.data["seachcode"]
        data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
        data_user = User.objects.get(pk=data_token.user_id)
        if str(data_user.username) == str(username):
            if seachcode != None and seachcode != "" :
                data_history = PersonalTransactionHistory.objects.filter(Code_Orders=seachcode,Active=True)
                data_history_serializer =PersonalTransactionHistorySerializer(data_history,many=True)
                data = data_history_serializer.data
                message = {"Information get transaction history":"Get successful transaction history !","User":data_user.username,"Data":data}
                return Response(message, status=status.HTTP_200_OK)
            else:
                data_history = PersonalTransactionHistory.objects.filter(User_Link=data_token.user_id,Active=True)
                data_history_serializer =PersonalTransactionHistorySerializer(data_history,many=True)
                data_all = data_history_serializer.data
                if int(pagehistory) == 1:
                    data = data_all[:20]
                if int(pagehistory) > 1:
                    data = data_all[int(str(pagehistory)+str(1)):int(str(int(pagehistory)+2)+str(1))]

                message = {"Information get transaction history":"Get successful transaction history !","User":data_user.username,"Data":data}
                return Response(message, status=status.HTTP_200_OK)
        else:
            message = {'Purchase information': 'This account is Invalid !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    # except:
    #     message = {'Error message': 'Server error !'}
    #     return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def down_load_txt(request):
    try:
        CodeOrders = request.data["CodeOrders"]
        token = request.data["token"]
        data_CodeOrders = PersonalTransactionHistory.objects.get(Code_Orders=CodeOrders)
        data_token = AuthToken.objects.get(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
        data_user = User.objects.get(pk=data_token.user_id)
        if str(data_CodeOrders.User_Link) == str(data_user.username):
            file_data = data_CodeOrders.Buy_Data
            response = HttpResponse(file_data, content_type='application/text charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename='+CodeOrders+'.txt'
            return response
        else:
            message = {'Error message': 'Invalid authentication !'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'Error message': 'Server error !'}
        return Response(message,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

