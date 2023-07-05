from os import remove
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from petition.models import Petition, StaticPetition
from django.conf import settings
from petition.serializers import PetitionSerializer

from utils.utils import *

class PetitionView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            text = gson_to_string(data["text"])
            dimension = gson_to_string(data["dimension"])

            petition = Petition.objects.create(user = user,
                        dimension = dimension,
                        text = text)

            if "font" in data.keys() and "color" in data.keys():
                font = gson_to_string(data["font"])
                color = gson_to_string(data["color"])
                petition.color = color
                petition.font = font

            petition.save()

            if "image" in files.keys():
                imagePetition  = files["image"]
                imageName = str(petition.id) + ".png"

                if path.exists(f'{settings.MEDIA_ROOT}/petition/{imageName}')  and "static_petition" not in imageName:
                    remove(f'{settings.MEDIA_ROOT}/petition/{imageName}')

                petition.image.save(imageName,imagePetition)
                 
            else:       
                imagePetition = gson_to_string(data["imageString"])
                if "http" in imagePetition:
                    imagePetitionList = imagePetition.split("/")
                    petition.image = f"{imagePetitionList[-2]}/{imagePetitionList[-1]}"
                else:
                    petition.image = str(imagePetition)
                petition.save()
            

            petition = PetitionSerializer(petition).data
            return Response({"petition":petition},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al realizar petición'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data
        files = self.request.FILES

        try:
            text = gson_to_string(data["text"])
            id = gson_to_string(request.POST["id"])
            dimension = gson_to_string(data["dimension"])

            petition = Petition.objects.get(id = id, user = user)
    
            petition.text = text
            petition.dimension = dimension

            if "font" in data.keys() and "color" in data.keys():
                font = gson_to_string(data["font"])
                color = gson_to_string(data["color"])
                petition.color = color
                petition.font = font
            else:
                petition.color = None
                petition.font = None

            petition.save()

            if "image" in files.keys():
                imagePetition  = files["image"]
                imageName = str(petition.id) + ".png"

                if path.exists(f'{settings.MEDIA_ROOT}/petition/{imageName}')  and "static_petition" not in imageName:
                    remove(f'{settings.MEDIA_ROOT}/petition/{imageName}')

                petition.image.save(imageName,imagePetition)
                 
            else:       
                imagePetition = gson_to_string(data["imageString"])
                if "http" in imagePetition:
                    imagePetitionList = imagePetition.split("/")
                    petition.image = f"{imagePetitionList[-2]}/{imagePetitionList[-1]}"
                else:
                    petition.image = str(imagePetition)
                petition.save()
            

            petition = PetitionSerializer(petition).data
            return Response({"petition":petition},
                status=status.HTTP_200_OK)
            
        except: 
            return Response(
                {"error": 'Ha ocurrido un error al actualizar petición'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        user = self.request.user
        try:
            id = request.query_params.get('id')
            petition = Petition.objects.get(id = id, user = user)
            if path.exists(f'{settings.MEDIA_ROOT}/{petition.image}')  and "static_petition" not in str(petition.image):
                remove(f'{settings.MEDIA_ROOT}/{petition.image}')
            petition.delete()

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
        petitions = StaticPetition.objects.filter(is_active = True)

        for petition in petitions:
            lists_tatics.append(petition.getImage())
            
        return Response(lists_tatics,
            status=status.HTTP_200_OK)