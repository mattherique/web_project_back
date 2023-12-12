from rest_framework import serializers
from .models import Usuarios, EstoqueItem, ItensUsuario

class UsuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuarios
        fields = "__all__"

class EstoqueItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstoqueItem
        fields = "__all__"

class ItensUsuarioSerializer(serializers.ModelSerializer):

    item_estoque = EstoqueItemSerializer()

    class Meta:
        model = ItensUsuario
        fields = "__all__"