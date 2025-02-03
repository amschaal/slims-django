from django.contrib.auth.models import User, Group
from slims.models import Run, RunLane
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class GroupDetailSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.SerializerMethodField()
    def get_users(self, instance):
        return UserSerializer(instance.user_set.all(), many=True).data
    # UserSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'users']

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'groups']

class RunSerializer(serializers.ModelSerializer):
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