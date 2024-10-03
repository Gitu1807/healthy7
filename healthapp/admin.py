
# Register your models here.
# admin.site.register(meds,MedsAdmin)
from django.contrib import admin
from .models import product 

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','cdetail','is_active']
    list_filter=['cat','is_active']

class notesAdmin(admin.ModelAdmin):
    list_display=['id','name','cat','cdata','is_active']
    list_filter=['cat','is_active']

admin.site.register(product,ProductAdmin)    
