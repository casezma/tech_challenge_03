from rest_framework import serializers
from app.models import Registro

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id','timestamp','velocidade']