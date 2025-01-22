from django.urls import path, include
from django.contrib.auth.models import User
from slims.models import Run
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        ordering_fields = ['run_date', 'machine', 'submitted', 'run_type']
        ordering = ['username']
        model = Run
        exclude = []

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RunViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'runs', RunViewSet)
