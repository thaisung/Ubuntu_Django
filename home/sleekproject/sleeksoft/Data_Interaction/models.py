from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	class Meta:
		ordering = ["id"]
	AbstractUser._meta.get_field('email').blank = False
	AbstractUser._meta.get_field('email').null = False
	AbstractUser._meta.get_field('username').blank = False
	AbstractUser._meta.get_field('username').null = False
	AbstractUser._meta.get_field('password').blank = False
	AbstractUser._meta.get_field('password').null = False
	Money = models.IntegerField(default = 0,null=False)
	Total_recharge_money = models.IntegerField(default = 0,null=True, blank=True)
	Total_amount_deducted = models.IntegerField(default = 0,null=True, blank=True)
	Avatar = models.ImageField(upload_to='upload/User',null=True,blank=True)
	OTP = models.CharField(max_length=10, null=True, blank=True)
	Two_factor_authentication = models.CharField(max_length=200, null=True, blank=True,default='OFF')
	Password_Level_2 = models.CharField(max_length=10, null=True, blank=True)

class PersonalTransactionHistory(models.Model):
	class Meta:
		ordering = ["-id"]
	Content = models.CharField(max_length=200, null=True, blank=True)
	Code_Orders = models.CharField(max_length=200, null=False, blank=True,unique=True)
	Transaction_Time = models.DateTimeField(auto_now_add=True)
	Payment_Amount = models.CharField(max_length=200, null=False, blank=True)
	Buy_Data = models.TextField(null=True,blank=True)
	Status = models.CharField(max_length=200, null=True, blank=True)
	User_Link = models.ForeignKey('User',related_name='userlink',on_delete=models.CASCADE,null=True,blank=True)
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Code_Orders

# class Tag(models.Model):
# 	Name = models.CharField(max_length=100,unique=True)

class CategoryProduct(models.Model):
	class Meta:
		ordering = ["id"]

	Name = models.CharField(max_length=100,null=False,unique=True)
	Name_English = models.CharField(max_length=100,null=True,unique=True,blank=True)
	Avatar = models.ImageField(upload_to='upload/CategoryProduct',null=True)
	Create_Date = models.DateTimeField(auto_now_add=True)
	Up_Date = models.DateTimeField(auto_now=True)
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Name


class ListProduct(models.Model):
	class Meta:
		unique_together = ('Name','Category')
		ordering = ["id"]
	Name = models.CharField(max_length=100,null=False,unique=True)
	Name_English = models.CharField(max_length=100,null=True,unique=True,blank=True)
	Information = models.TextField()
	Data_Txt = models.TextField(null=True,blank=True)
	Price = models.IntegerField()
	Nation = models.ImageField(upload_to='upload/ListProduct',null=True)
	Create_Date = models.DateTimeField(auto_now_add=True)
	Up_Date = models.DateTimeField(auto_now=True)
	Category = models.ForeignKey('CategoryProduct',related_name='Categoryy',on_delete=models.CASCADE,null=False) 
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Name

class AdminInformation(models.Model):
	Name = models.CharField(max_length=100,null=False,blank=True)
	Email = models.CharField(max_length=100,null=True)
	Phone = models.CharField(max_length=100,null=True)
	Avatar = models.ImageField(upload_to='upload/AdminInformation',null=True,blank=True)
	Brand_Name = models.CharField(max_length=100,null=True,blank=True)
	Main_Color = models.CharField(max_length=100,null=True,blank=True)
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Name

class BankInformation(models.Model):
	class Meta:
		ordering = ["id"]

	Account_Name = models.CharField(max_length=100,null=False,blank=True)
	Account_Number = models.CharField(max_length=100,null=False,unique=True,blank=True)
	Bank_Name = models.CharField(max_length=100,null=False,unique=True,blank=True)
	Short_Name = models.CharField(max_length=100,null=False,blank=True,unique=True)
	QR_Code_Link = models.CharField(max_length=100,null=False,unique=True,blank=True)
	Main_Color = models.CharField(max_length=100,null=False,blank=True)
	Background_Color = models.CharField(max_length=100,null=True,blank=True)
	Avatar = models.ImageField(upload_to='upload/Bank',null=True,blank=True)
	Api_Key = models.CharField(max_length=500,null=True,blank=True)
	Code_Api_Key = models.CharField(max_length=100,null=True,blank=True)
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Bank_Name

class CryptoInformation(models.Model):
	class Meta:
		ordering = ["id"]

	Crytop_Name = models.CharField(max_length=100,null=False,blank=True)
	Short_Name = models.CharField(max_length=100,null=True,blank=True,unique=True)
	Avatar_Logo = models.ImageField(upload_to='upload/Crypto',null=True,blank=True)
	Wallet_Address = models.CharField(max_length=100,null=False,unique=True,blank=True)
	Exchanges = models.CharField(max_length=100,null=False,unique=True,blank=True)
	Avatar_QR_Code = models.ImageField(upload_to='upload/Crypto',null=True,blank=True)
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Crytop_Name
