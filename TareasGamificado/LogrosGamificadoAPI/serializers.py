from rest_framework import serializers
from logros.models import Logro

class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = '__all__'