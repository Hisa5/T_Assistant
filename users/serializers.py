from rest_framework import serializers
from .models import CustomUser

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password2', 'full_name', 'phone_number',
            'address', 'country', 'date_of_birth', 'gender', 'accepted_terms'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
