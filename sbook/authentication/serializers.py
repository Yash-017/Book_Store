from rest_framework import serializers

from authentication.models import Nuser, UploadedFile

class UserRegistraionSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},
                                    write_only=True)
    class Meta:
        model = Nuser
        fields=['email','name','password','password2','public_visibility','is_author','is_seller','birthyear','address','is_active','is_staff','date_joined']
        extrakwargs={
            'password':{'write_only':True}

        }
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm password does not match')
        return attrs
    

  



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = Nuser
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nuser        
        field = ['id','email','name']
        


class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model=Nuser
            fields=['email', 'password','is_verified']


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
