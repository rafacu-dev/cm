from rest_framework import serializers

from user_profile.models import UserProfile
from .models import CommentsProduct


class CommentsProductSerializer(serializers.ModelSerializer):
    remitter = serializers.SerializerMethodField('getRemitter')
    remitter_image = serializers.SerializerMethodField('getRemitterImage')
    date = serializers.SerializerMethodField('getDate')

    class Meta:
        model = CommentsProduct
        fields = (
            "id",
            "remitter",
            "remitter_image",
            "text",
            "response",
            "date"
        )

    def getDate(self,obj):
        return obj.date.strftime("%y%m%d%H%M%S")

    def getRemitter(self,obj):
        if obj.user == obj.product.shop.user:
            return obj.product.shop.name
        else:
            return UserProfile.objects.get(user = obj.user).name

    def getRemitterImage(self,obj):
        if obj.user == obj.product.shop.user:
            return obj.product.shop.getImage()
        else:
            return UserProfile.objects.get(user = obj.user).getImage()
            