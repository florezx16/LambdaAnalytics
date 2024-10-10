from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta():
        model = CustomUser
        fields = ['username','first_name','last_name','email','phone_number','gender','is_staff','password','is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self,validated_data):
        user = CustomUser(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            gender = validated_data['gender'],
            is_staff = validated_data['is_staff'],
            password = validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self,instance,validated_data):
        #Use .get() if the field exist in instance if not, will return the instance value
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)      
        instance.is_active = validated_data.get('is_active', instance.is_active)   
        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
           
        instance.save()
        return instance
        
class CustomUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def validate_username(self,value):
        if not CustomUser.objects.filter(username=value,is_active=True).exists():
                raise serializers.ValidationError("This username doesn't exist or is currently disabled.")
        return value
    
        