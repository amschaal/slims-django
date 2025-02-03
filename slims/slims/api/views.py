from django.urls import path, include
from django.contrib.auth.models import User, Group
from slims.models import Run, RunLane
from .serializers import UserDetailSerializer, GroupDetailSerializer, RunSerializer, RunLaneSerializer
from rest_framework import routers, viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().prefetch_related('groups')
    serializer_class = UserDetailSerializer
    search_fields = ['username', 'email', 'first_name', 'last_name', 'groups__name']

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().prefetch_related('user_set')
    serializer_class = GroupDetailSerializer
    search_fields = ['name', 'user__email', 'user__first_name', 'user__last_name', 'user__username']

class RunViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    ordering_fields = ['run_date', 'machine', 'submitted', 'run_type', 'num_cycles', 'run_dir']
    ordering = ['run_date']
    search_fields = ['run_date', 'machine', 'submitted', 'run_type', 'description']

class RunLaneProfileViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        # return RunLane.objects.all()
        user = self.request.user
        user_id = self.request.query_params.get('user_id', None)
        group_id = self.request.query_params.get('group_id', None)
        if group_id and self.request.user.is_staff:
            return RunLane.objects.filter(group_id=group_id)
        if user_id and self.request.user.is_staff:
            user = User.objects.get(id=user_id)
        return RunLane.get_user_lanes(user)
    serializer_class = RunLaneSerializer
    # ordering_fields = ['run__run_date', 'machine', 'submitted', 'run_type', 'num_cycles', 'run_dir']
    ordering = ['-run__run_date', 'run__run_id']
    search_fields = ['run__run_date', 'run__machine', 'run__submitted', 'run__run_type', 'run__description', 'description', 'lane_number', 'group__name']

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'runs', RunViewSet)
router.register(r'profile_lanes', RunLaneProfileViewSet, 'profile_lanes')