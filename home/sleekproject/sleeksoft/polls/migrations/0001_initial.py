# Generated by Django 4.1.6 on 2023-02-25 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryIndustry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, unique=True, verbose_name='Tên nghành')),
                ('Create_Date', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('Up_Date', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('Active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Danh mục nghành',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ListProductIndustry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100, unique=True, verbose_name='Tiêu đề')),
                ('Title_English', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Tiêu đề tiếng anh')),
                ('Information', models.TextField(verbose_name='Thông tin')),
                ('Information_English', models.TextField(blank=True, null=True, verbose_name='Thông tin tiếng anh')),
                ('Domain_Server', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tên miền')),
                ('Oder_Image', models.IntegerField(blank=True, default=0, null=True, verbose_name='Số đánh dấu thứ tự ảnh')),
                ('Create_Date', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('Up_Date', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('Active', models.BooleanField(default=True)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Category_Industry', to='polls.categoryindustry', verbose_name='Thuộc danh mục nghành')),
            ],
            options={
                'verbose_name_plural': 'Sản phẩm nghành',
                'ordering': ['id'],
                'unique_together': {('Title', 'Category')},
            },
        ),
        migrations.CreateModel(
            name='ImageProductIndustry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.FileField(null=True, upload_to='upload/ImageProduct')),
                ('Create_Date', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('Up_Date', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
                ('Active', models.BooleanField(default=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product_Industry', to='polls.listproductindustry', verbose_name='Thuộc sản phẩm')),
            ],
            options={
                'verbose_name_plural': 'Ảnh sản phẩm',
                'ordering': ['id'],
            },
        ),
    ]
