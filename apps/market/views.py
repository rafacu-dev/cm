from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from apps.petition.serializers import PetitionSerializer
from apps.poster.serializers import PosterSerializer
from apps.product.serializers import ProductSerializer
from apps.shop.serializers import ShopSerializer

from apps.user.models import UserAccount
from apps.user_profile.models import UserProfile
from apps.shop.models import Shop
from apps.product.models import Product
from apps.poster.models import Poster
from apps.petition.models import Petition

from apps.map.views import *

from django.db.models import Q


class GetMarketView(APIView):
    def get(self, request, format=None):
        #try:
            userAccount = self.request.user
            user = UserProfile.objects.get(user=userAccount)

            category = request.query_params.get("filter")
            if not category:
                category = "All"

            search = request.query_params.get("search")
            if not search:
                search = ""

            category_filters = ["Clothing","Technology","Food","Toys","Furniture","Utensil","Art","Cosmetics","Pets","Medications"]
            
            list_market = []
            list_recomended_shops = []
            
            shops = Shop.objects.filter(open = True).exclude(user = userAccount)

            for shop in shops:                
                if shop.poster_set.exists() or shop.product_set.exists():
                    distance = str(calculate_distance(user.longitude,user.latitude,shop.longitude,shop.latitude)) + " km"

                    if category  == "All" or category in category_filters or category == "Products":    #Esto es para determinar  los productos a retornar
                        list_products = Product.objects.filter(shop = shop)#.order_by("date").reverse()

                        if search != "":
                            list_products = list_products.filter(Q(name__icontains = search) | Q(description__icontains = search)).distinct()
                        elif category in category_filters:
                            category_to_int = category_filters.index(category)
                            list_products = list_products.filter(category=category_to_int)

                        for product in list_products:
                            product = ProductSerializer(product).data
                            product["distance"] = distance
                            list_market.append({"product":product})

                    if category  == "Posters" or category  == "All":    #Esto es para determinar  los posters a retornar
                        list_posters = Poster.objects.filter(shop = shop)
                        if search != "":
                            list_posters = list_posters.filter(Q(text__icontains = search))

                        for poster in list_posters:
                            poster = PosterSerializer(poster).data
                            poster["distance"] = distance
                                                            
                            #list_market.append({"poster":poster})

                    if  search == "" or search.lower() in str(shop.name).lower():   #Esto es para determinar si retornar esta tienda
                        data_shop = ShopSerializer(shop).data
                        data_shop["sales"] = 0
                        list_recomended_shops.append(data_shop)

            
            
            if category  == "Petitions" or category  == "All":  #Esto es para determinar las peticiones a retornar
                list_petitions = Petition.objects.exclude(user = userAccount)

                if search != "":
                    list_petitions = list_petitions.filter(text__icontains = search).distinct()

                for petition in list_petitions:
                    userPetition = UserProfile.objects.get(user=petition.user)
                    
                    distance = str(calculate_distance(user.longitude,user.latitude,userPetition.longitude,userPetition.latitude)) + " km"
                    petition = PetitionSerializer(petition).data
                    petition["distance"] = distance
                    list_market.append({"petition":petition})
                    
            respuesta = sorted(list_market, key = lambda dato: dato[list(dato.keys())[0]]['date'],reverse=True)

            if len(list_recomended_shops) > 0:
                list_shops = {
                    "shops":list_recomended_shops,
                }

                respuesta.insert(0,
                    {"recomended_shops":list_shops}
                )

            if search != "" and len(respuesta) == 0:
                option_text = "Sin resutados"
            else:
                option_text = ""
                    
            options = {
                    "text": option_text,
                    "images" : ["https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__340.jpg",]
                    }
            respuesta.insert(0,{"options":options})

            return Response({"items":respuesta},status=status.HTTP_200_OK)

        #except:
            return Response(
                {'error': 'Algo salió mal cargar las ofertas en el mercado'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
  
class GetProductsView(APIView):

    def get(self, request, format=None):
        #try:
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)

            shops = Shop.objects.filter(open = True).exclude(user = user)
            return_products = []
            for shop in shops:
                data_shop = {
                    "id":shop.id,
                    "userId": shop.user.id,
                    "image": shop.getImage(),
                    "name":shop.name,
                    "description":shop.description,
                    "rating":0.0,
                    "latitude":shop.latitude,
                    "longitude":shop.longitude,
                    "address":shop.get_address(),
                    "open":shop.open}
                distance = str(calculate_distance(user.longitude,user.latitude,shop.longitude,shop.latitude)) + " km"
                list_products = Product.objects.filter(shop = shop)
                
                for product in list_products:
                    images =  product.get_images()

                    product = ProductSerializer(product).data
                    product["distance"] = distance
                        
                    return_products.append(product)
            
