from rest_framework import serializers
from shopping.models import ShoppingRegistered

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer

from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('getImage')
    user = serializers.SerializerMethodField('getUser')
    sales = serializers.SerializerMethodField('getSales')

    class Meta:
        model = Shop
        fields = (
            "id",
            "user",
            "image",
            "name",
            "rating",
            "averageTime",
            "description",
            "latitude",
            "longitude",
            "address",
            "open",
            "sales",
            "verified"
        )

    def getImage(self,obj):
        return obj.getImage()

    def getUser(self,obj):
        user_profile = UserProfile.objects.get(user=obj.user)
        user_profile = UserProfileSerializer(user_profile).data
        return user_profile

    def getSales(self,obj):
        sales = ShoppingRegistered.objects.filter(product__shop = obj)
        return len(sales)