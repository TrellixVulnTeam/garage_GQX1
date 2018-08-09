from import_export import resources

from .models import Vehicle,ClientRepairs

class VehicleResource(resources.ModelResource):
    class Meta:
        model = Vehicle

        def get_queryset(self):
            vehicles = Vehicle.objects.filter(user=self.request.user)
            return vehicles

        def get_context_data(self, **kwargs):
            context=super().get_context_data(**kwargs)
            context['vehicles']=VehicleResource(user=self.request.user)
            return context

class ClientResource(resources.ModelResource):
    class Meta:
        model = ClientRepairs

