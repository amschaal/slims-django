from django.contrib.auth.models import User, Group
from slims.models import Run
from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'groups']

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        exclude = []