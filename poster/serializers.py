from rest_framework import serializers
from proposal.models import Proposal
from shop.models import Shop
from shop.serializers import ShopSerializer

from .models import Poster


class PosterSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('getImage')
    shop = serializers.SerializerMethodField('getShop')
    date = serializers.SerializerMethodField('getDate')

    class Meta:
        model = Poster
        fields = (
            "shop",
            "id",
            "image",
            "dimension",
            "text",
            "font",
            "color",
            "date"
        )

    def getDate(self,obj):
        return obj.date.strftime("%y%m%d%H%M%S")
        
    def getImage(self,obj):
        return obj.getImage()

    def getShop(self,obj):       
        shop = ShopSerializer(obj.shop).data
        return shop
        
