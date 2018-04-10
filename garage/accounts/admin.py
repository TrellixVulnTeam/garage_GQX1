from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Vehicle,MechProfile,CarHistory,Review,Wine,Cluster


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','is_customer','is_mechanic','is_staff')
admin.site.register(User,UserAdmin)


class MechAdmin(admin.ModelAdmin):
  list_display = ('garage_name','county','desc',)
admin.site.register(MechProfile,MechAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner','car_model','car_make')

admin.site.register(Vehicle,VehicleAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('service_date','mechanic_name','service','garage_location','New_Car_Part','Part_Cost','location','repair_done','service_cost')

admin.site.register(CarHistory,HistoryAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('mechanicname','rating','customer_name','comment','pub_date')
    list_filter = ['pub_date','customer_name']
    search_fields = ['comments']


class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name','get_members']

admin.site.register(Review,ReviewAdmin)
admin.site.register(Wine)
admin.site.register(Cluster,ClusterAdmin)

