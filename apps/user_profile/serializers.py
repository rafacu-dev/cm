from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('getImage')
    id = serializers.SerializerMethodField('getUserId')
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "name",
            "image",
            "latitude",
            "longitude",
            "address",
            "phone",
            "email",
            "web",
            "whatsapp",
            "telegram"
        ]
    
    def getImage(self,obj):
        return obj.getImage()

    def getUserId(self,obj):
        return obj.getUserId()
