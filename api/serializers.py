from rest_framework import serializers
from api.models import User


# Create your serializers here.
class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        validated_data.pop('password', None)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

