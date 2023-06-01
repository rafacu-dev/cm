from os import remove, rename
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.payment.models import Wallet
from apps.product.serializers import ProductSerializer
from apps.shopping.models import ShoppingRegistered
from apps.utils.utils import *
from apps.shop.models import Shop
from .models import Product
from django.conf import settings
from apps.map.views import *

class ProductView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            id = request.query_params.get("id")
            product = Product.objects.get(id = id)
            
            if product.shop.user == user:
                return Response(
                    {'error': 'Usted es el dueño del producto'},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            else:
                product = ProductSerializer(product).data
                return Response(
                    {"product":product},
                    status=status.HTTP_200_OK
                )
        except:
            return Response(
                {'error': 'Algo salió mal al cargar los productos'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            dimension = gson_to_string(data["dimension"])
            shopID = gson_to_string(data["shopID"])
            name = gson_to_string(data["name"])
            description = gson_to_string(data["description"])
            price = gson_to_string(data["price"])

            stock = gson_to_string(data["stock"])
            unit = gson_to_string(data["unit"])
            category = gson_to_string(data["category"])
            colors = gson_to_string(data["colors"])
            sizes = gson_to_string(data["sizes"])
            tastes = gson_to_string(data["tastes"])
            smells = gson_to_string(data["smells"])
            textures = gson_to_string(data["textures"])
            
            shop = Shop.objects.get(user = user, id = shopID)
            new_product = Product.objects.create(shop = shop,
                        dimension = dimension,
                        name = name,
                        description = description,
                        price = price,
                        stock = stock,
                        unit = unit,
                        category = category,
                        colors = colors,
                        sizes = sizes,
                        tastes = tastes,
                        smells = smells,
                        textures = textures,
                        date=fecha_actual())
            
            if "delivery" in data.keys():
                delivery = data["delivery"]
                new_product.delivery = delivery

            new_product.save()

            

            if "imageProduct1" in files.keys():
                productsImage1 = request.FILES["imageProduct1"] 
                imageName = str(new_product.id) + "_1.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                new_product.image1.save(imageName,productsImage1)
            
            if "imageProduct2" in files.keys():
                productsImage2 = request.FILES["imageProduct2"]
                imageName = str(new_product.id) + "_2.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                new_product.image2.save(imageName,productsImage2)
            
            if "imageProduct3" in files.keys():
                productsImage3 = request.FILES["imageProduct3"]
                imageName = str(new_product.id) + "_3.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                new_product.image3.save(imageName,productsImage3)
            
            if "imageProduct4" in files.keys():
                productsImage4 = request.FILES["imageProduct4"]
                imageName = str(new_product.id) + "_4.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                new_product.image4.save(imageName,productsImage4)
            
            if "imageProduct5" in files.keys():
                productsImage5 = request.FILES["imageProduct5"]
                imageName = str(new_product.id) + "_5.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                new_product.image5.save(imageName,productsImage5)
            
            
            product_return = ProductSerializer(new_product).data
            return Response({"product":product_return},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al crear el producto'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            id = data["id"]
            name = gson_to_string(data["name"])
            description = gson_to_string(data["details"])
            price = data["price"]
            stock = data["stock"]
            unit = data["unit"]
            category = data["category"]
            colors = gson_to_string(data["colors"])
            sizes = gson_to_string(data["sizes"])
            tastes = gson_to_string(data["tastes"])
            smells = gson_to_string(data["smells"])
            textures = gson_to_string(data["textures"])
            dimension = gson_to_string(data["dimension"])

            product = Product.objects.get(id = id)
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.unit = unit
            product.category = category
            product.colors = colors
            product.sizes = sizes
            product.tastes = tastes
            product.smells = smells
            product.textures = textures
            product.dimension = dimension

            if "delivery" in data.keys():
                delivery = data["delivery"]
                product.delivery = delivery
            else:
                product.delivery = None

            

            keys_POST = list(data.keys())
            images_count = 0
            if "imageStrProduct1" in keys_POST:
                images_count += 1
                imageStrProduct1 = gson_to_string(data["imageStrProduct1"])
                imageName = str(id) + "_1.png"
                if "_1.png" not in imageStrProduct1:
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                        remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                    imageNameOld = imageStrProduct1.split("/")[-1]
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageNameOld}'):
                        rename(f'{settings.MEDIA_ROOT}/product/{imageNameOld}',f'{settings.MEDIA_ROOT}/product/{imageName}')

                product.image1 = "product/" + imageName

            if "imageStrProduct2" in keys_POST:
                images_count += 1
                imageStrProduct2 = gson_to_string(data["imageStrProduct2"])
                imageName = str(id) + "_2.png"
                if "_2.png" not in imageStrProduct2:
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                        remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                    imageNameOld = imageStrProduct2.split("/")[-1]
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageNameOld}'):
                        rename(f'{settings.MEDIA_ROOT}/product/{imageNameOld}',f'{settings.MEDIA_ROOT}/product/{imageName}')
                    
                product.image2 = "product/" +imageName
                        
            if "imageStrProduct3" in keys_POST:
                images_count += 1
                imageStrProduct3 = gson_to_string(data["imageStrProduct3"])
                imageName = str(id) + "_3.png"
                if "_3.png" not in imageStrProduct3:
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                        remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                    imageNameOld = imageStrProduct3.split("/")[-1]
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageNameOld}'):
                        rename(f'{settings.MEDIA_ROOT}/product/{imageNameOld}',f'{settings.MEDIA_ROOT}/product/{imageName}')
                    
                product.image3 = "product/" +imageName
                        
            if "imageStrProduct4" in keys_POST:
                images_count += 1
                imageStrProduct4 = gson_to_string(data["imageStrProduct4"])
                imageName = str(id) + "_4.png"
                if "_4.png" not in imageStrProduct4:
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                        remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                    imageNameOld = imageStrProduct4.split("/")[-1]
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageNameOld}'):
                        rename(f'{settings.MEDIA_ROOT}/product/{imageNameOld}',f'{settings.MEDIA_ROOT}/product/{imageName}')
                    
                product.image4 = "product/" +imageName
                        
            if "imageStrProduct5" in keys_POST:
                images_count += 1
                imageStrProduct5 = gson_to_string(data["imageStrProduct5"])
                imageName = str(id) + "_5.png"
                if "_5.png" not in imageStrProduct5:
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                        remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                    imageNameOld = imageStrProduct5.split("/")[-1]
                    if path.exists(f'{settings.MEDIA_ROOT}/product/{imageNameOld}'):
                        rename(f'{settings.MEDIA_ROOT}/product/{imageNameOld}',f'{settings.MEDIA_ROOT}/product/{imageName}')
                    
                product.image5 = "product/" +imageName

            product.save()

            keys_FILES = list(files.keys())
            
            if "imageProduct1" in keys_FILES:
                images_count += 1
                productsImage1 = files["imageProduct1"] 
                imageName = str(id) + "_1.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                product.image1.save(imageName,productsImage1)
            
            if "imageProduct2" in keys_FILES:
                images_count += 1
                productsImage2 = files["imageProduct2"]
                imageName = str(id) + "_2.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                product.image2.save(imageName,productsImage2)
            
            if "imageProduct3" in keys_FILES:
                images_count += 1
                productsImage3 = files["imageProduct3"]
                imageName = str(id) + "_3.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                product.image3.save(imageName,productsImage3)
            
            if "imageProduct4" in keys_FILES:
                images_count += 1
                productsImage4 = files["imageProduct4"]
                imageName = str(id) + "_4.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                product.image4.save(imageName,productsImage4)
            
            if "imageProduct5" in keys_FILES:
                images_count += 1
                productsImage5 = files["imageProduct5"]
                imageName = str(id) + "_5.png"

                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')

                product.image5.save(imageName,productsImage5)

            if images_count < 5:
                product.image5.delete()
                imageName = str(id) + "_5.png"
                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')
            
            if images_count < 4:
                product.image4.delete() 
                imageName = str(id) + "_4.png"
                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')
            
            if images_count < 3:
                product.image3.delete()
                imageName = str(id) + "_3.png"
                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')
            
            if images_count < 2:
                imageName = str(id) + "_2.png"
                product.image2.delete()
                if path.exists(f'{settings.MEDIA_ROOT}/product/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/product/{imageName}')
            
            product.save()
            images =  [base_url + "media/" + str(product.image1),]
            if product.image2:
                images.append(base_url + "media/" + str(product.image2))
            if product.image3:
                images.append(base_url + "media/" + str(product.image3))
            if product.image4:
                images.append(base_url + "media/" + str(product.image4))
            if product.image5:
                images.append(base_url + "media/" + str(product.image5))

            product_return = ProductSerializer(product).data
            return Response({"product":product_return},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al crear el producto'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            
            productID = request.query_params.get('id') 
            product = Product.objects.get(id = productID)
            salesRegister = ShoppingRegistered.objects.filter(completed = False,product = product)

            for sale in salesRegister:
                if sale.coin != "Efectivo":
                    sale.detail = f"<spam> La tienda <b>{sale.product.shop.name}</b> ha eliminado el producto <b>{sale.product.name}</b>, el dinero ha sido reintegrado a su cuenta</spam>"
                    wallet = Wallet.objects.get(user = sale.user)

                    if sale.coin == "MLC":
                        wallet.quantityMLC += sale.price
                        wallet.save()
                    elif sale.coin == "CUP":
                        wallet.quantityCUP += sale.price
                        wallet.save()

                else:
                    sale.detail = f"<spam> La tienda <b>{sale.product.shop.name}</b> ha eliminado el producto <b>{sale.product.name}</b></spam>"

                sale.key = "PRODUCT_DELETE"
                sale.save()

            product.delete()
            if ".png" in str(product.image1) and path.exists(f'{settings.MEDIA_ROOT}/{product.image1}'):
                remove(f'{settings.MEDIA_ROOT}/{product.image1}')
            if ".png" in str(product.image2) and path.exists(f'{settings.MEDIA_ROOT}/{product.image2}'):
                remove(f'{settings.MEDIA_ROOT}/{product.image2}')
            if ".png" in str(product.image3) and path.exists(f'{settings.MEDIA_ROOT}/{product.image13}'):
                remove(f'{settings.MEDIA_ROOT}/{product.image3}')
            if ".png" in str(product.image4) and path.exists(f'{settings.MEDIA_ROOT}/{product.image4}'):
                remove(f'{settings.MEDIA_ROOT}/{product.image4}')
            if ".png" in str(product.image5) and path.exists(f'{settings.MEDIA_ROOT}/{product.image5}'):
                remove(f'{settings.MEDIA_ROOT}/{product.image5}')


            return Response(
                {"success": "success"},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": 'Ha ocurrido un error al eliminar el producto'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductsView(APIView):
    def get(self, request, format=None):
        try:
            id = request.query_params.get("shopId")
            shop = Shop.objects.get(id = id)
            products_return = []

            products = Product.objects.filter(shop = shop)
            for product in products:
                product = ProductSerializer(product).data
                products_return.append(product)
            return Response(
                {'products': products_return},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al cargar los productos'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
                