from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Vehicle,MechProfile,RegularService,Review,Cluster,CarMake,Repair


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','is_customer','is_mechanic','is_staff')
admin.site.register(User,UserAdmin)


class MechAdmin(admin.ModelAdmin):
  list_display = ('name','garage_name','county','desc','profile_photo')
admin.site.register(MechProfile,MechAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name','car_model','number_plate','fuel_type',)

admin.site.register(Vehicle,VehicleAdmin)


class RegularServiceAdmin(admin.ModelAdmin):
    list_display =  fields = ('periodic_service','other_service',)
admin.site.register(RegularService,RegularServiceAdmin)

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('make',)
admin.site.register(CarMake,CarMakeAdmin)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brake_issues','suspension_issues','steering_ride_issues','engine_issues',)
admin.site.register(Repair,VehicleAdmin)

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
