from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nome = models.CharField(max_length = 180)
    email = models.CharField(max_length = 180)

    class Meta:
        db_table="usr_usuarios"