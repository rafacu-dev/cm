from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.map.views import calculate_distance, getDirections

from apps.product.models import Product
from apps.shop.models import Shop
from apps.payment.models import Wallet
from apps.shopping.serializers import BuySerializer, SaleSerializer
from apps.user_profile.models import UserProfile
from .models import ShoppingRegistered

from apps.utils.utils import *

class ShoppingView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            id = int(data["productId"])
            product = Product.objects.get(id = id)

            wallet = Wallet.objects.get(user = user)

            price = float(data["price"])
            quantity = float(data["quantity"])
            
            delivery = product.delivery
            if delivery == None : delivery = 0
            
            shopping_exist = ShoppingRegistered.objects.filter(user = user,product = product)

            if len(shopping_exist) > 0:
                return Response(
                    {"error": 'El producto ya se encuentra en el carrito'},
                    status=status.HTTP_406_NOT_ACCEPTABLE)


            detail = gson_to_string(data["detail"])
            color = gson_to_string(data["color"])
            size = gson_to_string(data["size"])
            smell = gson_to_string(data["smell"])
            taste = gson_to_string(data["taste"])
            texture = gson_to_string(data["texture"])
                        
            
            buy = ShoppingRegistered.objects.create(
                user = user,
                product = product,
                detail = detail,
                color = color,
                size = size,
                smell = smell,
                taste = taste,
                texture = texture,
                quantity = quantity,
                price = price,
                key = generate_key(50),
            )
            
            if "latitudeDelivery" in data.keys() and "longitudeDelivery" in data.keys() and "addressDelivery" in data.keys():
                latitudeDelivery = float(data["latitudeDelivery"])
                longitudeDelivery = float(data["longitudeDelivery"])
                addressDelivery = gson_to_string(data["addressDelivery"])
            
                buy.latitudeDelivery = latitudeDelivery
                buy.longitudeDelivery = longitudeDelivery
                buy.addressDelivery = addressDelivery


                rute = ''
                rute_list = getDirections(f"{latitudeDelivery}, {longitudeDelivery}",f"{product.shop.latitude}, {product.shop.longitude}")

                for r in rute_list:
                    rute += r + " "

                distance = str(calculate_distance(longitudeDelivery,latitudeDelivery,buy.product.shop.longitude,buy.product.shop.latitude)) + " km"
            
            else:
                profile = UserProfile.objects.get(user = user)
                rute = ''
                rute_list = getDirections(f"{profile.latitude}, {profile.longitude}",f"{product.shop.latitude}, {product.shop.longitude}")
                for r in rute_list:
                    rute += r + " "                

                distance = str(calculate_distance(profile.longitude,profile.latitude,buy.product.shop.longitude,buy.product.shop.latitude)) + " km"

            if len(rute) > 0 and rute[-1] == " ": rute = rute[:-1]
            buy.rute = rute
            buy.save()
            
            buy = BuySerializer(buy).data
            buy["distance"] = distance
            
            return Response({"shopping": buy},status=status.HTTP_200_OK)
        
        except:
            return Response(
                {"error": 'Ha ocurrido un error al realizar compra'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompleteShoppingView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data
        
        try:

            code_register = gson_to_string(data["code_register"])

            salesID,code = code_register.split(" ")            
            salesID = int(salesID.replace("BuyId:",""))
            code = code.replace("CodeRegister:","")

            shoppingRegistered = ShoppingRegistered.objects.get(completed = False,id = salesID,product__shop__user = user,key = code)

            #if shoppingRegistered.coin != "Efectivo":
                #shopWallet = Wallet.objects.get(user=user)
                
                #if shoppingRegistered.coin == "MLC":
                #    shopWallet.quantityMLC += shoppingRegistered.price
                #else:
                #    shopWallet.quantityCUP += shoppingRegistered.price
            
            shoppingRegistered.completed = True
            shoppingRegistered.save()

            return Response(
                {"success": 'success'},
                status=status.HTTP_200_OK)


        except:
            return Response(
                {"error": 'Ha ocurrido un error al cancelar la compra'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            buyRegister = ShoppingRegistered.objects.filter(completed = False,user = user).exclude(key = "BUY_CANCEL")
            
            buyRegisterList = []
            itemsCount = 0
            for buy in buyRegister:
                if buy.product:
                    if buy.longitudeDelivery and buy.latitudeDelivery:
                        distance = str(calculate_distance(buy.longitudeDelivery,buy.latitudeDelivery,buy.product.shop.longitude,buy.product.shop.latitude)) + " km"
                    else:
                        profile = UserProfile.objects.get(user = user)
                        distance = str(calculate_distance(profile.longitude,profile.latitude,buy.product.shop.longitude,buy.product.shop.latitude)) + " km"
                else: distance = ""

                buy = BuySerializer(buy).data
                buy["distance"] = distance

                buyRegisterList.insert(0,buy)
                if buy["key"] != "SALE_CANCEL" and buy["key"] != "PRODUCT_DELETE":itemsCount += 1
                
            return Response(
                {"buys": buyRegisterList,
                "itemsCount":itemsCount},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": 'Ha ocurrido un error al obtener la compra'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        try:
            id = gson_to_string(data["id"])
            cause = gson_to_string(data["cause"])

            buyRegister = ShoppingRegistered.objects.get(completed = False, id = id, user = user)
            buyRegister.detail = cause
            buyRegister.key = "BUY_CANCEL"
            buyRegister.save()

            return Response(
                {"success": 'success'},
                status=status.HTTP_200_OK)


        except:
            return Response(
                {"error": 'Ha ocurrido un error al cancelar la compra'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def delete(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            id = request.query_params.get('id')

            register = ShoppingRegistered.objects.get(completed = False,id=id,user = user)
            register.delete()

            return Response(
                {"success": 'success'},
                status=status.HTTP_200_OK)

            
        except:
            return Response(
                {"error": 'Ha ocurrido un error al eliminar el registro'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SaleView(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            shopId = request.query_params.get('id')
            salesRegister = ShoppingRegistered.objects.filter(completed = False,product__shop__id = shopId,product__shop__user = user).exclude(key = "SALE_CANCEL").exclude(key = "PRODUCT_DELETE")
            
            salesRegisterList = []
            for sale in salesRegister:
                if sale.product:
                    if sale.longitudeDelivery and sale.latitudeDelivery:
                        distance = str(calculate_distance(sale.longitudeDelivery,sale.latitudeDelivery,sale.product.shop.longitude,sale.product.shop.latitude)) + " km"
                    else:
                        profile = UserProfile.objects.get(user = user)
                        distance = str(calculate_distance(profile.longitude,profile.latitude,sale.product.shop.longitude,sale.product.shop.latitude)) + " km"
                else: distance = ""


                sale = SaleSerializer(sale).data
                sale["distance"] = distance
                salesRegisterList.insert(0,sale)
                
            return Response(
                {"sales": salesRegisterList},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": 'Ha ocurrido un error al obtener los productos vendidos'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        try:
            id = gson_to_string(data["id"])
            cause = gson_to_string(data["cause"])


            saleRegister = ShoppingRegistered.objects.get(completed = False,id = id,product__shop__user = user)
            saleRegister.detail = cause
            saleRegister.key = "SALE_CANCEL"
            saleRegister.save()

            return Response(
                {"success": 'success'},
                status=status.HTTP_200_OK)


        except:
            return Response(
                {"error": 'Ha ocurrido un error al cancelar la compra'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def delete(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            id = request.query_params.get('id')

            salesRegister = ShoppingRegistered.objects.get(completed = False,id=id,product__shop__user = user)
            salesRegister.delete()

            return Response(
                {"success": 'success'},
                status=status.HTTP_200_OK)

            
        except:
            return Response(
                {"error": 'Ha ocurrido un error al eliminar el registro'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
