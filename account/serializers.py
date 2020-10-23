import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from rest_framework import serializers

from account.models import Client

User = get_user_model()

logger = logging.getLogger(__name__)


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def save(self, **kwargs):
        try:
            logger.info("User created successfully!")
            super().save(**kwargs)
        except ValidationError as e:
            raise serializers.ValidationError(e)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    
    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        
        user_data = validated_data.pop("user")
        UserSerializer(data=user_data).is_valid(raise_exception=ValidationError)
        user = User.objects.create(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        
        return client