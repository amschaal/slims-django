import csv
from datetime import datetime
from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.db.models import Count
from coreomics.models import Submission
from bioshare.models import SubmissionShare
from coreomics.utils import format_note
from slims.models import Run, RunLane, LaneData
from .serializers import BioshareSerializer, UserDetailSerializer, GroupDetailSerializer, RunSerializer, RunLaneSerializer, SubmissionSerializer, RunLaneDetailSerializer, LaneDataSerializer
from rest_framework import routers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import HttpResponse

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
    queryset = Run.objects.all().annotate(num_lanes=Count('lanes')).prefetch_related('lanes', 'lanes__submission')
    serializer_class = RunSerializer
    ordering_fields = ['run_date', 'machine', 'submitted', 'run_type', 'type', 'num_cycles', 'run_dir']
    ordering = ['run_date']
    search_fields = ['run_date', 'machine__name', 'machine__id', 'submitted', 'run_type', 'type__name', 'type__id', 'run_dir', 'description', 'lanes__submission__internal_id']
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        note = request.data.get('note')
        run = self.get_object()
        submissions = Submission.objects.filter(lanes__run=run).distinct()
        notes_sent = []
        notes_failed = []
        for submission in submissions:
            formatted_note = format_note(note, submission, LaneData.objects.filter(lane__run=run, lane__submission=submission, status=LaneData.STATUS_COMPLETE))
            try:
                response = submission.create_note(formatted_note)
                notes_sent.append((submission.submission_id, formatted_note))
            except:
                notes_failed.append(submission.submission_id)
        return Response({'sent': notes_sent, 'failed': notes_failed, 'run': RunSerializer(run).data, 'submissions': SubmissionSerializer(submissions, many=True).data})

class RunLaneProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # return RunLane.objects.all()
        user = self.request.user
        user_id = self.request.query_params.get('user_id', None)
        group_id = self.request.query_params.get('group_id', None)
        if group_id:
            if self.request.user.is_staff:
                return RunLane.objects.filter(group_id=group_id).select_related('run', 'group')
            else:
                return RunLane.objects.filter(group__in=user.groups.filter(id=group_id)).select_related('run', 'group')
        if user_id and self.request.user.is_staff:
            user = User.objects.get(id=user_id)
        return RunLane.get_user_lanes(user)
    serializer_class = RunLaneSerializer
    # ordering_fields = ['run__run_date', 'machine', 'submitted', 'run_type', 'num_cycles', 'run_dir']
    filterset_fields = { 'submission__id':['exact'], 'submission__internal_id':['exact']}
    ordering = ['-run__run_date', 'run__run_id']
    search_fields = ['run__run_date', 'run__machine_name', 'run__run_type', 'run__description', 'description', 'lane_number', 'group__name']
    @action(detail=False, methods=['get'])
    def to_csv(self, request):
        qs = self.get_queryset().order_by('-run__run_date')
        response = HttpResponse(content_type='text/csv')
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d_%H-%M-%S')
        response['Content-Disposition'] = 'attachment; filename="runs_export_{}.csv"'.format(date_str)
        writer = csv.writer(response)
        writer.writerow(['Run Date','Machine', 'Group', 'Number of Cycles', 'Description', 'Data URL'])
        for l in RunLaneSerializer(qs, many=True).data:
            writer.writerow([l['run']['run_date'], l['run']['machine_name'], l['group']['name'], l['run']['num_cycles'], l['description'], l['data_url']])
        return response


class RunLaneViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RunLaneDetailSerializer
    queryset = RunLane.objects.all()
    filterset_fields = { 'submission':['exact'], 'submission__internal_id':['exact'], 'run':['exact']}
    ordering = ['-run__run_date', 'run__run_id', 'lane_number']

class LaneDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LaneDataSerializer
    queryset = LaneData.objects.all()
    filterset_fields = { 'lane__submission__id':['exact'], 'lane__submission__internal_id':['exact'], 'lane__run':['exact']}
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        instance = self.get_object()
        instance.share()
        return Response(LaneDataSerializer(instance).data)

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    ordering_fields = ['submitted', 'internal_id', 'submitter_name', 'submitter_email', 'pi_name', 'pi_email', 'submission_type']
    ordering = ['-submitted']
    search_fields = ['internal_id', 'id', 'submitter_name', 'pi_name', 'submitter_email', 'pi_email', 'submission_type']
    @action(detail=True, methods=['post'])
    def link_share(self, request, pk=None):
        submission = self.get_object()
        submission.link_share()
        return Response(SubmissionSerializer(submission).data)

class BioshareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubmissionShare.objects.all()
    serializer_class = BioshareSerializer
    @action(detail=True, methods=['post'])
    def share_with_clients(self, request, pk=None):
        share = self.get_object()
        share.share(email=settings.BIOSHARE_EMAIL_CLIENT)
        share.submission.link_share()
        return Response(BioshareSerializer(share).data)
    @action(detail=True, methods=['post'])
    def update_share(self, request, pk=None):
        share = self.get_object()
        share.update_share()
        return Response(BioshareSerializer(share).data)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'runs', RunViewSet)
router.register(r'profile_lanes', RunLaneProfileViewSet, 'profile_lanes')
router.register(r'run_lanes', RunLaneViewSet, 'run_lanes')
router.register(r'lane_data', LaneDataViewSet, 'lane_data')
router.register(r'submissions', SubmissionViewSet)
router.register(r'submission_shares', BioshareViewSet)