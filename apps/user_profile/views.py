from os import path, remove
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from apps.petition.models import Petition
from apps.petition.serializers import PetitionSerializer
from apps.shop.models import Shop
from apps.shop.serializers import ShopSerializer

from apps.user.models import UserAccount
from apps.utils.utils import *
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.conf import settings


class GetUserProfileView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            id = request.query_params.get('id')
            user = UserAccount.objects.get(id = id)
            
            shops_return = []
            shops_exist = Shop.objects.filter(user = user)

            for shop in shops_exist:
                shop_serializer = ShopSerializer(shop).data                
                shops_return.append(shop_serializer)
                

            petitions_return = []
            petitions_exist = Petition.objects.filter(user = user)
            
            for petition in petitions_exist:                
                petition = PetitionSerializer(petition).data
                petitions_return.append(petition)
                
            listPetitions = sorted(petitions_return, key=lambda petitions_list: petitions_list["date"],reverse=True)
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile).data
            
            return Response(
                {'profile': user_profile,
                "shops":shops_return,
                "petitions":listPetitions},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al recuperar su información de perfil'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            data = self.request.data

            name = gson_to_string(data['name'])
            latitude = data['latitude']
            longitude = data['longitude']
            address = gson_to_string(data['address'])

            phone = gson_to_string(data['phone'])
            email = gson_to_string(data['email'])
            web = gson_to_string(data['web'])
            whatsapp = gson_to_string(data['whatsapp'])
            telegram = gson_to_string(data['telegram'])

            UserProfile.objects.filter(user=user).update(
                name = name,
                latitude = latitude,
                longitude = longitude,
                address = address,
                phone = phone,
                email = email,
                web = web,
                whatsapp = whatsapp,
                telegram = telegram
            )

            files = self.request.FILES
            
            if 'image' in list(files.keys()):
                image = files['image']

                user_profile = UserProfile.objects.get(user=user)
                imageName = str(user_profile.id) + ".png"
                if path.exists(f'{settings.MEDIA_ROOT}/user/{imageName}'):
                    remove(f'{settings.MEDIA_ROOT}/user/{imageName}')

                user_profile.image.save(imageName,image)

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({"image": user_profile.data["image"]},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al crear el perfil'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UploadDataUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            data = self.request.data
            files = self.request.FILES

            image = files['image']
            name = gson_to_string(data['name'])
            latitude = data['latitude']
            longitude = data['longitude']
            address = gson_to_string(data['address'])

            UserProfile.objects.filter(user=user).update(
                name = name,
                latitude = latitude,
                longitude = longitude,
                address = address
            )

            user_profile = UserProfile.objects.get(user=user)
            imageName = str(user_profile.id) + ".png"
            
            if path.exists(f'{settings.MEDIA_ROOT}/user/{imageName}'):
                remove(f'{settings.MEDIA_ROOT}/user/{imageName}')

            user_profile.image.save(imageName,image)

            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)
                    
            return Response({"image": user_profile.data["image"]},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al actualizar el perfil'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UploadContactUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            data = self.request.data

            phone = gson_to_string(data['phone'])
            email = gson_to_string(data['email'])
            web = gson_to_string(data['web'])
            whatsapp = gson_to_string(data['whatsapp'])
            telegram = gson_to_string(data['telegram'])

            UserProfile.objects.filter(user=user).update(
                phone = phone,
                email = email,
                web = web,
                whatsapp = whatsapp,
                telegram = telegram
            )
            return Response(
                {'success': "success"},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Algo salió mal al actualizar el perfil'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

