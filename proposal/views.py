from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from map.views import calculate_distance
from petition.models import Petition
from product.models import Product
from product.serializers import ProductSerializer

from proposal.models import Proposal
from user_profile.models import UserProfile
from utils.utils import fecha_actual

class ProposeProductView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            user = UserProfile.objects.get(user=user)
            id = request.query_params.get("petitionId")
            petition = Petition.objects.get(id = id)
            proposals = Proposal.objects.filter(petition = petition)
            return_products = []
            for proposal in proposals:
                distance = str(calculate_distance(user.longitude,user.latitude,proposal.product.shop.longitude,proposal.product.shop.latitude)) + " km"
                product = ProductSerializer(proposal.product).data
                product["distance"] = distance
                return_products.append(product)


            return Response(
                {'proposals': return_products},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Algo salió mal al cargar las propuestas'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        try:
            productID = data["productID"]
            petitionID = data["petitionID"]
            
            product = Product.objects.get(id = productID)
            petition = Petition.objects.get(id = petitionID)

            proposal = Proposal.objects.filter(product = product, petition = petition)
            if len(list(proposal)) == 0:
                registro = Proposal.objects.create(product = product,
                            petition = petition)
                registro.save()
            return Response(
                {"propose": 'true'},
                status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": 'Ha ocurrido un error al realizar propuesta'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, format=None):
        user = self.request.user

        try:
            productId = request.query_params.get('productId')
            petitionId = request.query_params.get('petitionId')

            product = Product.objects.get(id = productId)
            petition = Petition.objects.get(id = petitionId)

            proposal = Proposal.objects.get(product = product, petition = petition)
            proposal.delete()

            return Response(
                {"success": "success"},
                status=status.HTTP_200_OK)

        except:
            return Response(
                {"error": 'Ha ocurrido un error al actualizar petición'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

