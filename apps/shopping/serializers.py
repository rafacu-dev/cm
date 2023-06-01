from rest_framework import serializers
from apps.product.serializers import ProductSerializer
from apps.user_profile.models import UserProfile
from apps.user_profile.serializers import UserProfileSerializer

from .models import ShoppingRegistered


class BuySerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('getProduct')
    characteristics = serializers.SerializerMethodField('getCharacteristics')
    delivery = serializers.SerializerMethodField('getDelivery')
    distance = serializers.SerializerMethodField('getDistance')
    rute = serializers.SerializerMethodField('getRute')
    date = serializers.SerializerMethodField('getDate')

    class Meta:
        model = ShoppingRegistered
        fields = (
            "id",
            "product",
            "distance",
            "detail",
            "characteristics",
            "quantity",
            "price",
            "coin",
            "key",
            "date",
            "delivery",
            "rute"
        )
    def getDate(self,obj):
        return obj.date.strftime("%y%m%d%H%M%S")

    def getProduct(self,obj):
        if obj.product:
            product = ProductSerializer(obj.product).data
            return product
        return None
        
    def getCharacteristics(self,obj):
        if obj.key == "SALE_CANCEL":
            characteristics = "SALE_CANCEL"
        else:
            characteristics = ""
            if obj.color != "": characteristics += "Color: " + obj.color + " "
            if obj.size != "": characteristics += "Tamaño: " + obj.size + " "
            if obj.smell != "": characteristics += "Olor: " + obj.smell + " "
            if obj.taste != "": characteristics += "Sabor: " + obj.taste + " "
            if obj.texture != "": characteristics += "Textura: " + obj.texture + " "

        return characteristics
        
    def getDelivery(self,obj):
        if obj.product:
            if not obj.product.delivery:
                delivery = None
            else:
                delivery = "La compra se le entregará en " + obj.addressDelivery
            return delivery
        return ""
        
    def getRute(self,obj):
        rute = obj.rute
        if rute != "":
            return rute.split(" ")
        return []

    def getDistance(self,obj):
        return ""

class SaleSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('getProduct')
    user = serializers.SerializerMethodField('getUser')
    characteristics = serializers.SerializerMethodField('getCharacteristics')
    delivery = serializers.SerializerMethodField('getDelivery')
    distance = serializers.SerializerMethodField('getDistance')
    rute = serializers.SerializerMethodField('getRute')
    date = serializers.SerializerMethodField('getDate')


    class Meta:
        model = ShoppingRegistered
        fields = (
            "id",
            "user",
            "product",
            "distance",
            "detail",
            "characteristics",
            "quantity",
            "price",
            "coin",
            "date",
            "delivery",
            "rute"
        )

    def getDate(self,obj):
        return obj.date.strftime("%y%m%d%H%M%S")

    def getProduct(self,obj):
        if obj.product:
            product = ProductSerializer(obj.product).data
            return product
        return None

    def getUser(self,obj):
        user_profile = UserProfile.objects.get(user=obj.user)
        user_profile = UserProfileSerializer(user_profile).data
        return user_profile
        
    def getCharacteristics(self,obj):
        if obj.key == "BUY_CANCEL":
            characteristics = "BUY_CANCEL"
        else:
            characteristics = ""
            if obj.color != "": characteristics += "Color: " + obj.color + " "
            if obj.size != "": characteristics += "Tamaño: " + obj.size + " "
            if obj.smell != "": characteristics += "Olor: " + obj.smell + " "
            if obj.taste != "": characteristics += "Sabor: " + obj.taste + " "
            if obj.texture != "": characteristics += "Textura: " + obj.texture + " "

        return characteristics
        
    def getDelivery(self,obj):
        if not obj.product.delivery:
            delivery = None
        else:
            delivery = "Entregar encargo en "  + obj.addressDelivery
        return delivery

    def getRute(self,obj):
        rute = obj.rute.split(" ")
        return rute

    def getDistance(self,obj):
        return ""

        