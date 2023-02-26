from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe
from django.contrib import auth
from .models import User,CategoryProduct,ListProduct,AdminInformation,BankInformation,CryptoInformation,PersonalTransactionHistory



class UserAdmin(BaseUserAdmin):
    list_display = ('id','email', 'username','Money','Total_recharge_money','Total_amount_deducted','last_login','OTP','Two_factor_authentication','Password_Level_2','is_active',)
    search_fields = ('email', 'username','Money','Avatar','OTP','Two_factor_authentication','Password_Level_2','last_login',)

    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + (
        'Money','Total_recharge_money','Total_amount_deducted','Avatar','OTP','Two_factor_authentication'
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2','Avatar')}
        ),
    )

class PersonalTransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','Content','Code_Orders', 'Transaction_Time','Payment_Amount','Status','User_Link','Active')
    search_fields = ('Content','Code_Orders', 'Transaction_Time','Payment_Amount','Status',)

class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Name_English','Active')
    search_fields = ('Name',)

    readonly_fields = ["Avatar1"]
    def Avatar1(self,CategoryProduct):
        return mark_safe("<img src='/{img_url}' alt='Image' style='width:120px;'/>".format(img_url=CategoryProduct.Avatar.name))

class ListProductAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Name_English','Price','Nation','Category','Active')
    # search_fields = ('Name','Price','Nation','foreignkeyfield__Category',)
    search_fields = ['Name','Price','Nation',]

    readonly_fields = ["Nation1"]
    def Nation1(self,ListProduct):
        return mark_safe("<img src='/{img_url}' alt='Image' style='width:120px;'/>".format(img_url=ListProduct.Nation.name))

class AdminInformationAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Email','Phone','Avatar','Brand_Name','Main_Color','Active')
    search_fields = ('Name','Email','Phone','Brand_Name','Main_Color',)

class BankInformationAdmin(admin.ModelAdmin):
    list_display = ('id','Account_Name','Account_Number','Bank_Name','Short_Name','QR_Code_Link','Main_Color','Background_Color','Avatar','Api_Key','Code_Api_Key','Active')
    search_fields = ('Account_Name','Account_Number','Bank_Name','Short_Name','QR_Code_Link','Main_Color','Api_Key','Code_Api_Key',)

class CryptoInformationAdmin(admin.ModelAdmin):
    list_display = ('id','Crytop_Name','Short_Name','Wallet_Address','Exchanges','Avatar_QR_Code','Active')
    search_fields = ('Crytop_Name','Short_Name','Wallet_Address','Exchanges',)

admin.site.register(User,UserAdmin)
admin.site.register(CategoryProduct,CategoryProductAdmin)
admin.site.register(ListProduct,ListProductAdmin)
admin.site.register(AdminInformation,AdminInformationAdmin)
admin.site.register(BankInformation,BankInformationAdmin)
admin.site.register(CryptoInformation,CryptoInformationAdmin)
admin.site.register(PersonalTransactionHistory,PersonalTransactionHistoryAdmin)

admin.site.unregister(auth.models.Group)




