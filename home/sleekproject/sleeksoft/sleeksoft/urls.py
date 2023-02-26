"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url

from rest_framework.routers import DefaultRouter,SimpleRouter

from polls import views as view
from Data_Interaction import views

from django.urls import path
from knox import views as knox_views

admin.site.site_header = 'VANTHAI'                    
admin.site.index_title = 'Site VANTHAI'                 
admin.site.site_title = 'VANTHAI site admin' 


router = DefaultRouter()
# Anaconda
router.register('admininfor',views.AdminInformationViewSet)
# router.register('SearchListProduct',views.ListProductIndustryListView)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # Webtoday
    path('ListProduct', view.List_Product),
    path('ListProductHome', view.List_Product_Home),
    path('SearchListProduct', view.Search_ListProduct),
    # Anaconda
    path('createuser/',views.create_user),
    path('login/', views.login_api),
    path('on_off_2_factor_authentication/', views.ON_OFF_2_factor_authentication),
    path('login_Two_factor_authentication/', views.login_Two_factor_authentication),
    path('keeplogin/', views.keep_login),
    path('changepassword/', views.change_password),
    path('changemoney/', views.change_money),
    path('transactionhistoryuser/', views.transaction_history_user),
    path('bankinfor/', views.bank_infor),
    path('cryptoinfor/', views.crypto_infor),
    path('sendrechargedata/', views.send_recharge_data),

    path('filteruser/', views.loc_usernam_vs_mail),
    path('sendotp/', views.gui_OTP_den_user),
    path('compareotp/', views.so_sanh_OTP),
    path('resetpassword/', views.reset_password),

    path('statistical_server_user/', views.statistical_server_user),
    path('statistical_server_money/', views.statistical_server_money),

    path('product_home_page/', views.product_home_page),
    path('api.check_list_category', views.check_list_category),
    path('api.check_list_product', views.check_list_product),
    path('api.check_list_product_one', views.check_list_product_one),
    path('api.check_money_user', views.check_money_user),


    path('buydata/', views.mua_hang),
    path('downloadfiletxt/', views.down_load_txt),

    url(r'user/auth/', include('knox.urls')),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
