from os import remove
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from poster.models import Poster, StaticPoster
from django.conf import settings
from poster.serializers import PosterSerializer
from shop.models import Shop

from utils.utils import *

class PosterView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            text = gson_to_string(data["text"])
            dimension = gson_to_string(data["dimension"])
            shopID = int(data["shopID"])

            shop = Shop.objects.get(user = user, id = shopID)

            poster = Poster.objects.create(shop = shop,
                        dimension = dimension,
                        text = text)

            if "font" in data.keys() and "color" in data.keys():
                font = gson_to_string(data["font"])
                color = gson_to_string(data["color"])
                poster.color = color
                poster.font = font

            poster.save()

            if "image" in files.keys():
                imagePoster  = files["image"]
                imageName = str(poster.id) + ".png"

                if path.exists(f'{settings.MEDIA_ROOT}/poster/{imageName}') and "static_poster" not in imageName:
                    remove(f'{settings.MEDIA_ROOT}/poster/{imageName}')

                poster.image.save(imageName,imagePoster)

            else:       
                imagePoster = gson_to_string(data["imageString"])
                if "http" in imagePoster:
                    imagePosterList = imagePoster.split("/")
                    poster.image = f"{imagePosterList[-2]}/{imagePosterList[-1]}"
                else:
                    poster.image = str(imagePoster)
                poster.save()
            

            poster = PosterSerializer(poster).data
            return Response({"poster":poster},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al realizar poster'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            text = gson_to_string(data["text"])
            id = gson_to_string(request.POST["id"])
            dimension = gson_to_string(data["dimension"])

            poster = Poster.objects.get(id = id)
    
            poster.text = text
            poster.dimension = dimension

            if "font" in data.keys() and "color" in data.keys():
                font = gson_to_string(data["font"])
                color = gson_to_string(data["color"])
                poster.color = color
                poster.font = font
            else:
                poster.color = None
                poster.font = None

            poster.save()

            if "image" in files.keys():
                imagePoster  = files["image"]
                imageName = str(poster.id) + ".png"

                if path.exists(f'{settings.MEDIA_ROOT}/poster/{imageName}') and "static_poster" not in imageName:
                    remove(f'{settings.MEDIA_ROOT}/poster/{imageName}')

                poster.image.save(imageName,imagePoster)
                    
            
            else:
                imagePoster = gson_to_string(data["imageString"])
                if "http" in imagePoster:
                    imagePosterList = imagePoster.split("/")
                    poster.image = f"{imagePosterList[-2]}/{imagePosterList[-1]}"
                else:
                    poster.image = str(imagePoster)
                poster.save()



            poster = PosterSerializer(poster).data
            return Response({"poster":poster},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al actualizar petición'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        try:
            id = request.query_params.get('id')
            poster = Poster.objects.get(id = id)
            if path.exists(f'{settings.MEDIA_ROOT}/{poster.image}') and "static_poster" not in str(poster.image):
                remove(f'{settings.MEDIA_ROOT}/{poster.image}')
            poster.delete()

            return Response(
                {"success": "success"},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": 'Ha ocurrido un error al actualizar petición'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StaticView(APIView):
    def get(self, request, format=None):

        lists_tatics = ["GALLERY","POTHO","COLOR"]
        posters = StaticPoster.objects.filter(is_active = True)

        for poster in posters:
            lists_tatics.append(poster.getImage())
            
        return Response(lists_tatics,
            status=status.HTTP_200_OK)