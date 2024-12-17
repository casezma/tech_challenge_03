from django.db import models

class Registro(models.Model):
    timestamp = models.DecimalField(decimal_places=2,max_digits=12)
    velocidade = models.DecimalField(decimal_places=2,max_digits=12)

class Desaceleracao(models.Model):
    timestamp = models.DecimalField(decimal_places=2,max_digits=12)