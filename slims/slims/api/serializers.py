from django.contrib.auth.models import User, Group
from coreomics.models import Submission
from slims.models import Run, RunLane
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class GroupDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    def get_users(self, instance):
        return UserSerializer(instance.user_set.all(), many=True).data
    # UserSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'users']

class UserDetailSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    is_pi = serializers.SerializerMethodField()
    def is_pi(self, instance):
        return instance.is_pi()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'groups', 'is_pi']

class RunSerializer(serializers.ModelSerializer):
    num_lanes = serializers.IntegerField(read_only=True)
    can_modify = serializers.BooleanField(read_only=True)
    class Meta:
        model = Run
        exclude = []

class RunLaneSerializer(serializers.ModelSerializer):
    run = RunSerializer()
    group = GroupSerializer()
    data_url = serializers.URLField()
    class Meta:
        model = RunLane
        exclude = []

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        exclude = ['data']