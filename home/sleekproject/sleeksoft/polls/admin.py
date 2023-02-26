from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import mark_safe
from .models import CategoryIndustry,ListProductIndustry,ImageProductIndustry
import django.contrib.auth.models
from django.contrib import auth


class CategoryIndustryAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Active')
    search_fields = ('Name',)


class ImageProductIndustryAdmin(admin.StackedInline):
    list_display = ('Image','Product','Active')
    search_fields = ('Product','Active',)

    model= ImageProductIndustry

class ListProductIndustryAdmin(admin.ModelAdmin):
    list_display = ('Title','Information','Category','Domain_Server')
    search_fields = ('Title','Category','Domain_Server')
    inlines = [ImageProductIndustryAdmin]

# @admin.register(ListProductIndustry)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [PostImageAdmin]
 
#     class Meta:
#        model = Post
 
# @admin.register(PostImage)
# class PostImageAdmin(admin.ModelAdmin):
#     pass


admin.site.register(CategoryIndustry,CategoryIndustryAdmin)
admin.site.register(ListProductIndustry,ListProductIndustryAdmin)
admin.site.register(ImageProductIndustry)

# admin.site.unregister(auth.models.User)
# admin.site.unregister(auth.models.Group)