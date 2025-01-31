from django.urls import path, include
from django.contrib.auth.models import User
from slims.models import Run
from .serializers import UserSerializer, RunSerializer
from rest_framework import routers, viewsets



# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('groups')
    serializer_class = UserSerializer
    search_fields = ['username', 'email', 'first_name', 'last_name', 'groups__name']

class RunViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    ordering_fields = ['run_date', 'machine', 'submitted', 'run_type', 'num_cycles', 'run_dir']
    ordering = ['run_date']
    search_fields = ['run_date', 'machine', 'submitted', 'run_type', 'description']

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'runs', RunViewSet)
