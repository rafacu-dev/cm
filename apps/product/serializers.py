from rest_framework import serializers
from apps.comments_product.models import CommentsProduct
from apps.shop.serializers import ShopSerializer
from apps.utils.utils import formateDate
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('getImages')
    shop = serializers.SerializerMethodField('getShop')
    price = serializers.SerializerMethodField('getPrice')
    comments = serializers.SerializerMethodField('getComments')
    date = serializers.SerializerMethodField('getDate')

    class Meta:
        model = Product
        fields = (
            "shop",
            "id",
            "dimension",
            "name",
            "description",
            "stock",
            "images",
            "unit",
            "category",
            "date",
            "price",
            "colors",
            "sizes",
            "tastes",
            "smells",
            "textures",
            "sales",
            "comments"
        )
        
    def getDate(self,obj):
        return obj.date.strftime("%y%m%d%H%M%S")

    def getImages(self,obj):
        return obj.getImages()

    def getShop(self,obj):
        shop = ShopSerializer(obj.shop).data
        return shop
        
    def getComments(self,obj):
        comments = CommentsProduct.objects.filter(product=obj)
        return len(comments)
        
    def getPrice(self,obj):
        
        price = [
            {
                "coin":"CUP",
                "oldCost":0.0,
                "newCost":obj.price,
                "send":obj.delivery
            },
        ]
        return price