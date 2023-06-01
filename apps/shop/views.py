from os import remove
from unicodedata import name
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from apps.poster.serializers import PosterSerializer
from apps.product.serializers import ProductSerializer
from apps.shop.models import Shop
from django.conf import settings
from apps.poster.models import Poster
from apps.product.models import Product
from apps.shop.serializers import ShopSerializer

from apps.utils.utils import *

class NewShopView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            name = gson_to_string(data["name"])
            description = gson_to_string(data["description"])
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])
            address = gson_to_string(data["address"])
            image  = files["image"]
            
            registro = Shop.objects.create(
                user = user, 
                name = name, 
                description = description, 
                latitude = float(latitude), 
                longitude = float(longitude),
                address = address
                )
            registro.save()
            
            imageName = str(registro.id) + ".png"

            if path.exists(f'{settings.MEDIA_ROOT}/shop/{imageName}'):
                remove(f'{settings.MEDIA_ROOT}/shop/{imageName}')

            registro.image.save(imageName,image)
            
            return Response({"id":registro.id,
                    "image":registro.getImage()},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": 'Ha ocurrido un error al crear la tienda'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateShopView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            data = self.request.data


            name = gson_to_string(data["name"])
            description = gson_to_string(data["description"])
            latitude = float(data["latitude"])
            longitude = float(data["longitude"])
            address = gson_to_string(data["address"])
            id = int(data["id"])

            Shop.objects.filter(user=user,id=id).update(
                user = user, 
                name = name, 
                description = description, 
                latitude = latitude, 
                longitude = longitude,
                address = address
            )

            shop = Shop.objects.get(user=user,id=id)
            files = self.request.FILES
            if 'image' in files.keys():
                image = files['image']

                imageName = str(shop.id) + ".png"
                
                if path.exists(f'{settings.MEDIA_ROOT}/shop/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/shop/{imageName}')

                shop.image.save(imageName,image)


            return Response({"image": shop.getImage(),"id":shop.id},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al editar la tienda'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data


        try:        
            id = int(gson_to_string(data["id"]))
            open = bool(int(data["open"]))
            shop = Shop.objects.get(user = user, id = id)
            shop.open = open
            shop.save()

            return Response(
                {'success': "success"},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al cerrar la tienda'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            shopId = request.query_params.get('id')            
            shop = Shop.objects.get(id = shopId, user = user)
            poster_exist = Poster.objects.filter(shop = shop)
            products_exist = Product.objects.filter(shop = shop)
            
            for poster in poster_exist:
                if ".png" in str(poster.image) and path.exists(f'{settings.MEDIA_ROOT}/{poster.image}'):
                    remove(f'{settings.MEDIA_ROOT}/{poster.image}')
                    
            for product in products_exist:
                if ".png" in str(product.image1) and path.exists(f'{settings.MEDIA_ROOT}/{product.image1}'):
                    remove(f'{settings.MEDIA_ROOT}/{product.image1}')
                if ".png" in str(product.image2) and path.exists(f'{settings.MEDIA_ROOT}/{product.image2}'):
                    remove(f'{settings.MEDIA_ROOT}/{product.image2}')
                if ".png" in str(product.image3) and path.exists(f'{settings.MEDIA_ROOT}/{product.image3}'):
                    remove(f'{settings.MEDIA_ROOT}/{product.image3}')
                if ".png" in str(product.image4) and path.exists(f'{settings.MEDIA_ROOT}/{product.image4}'):
                    remove(f'{settings.MEDIA_ROOT}/{product.image4}')
                if ".png" in str(product.image5) and path.exists(f'{settings.MEDIA_ROOT}/{product.image5}'):
                    remove(f'{settings.MEDIA_ROOT}/{product.image5}')

            if path.exists(f'{settings.MEDIA_ROOT}/{shop.image}'):
                remove(f'{settings.MEDIA_ROOT}/{shop.image}')

            shop.delete()


            return Response(
                {"success": "success"},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al eliminar la tienda'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetDataShopView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            id = request.query_params.get('id')            
            shop = Shop.objects.get(id = id)
            
            list_datos = []
            list_products = Product.objects.filter(shop = shop)
            for product in list_products:
                product = ProductSerializer(product).data
                list_datos.append({"product":product})
                

            list_posters = Poster.objects.filter(shop = shop)
            for poster in list_posters:
                poster = PosterSerializer(poster).data
                    
                list_datos.append({"poster":poster})

            respuesta = sorted(list_datos, key = lambda dato: dato[list(dato.keys())[0]]['date'],reverse=True)

            
            shop = ShopSerializer(shop).data
            respuesta.insert(0,{"shop":shop})
            
            return Response(
                {'items': respuesta},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al obtener las ofertas de la tienda'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


