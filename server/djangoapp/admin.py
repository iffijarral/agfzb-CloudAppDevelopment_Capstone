from django.contrib import admin
from .models import *


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel 
    extra = 5
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'name', 'type_choice', 'year']
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)