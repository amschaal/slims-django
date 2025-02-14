from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.db.models import Count
from coreomics.models import Submission
from slims.models import Run, RunLane
from .serializers import UserDetailSerializer, GroupDetailSerializer, RunSerializer, RunLaneSerializer, SubmissionSerializer
from rest_framework import routers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().prefetch_related('groups', 'user_permissions')
    serializer_class = UserDetailSerializer
    search_fields = ['username', 'email', 'first_name', 'last_name']

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().prefetch_related('user_set')
    serializer_class = GroupDetailSerializer
    filterset_fields = { 'name':['icontains']}
    search_fields = ['name', 'user__email', 'user__first_name', 'user__last_name', 'user__username']
    @action(detail=True, methods=['post'])
    def add_users(self, request, pk=None):
        group = self.get_object()
        user_ids = request.data.getlist('users', [])
        users = User.objects.filter(id__in=user_ids)
        group.user_set.add(*users)
        return Response({'users': UserDetailSerializer(users, many=True).data})
    @action(detail=True, methods=['post'])
    def remove_users(self, request, pk=None):
        group = self.get_object()
        user_ids = request.data.getlist('users', [])
        users = User.objects.filter(id__in=user_ids)
        group.user_set.remove(*users)
        return Response({'users': UserDetailSerializer(users, many=True).data})

class RunViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Run.objects.all().annotate(num_lanes=Count('lanes'))
    serializer_class = RunSerializer
    ordering_fields = ['run_date', 'machine', 'submitted', 'run_type', 'num_cycles', 'run_dir']
    ordering = ['run_date']
    search_fields = ['run_date', 'machine', 'submitted', 'run_type', 'run_dir', 'description']

class RunLaneProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
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

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    ordering_fields = ['submitted', 'internal_id']
    ordering = ['-submitted']
    search_fields = ['internal_id', 'id', 'submitter_name', 'pi_name', 'submitter_email', 'pi_email', 'submission_type']

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'runs', RunViewSet)
router.register(r'profile_lanes', RunLaneProfileViewSet, 'profile_lanes')
router.register(r'submissions', SubmissionViewSet)