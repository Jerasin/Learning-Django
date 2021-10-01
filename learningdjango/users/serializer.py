from rest_framework import serializers
# from django.contrib.auth.models import User 
from users.models import NewUser
from rest_framework.response import Response
#? serializers คือตัวแปลง boj -> str
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id' , 'username' , 'email' ]


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField()
    user_name = serializers.CharField()
    #? write_only อ่านได้เฉพาะ เมื่ออัปเดตหรือสร้างอินสแตนซ์ แต่จะแสดงใน console
    password = serializers.CharField(min_length=8, write_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = NewUser
        fields = ('id' , 'email', 'user_name', 'password' , 'is_active', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance , validated_data):
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.email = validated_data.get('email', instance.email)
        print("Serializer Update")
        print(instance.user_name)
        print(instance.email)
        instance.save()
        password = validated_data.get('password', None)     
        #? Hash Password
        if password:
            instance.set_password(password)          
            instance.save()  
        print(dir(instance))   
        print(instance.email) 
        return instance

        
