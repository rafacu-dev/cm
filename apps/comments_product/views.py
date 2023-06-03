from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.comments_product.models import CommentsProduct
from apps.comments_product.serializers import CommentsProductSerializer

from apps.product.models import Product
from apps.utils.utils import fecha_actual, gson_to_string



class CommentsProductView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user           
            id = request.query_params.get("id")
            product = Product.objects.get(id = id)
            list_comments = []

            comments = CommentsProduct.objects.filter(product = product)
            for comment in comments:
                comment = CommentsProductSerializer(comment).data
                list_comments.insert(0,comment)
            print(list_comments)
            return Response(
                {'comments': list_comments},
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
            text = gson_to_string(data["text"])
            id = int(data["id"])

            product = Product.objects.get(id = id)
            new_comment = CommentsProduct.objects.create(
                        product = product,
                        user = user,
                        text = text)

            new_comment.save()

            return Response(
                {'success': 'success'},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Algo salió mal al enviar comentario'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def put(self, request, format=None):
        user = self.request.user
        try:
            id = request.query_params.get("id")
            response = request.query_params.get("response")

            comments = CommentsProduct.objects.get(id = id)
            comments.response = response
            comments.save()

            return Response(
                {'success': 'success'},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'Algo salió mal al enviar respuesta'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            