from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.views import TokenViewBase
from payment.models import Wallet


from user.models import UserAccount,CheckCode
from user_profile.models import UserProfile
    
class UserVerify(TokenViewBase):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.TokenObtainPairSerializer

    def post(self, request, format=None):
        data = self.request.data

        try:
            user_email = data['email']
            user = UserAccount.objects.get(email=user_email)
        except:
            return Response(
                {'error': 'Usuario no existe'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
               
        try:
            code = int(data['code'])
            code_confirm = CheckCode.objects.get(user=user,code_confirm=code)
            user.is_staff = True
            user.save()
            code_confirm.delete()

            # --> Creacion del perfil del usuario
            profile = UserProfile.objects.create(user=user)
            profile.save()
            
            # --> Creacion de la wallet del usuario
            profile = Wallet.objects.create(
                user=user,
                quantityCUP = 0.0,
                quantityMLC = 0.0
                )
            profile.save()

        except:
            return Response(
                {'error': 'El codigo de confirmación no coincide'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
            
        except:
            return Response(
                {'error': 'Ha ocurrido un error inesperado'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
