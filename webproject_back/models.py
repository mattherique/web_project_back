from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nome = models.CharField(max_length = 180)
    email = models.CharField(max_length = 180)
    senha = models.CharField(max_length = 180, null=True, blank=True)

    class Meta:
        db_table="usr_usuarios"

# Create your models here.
class EstoqueItem(models.Model):
    nome = models.CharField(max_length = 180)
    quantidade = models.IntegerField()

    class Meta:
        db_table="rgt_item"

class ItensUsuario(models.Model):
    item_estoque = models.ForeignKey(EstoqueItem, verbose_name="Item do usuario no estoque", on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, verbose_name="ID do usuario", on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    class Meta:
        db_table="rgt_item_usuario"