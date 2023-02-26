from django.db import models
# from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CategoryIndustry(models.Model):
	class Meta:
		ordering = ["id"]
		# verbose_name = "Danh mục nghành"
		verbose_name_plural = "Danh mục nghành"

	Name = models.CharField(max_length=100,null=False,unique=True,verbose_name="Tên nghành")
	Create_Date = models.DateTimeField(auto_now_add=True,verbose_name="Ngày tạo")
	Up_Date = models.DateTimeField(auto_now=True,verbose_name="Ngày cập nhật")
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Name

class ListProductIndustry(models.Model):
	class Meta:
		unique_together = ('Title','Category')
		ordering = ["id"]
		verbose_name_plural = "Sản phẩm nghành"
	Title = models.CharField(max_length=100,null=False,unique=True,verbose_name="Tiêu đề")
	Title_English = models.CharField(max_length=100,null=True,blank=True,unique=True,verbose_name="Tiêu đề tiếng anh")
	Information = models.TextField(verbose_name="Thông tin")
	Information_English = models.TextField(null=True,blank=True,verbose_name="Thông tin tiếng anh")
	Domain_Server = models.CharField(max_length=100,null=True,blank=True,verbose_name="Tên miền")
	Oder_Image = models.IntegerField(default = 0,null=True,blank=True,verbose_name="Số đánh dấu thứ tự ảnh")
	Create_Date = models.DateTimeField(auto_now_add=True,verbose_name="Ngày tạo")
	Up_Date = models.DateTimeField(auto_now=True,verbose_name="Ngày cập nhật")
	Category = models.ForeignKey('CategoryIndustry',related_name='Category_Industry',on_delete=models.CASCADE,null=False,verbose_name="Thuộc danh mục nghành") 
	Active = models.BooleanField(default=True)

	def __str__(self):	
		return self.Title

class ImageProductIndustry(models.Model):
    class Meta:
        # unique_together = ('Name','Product')
        ordering = ["id"]
        verbose_name_plural = "Ảnh sản phẩm"

    Image = models.FileField(upload_to='upload/ImageProduct',null=True)
    Create_Date = models.DateTimeField(auto_now_add=True,verbose_name="Ngày tạo")
    Up_Date = models.DateTimeField(auto_now=True,verbose_name="Ngày cập nhật")
    Product = models.ForeignKey('ListProductIndustry',related_name='Product_Industry',on_delete=models.CASCADE,null=False,verbose_name="Thuộc sản phẩm") 
    Active = models.BooleanField(default=True)

    # def __str__(self):	
    #     return self.Product