from import_export import resources

from .models import Vehicle

class PersonResource(resources.ModelResource):
    class Meta:
        model = Vehicle
