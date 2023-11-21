from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST
)
from rest_framework import permissions
from .models import Usuarios, EstoqueItem
from .serializers import UsuariosSerializer, EstoqueItemSerializer

from rest_framework.decorators import api_view

from hashlib import sha256
# Create your views here.

@api_view(["POST"])
def register_users(request):
    try:
        
        params = request.data

        password = sha256(params["password"].encode('utf-8')).hexdigest()

        new_user = Usuarios(
            nome=params["name"],
            email=params["email"],
            senha=password
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
    # try:

        users = Usuarios.objects.all()

        serializer = UsuariosSerializer(users, many=True)

        return Response(
            {
                "status": "Success",
                "message": "Usuários listados com sucesso",
                "users": serializer.data
            }, status=HTTP_200_OK
        )

    # except:
    #     return Response(
    #         {
    #             "status": "Error",
    #             "message": "Erro ao listar usuários"
    #         }, status=HTTP_500_INTERNAL_SERVER_ERROR
    #     )

@api_view(["POST"])
def login(request):
    try:
        
        params = request.data

        user = Usuarios.objects.get(email=params["email"])

        password = sha256(params["password"].encode('utf-8')).hexdigest()

        if user.senha == password:
            return Response(
                {
                    "status": "Success",
                    "message": "Login efetuado com sucesso!"
                }, status=HTTP_200_OK
            )

        else:
            return Response(
                {
                    "status": "Error",
                    "message": "Erro ao realizar login"
                }, status=HTTP_400_BAD_REQUEST
            )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def register_item(request):
    try:
        
        params = request.data

        item = EstoqueItem(
            nome=params["item_name"],
            quantidade=params["item_amount"]
        )

        item.save()

        return Response(
            {
                "status": "Success",
                "message": "Login efetuado com sucesso!"
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
def list_itens(request):
    try:
        
        params = request.query_params

        itens = EstoqueItem.objects.all()

        serializer = EstoqueItemSerializer(itens, many=True)

        return Response(
            {
                "status": "Success",
                "message": "Login efetuado com sucesso!",
                "itens": serializer.data
            }, status=HTTP_200_OK
        )

    except:
        return Response(
            {
                "status": "Error",
                "message": "Erro ao registrar usuário"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR
        )