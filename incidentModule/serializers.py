from rest_framework import serializers
from .models import *
from authentication.serializers import UserBasicDetailsSerializer

class IncidentSerializer(serializers.ModelSerializer):
    userDetails = serializers.SerializerMethodField("userDetailsData")

    def  userDetailsData(self,instance):
        user = instance.createBy
        return {
            "id": user.id,
            "fullname": user.get_full_name(),
            "email": user.email,
            "username": user.username
        }
    class Meta:
        model = IncidentModel
        fields = '__all__'
