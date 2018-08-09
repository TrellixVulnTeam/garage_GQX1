from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,Vehicle,
                     MechProfile,
                     Review,Cluster,
                     Make,ClientRepairs,Repair,Contact)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','is_customer','is_mechanic','is_staff')

admin.site.register(User,UserAdmin)


class RepairAdmin(admin.ModelAdmin):
    list_display =  ('vehicle','summary','description','mileage','priority','image')

admin.site.register(Repair,RepairAdmin)

class MechAdmin(admin.ModelAdmin):
  list_display = ('name','garage_name','county','desc','image','town','estate','dental_removal','car_spa','interior_detailing','general_service')
admin.site.register(MechProfile,MechAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name','car_model','number_plate','type','vehicle_name','image','ownership','status','image1','image2')


    def queryset(self, request):
        return Vehicle.objects.filter(owner=request.user)

admin.site.register(Vehicle,VehicleAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone_number','group','image','file')

admin.site.register(Contact,ContactAdmin)

# class RegularServiceAdmin(admin.ModelAdmin):
#     list_display =('periodic_service','other_service',)
# admin.site.register(RegularService,RegularServiceAdmin)

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('make',)
admin.site.register(Make,CarMakeAdmin)
#
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ('brake_issues','suspension_issues','steering_ride_issues','engine_issues',)
# admin.site.register(Repair,VehicleAdmin)


class ClientRepairAdmin(admin.ModelAdmin):
     list_display = ('name','created_on','location','car_model','license_plate','phone_number','Issue',)
admin.site.register(ClientRepairs,ClientRepairAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('mechprofile','rating','user_name','comment','pub_date')
    list_filter = ['pub_date',]
    search_fields = ['comment']


class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name','get_members']


admin.site.register(Review,ReviewAdmin)

admin.site.register(Cluster,ClusterAdmin)
#
