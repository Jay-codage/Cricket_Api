from rest_framework import serializers
from .models import MatchRestApiData

class MatchRestApiDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRestApiData
        fields = '__all__'