from rest_framework import serializers
from .models import Users
from utilities.utilites import (
    checkEmailExisted,
    createUserName,
    check_email,
    createHashedPassword,
    check_password,make_password,
    sendForgetMail,
    decodeJwt
)
from django.contrib.auth import authenticate

class UserBasicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "email",
            "username"
        ]

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = [
            "username",
            "password",  # Include the password field here
            "email",
            "first_name",
            "last_name",
            "phoneNumber",
            "Address1",
            "Address2",
            "city",
            "pinCode",
            "token",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # check all data
        email=validated_data.pop('email')
        password=validated_data.pop('password',None)
        first_name=validated_data.pop('first_name')
        last_name=validated_data.pop('last_name')
        phoneNumber = validated_data.pop("phoneNumber")
        Address1 = validated_data.pop("Address1")
        Address2 = validated_data.pop("Address2")
        city  = validated_data.pop("city")
        pinCode = validated_data.pop("pinCode")
        if password is None:
            raise serializers.ValidationError(
                "please provide the password"
            )        
        # password = make_password(password)
        if not check_email(email):
            raise serializers.ValidationError(
                    'email id is not correct'
                )
        if checkEmailExisted(email):
            raise serializers.ValidationError(
                "Email address already existed"
            )
        user=Users.objects.create_user(
            username = createUserName(email),
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phoneNumber = phoneNumber,
            Address1 = Address1,
            Address2 = Address2,
            city = city,
            pinCode = pinCode
        )
        return user
    
    def update(self, instance, validated_data):
        updateData={
                    "first_name" : validated_data.pop('first_name'),
                    "last_name":validated_data.pop('last_name'),
                    "phoneNumber" : validated_data.pop("phoneNumber"),
                    "Address1" : validated_data.pop("Address1"),
                    "Address2" : validated_data.pop("Address2"),
                    "city" : validated_data.pop("city"),
                    "pinCode" : validated_data.pop("pinCode"),
        }
        if Users.objects.filter(phoneNumber = updateData["phoneNumber"]).exists():
            raise "Can't update this phone number other user with same number existed you can report about this problem"
        return super().update(instance, updateData)

    def to_representation(self, instance):
        # Call the superclass method first
        ret = super(UserSerializer, self).to_representation(instance)
        # Remove the password field from the response
        ret.pop('password', None)
        return ret
    
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 1000)
    password = serializers.CharField(max_length = 2000,write_only = True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    phoneNumber = serializers.CharField(read_only=True)
    Address1 = serializers.CharField(read_only=True)
    Address2 = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    pinCode = serializers.CharField(read_only=True)
    token = serializers.CharField(max_length = 1000,read_only=True)
    userId = serializers.CharField(read_only=True)
    def validate(self, attrs):
        email = attrs.get("email",None)
        password = attrs.get("password",None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        # user = authenticate(username=email, password=password)
        try:
            user = Users.objects.get(email = email)
        except:
            raise serializers.ValidationError("user not found")
        if not check_password(password,user.password):
            raise serializers.ValidationError("email and password not matched")
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            "userId":user.id,
            "email":user.email,
            "first_name":user.first_name,
            "last_name" : user.last_name,
            "phoneNumber":user.phoneNumber,
            "Address1":user.Address1,
            "Address2":user.Address2,
            "city":user.city,
            "pinCode":user.pinCode,
            "token":user.token
        }
    
    def create(self, validated_data):
        return validated_data
    
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only = True)
    message = serializers.CharField(read_only = True)
    def validate(self, attrs):
        if not Users.objects.filter(email = attrs.get("email")).exists():
            message = f"No User with {attrs.get('email') }"
        else:
            user = Users.objects.get(email = attrs.get("email"))
            if not user.is_active:
                message = f"Either user with {attrs.get('email') } is not active or not exists"
            else:
                url = sendForgetMail(user)
                message = f"currently no smtp configure so we share message here {url}"
        attrs["message"] = message
        return super().validate(attrs)
    
    def create(self, validated_data):
        return validated_data
    
class ValidateAndChangePassword(serializers.Serializer):
    token = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    message = serializers.CharField(read_only = True)

    def validate(self, attrs):
        token = attrs.get("token")
        password = attrs.get("password")
        decodedData = decodeJwt(token)
        if not decodeJwt(token)[0]:
            raise serializers.ValidationError(decodedData[1]["msg"])
        else:
            email = decodedData[1].get("email")
            try:
                user = Users.objects.get(email=email)
                # password = make_password(password)
                user.password = make_password(password)
                user.save()
                attrs["message"] = "success"
                return super().validate(attrs)
            except Exception as e:
                raise serializers.ValidationError( "No user with this email")
    
    def create(self, validated_data):
        return validated_data
