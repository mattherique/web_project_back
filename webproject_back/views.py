from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework import permissions
from .models import Usuarios
from .serializers import UsuariosSerializer

from rest_framework.decorators import api_view
# Create your views here.

@api_view(["POST"])
def register_users(request):
    try:
        
        params = request.data

        new_user = Usuarios(
            nome=params["name"],
            email=params["email"]
        )

        new_user.save()

        return Response(
            {
                "status": "Success",
                "message": "Usuário registrado com sucesso"
            }, status=HTTP_200_OK
        )
    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def list_users(request):
    try:

        users = Usuarios.objects.all()

        serializer = UsuariosSerializer(users, many=True)

        return Response(
            {
                "status": "Success",
                "message": "Usuários listados com sucesso",
                "users": serializer.data
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao listar usuários"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )
