from rest_framework import serializers
from .models import Usuarios, EstoqueItem

class UsuariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuarios
        fields = "__all__"

class EstoqueItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstoqueItem
        fields = "__all__"